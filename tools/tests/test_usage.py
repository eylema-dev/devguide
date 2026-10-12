"""Regression coverage for metadata scope, duplicate billing and private ledgers."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

TOOL = Path(__file__).resolve().parents[1] / 'usage' / 'collect.py'
spec = importlib.util.spec_from_file_location('usage_collect', TOOL)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
RATES = json.loads(TOOL.with_name('rates.json').read_text())


def counters(input_tokens=100, cached=80, output=10, reasoning=7, writes=0):
    return dict(input_tokens=input_tokens, cached_input_tokens=cached,
                cache_write_input_tokens=writes, output_tokens=output,
                reasoning_output_tokens=reasoning, total_tokens=input_tokens + output)


def response(sid='root', rid='response', turn='turn', amount=None):
    return {'type': 'token_usage_record', 'timestamp': '2026-10-12T12:00:00Z',
            'payload': dict(thread_id=sid, turn_id=turn, response_id=rid, usage=amount or counters(),
                            thread_token_usage=counters(100000, 90000, 10000))}


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'sessions'
        self.source.mkdir()
        self.project = self.root / 'project'
        self.project.mkdir()
        self.output = self.root / 'private'

    def session(self, name='a', sid='root', parent=None, cwd=None, items=(), context=True):
        p = self.source / (name + '.jsonl')
        data = [{'type': 'session_meta', 'payload': dict(id=sid, cwd=str(cwd or self.project),
                parent_thread_id=parent, model_provider='openai', timestamp='2026-10-12T11:00:00Z')}]
        if context:
            data += [{'type': 'turn_context', 'payload': dict(turn_id='turn', model='gpt-6.1-sol', effort='high')}]
        data += list(items)
        p.write_text(''.join(json.dumps(v) + '\n' for v in data))
        return p

    def config(self):
        return dict(session_roots=[str(self.source)], project_roots=[str(self.project)])

    def test_resume_and_fork_copies_are_charged_once(self):
        self.session(items=[response(), response(rid='second')])
        self.session(name='resume', items=[response()])
        self.session(name='fork', sid='child', parent='root', cwd=self.root / 'outside',
                     items=[response(), response(sid='child', rid='child-response')])
        result = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(result['summary']['responses'], 3)
        self.assertEqual(result['summary']['tokens']['total_tokens'], 330)
        self.assertEqual(result['coverage']['duplicate_responses'], 2)
        self.assertEqual(result['coverage']['ledger_sessions'], 2)

    def test_unrelated_sibling_is_excluded(self):
        self.session(items=[response()])
        self.session(name='unrelated', sid='foreign', cwd=self.root / 'project-extra',
                     items=[response(sid='foreign', rid='other')])
        files = usage.discover([self.source], [str(self.project)])
        self.assertEqual(len(files), 1)

    def test_canonical_remote_accepts_new_worktree_but_not_lookalikes(self):
        other = self.root / 'worktree'
        other.mkdir()
        subprocess.run(['git', 'init', '-q', str(other)], check=True)
        subprocess.run(['git', '-C', str(other), 'remote', 'add', 'origin',
                        'https://github.com/eylema-dev/eylema.git'], check=True)
        self.assertTrue(usage.project_cwd(str(other), [], {}))
        subprocess.run(['git', '-C', str(other), 'remote', 'set-url', 'origin',
                        'https://github.com/eylema-dev/eylemadotdev.git'], check=True)
        self.assertTrue(usage.project_cwd(str(other), [], {}))
        subprocess.run(['git', '-C', str(other), 'remote', 'set-url', 'origin',
                        'https://github.com/eylema-dev/eylema-evil.git'], check=True)
        self.assertFalse(usage.project_cwd(str(other), [], {}))

    def test_cache_and_reasoning_are_subsets_not_extra_tokens(self):
        self.session(items=[response(amount=counters(writes=5))])
        result = usage.refresh(self.config(), self.output, RATES)['summary']
        self.assertEqual(result['tokens']['total_tokens'], 110)
        # 15 uncached *2 +80 cached *.1 +5 cache-write *2.5 +10 output *10.
        self.assertEqual(result['priced_standard_api_equivalent_usd'], '0.0001505')

    def test_long_context_rate_applies_to_whole_request_strictly_above_threshold(self):
        self.session(items=[response(amount=counters(272000, 270000, 100)),
                            response(rid='long', amount=counters(272001, 270000, 100))])
        result = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(result['summary']['priced_standard_api_equivalent_usd'], '0.095504')

    def test_missing_context_and_unpriced_model_are_preserved(self):
        p = self.session(items=[response()], context=False)
        result = usage.refresh(self.config(), self.output, RATES)['summary']
        self.assertEqual(result['by_model_effort'][0]['model'], 'unknown')
        self.assertIsNone(result['by_model_effort'][0]['standard_api_equivalent_usd'])
        self.assertEqual(result['unpriced_tokens']['total_tokens'], 110)
        self.assertIsNone(result['actual_paid_cost_usd'])

    def test_invalid_counter_or_conflicting_response_does_not_replace_ledger(self):
        p = self.session(items=[response()])
        usage.refresh(self.config(), self.output, RATES)
        before = (self.output / 'ledger.json').read_bytes()
        self.session(items=[response(amount=counters(101))])
        with self.assertRaises(usage.UsageError):
            usage.refresh(self.config(), self.output, RATES)
        self.assertEqual((self.output / 'ledger.json').read_bytes(), before)
        bad = counters(); bad['cached_input_tokens'] = 101
        self.session(items=[response(amount=bad)])
        with self.assertRaises(usage.UsageError):
            usage.refresh(self.config(), self.output, RATES)
        self.assertEqual((self.output / 'ledger.json').read_bytes(), before)

    def test_deleted_history_retained_refresh_idempotent_and_messages_not_exported(self):
        p = self.session(items=[response(), {'type': 'response_item', 'payload': {'secret': 'PRIVATE_PROMPT_SENTINEL'}}])
        usage.refresh(self.config(), self.output, RATES)
        usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(len((self.output / 'snapshots.jsonl').read_text().splitlines()), 1)
        p.unlink()
        report = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(report['summary']['responses'], 1)
        self.assertEqual(report['coverage']['archived_responses_retained'], 1)
        for path in self.output.iterdir():
            self.assertNotIn('PRIVATE_PROMPT_SENTINEL', path.read_text())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o700)

    def test_cumulative_only_events_are_gap_not_additional_charge(self):
        self.session(items=[{'type': 'event_msg', 'payload': {'type': 'token_count',
                     'info': {'total_token_usage': counters(1000000)}}}], context=False)
        report = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(report['summary']['responses'], 0)
        self.assertEqual(report['coverage']['sessions_with_only_cumulative_events'], 1)

    def test_active_partial_line_deferred_and_malformed_complete_line_fails(self):
        p = self.session(items=[response()])
        with p.open('ab') as f:
            f.write(b'{"type":')
        report = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(report['summary']['responses'], 1)
        self.assertEqual(report['coverage']['deferred_partial_lines'], 1)
        with p.open('ab') as f:
            f.write(b'BROKEN}\n')
        with self.assertRaises(usage.UsageError):
            usage.refresh(self.config(), self.output, RATES)

    def test_explicit_external_provider_usage_stays_unpriced_and_private(self):
        source = self.root / 'external.jsonl'
        event = dict(provider='anthropic', response_id='external-response', session_id='external',
                     turn_id='external-turn', timestamp='2026-10-12T12:00:00Z',
                     model='claude-example', effort='unknown', tokens=counters())
        source.write_text(json.dumps(event) + '\n')
        config = dict(self.config(), external_usage_files=[str(source)])
        report = usage.refresh(config, self.output, RATES)
        self.assertEqual(report['summary']['responses'], 1)
        self.assertEqual(report['summary']['unpriced_tokens']['total_tokens'], 110)
        self.assertEqual(report['coverage']['external_responses'], 1)
        self.assertEqual(report['coverage']['ledger_sessions'], 0)
        event['prompt'] = 'must not be accepted'
        source.write_text(json.dumps(event) + '\n')
        with self.assertRaises(usage.UsageError):
            usage.refresh(config, self.output, RATES)

    def test_invalid_rates_fail_before_creating_ledger(self):
        self.session(items=[response()])
        rates = json.loads(json.dumps(RATES))
        rates['models']['gpt-6.1-sol']['input'] = 'NaN'
        with self.assertRaises(usage.UsageError):
            usage.refresh(self.config(), self.output, rates)
        self.assertFalse(self.output.exists())

    def test_missing_root_and_complete_invalid_header_are_errors(self):
        config = dict(self.config(), session_roots=[str(self.root / 'missing')])
        with self.assertRaises(usage.UsageError):
            usage.refresh(config, self.output, RATES)
        for invalid in ('BROKEN\n', '[]\n', '{"type":"response_item"}\n'):
            (self.source / 'bad.jsonl').write_text(invalid)
            with self.assertRaises(usage.UsageError):
                usage.refresh(self.config(), self.output, RATES)
        self.assertFalse((self.output / 'ledger.json').exists())

    def test_discovery_and_external_partial_lines_remain_visible_as_gaps(self):
        (self.source / 'new.jsonl').write_text('{"type":')
        external = self.root / 'external.jsonl'
        external.write_text('{"provider":')
        config = dict(self.config(), external_usage_files=[str(external)])
        report = usage.refresh(config, self.output, RATES)
        self.assertEqual(report['coverage']['deferred_discovery_headers'], 1)
        self.assertEqual(report['coverage']['deferred_partial_lines'], 1)

    def test_late_model_effort_enrichment_updates_price_without_changing_tokens(self):
        self.session(items=[response()], context=False)
        first = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(first['summary']['unpriced_tokens']['total_tokens'], 110)
        self.session(items=[response()])
        second = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(second['summary']['responses'], 1)
        self.assertEqual(second['summary']['tokens'], first['summary']['tokens'])
        self.assertEqual(second['summary']['unpriced_tokens'], {})
        self.assertGreater(float(second['summary']['priced_standard_api_equivalent_usd']), 0)

    def test_late_output_failure_preserves_history_and_next_refresh_repairs_report(self):
        self.session(items=[response()])
        usage.refresh(self.config(), self.output, RATES)
        self.session(items=[response(), response(rid='second')])
        original = usage.atomic
        def fail_latest(path, content):
            if path.name == 'latest.json':
                raise OSError('synthetic IO failure')
            original(path, content)
        with mock.patch.object(usage, 'atomic', side_effect=fail_latest):
            with self.assertRaises(OSError):
                usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(len(json.loads((self.output / 'ledger.json').read_text())['responses']), 2)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text())['summary']['responses'], 1)
        recovered = usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(recovered['summary']['responses'], 2)
        self.assertEqual(json.loads((self.output / 'latest.json').read_text())['summary']['responses'], 2)

    def test_symlink_output_never_overwrites_other_file(self):
        self.session(items=[response()])
        self.output.mkdir()
        outside = self.root / 'outside'
        outside.write_text('keep')
        (self.output / 'snapshots.jsonl').symlink_to(outside)
        with self.assertRaises(usage.UsageError):
            usage.refresh(self.config(), self.output, RATES)
        self.assertEqual(outside.read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
