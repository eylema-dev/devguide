"""Verify a pinned Eylema repository set as data; never execute fetched member code."""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

from check_repository import (ROOT, ROLES, PRODUCT_DOCS, CheckFailure, load_json,
                              require, repository_files, validate_api, verify_vendor)

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
        require(member.get('repository') == 'eylema-dev/' + name, 'Repository identity is outside the approved set')
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
        # All values passed to git were validated against a fixed identity set above.
        path = cache / ('organization-github' if name == '.github' else name) / member['revision']
        if not path.exists():
            path.mkdir(parents=True)
            git(path, 'init', '--quiet')
            git(path, 'remote', 'add', 'origin', f'https://github.com/{member["repository"]}.git')
        origin = git(path, 'remote', 'get-url', 'origin')
        require(origin == f'https://github.com/{member["repository"]}.git', 'Unexpected cached origin')
        git(path, 'fetch', '--quiet', '--depth=1', 'origin', member['revision'])
        git(path, 'checkout', '--quiet', '--detach', member['revision'])
        roots[name] = path
    return roots


def validate_heads(roots, members):
    require(set(roots) == MEMBERS, 'Workspace roots must match the pinned repository set')
    for name, root in roots.items():
        require(git(root, 'rev-parse', 'HEAD') == members[name]['revision'], f'Wrong pinned revision: {name}')
        require(not git(root, 'status', '--porcelain', '--untracked-files=all'), f'Dirty repository cannot represent a pinned snapshot: {name}')
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
        if len(parts) < 5 or parts[0] != 'eylema-dev' or parts[1] not in roots:
            continue
        if parts[2] not in {'blob', 'tree'} or parts[3] != 'main':
            continue  # historical commit, PR and issue references are not current-layout targets
        root = roots[parts[1]].resolve()
        path = root.joinpath(*parts[4:]).resolve()
        valid = path.is_file() if parts[2] == 'blob' else path.is_dir()
        if not path.is_relative_to(root) or not valid:
            errors.append(target)
    return errors


def validate_product_pairs(roots, manifest):
    for name in PRODUCT_DOCS:
        for lang in ('en', 'tr'):
            path = roots[f'eylema-docs-{lang}'] / f'docs/{name}.md'
            require(path.is_file(), f'Missing product translation: {lang}/{name}')
            require(digest(path) == manifest['product_translations'][name][lang + '_sha256'],
                    f'Product translation fingerprint is stale: {lang}/{name}')
    en = roots['eylema-docs-en'] / 'docs'
    tr = roots['eylema-docs-tr'] / 'docs'
    operations = validate_api((en / 'api-reference.md').read_text(), (tr / 'api-reference.md').read_text())
    ids = lambda path: re.findall(r'^\| (M\d+|EYL-\d+) \|', path.read_text(), re.M)
    require(bool(ids(en / 'roadmap.md')) and ids(en / 'roadmap.md') == ids(tr / 'roadmap.md'), 'Cross-repository roadmap ID mismatch')
    return operations


def validate_migration(roots, inventory):
    documents = inventory.get('documents', [])
    require(len(documents) == 26, 'Migration inventory is incomplete')
    seen = set()
    removed = set()
    for row in documents:
        repo = row['destination_repository'].removeprefix('eylema-dev/')
        require(repo in roots, 'Unknown migration destination')
        key = (repo, row['destination_path'])
        require(key not in seen, 'Duplicate migration destination')
        seen.add(key)
        root = roots[repo].resolve()
        path = (root / row['destination_path']).resolve()
        require(path.is_relative_to(root) and path.is_file(), 'Missing or escaping migration destination')
        require(digest(path) == row['destination_sha256'], f'Migration destination changed: {key}')
        if old := row.get('previous_main_path'):
            require(old not in removed, 'Duplicate migration removal')
            removed.add(old)
            require(not (roots['eylema'] / old).exists(), f'Duplicate original document remains in core: {old}')
    require(len(removed) == 21, 'Core removal inventory is incomplete')
    return len(documents)


def check(guide, roots, manifest):
    validate_heads(roots, validate_set(manifest))
    roots = dict(roots, devguide=guide)
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
    print(f'PASS: {len(roots)} repositories, {len(PRODUCT_DOCS)} product translation pairs, {operations} API operations, {count} migration destinations, {links} Markdown documents checked for cross-repository targets')
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
