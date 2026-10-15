"""Negative tests for immutable multi-repository document validation."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_repository import CheckFailure, PRODUCT_DOCS
from check_workspace import (MEMBERS, cross_link_errors, validate_migration,
                             validate_product_pairs, validate_set, validate_heads,
                             validate_snapshot, validate_historical_migration, historical_bytes)


def repository_set():
    return {'format_version': 1,
            'members': {n: {'repository': 'eyleme-dev/' + n, 'revision': 'a' * 40} for n in MEMBERS},
            'product_translations': {n: {'en_sha256': 'b' * 64, 'tr_sha256': 'c' * 64} for n in PRODUCT_DOCS}}


class WorkspaceTests(unittest.TestCase):
    def test_missing_member_mutable_ref_and_foreign_repository_fail(self):
        manifest = repository_set()
        validate_set(manifest)
        for mode in ('missing', 'branch', 'foreign', 'missing-translation'):
            bad = copy.deepcopy(manifest)
            if mode == 'missing': del bad['members']['eyleme']
            if mode == 'branch': bad['members']['eyleme']['revision'] = 'main'
            if mode == 'foreign': bad['members']['eyleme']['repository'] = 'other/repo'
            if mode == 'missing-translation': del bad['product_translations']['architecture']
            with self.subTest(mode=mode):
                with self.assertRaises(CheckFailure): validate_set(bad)

    def test_cross_repo_missing_and_escaping_targets_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'docs').mkdir()
            (root / 'docs/guide.md').write_text('Guide')
            roots = {'eyleme-docs-en': root}
            prefix = 'https://github.com/eyleme-dev/eyleme-docs-en/blob/main/'
            self.assertEqual(cross_link_errors(roots, f'[ok]({prefix}docs/guide.md)'), [])
            for target in ('missing.md', '../outside.md', '%2e%2e/outside.md'):
                with self.subTest(target=target):
                    self.assertTrue(cross_link_errors(roots, f'[bad]({prefix}{target})'))

    def test_product_hash_api_and_roadmap_drift_each_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            roots = {f'eyleme-docs-{lang}': Path(temp) / lang for lang in ('en', 'tr')}
            manifest = repository_set()
            for lang in ('en', 'tr'):
                docs = roots[f'eyleme-docs-{lang}'] / 'docs'
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
                path = roots['eyleme-docs-tr'] / f'docs/{name}.md'
                original = path.read_text()
                path.write_text(change(original))
                bad = copy.deepcopy(manifest)
                if refresh: bad['product_translations'][name]['tr_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                with self.subTest(name=name):
                    with self.assertRaises(CheckFailure): validate_product_pairs(roots, bad)
                path.write_text(original)

    def test_missing_workspace_roots_fail_before_git(self):
        with self.assertRaises(CheckFailure): validate_heads({}, repository_set()['members'])

    def test_current_migration_accepts_reviewed_edits_and_rejects_duplicates_missing_and_escapes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            core = root / 'core'
            dest = root / 'dest'
            core.mkdir(); dest.mkdir()
            roots = {'eyleme': core, 'devguide': dest, 'eyleme-docs-en': dest}
            inventory = {'documents': []}
            for i in range(26):
                path = dest / f'{i}.md'
                path.write_text('migrated')
                row = {'destination_repository': 'eylema-dev/devguide', 'destination_path': path.name,
                       'destination_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                if i < 21: row['previous_main_path'] = f'old-{i}.md'
                inventory['documents'].append(row)
            inventory['documents'][0]['destination_repository'] = 'eylema-dev/eylema-docs-en'
            self.assertEqual(validate_migration(roots, inventory), 26)
            duplicate = copy.deepcopy(inventory)
            duplicate['documents'][1].update(destination_repository='eyleme-dev/eyleme-docs-en', destination_path='0.md')
            with self.assertRaises(CheckFailure): validate_migration(roots, duplicate)
            (core / 'old-0.md').write_text('duplicate')
            with self.assertRaises(CheckFailure): validate_migration(roots, inventory)
            (core / 'old-0.md').unlink()
            (dest / '0.md').write_text('unreviewed change')
            # Current reviewed bytes are checked by the translation manifest, not historical hashes.
            self.assertEqual(validate_migration(roots, inventory), 26)
            (dest / '0.md').unlink()
            with self.assertRaises(CheckFailure): validate_migration(roots, inventory)
            (dest / '0.md').write_text('reviewed')
            for field in ('destination_path', 'previous_main_path'):
                bad = copy.deepcopy(inventory)
                bad['documents'][0][field] = '../outside.md'
                with self.subTest(field=field), self.assertRaises(CheckFailure):
                    validate_migration(roots, bad)

    def test_historical_inventory_and_source_destination_previous_bytes_remain_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            guide = Path(temp)
            (guide / 'records').mkdir()
            snapshot = {'format_version':1,
                        'inventory':{'repository':'eylema-dev/devguide','revision':'a'*40,
                                     'path':'records/document-migration.json'},
                        'destinations':{name:{'repository':'eylema-dev/'+name,'revision':'a'*40}
                                        for name in ('devguide','eylema-docs-en','eylema-docs-tr')},
                        'sources':{'repository':'eylema-dev/eylema','revisions':['b'*40,'c'*40]}}
            documents, blobs = [], {}
            h = lambda data: hashlib.sha256(data).hexdigest()
            for i in range(26):
                row={'source_repository':'eylema-dev/eylema','source_revision':'b'*40,
                     'source_path':f'source/{i}.md','source_sha256':h(b'source'),
                     'destination_repository':'eylema-dev/devguide','destination_path':f'docs/{i}.md',
                     'destination_sha256':h(b'destination')}
                blobs[('eylema-dev/eylema','b'*40,row['source_path'])]=b'source'
                blobs[('eylema-dev/devguide','a'*40,row['destination_path'])]=b'destination'
                if i<21:
                    row.update(previous_main_path=f'old/{i}.md',previous_main_revision='c'*40,previous_main_sha256=h(b'old'))
                    blobs[('eylema-dev/eylema','c'*40,row['previous_main_path'])]=b'old'
                if i>=23:
                    row.update(replaced_main_path=f'contributor/{i}.md',replaced_main_revision='c'*40,replaced_main_sha256=h(b'replaced'))
                    blobs[('eylema-dev/eylema','c'*40,row['replaced_main_path'])]=b'replaced'
                documents.append(row)
            original=json.dumps({'documents':documents}).encode()
            inventory=guide/'records/document-migration.json'
            inventory.write_bytes(original)
            snapshot['inventory']['sha256']=h(original)
            blobs[('eylema-dev/devguide','a'*40,'records/document-migration.json')]=original
            def read_blob(roots,repo,rev,path):
                key=(repo,rev,path)
                if key not in blobs:
                    raise CheckFailure('Missing historical fixture artifact')
                return blobs[key]
            with patch('check_workspace.historical_bytes',side_effect=read_blob):
                self.assertEqual(validate_historical_migration(guide,{},snapshot),26)
                inventory.write_bytes(original+b' ')
                with self.assertRaises(CheckFailure): validate_historical_migration(guide,{},snapshot)
                inventory.write_bytes(original)
                for key in [('eylema-dev/eylema','b'*40,'source/0.md'),
                            ('eylema-dev/devguide','a'*40,'docs/0.md'),
                            ('eylema-dev/eylema','c'*40,'old/0.md'),
                            ('eylema-dev/eylema','c'*40,'contributor/23.md'),
                            ('eylema-dev/eylema','c'*40,'contributor/24.md'),
                            ('eylema-dev/eylema','c'*40,'contributor/25.md')]:
                    before=blobs[key];blobs[key]=b'corrupted'
                    with self.subTest(key=key), self.assertRaises(CheckFailure):
                        validate_historical_migration(guide,{},snapshot)
                    del blobs[key]
                    with self.subTest(missing=key), self.assertRaises(CheckFailure):
                        validate_historical_migration(guide,{},snapshot)
                    blobs[key]=before
                bad=copy.deepcopy(snapshot);bad['inventory']['sha256']='d'*64
                with self.assertRaises(CheckFailure): validate_historical_migration(guide,{},bad)
            for mode in ('mutable','foreign','missing','anchor'):
                bad=copy.deepcopy(snapshot)
                if mode=='mutable': bad['sources']['revisions'][0]='main'
                if mode=='foreign': bad['sources']['repository']='other/repo'
                if mode=='missing': del bad['destinations']['eylema-docs-en']
                if mode=='anchor': bad['inventory']['revision']='d'*40
                with self.subTest(mode=mode), self.assertRaises(CheckFailure): validate_snapshot(bad)

    def test_historical_blobs_ignore_worktree_edits_and_reject_symlinks_wrong_heads_and_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            def git(*args):
                return subprocess.check_output(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],cwd=root).decode().strip()
            git('init','--quiet')
            (root/'record.md').write_text('accepted bytes')
            (root/'link.md').symlink_to('record.md')
            git('add','record.md','link.md');git('commit','--quiet','-m','historical fixture')
            head=git('rev-parse','HEAD');roots={('eylema-dev/devguide',head):root}
            (root/'record.md').write_text('current edit')
            self.assertEqual(historical_bytes(roots,'eylema-dev/devguide',head,'record.md'),b'accepted bytes')
            for path in ('link.md','missing.md','../record.md','/record.md'):
                with self.subTest(path=path),self.assertRaises(CheckFailure):
                    historical_bytes(roots,'eylema-dev/devguide',head,path)
            with self.assertRaises(CheckFailure): historical_bytes(roots,'eylema-dev/devguide','a'*40,'record.md')
            git('add','record.md');git('commit','--quiet','-m','new revision')
            with self.assertRaises(CheckFailure): historical_bytes(roots,'eylema-dev/devguide',head,'record.md')


if __name__ == '__main__':
    unittest.main()
