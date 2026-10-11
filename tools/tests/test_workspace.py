"""Negative tests for immutable multi-repository document validation."""
import copy
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_repository import CheckFailure, PRODUCT_DOCS
from check_workspace import (MEMBERS, cross_link_errors, validate_migration,
                             validate_product_pairs, validate_set, validate_heads)


def repository_set():
    return {'format_version': 1,
            'members': {n: {'repository': 'eylema-dev/' + n, 'revision': 'a' * 40} for n in MEMBERS},
            'product_translations': {n: {'en_sha256': 'b' * 64, 'tr_sha256': 'c' * 64} for n in PRODUCT_DOCS}}


class WorkspaceTests(unittest.TestCase):
    def test_missing_member_mutable_ref_and_foreign_repository_fail(self):
        manifest = repository_set()
        validate_set(manifest)
        for mode in ('missing', 'branch', 'foreign', 'missing-translation'):
            bad = copy.deepcopy(manifest)
            if mode == 'missing': del bad['members']['eylema']
            if mode == 'branch': bad['members']['eylema']['revision'] = 'main'
            if mode == 'foreign': bad['members']['eylema']['repository'] = 'other/repo'
            if mode == 'missing-translation': del bad['product_translations']['architecture']
            with self.subTest(mode=mode):
                with self.assertRaises(CheckFailure): validate_set(bad)

    def test_cross_repo_missing_and_escaping_targets_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'docs').mkdir()
            (root / 'docs/guide.md').write_text('Guide')
            roots = {'eylema-docs-en': root}
            prefix = 'https://github.com/eylema-dev/eylema-docs-en/blob/main/'
            self.assertEqual(cross_link_errors(roots, f'[ok]({prefix}docs/guide.md)'), [])
            for target in ('missing.md', '../outside.md', '%2e%2e/outside.md'):
                with self.subTest(target=target):
                    self.assertTrue(cross_link_errors(roots, f'[bad]({prefix}{target})'))

    def test_product_hash_api_and_roadmap_drift_each_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            roots = {f'eylema-docs-{lang}': Path(temp) / lang for lang in ('en', 'tr')}
            manifest = repository_set()
            for lang in ('en', 'tr'):
                docs = roots[f'eylema-docs-{lang}'] / 'docs'
                docs.mkdir(parents=True)
                for name in PRODUCT_DOCS:
                    content = 'Reviewed document'
                    if name == 'api-reference': content = 'source_revision: 0.1.0\n| `getTask` | `GET /tasks` | Read |\n'
                    if name == 'roadmap': content = '| M0 | Gate |\n| EYL-001 | Task |\n'
                    (docs / f'{name}.md').write_text(content)
                    manifest['product_translations'][name][lang + '_sha256'] = hashlib.sha256(content.encode()).hexdigest()
            self.assertEqual(validate_product_pairs(roots, manifest), 1)
            for name, change, refresh in [('architecture', lambda s: s + ' edit', False),
                                          ('api-reference', lambda s: s.replace('GET', 'POST'), True),
                                          ('roadmap', lambda s: s.replace('M0', 'M9'), True)]:
                path = roots['eylema-docs-tr'] / f'docs/{name}.md'
                original = path.read_text()
                path.write_text(change(original))
                bad = copy.deepcopy(manifest)
                if refresh: bad['product_translations'][name]['tr_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                with self.subTest(name=name):
                    with self.assertRaises(CheckFailure): validate_product_pairs(roots, bad)
                path.write_text(original)

    def test_missing_workspace_roots_fail_before_git(self):
        with self.assertRaises(CheckFailure): validate_heads({}, repository_set()['members'])

    def test_migration_catches_duplicate_old_files_and_destination_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            core = root / 'core'
            dest = root / 'dest'
            core.mkdir(); dest.mkdir()
            roots = {'eylema': core, 'devguide': dest}
            inventory = {'documents': []}
            for i in range(26):
                path = dest / f'{i}.md'
                path.write_text('migrated')
                row = {'destination_repository': 'eylema-dev/devguide', 'destination_path': path.name,
                       'destination_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                if i < 15: row['previous_main_path'] = f'old-{i}.md'
                inventory['documents'].append(row)
            self.assertEqual(validate_migration(roots, inventory), 26)
            (core / 'old-0.md').write_text('duplicate')
            with self.assertRaises(CheckFailure): validate_migration(roots, inventory)
            (core / 'old-0.md').unlink()
            (dest / '0.md').write_text('unreviewed change')
            with self.assertRaises(CheckFailure): validate_migration(roots, inventory)


if __name__ == '__main__':
    unittest.main()
