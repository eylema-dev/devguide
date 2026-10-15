"""Local development audit: persist allowlisted usage metadata, never messages.

This tool has no model/network calls. The ledger and reports must remain private.
"""
import argparse
import collections
import datetime
import decimal
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

FIELDS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens')
REPOSITORIES = {'eylema', 'eyleme', 'devguide', 'eylema-docs-en', 'eylema-docs-tr',
                'eylema-evals', 'eylema-examples', 'eylema-models',
                'eylema-training', 'eylemadotdev', '.github',
                'eyleme-docs-en', 'eyleme-docs-tr', 'eyleme-evals',
                'eyleme-examples', 'eyleme-models', 'eyleme-training'}
SAFE_LABEL = re.compile(r'[A-Za-z0-9_.:/-]{1,160}\Z')


class UsageError(ValueError):
    """Invalid or conflicting metadata; never includes original record content."""


def label(value):
    return value if isinstance(value, str) and SAFE_LABEL.fullmatch(value) else 'unknown'


def tokens(value):
    if not isinstance(value, dict):
        raise UsageError('Missing usage object')
    result = {}
    for field in FIELDS:
        item = value.get(field, 0 if field in ('cache_write_input_tokens', 'reasoning_output_tokens') else None)
        if type(item) is not int or item < 0:
            raise UsageError('Invalid token counter')
        result[field] = item
    if (result['input_tokens'] + result['output_tokens'] != result['total_tokens']
            or result['cached_input_tokens'] + result['cache_write_input_tokens'] > result['input_tokens']
            or result['reasoning_output_tokens'] > result['output_tokens']):
        raise UsageError('Inconsistent token counters')
    return result


def records(path, diagnostics):
    """An incomplete active final line is deferred; malformed complete lines fail."""
    with path.open('rb') as source:
        for line in source:
            if not line.endswith(b'\n'):
                diagnostics['deferred_partial_lines'] += 1
                break
            try:
                item = json.loads(line)
            except (ValueError, UnicodeError):
                raise UsageError('Malformed complete session record') from None
            if isinstance(item, dict):
                yield item


def metadata(path, diagnostics):
    with path.open('rb') as source:
        line = source.readline()
    if not line.endswith(b'\n'):
        diagnostics['deferred_discovery_headers'] += 1
        return None
    try:
        item = json.loads(line)
    except (ValueError, UnicodeError):
        raise UsageError('Malformed complete discovery header') from None
    if not isinstance(item, dict):
        raise UsageError('Invalid discovery header')
    payload = item.get('payload')
    if (item.get('type') != 'session_meta' or not isinstance(payload, dict)
            or not isinstance(payload.get('id'), str) or not payload['id']):
        raise UsageError('Invalid discovery session identity')
    return {key: payload.get(key) for key in
            ('id', 'parent_thread_id', 'forked_from_id', 'cwd', 'model_provider', 'timestamp')}


def project_cwd(cwd, roots, cache):
    if not isinstance(cwd, str) or not cwd:
        return False
    if cwd in cache:
        return cache[cwd]
    path = Path(cwd).resolve()
    selected = any(path == root or path.is_relative_to(root) for root in roots)
    if not selected and path.is_dir():
        try:
            proc = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(path),
                                   'remote', 'get-url', 'origin'], capture_output=True,
                                  text=True, timeout=3, check=False)
            remote = proc.stdout.strip()
            match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)(eyleme-dev|eylema-dev)/([^/]+?)(?:\.git)?', remote)
            selected = (proc.returncode == 0 and bool(match) and match.group(2) in REPOSITORIES
                        and not (match.group(1) == 'eylema-dev' and match.group(2).startswith('eyleme')))
        except (OSError, subprocess.TimeoutExpired):
            selected = False
    cache[cwd] = selected
    return selected


def discover(source_roots, project_roots, known_ids=(), diagnostics=None):
    diagnostics = diagnostics if diagnostics is not None else collections.Counter()
    metas = {}
    for root in source_roots:
        if not root.is_dir():
            raise UsageError('Configured session root is missing or unavailable')
        for path in sorted(root.rglob('*.jsonl')):
            if path.is_symlink():
                diagnostics['skipped_symlink_source_files'] += 1
                continue
            meta = metadata(path, diagnostics)
            if meta and isinstance(meta.get('id'), str):
                metas[path] = meta
    roots = [Path(p).resolve() for p in project_roots]
    cache = {}
    selected = set(known_ids)
    selected.update(m['id'] for m in metas.values() if project_cwd(m.get('cwd'), roots, cache))
    while True:
        descendants = {m['id'] for m in metas.values()
                       if m.get('parent_thread_id') in selected or m.get('forked_from_id') in selected}
        if descendants <= selected:
            break
        selected |= descendants
    return {p: m for p, m in metas.items() if m['id'] in selected}


def scan(files):
    contexts = {}
    pending = []
    incoming = {}
    sessions = {meta['id'] for meta in files.values()}
    diagnostics = collections.Counter()
    token_events = set()
    # Read each append-only file once; retain only allowlisted metadata. Join
    # contexts after all files so parent/fork/resume order does not matter.
    for path, meta in files.items():
        sid = meta['id']
        for obj in records(path, diagnostics):
            p = obj.get('payload', {})
            if not isinstance(p, dict):
                continue
            if obj.get('type') == 'turn_context':
                turn = p.get('turn_id')
                if isinstance(turn, str):
                    key = (sid, turn)
                    value = (label(p.get('model')), label(p.get('effort', p.get('reasoning_effort'))))
                    if key in contexts and contexts[key] != value:
                        raise UsageError('Conflicting model/effort for one turn')
                    contexts[key] = value
            elif obj.get('type') == 'event_msg' and p.get('type') == 'token_count' and p.get('info'):
                token_events.add(sid)
            elif obj.get('type') == 'token_usage_record':
                pending.append((obj.get('timestamp'), label(meta.get('model_provider')),
                                {k: p.get(k) for k in ('response_id', 'thread_id', 'turn_id', 'usage')}))
    has_usage = set()
    for timestamp, provider, p in pending:
        rid, sid, turn = p.get('response_id'), p.get('thread_id'), p.get('turn_id')
        if not all(isinstance(v, str) and v for v in (rid, sid, turn)):
            raise UsageError('Usage record lacks stable response/thread/turn identity')
        if sid not in sessions:
            diagnostics['ignored_foreign_responses'] += 1
            continue
        has_usage.add(sid)
        try:
            stamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            if stamp.utcoffset() is None:
                raise ValueError
        except (ValueError, AttributeError, TypeError):
            raise UsageError('Invalid usage timestamp') from None
        model, effort = contexts.get((sid, turn), ('unknown', 'unknown'))
        value = {'session_id': sid, 'turn_id': turn, 'timestamp': stamp.astimezone(datetime.timezone.utc).isoformat(),
                 'provider': provider, 'model': model, 'effort': effort, 'tokens': tokens(p.get('usage'))}
        key = hashlib.sha256((provider + ':' + rid).encode()).hexdigest()
        if key in incoming:
            if incoming[key] != value:
                raise UsageError('Conflicting usage for duplicated response identity')
            diagnostics['duplicate_responses'] += 1
        else:
            incoming[key] = value
    diagnostics['sessions_without_response_usage'] = len(sessions - has_usage)
    diagnostics['sessions_with_only_cumulative_events'] = len(token_events - has_usage)
    return incoming, sessions, dict(diagnostics)


def external_records(paths, diagnostics=None):
    """Explicit normalized provider exports; never infer effort, prices or totals."""
    diagnostics = diagnostics if diagnostics is not None else collections.Counter()
    result = {}
    required = {'provider', 'response_id', 'session_id', 'turn_id', 'timestamp', 'model', 'effort', 'tokens'}
    for name in paths:
        path = Path(name).expanduser()
        for obj in records(path, diagnostics):
            if set(obj) != required or not all(isinstance(obj[k], str) and obj[k]
                                               for k in required - {'tokens'}):
                raise UsageError('External usage must contain only normalized metadata')
            try:
                stamp = datetime.datetime.fromisoformat(obj['timestamp'].replace('Z', '+00:00'))
                if stamp.utcoffset() is None:
                    raise ValueError
            except (ValueError, TypeError):
                raise UsageError('Invalid external usage timestamp') from None
            provider = label(obj['provider'])
            key = hashlib.sha256((provider + ':' + obj['response_id']).encode()).hexdigest()
            value = {k: obj[k] for k in ('session_id', 'turn_id')}
            value.update(timestamp=stamp.astimezone(datetime.timezone.utc).isoformat(),
                         provider=provider, model=label(obj['model']), effort=label(obj['effort']),
                         tokens=tokens(obj['tokens']))
            if key in result and result[key] != value:
                raise UsageError('Conflicting normalized external response')
            result[key] = value
    return result


def validate_rates(rates):
    if rates.get('version') != 1 or rates.get('currency') != 'USD' or not isinstance(rates.get('models'), dict):
        raise UsageError('Invalid rates registry')
    datetime.date.fromisoformat(rates['valuation_date'])
    for rate in rates['models'].values():
        if type(rate['long_input_threshold']) is not int or rate['long_input_threshold'] < 0:
            raise UsageError('Invalid context price threshold')
        for key in ('input', 'cached_input', 'cache_write_input', 'output',
                    'long_input_multiplier', 'long_output_multiplier'):
            price = decimal.Decimal(rate[key])
            if not price.is_finite() or price < 0:
                raise UsageError('Invalid token price')


def merge(previous, incoming):
    result = dict(previous)
    for key, value in incoming.items():
        if key in result and result[key] != value:
            old = result[key]
            differences = {field for field in set(old) | set(value) if old.get(field) != value.get(field)}
            if not (differences <= {'model', 'effort'}
                    and all(old.get(field) == 'unknown' or value.get(field) == 'unknown'
                            for field in differences)):
                raise UsageError('Ledger conflicts with recorded response; preserve previous ledger')
            value = dict(value)
            for field in differences:
                if value[field] == 'unknown':
                    value[field] = old[field]
        result[key] = value
    return result


def cost(record, rates):
    rate = rates['models'].get(record['model']) if record['provider'] == 'openai' else None
    if rate is None:
        return None
    u = record['tokens']
    # Cached reads and cache writes are portions of input, reasoning is a
    # portion of output. Neither is added again to total tokens.
    raw = u['input_tokens'] - u['cached_input_tokens'] - u['cache_write_input_tokens']
    subtotal = (decimal.Decimal(raw) * decimal.Decimal(rate['input'])
                + decimal.Decimal(u['cached_input_tokens']) * decimal.Decimal(rate['cached_input'])
                + decimal.Decimal(u['cache_write_input_tokens']) * decimal.Decimal(rate['cache_write_input']))
    output = decimal.Decimal(u['output_tokens']) * decimal.Decimal(rate['output'])
    if u['input_tokens'] > rate['long_input_threshold']:
        subtotal *= decimal.Decimal(rate['long_input_multiplier'])
        output *= decimal.Decimal(rate['long_output_multiplier'])
    return (subtotal + output) / decimal.Decimal(1000000)


def summarize(ledger, rates):
    groups = {}
    daily = {}
    total = collections.Counter()
    priced = decimal.Decimal(0)
    unpriced = collections.Counter()
    for record in ledger.values():
        keys = (record['provider'], record['model'], record['effort'])
        group = groups.setdefault(keys, {'responses': 0, 'tokens': collections.Counter(),
                                        'cost': decimal.Decimal(0), 'unpriced_responses': 0})
        day = record['timestamp'][:10]
        date_group = daily.setdefault((day, *keys), {'responses': 0, 'tokens': collections.Counter(),
                                                    'cost': decimal.Decimal(0), 'unpriced_responses': 0})
        u = tokens(record['tokens'])
        amount = cost(record, rates)
        total.update(u)
        for g in (group, date_group):
            g['responses'] += 1
            g['tokens'].update(u)
            if amount is None:
                g['unpriced_responses'] += 1
            else:
                g['cost'] += amount
        if amount is None:
            unpriced.update(u)
        else:
            priced += amount
    def row(key, value, names):
        return dict(zip(names, key), responses=value['responses'], tokens=dict(value['tokens']),
                    standard_api_equivalent_usd=str(value['cost']) if not value['unpriced_responses'] else None,
                    priced_subtotal_usd=str(value['cost']), unpriced_responses=value['unpriced_responses'])
    return {'responses': len(ledger), 'tokens': dict(total), 'priced_standard_api_equivalent_usd': str(priced),
            'fast_api_equivalent_scenario_usd': str(priced * 2), 'actual_paid_cost_usd': None,
            'unpriced_tokens': dict(unpriced),
            'by_model_effort': [row(k, v, ('provider', 'model', 'effort')) for k, v in sorted(groups.items())],
            'by_day_model_effort_utc': [row(k, v, ('day_utc', 'provider', 'model', 'effort')) for k, v in sorted(daily.items())]}


def atomic(path, content):
    fd, temp = tempfile.mkstemp(prefix='.usage-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def report_markdown(report):
    s = report['summary']
    lines = ['# Eyleme token ve maliyet takibi', '', f"Güncellendi (UTC): {report['generated_at']}", '',
             f"Toplam: **{s['tokens'].get('total_tokens', 0):,} token**, {s['responses']:,} yanıt; "
             f"{report['coverage']['ledger_sessions']} sohbet.", '',
             '| Model | Effort | Giriş | Önbellek (giriş içinde) | Çıkış | Toplam | API karşılığı USD |',
             '|---|---|---:|---:|---:|---:|---:|']
    for row in s['by_model_effort']:
        t = row['tokens']
        price = row['standard_api_equivalent_usd']
        value = f"{decimal.Decimal(price):.2f}" if price is not None else 'Fiyat bilinmiyor'
        lines.append(f"| {row['model']} | {row['effort']} | {t['input_tokens']:,} | "
                     f"{t['cached_input_tokens']:,} | {t['output_tokens']:,} | {t['total_tokens']:,} | {value} |")
    lines += ['', f"Fiyatı bilinen kullanımın Standard API karşılığı: **${decimal.Decimal(s['priced_standard_api_equivalent_usd']):.2f}**.",
              f"Fast API senaryosu (ayrı varsayım): **${decimal.Decimal(s['fast_api_equivalent_scenario_usd']):.2f}**.",
              '', f"Tarife tarihi: {report['pricing']['valuation_date']}; [resmî kaynak]({report['pricing']['source']}).",
              '', 'Bu hesap gerçek ChatGPT/Codex faturası değildir. Kayıtlardaki model/effort ayarını kullanır; '
              'gizli sunucu model kimliğini doğrulamaz. Reasoning çıkışa dahildir. Uzun bağlam kuralı her yanıta uygulanır.',
              '', 'Kapsam: erişilebilir yerel Codex kayıtları, Eyleme depo kökleri ve ilişkili alt/fork sohbetleri. '
              'Silinmiş geçmiş, başka hesap/cihaz/provider kayıtları, görsel/arama araçlarının ayrı ücretleri, '
              'abonelik, vergi ve kur dönüşümü bu tutara dahil değildir; bunlar sıfır kabul edilmez.',
              '', f"Kapsam durumu: {json.dumps(report['coverage'], ensure_ascii=False)}", '']
    return '\n'.join(lines)


def refresh(config, output, rates):
    validate_rates(rates)
    if not config.get('project_roots') or not config.get('session_roots'):
        raise UsageError('Explicit project and session roots are required')
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    if output.is_symlink():
        raise UsageError('Output directory must not be a symlink')
    os.chmod(output, 0o700)
    for name in ('.lock', 'ledger.json', 'latest.json', 'latest.tr.md', 'snapshots.jsonl'):
        if (output / name).is_symlink():
            raise UsageError('Private output files must not be symlinks')
    lock_path = output / '.lock'
    with lock_path.open('a') as lock:
        os.chmod(lock_path, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger_path = output / 'ledger.json'
        previous = json.loads(ledger_path.read_text()) if ledger_path.exists() else {'version': 1, 'sessions': [], 'responses': {}}
        if previous.get('version') != 1:
            raise UsageError('Unsupported ledger version')
        discovery_diagnostics = collections.Counter()
        files = discover([Path(p).expanduser() for p in config['session_roots']],
                         config['project_roots'], previous['sessions'], discovery_diagnostics)
        incoming, sessions, diagnostics = scan(files)
        discovery_diagnostics.update(diagnostics)
        diagnostics = discovery_diagnostics
        external = external_records(config.get('external_usage_files', []), diagnostics)
        incoming = merge(incoming, external)
        values = merge(previous['responses'], incoming)
        diagnostics['external_responses'] = len(external)
        # Only Codex IDs enter discovery; external IDs cannot authorize membership.
        known = sorted(set(previous['sessions']) | sessions)
        ledger = {'version': 1, 'sessions': known, 'responses': values}
        digest = hashlib.sha256(json.dumps(ledger, sort_keys=True).encode()).hexdigest()
        observed = [r['timestamp'] for r in values.values()]
        report = {'version': 1, 'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'first_response_at': min(observed) if observed else None,
                  'last_response_at': max(observed) if observed else None,
                  'ledger_digest': digest, 'pricing': rates,
                  'coverage': dict(diagnostics, scanned_files=len(files), current_sessions=len(sessions),
                                   ledger_sessions=len(known), archived_responses_retained=len(set(values) - set(incoming)),
                                   scope='available local Codex response usage; external/provider/tool-only charges unavailable'),
                  'summary': summarize(values, rates)}
        prior_report = json.loads((output / 'latest.json').read_text()) if (output / 'latest.json').exists() else {}
        atomic(ledger_path, json.dumps(ledger, indent=2, sort_keys=True) + '\n')
        atomic(output / 'latest.json', json.dumps(report, indent=2, ensure_ascii=False) + '\n')
        atomic(output / 'latest.tr.md', report_markdown(report))
        if prior_report.get('ledger_digest') != digest or prior_report.get('pricing') != rates:
            with (output / 'snapshots.jsonl').open('a', encoding='utf-8') as f:
                os.chmod(output / 'snapshots.jsonl', 0o600)
                f.write(json.dumps(report, ensure_ascii=False) + '\n')
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True, help='Private JSON with session_roots and project_roots')
    parser.add_argument('--output', type=Path, required=True, help='Private ignored ledger/report directory')
    parser.add_argument('--rates', type=Path, default=Path(__file__).with_name('rates.json'))
    args = parser.parse_args()
    try:
        report = refresh(json.loads(args.config.read_text()), args.output, json.loads(args.rates.read_text()))
    except (UsageError, OSError, ValueError, KeyError, decimal.InvalidOperation) as exc:
        # Never echo arbitrary raw source content, paths, provider errors or prompts.
        parser.exit(1, f'Usage refresh failed ({type(exc).__name__}); existing artifacts are not deleted; reports may be stale or partial. Resolve the source/IO failure and rerun.\n')
    print(json.dumps({'responses': report['summary']['responses'], 'tokens': report['summary']['tokens'],
                      'standard_api_equivalent_usd': report['summary']['priced_standard_api_equivalent_usd'],
                      'unpriced_tokens': report['summary']['unpriced_tokens'], 'coverage': report['coverage']}))


if __name__ == '__main__':
    main()
