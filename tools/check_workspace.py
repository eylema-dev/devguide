"""Verify a pinned Eyleme repository set as data; never execute fetched member code."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from check_repository import (ROOT, ROLES, PRODUCT_DOCS, CheckFailure, load_json,
                              require, repository_files, validate_api, verify_vendor, validate_repository_config)

from github_identity import canonical_repository, RENAMED_REPOSITORIES

MEMBERS = set(ROLES) - {'devguide'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', *args], cwd=root,
                          check=True, capture_output=True, text=True, timeout=60).stdout.strip()


def validate_set(manifest):
    require(manifest.get('format_version') == 1, 'Unknown repository-set version')
    members = manifest.get('members', {})
    require(set(members) == MEMBERS, 'Repository set must include every managed member exactly once')
    for name, member in members.items():
        require(member.get('repository') == 'eyleme-dev/' + name, 'Repository identity is outside the approved set')
        require(bool(re.fullmatch('[0-9a-f]{40}', member.get('revision', ''))), 'Repository revision must be a full immutable SHA')
    pairs = manifest.get('product_translations', {})
    require(set(pairs) == set(PRODUCT_DOCS), 'Product translation coverage is incomplete')
    for name, pair in pairs.items():
        require(set(pair) == {'en_sha256', 'tr_sha256'}, f'Unexpected translation record: {name}')
        require(all(re.fullmatch('[0-9a-f]{64}', x) for x in pair.values()), 'Invalid translation hash')
    return members


def fetch_members(members, cache):
    roots = {}
    cache.mkdir(parents=True, exist_ok=True)
    for name, member in members.items():
        # Historical evidence keeps its old identity; fetch/cache use the canonical slug.
        repository = canonical_repository(member['repository'])
        current_name = RENAMED_REPOSITORIES.get(name, name)
        require(repository == 'eyleme-dev/' + current_name, 'Mismatched repository/cache identity')
        require(bool(re.fullmatch('[0-9a-f]{40}', member['revision'])), 'Immutable fetch revision required')
        path = cache / 'eyleme-dev' / ('organization-github' if current_name == '.github' else current_name) / member['revision']
        if not path.exists():
            path.mkdir(parents=True)
            git(path, 'init', '--quiet')
            git(path, 'remote', 'add', 'origin', f'https://github.com/{repository}.git')
        origin = git(path, 'remote', 'get-url', 'origin')
        require(origin == f'https://github.com/{repository}.git', 'Unexpected cached origin')
        git(path, 'fetch', '--quiet', '--depth=1', 'origin', member['revision'])
        git(path, 'checkout', '--quiet', '--detach', member['revision'])
        roots[name] = path
    return roots


def validate_heads(roots, members):
    require(set(roots) == MEMBERS, 'Workspace roots must match the pinned repository set')
    for name, root in roots.items():
        require(git(root, 'rev-parse', 'HEAD') == members[name]['revision'], f'Wrong pinned revision: {name}')
        require(not git(root, 'status', '--porcelain', '--untracked-files=all'), f'Dirty repository cannot represent a pinned snapshot: {name}')
        require(validate_repository_config(load_json(root / 'repository.json')) == name, 'Pinned repository profile mismatch')
        print(f'PIN {name}: {members[name]["revision"]}')


def cross_link_errors(roots, text):
    errors = []
    text = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
    targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
    for target in targets:
        parsed = urlsplit(target.strip().strip('<>'))
        if parsed.scheme != 'https' or parsed.netloc != 'github.com':
            continue
        parts = unquote(parsed.path).strip('/').split('/')
        if len(parts) < 5 or parts[0] not in {'eyleme-dev', 'eylema-dev'}:
            continue
        if parts[2] not in {'blob', 'tree'} or parts[3] != 'main':
            continue  # historical commit, PR and issue references are not current-layout targets
        try:
            name = canonical_repository('/'.join(parts[:2])).split('/')[1]
        except ValueError:
            errors.append(target)
            continue
        if name not in roots:
            continue  # approved repository outside this pinned document set
        root = roots[name].resolve()
        path = root.joinpath(*parts[4:]).resolve()
        valid = path.is_file() if parts[2] == 'blob' else path.is_dir()
        if not path.is_relative_to(root) or not valid:
            errors.append(target)
    return errors


def validate_product_pairs(roots, manifest):
    for name in PRODUCT_DOCS:
        for lang in ('en', 'tr'):
            path = roots[f'eyleme-docs-{lang}'] / f'docs/{name}.md'
            require(path.is_file(), f'Missing product translation: {lang}/{name}')
            require(digest(path) == manifest['product_translations'][name][lang + '_sha256'],
                    f'Product translation fingerprint is stale: {lang}/{name}')
    en = roots['eyleme-docs-en'] / 'docs'
    tr = roots['eyleme-docs-tr'] / 'docs'
    operations = validate_api((en / 'api-reference.md').read_text(), (tr / 'api-reference.md').read_text())
    ids = lambda path: re.findall(r'^\| (M\d+|EYL-\d+) \|', path.read_text(), re.M)
    require(bool(ids(en / 'roadmap.md')) and ids(en / 'roadmap.md') == ids(tr / 'roadmap.md'), 'Cross-repository roadmap ID mismatch')
    return operations


def validate_migration(roots, inventory):
    """Check today's layout; historical byte identity is checked separately."""
    documents = inventory.get('documents', [])
    require(len(documents) == 26, 'Migration inventory is incomplete')
    seen = set()
    removed = set()
    for row in documents:
        repo = canonical_repository(row['destination_repository']).split('/')[1]
        require(repo in roots, 'Unknown migration destination')
        key = (repo, row['destination_path'])
        require(key not in seen, 'Duplicate migration destination')
        seen.add(key)
        root = roots[repo].resolve()
        require(safe_path(row['destination_path']), 'Invalid migration destination path')
        path = (root / row['destination_path']).resolve()
        require(path.is_relative_to(root) and path.is_file(), 'Missing or escaping migration destination')
        if old := row.get('previous_main_path'):
            require(safe_path(old), 'Invalid migration removal path')
            require(old not in removed, 'Duplicate migration removal')
            removed.add(old)
            require(not (roots['eyleme'] / old).exists(), f'Duplicate original document remains in core: {old}')
    require(len(removed) == 21, 'Core removal inventory is incomplete')
    return len(documents)


def safe_path(value):
    return (isinstance(value, str) and bool(value) and '\\' not in value
            and not PurePosixPath(value).is_absolute()
            and all(part not in {'..', '.'} for part in value.split('/')))


def validate_snapshot(snapshot):
    require(snapshot.get('format_version') == 1, 'Unknown migration snapshot version')
    inventory = snapshot.get('inventory', {})
    require(inventory.get('repository') == 'eylema-dev/devguide'
            and inventory.get('path') == 'records/document-migration.json', 'Unexpected inventory source')
    require(bool(re.fullmatch('[0-9a-f]{64}', inventory.get('sha256', ''))), 'Invalid inventory hash')
    destinations = snapshot.get('destinations', {})
    require(set(destinations) == {'eylema-docs-en', 'eylema-docs-tr', 'devguide'}, 'Historical destination coverage')
    for name, member in destinations.items():
        require(member.get('repository') == 'eylema-dev/' + name, 'Unexpected historical repository')
    sources = snapshot.get('sources', {})
    require(sources.get('repository') == 'eylema-dev/eylema', 'Unexpected historical source repository')
    revisions = sources.get('revisions', [])
    require(len(revisions) == 2 and len(set(revisions)) == 2, 'Historical source coverage')
    revisions = revisions + [inventory.get('revision', '')] + [m.get('revision', '') for m in destinations.values()]
    require(all(re.fullmatch('[0-9a-f]{40}', r) for r in revisions), 'Historical references must be immutable SHAs')
    require(inventory['revision'] == destinations['devguide']['revision'], 'Inventory/destination anchor mismatch')
    return snapshot


def history_roots(snapshot, cache):
    """Fetch fixed public identities and validated commits as data, never code."""
    validate_snapshot(snapshot)
    roots = {}
    for name, member in snapshot['destinations'].items():
        roots[(member['repository'], member['revision'])] = fetch_members({name: member}, cache)[name]
    for revision in snapshot['sources']['revisions']:
        member = {'repository': snapshot['sources']['repository'], 'revision': revision}
        roots[(member['repository'], revision)] = fetch_members({'eylema': member}, cache)['eylema']
    return roots


def historical_bytes(roots, repository, revision, path):
    require(safe_path(path), 'Invalid historical artifact path')
    require((repository, revision) in roots, 'Unpinned historical artifact')
    root = roots[(repository, revision)]
    require(git(root, 'rev-parse', 'HEAD') == revision, 'Wrong historical checkout revision')
    # Read Git blobs rather than potentially edited working files or symlinks.
    mode = git(root, 'ls-tree', revision, '--', path).split()
    require(mode and mode[0] in {'100644', '100755'}, 'Historical artifact is missing or not a regular file')
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', 'show', revision + ':' + path],
                          cwd=root, check=True, capture_output=True, timeout=60).stdout


def validate_historical_migration(guide, roots, snapshot):
    validate_snapshot(snapshot)
    anchor = snapshot['inventory']
    original = historical_bytes(roots, anchor['repository'], anchor['revision'], anchor['path'])
    require(hashlib.sha256(original).hexdigest() == anchor['sha256'], 'Historical inventory hash mismatch')
    require((guide / anchor['path']).read_bytes() == original, 'Historical migration inventory was changed')
    inventory = json.loads(original)
    documents = inventory.get('documents', [])
    require(len(documents) == 26, 'Historical inventory coverage')
    for row in documents:
        for prefix, repository, revision, path, expected in [
            ('source', row['source_repository'], row['source_revision'], row['source_path'], row['source_sha256']),
            ('destination', row['destination_repository'],
             snapshot['destinations'][row['destination_repository'].removeprefix('eylema-dev/')]['revision'],
             row['destination_path'], row['destination_sha256']),
        ]:
            actual = historical_bytes(roots, repository, revision, path)
            require(hashlib.sha256(actual).hexdigest() == expected, f'Historical {prefix} hash mismatch: {path}')
        for prefix in ('previous_main', 'replaced_main'):
            if row.get(prefix + '_path'):
                actual = historical_bytes(roots, row['source_repository'], row[prefix + '_revision'], row[prefix + '_path'])
                require(hashlib.sha256(actual).hexdigest() == row[prefix + '_sha256'], f'Historical {prefix} hash mismatch')
    return len(documents)


def check(guide, roots, manifest, history=None):
    validate_heads(roots, validate_set(manifest))
    roots = dict(roots, devguide=guide)
    snapshot = load_json(guide / 'records/migration-snapshot.json')
    if history is None:
        history = history_roots(snapshot, guide / '.cache/migration-history')
    historical = validate_historical_migration(guide, history, snapshot)
    operations = validate_product_pairs(roots, manifest)
    count = validate_migration(roots, load_json(guide / 'records/document-migration.json'))
    links = 0
    for name, root in roots.items():
        if name != 'devguide':
            vendor = load_json(root / 'tools/vendor.json')
            verify_vendor(root, vendor)
            for path, expected in vendor['files'].items():
                require((guide / path).is_file() and digest(guide / path) == expected,
                        f'Shared-tool source/copy drift: {name}/{path}')
        for path in repository_files(root):
            if path.endswith('.md'):
                text = (root / path).read_text()
                errors = cross_link_errors(roots, text)
                require(not errors, f'Broken cross-repository target in {name}/{path}: {errors}')
                links += 1
    print(f'PASS: {len(roots)} repositories, {len(PRODUCT_DOCS)} product translation pairs, {operations} API operations, {count} current migration destinations, {historical} immutable historical records, {links} Markdown documents checked for cross-repository targets')
    print('Scope: pinned document snapshots only; no fetched member code, runtime, GPU, model or training was executed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true')
    group.add_argument('--workspace-file', type=Path)
    args = parser.parse_args()
    manifest = load_json(ROOT / 'tools/repository-set.json')
    members = validate_set(manifest)
    roots = fetch_members(members, ROOT / '.cache/repository-set') if args.fetch else {
        name: Path(path) for name, path in load_json(args.workspace_file).items() if name != 'devguide'}
    check(ROOT, roots, manifest)


if __name__ == '__main__':
    try:
        main()
    except (CheckFailure, ValueError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f'FAIL: {error}') from error
