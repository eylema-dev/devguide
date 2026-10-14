"""The organization rename preserves historical evidence without trusting lookalikes."""
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from github_identity import canonical_endpoint, canonical_repository, canonical_url
from check_workspace import fetch_members, cross_link_errors, validate_set
from check_repository import CheckFailure, PRODUCT_DOCS
from check_workspace import MEMBERS


class GitHubIdentityTests(unittest.TestCase):
    def test_only_exact_renamed_managed_repositories_are_equivalent(self):
        for org in ('eylema-dev', 'eyleme-dev'):
            self.assertEqual(canonical_repository(org + '/eylema'), 'eyleme-dev/eyleme')
            self.assertEqual(canonical_url(f'https://github.com/{org}/eylema/pull/7'),
                             'https://github.com/eyleme-dev/eyleme/pull/7')
            self.assertEqual(canonical_endpoint(f'repos/{org}/eylema/commits/abc/check-runs?per_page=100'),
                             'repos/eyleme-dev/eyleme/commits/abc/check-runs?per_page=100')
        self.assertEqual(canonical_repository('eyleme-dev/eyleme'), 'eyleme-dev/eyleme')
        for value in ('other/eylema', 'eyleme-dev-evil/eylema', 'eyleme-dev/eylema-evil',
                      'eylema-dev/eyleme', 'eyleme-dev/eylema/extra', 'eyleme-dev/../eylema', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                canonical_repository(value)
        for value in ('https://github.com.evil/eylema-dev/eylema/pull/7',
                      'http://github.com/eylema-dev/eylema/pull/7'):
            with self.assertRaises(ValueError): canonical_url(value)
        for value in ('https://outside/permissions', 'repos/eyleme-dev/eyleme/../other',
                      'repos/eyleme-dev/eyleme/issues/1#fragment'):
            with self.assertRaises(ValueError): canonical_endpoint(value)

    def test_current_manifest_cannot_claim_historical_or_foreign_owner(self):
        manifest = {'format_version': 1,
                    'members': {name: {'repository': 'eyleme-dev/' + name, 'revision': 'a' * 40}
                                for name in MEMBERS},
                    'product_translations': {name: {'en_sha256': 'b' * 64, 'tr_sha256': 'c' * 64}
                                             for name in PRODUCT_DOCS}}
        validate_set(manifest)
        for owner in ('eylema-dev', 'eyleme-dev-evil', 'other'):
            bad = copy.deepcopy(manifest)
            bad['members']['eyleme']['repository'] = owner + '/eylema'
            with self.assertRaises(CheckFailure): validate_set(bad)

    def test_historical_fetch_uses_new_owner_and_preserves_old_evidence(self):
        members = {'eylema': {'repository': 'eylema-dev/eylema', 'revision': 'a' * 40}}
        original = copy.deepcopy(members)
        calls = []
        def fake_git(root, *args):
            calls.append(args)
            return 'https://github.com/eyleme-dev/eyleme.git' if args == ('remote', 'get-url', 'origin') else ''
        with tempfile.TemporaryDirectory() as temp, patch('check_workspace.git', side_effect=fake_git):
            fetch_members(members, Path(temp))
        self.assertEqual(members, original)
        self.assertIn(('remote', 'add', 'origin', 'https://github.com/eyleme-dev/eyleme.git'), calls)
        self.assertIn(('fetch', '--quiet', '--depth=1', 'origin', 'a' * 40), calls)
        for value in ({'repository': 'other/eylema', 'revision': 'a' * 40},
                      {'repository': 'eyleme-dev/devguide', 'revision': 'a' * 40},
                      {'repository': 'eyleme-dev/eyleme', 'revision': 'main'}):
            with tempfile.TemporaryDirectory() as temp, patch('check_workspace.git') as git:
                with self.assertRaises((ValueError, CheckFailure)):
                    fetch_members({'eylema': value}, Path(temp))
                git.assert_not_called()

    def test_old_and_new_current_document_links_keep_missing_target_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'README.md').write_text('Current document')
            for org in ('eyleme-dev', 'eylema-dev'):
                prefix = f'https://github.com/{org}/eylema/blob/main/'
                self.assertEqual(cross_link_errors({'eyleme': root}, f'[ok]({prefix}README.md)'), [])
                self.assertTrue(cross_link_errors({'eyleme': root}, f'[bad]({prefix}missing.md)'))
            self.assertTrue(cross_link_errors({'eyleme': root},
                '[unverified](https://github.com/eylema-dev/eyleme/blob/main/README.md)'))
            self.assertEqual(cross_link_errors({'eyleme': root},
                '[current](https://github.com/eyleme-dev/eyleme/blob/main/README.md)'), [])

    def test_historical_api_read_maps_owner_and_keeps_get_only(self):
        import check_goal_tracking
        import check_platform_plan
        for module in (check_goal_tracking, check_platform_plan):
            with patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '{}', '')) as run:
                self.assertEqual(module.api('repos/eylema-dev/devguide/issues/10'), {})
                self.assertEqual(run.call_args.args[0], ['gh', 'api', '--method', 'GET',
                                                       'repos/eyleme-dev/devguide/issues/10'])
            with patch.object(module.subprocess, 'run') as run, self.assertRaises(ValueError):
                module.api('repos/eyleme-dev-evil/devguide/issues/10')
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
