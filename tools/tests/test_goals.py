"""G00 record integrity only; no task authority or runtime support is established."""
import copy
import json
import re
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
IDS = {f'G{i:02}' for i in range(46)} | {'W01'}
REPOSITORIES = {'eylema', 'eylema-docs-en', 'eylema-docs-tr', 'devguide', '.github',
                'eylema-examples', 'eylema-evals', 'eylema-models', 'eylema-training', 'eylemadotdev'}


def validate_records(baseline, index):
    """Reject incomplete/drifting records. This cannot verify snapshot truth remotely."""
    def require(value, message):
        if not value:
            raise ValueError(message)

    def sha(value, length):
        return isinstance(value, str) and bool(re.fullmatch(f'[0-9a-f]{{{length}}}', value))

    def relative(path):
        return isinstance(path, str) and bool(path) and not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts and '\\' not in path

    require(baseline['format_version'] == index['format_version'] == 1, 'Record version')
    repos = baseline['repositories']
    require(set(repos) == REPOSITORIES, 'Ten repository coverage')
    for name, member in repos.items():
        require(member['repository'] == 'eylema-dev/' + name, 'Repository identity')
        require(sha(member['main_sha'], 40) and sha(member['tree_sha'], 40), 'Immutable main/tree revision')
        require(member['role'] and member['default_branch'] == 'main', 'Repository role/branch')
        require(all(c['head_sha'] == member['main_sha'] for c in member['checks']), 'Check revision binding')
    require(index['source_plan_sha256'] == baseline['source_plan']['sha256'] and sha(index['source_plan_sha256'], 64), 'Source plan binding')
    require(set(baseline['shared_contracts']) == {'AGENTS.md','CONTRIBUTING.md','docs/en/quality-gates.md','docs/en/tooling.md','tools/repository-set.json'}, 'Policy inventory')
    for path, contract in baseline['shared_contracts'].items():
        require(sha(contract['sha256'], 64) and f"/blob/{repos['devguide']['main_sha']}/{path}" in contract['url'], 'Policy commit/hash binding')
    require(bool(baseline['preserved_worktrees']), 'Missing preservation inventory')
    for entry in baseline['preserved_worktrees'].values():
        require(sha(entry['head'], 40) and sha(entry['content_manifest_sha256'], 64) and sha(entry['status_sha256'], 64), 'Preservation digests')
        require(entry['branch'] and entry['file_count'] > 0 and isinstance(entry['dirty'], bool), 'Preservation scope')
    cards = index['goals']
    require(len(cards) == len(IDS) and {c['id'] for c in cards} == IDS, 'All 47 unique Goal IDs')
    by_id = {c['id']: c for c in cards}
    for card in cards:
        name = card['repository'].removeprefix('eylema-dev/')
        require(name in repos and card['repository'] == 'eylema-dev/' + name, 'Goal owner')
        require(card['base_sha'] == repos[name]['main_sha'], 'Goal baseline binding')
        require(card['task_revision'] == 1 and card['objective'] and card['risk'], 'Task revision/objective/risk')
        dependencies = card['dependencies']
        require(len(dependencies) == len(set(dependencies)) and set(dependencies) <= IDS and card['id'] not in dependencies, 'Dependency identity')
        require(set(card['dependency_acceptance']) == set(dependencies), 'Dependency acceptance coverage')
        require(all(v is None for v in card['dependency_acceptance'].values()), 'No fabricated accepted dependency')
        require(card['allowed_paths'] and all(relative(p) for p in card['allowed_paths']), 'Scope paths')
        require(set(card['linked_scope']) == {r.removeprefix('eylema-dev/') for r in card['linked_repositories']}, 'Linked scope coverage')
        require(all(r in {'eylema-dev/' + n for n in repos} for r in card['linked_repositories']), 'Linked repository identity')
        require(card['contract_bindings'] and card['contract_versions'], 'Contract versions')
        require(card['acceptance'] and all(a['requirement'] and a['check'] and a['id'].startswith(card['id'] + '-') and a['result'].startswith('not_run') for a in card['acceptance']), 'Acceptance/check mapping without fabricated evidence')
        budget = card['budget']
        require(budget['active_minutes'] == 120 and budget['max_targeted_repairs'] == 3 and budget['token_budget'] is None and budget['new_spending'] is False, 'Finite plan budget')
        require(card['model']['planned'] == 'gpt-6.1-sol' and card['model']['reasoning_effort'] == 'high', 'Planned settings')
        require(set(card['roles']) == {'architect','implementer','verifier','independent_reviewer'}, 'Actual role slots')
        require(card['delivery']['checks'] and card['delivery']['review'] and card['delivery']['rollback'] and card['handoff']['remaining_blockers'] and card['stop_conditions'] and card['exclusions'], 'Delivery/handoff/stop boundary')
        require(card['status'] == ('implementing' if card['id'] == 'G00' else 'backlog'), 'No premature activation/acceptance')
        require((card['issue'] is not None) == (card['id'] == 'G00'), 'Only G00 issue materialized')
    require(by_id['W01']['conditional_dependencies'] == {'working_product_claims':['G44']}, 'Website acceptance condition')
    require(set(by_id['G44']['dependencies']) == {f'G{i:02}' for i in range(7,44)}, 'Full M1–M7 acceptance scope')
    visited, active = set(), set()

    def visit(gid):
        require(gid not in active, 'Dependency cycle')
        if gid in visited:
            return
        active.add(gid)
        card = by_id[gid]
        for dependency in card['dependencies'] + [d for group in card['conditional_dependencies'].values() for d in group]:
            require(dependency in IDS, 'Unknown conditional dependency')
            visit(dependency)
        active.remove(gid)
        visited.add(gid)

    for gid in IDS:
        visit(gid)
    require(set(x for group in index['recommended_order'] for x in group) == IDS, 'Recommended order coverage')


class GoalRecordTests(unittest.TestCase):
    def setUp(self):
        self.baseline = json.loads((ROOT / 'records/g00-baseline.json').read_text())
        self.index = json.loads((ROOT / 'records/goal-index.json').read_text())

    def test_checked_in_records_and_language_index_coverage(self):
        validate_records(self.baseline, self.index)
        for lang in ('en', 'tr'):
            text = (ROOT / f'docs/{lang}/goal-program.md').read_text()
            rows = re.findall(r'^\| \*\*((?:G\d\d|W01)) — ', text, re.M)
            self.assertEqual(len(rows), 47)
            self.assertEqual(set(rows), IDS)

    def test_missing_duplicate_unknown_and_cyclic_goals_fail(self):
        for mode in ('missing','duplicate','unknown','cycle','conditional-cycle'):
            bad = copy.deepcopy(self.index)
            if mode == 'missing': bad['goals'].pop()
            if mode == 'duplicate': bad['goals'][-1] = bad['goals'][0]
            if mode == 'unknown': bad['goals'][1]['dependencies'] = ['G99']
            if mode == 'cycle':
                bad['goals'][0]['dependencies'] = ['G01']
                bad['goals'][0]['dependency_acceptance'] = {'G01':None}
            if mode == 'conditional-cycle': bad['goals'][3]['conditional_dependencies'] = {'condition':['W01']}
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_records(self.baseline, bad)

    def test_wrong_pin_check_policy_owner_and_fabricated_acceptance_fail(self):
        for mode in ('pin','check','policy','owner','source','accepted','release-scope'):
            baseline, index = copy.deepcopy(self.baseline), copy.deepcopy(self.index)
            if mode == 'pin': index['goals'][0]['base_sha'] = 'main'
            if mode == 'check': baseline['repositories']['eylema']['checks'][0]['head_sha'] = 'a'*40
            if mode == 'policy': baseline['shared_contracts']['AGENTS.md']['url'] = 'https://github.com/eylema-dev/devguide/blob/main/AGENTS.md'
            if mode == 'owner': index['goals'][0]['repository'] = 'other/devguide'
            if mode == 'source': index['source_plan_sha256'] = 'b'*64
            if mode == 'accepted': index['goals'][1]['dependency_acceptance']['G00'] = 'c'*40
            if mode == 'release-scope': index['goals'][44]['dependencies'].remove('G35')
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_records(baseline, index)

    def test_missing_check_escaping_scope_unbounded_budget_and_premature_execution_fail(self):
        for mode in ('check','escape','absolute','budget','handoff','status','issue'):
            bad = copy.deepcopy(self.index)
            card = bad['goals'][1]
            if mode == 'check': card['acceptance'][0]['check'] = ''
            if mode == 'escape': card['allowed_paths'] = ['../outside']
            if mode == 'absolute': card['allowed_paths'] = ['/outside']
            if mode == 'budget': card['budget']['max_targeted_repairs'] = None
            if mode == 'handoff': card['handoff']['remaining_blockers'] = []
            if mode == 'status': card['status'] = 'accepted'
            if mode == 'issue': card['issue'] = 'https://github.com/eylema-dev/devguide/issues/999'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_records(self.baseline, bad)


if __name__ == '__main__':
    unittest.main()
