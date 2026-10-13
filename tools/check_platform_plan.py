"""Validate current harness cards without rewriting historical Goal evidence."""
import argparse
import hashlib
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ROLES = {'perception', 'reasoning', 'planning', 'decision', 'policy',
         'world_model', 'specialist', 'critic', 'representation'}
STATES = {'planned', 'blocked', 'implementing', 'verification', 'review',
          'ready_for_maintainer', 'accepted'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def sha(value):
    return isinstance(value, str) and bool(re.fullmatch('[0-9a-f]{40}', value))


def relative(value):
    return (isinstance(value, str) and bool(value)
            and not PurePosixPath(value).is_absolute()
            and '..' not in PurePosixPath(value).parts and '\\' not in value)


def validate_proof(proof, repository):
    require(proof['repository'] == repository and all(sha(proof[k]) for k in ('head', 'main', 'tree')), 'Accepted revision binding')
    require(bool(re.fullmatch(re.escape('https://github.com/' + repository + '/pull/') + '[1-9][0-9]*', proof['pr'])), 'Accepted owned PR')
    review, ci = proof['review'], proof['main_ci']
    reviewer = review['reviewer']
    require(review['status'] == 'passed' and review['reviewed_head'] == proof['head']
            and isinstance(reviewer, str) and bool(reviewer.strip())
            and not re.search(r'\b(?:unassigned|pending|unknown|tbd|todo)\b', reviewer, re.I), 'Separate exact-head review')
    require(type(ci['id']) is int and ci['id'] > 0 and ci['head'] == proof['main'] and ci['status'] == 'passed'
            and ci['url'] == f"https://github.com/{repository}/actions/runs/{ci['id']}", 'Exact-main CI')


def validate_plan(plan, index, tracking):
    require(plan['format_version'] == 1 and type(plan['revision']) is int and plan['revision'] > 0, 'Plan version')
    require(plan['historical_cards_sha256'] == digest(index)
            and plan['legacy_tracking_sha256'] == digest(tracking), 'Immutable source snapshot binding')
    historical = {g['id']: g for g in index['goals']}
    legacy = {g['id']: g for g in tracking['goals']}
    accepted = {g['id'] for g in tracking['goals'] if g['status'] == 'accepted'}
    require(len(plan['accepted_goal_ids']) == len(accepted)
            and set(plan['accepted_goal_ids']) == accepted, 'Historical accepted evidence preserved')
    remaining = set(legacy) - accepted
    require(len(plan['remaining_original_goal_ids']) == len(remaining)
            and set(plan['remaining_original_goal_ids']) == remaining, 'All remaining original cards')
    new = plan['new_goal_ids']
    require(len(new) == len(set(new)) and bool(new)
            and not set(new) & set(historical)
            and all(re.fullmatch(r'G[0-9]{2}', gid) for gid in new), 'New unique Goal identities')
    goals = plan['goals']
    require(len(goals) == len(remaining | set(new))
            and {g['id'] for g in goals} == remaining | set(new), 'Complete unique current cards')
    current = {g['id']: g for g in goals}
    ids = accepted | set(current)
    require(len(plan['roles']) == len(ROLES) and set(plan['roles']) == ROLES, 'Nine model roles')
    require({'speech_to_text', 'text_to_speech', 'image_video_perception'} <= set(plan['capability_profiles'])
            and len(plan['capability_profiles']) == len(set(plan['capability_profiles'])), 'Separate modality profiles')
    data = plan['data_policy']
    require(data['default'] == 'project_private' and data['derivative_permissions_inherited'] is True
            and data['automatic_private_sharing'] is False
            and set(data['permissions']) == {'execute', 'collect', 'train', 'external_disclosure', 'ecosystem_export'}, 'Project-private and derivative permissions')
    policy = plan['policy']
    require(policy['local_inference'] == 'first_party_rust_only'
            and policy['external_production_rust_crates'] is False
            and policy['hidden_inference_engine'] is False
            and policy['model_output_is_authority'] is False
            and policy['private_reasoning_collection'] is False, 'Rust, authority and privacy policy')
    require('explicit_opt_in' in policy['external_models'] and 'no silent fallback' in policy['external_models'], 'External calls stay explicit')
    require(policy['native_training'].startswith('first_party_rust_for_accepted_profiles')
            and 'not hidden production engines' in policy['native_training'], 'Owned Rust native training')
    require(set(plan['improvement_methods']) == {'model_specific_fine_tune', 'lora', 'qlora',
            'held_out_evaluation', 'controlled_promotion', 'versioned_skill_packaging'}, 'Bounded improvement methods')
    require('unknown' in plan['capacity_planning'] or 'uncertainty' in plan['capacity_planning'], 'Capacity uncertainty')
    require('no automatic investment/spend' in plan['capacity_planning'], 'No automatic investment')
    require({'G30', 'G57', 'G68', 'G70', 'G54', 'G50', 'G63', 'G73'} <= set(current['G72']['dependencies']), 'Early local job gates')
    require(not {'G49', 'G52', 'G53', 'G59', 'G60', 'G61', 'G62', 'G32'} & set(current['G72']['dependencies']), 'Early text proof independent of optional modalities')
    memory = plan['memory_policy']
    require(set(memory['kinds']) == {'working', 'episodic', 'semantic', 'procedural', 'knowledge_graph', 'analytical'}
            and len(memory['kinds']) == 6, 'Complete distinct memory kinds')
    require(memory['authority'] == 'retrieved_memory_is_untrusted_evidence'
            and memory['default'] == 'project_private' and memory['derivative_permissions_inherited'] is True,
            'Memory scope and evidence authority')
    require(memory['write_promotion'] == 'verified_outcome_or_explicit_review'
            and memory['retention'] == 'bounded_expiry_and_revocation_follow_indexes_caches_and_derivatives',
            'Reviewed memory promotion and lifecycle')
    require(memory['backend_policy'] == 'first_party_rust_production; SQLite and DuckDB are reference/interop candidates, no dependency exception or hidden engine'
            and memory['cortexdb_meaning'] == 'knowledge_graph_pattern_not_selected_product', 'Memory backend and graph policy')
    require(memory['goals'] == ['G87', 'G88', 'G89', 'G90'] and set(memory['goals']) <= set(new), 'Memory gate identity')
    memory_dependencies = {
        'G87': {'G46', 'G63'}, 'G88': {'G87', 'G70', 'G50'},
        'G89': {'G87', 'G33', 'G50'}, 'G90': {'G88', 'G89'},
        'G72': {'G88'}, 'G71': {'G88'}, 'G74': {'G87'},
        'G75': {'G87'}, 'G79': {'G89'}, 'G82': {'G89'},
    }
    require(all(required <= set(current[gid]['dependencies']) for gid, required in memory_dependencies.items()),
            'Memory acceptance before consuming jobs')
    require(plan['first_implementation_goal'] == 'G46', 'Independent first implementation slice')
    require(sum(g['status'] == 'implementing' for g in goals) <= 1, 'One implementation Goal')
    issue_urls = set()
    done = accepted | {g['id'] for g in goals if g['status'] == 'accepted'}
    for card in goals:
        gid = card['id']
        repo = card['repository']
        require(repo in {g['repository'] for g in historical.values()} and sha(card['base_sha']), 'Owner and immutable base')
        require(type(card['plan_card_revision']) is int and card['plan_card_revision'] > 0
                and card['title'] and card['objective'] and card['activation'], 'Card identity and activation binding')
        dependencies = card['dependencies']
        conditional = card['conditional_dependencies']
        require(len(dependencies) == len(set(dependencies)) and set(dependencies) <= ids and gid not in dependencies, 'Dependency identity')
        require(all(isinstance(group, list) and set(group) <= ids and gid not in group for group in conditional.values()), 'Conditional dependency identity')
        if gid in historical:
            require(repo == historical[gid]['repository']
                    and set(historical[gid]['dependencies']) <= set(dependencies)
                    and historical[gid]['conditional_dependencies'] == conditional, 'No waived original required gate')
            require(card['issue'] == legacy[gid]['issue'], 'Preserved original issue identity')
            original_acceptance = {(a['id'], a['requirement'], a['check']) for a in historical[gid]['acceptance']}
            current_acceptance = {(a['id'], a['requirement'], a['check']) for a in card['acceptance']}
            require(original_acceptance <= current_acceptance, 'Original required acceptance preserved')
        require(card['allowed_paths'] and all(relative(p) for p in card['allowed_paths']), 'Portable bounded scope')
        require(set(card['roles']) == {'architect', 'implementer', 'verifier', 'independent_reviewer'}
                and all(isinstance(actor, str) and actor for actor in card['roles'].values()), 'Execution role slots')
        require(all(relative(p) for paths in card['linked_scope'].values() if isinstance(paths, list) for p in paths), 'Linked scope')
        budget = card['budget']
        require(type(budget['active_minutes']) is int and 0 <= budget['active_minutes'] <= 120
                and type(budget['max_targeted_repairs']) is int and 0 <= budget['max_targeted_repairs'] <= 3
                and budget['token_budget'] is None and budget['new_spending'] is False
                and type(budget['new_provider_calls']) is int and budget['new_provider_calls'] == 0
                and type(budget['review_minutes']) is int and 0 < budget['review_minutes'] <= 15, 'Finite execution and review budget')
        require(type(budget['training_candidate_limit']) is int
                and budget['training_candidate_limit'] in (0, 1), 'Finite training candidate budget')
        require(gid == 'G40' or budget['active_minutes'] > 0, 'Positive new-task allowance')
        if gid == 'G40':
            require(card['status'] == 'blocked' and budget['active_minutes'] == 0
                    and budget['max_targeted_repairs'] == 0 and budget['training_candidate_limit'] == 0 and card['blockers'], 'G40 blocked with no reset')
        require(card['status'] in STATES, 'Current execution state')
        model = card['model']
        require(model['planned'] == 'gpt-6.1-sol' and model['reasoning_effort'] == 'high', 'Planned model settings')
        issue = card['issue']
        if issue is not None:
            require(type(issue['number']) is int and issue['number'] > 0
                    and issue['url'] == f"https://github.com/{repo}/issues/{issue['number']}"
                    and issue['url'] not in issue_urls, 'Unique owned issue')
            issue_urls.add(issue['url'])
        require(len(card['acceptance']) == len({a['id'] for a in card['acceptance']}), 'Unique acceptance identities')
        require(card['acceptance'] and all(a['requirement'] and a['check'] and a['id'].startswith(gid + '-') for a in card['acceptance']), 'Acceptance-to-check mapping')
        if card['status'] == 'accepted':
            require(issue is not None and all(a['result'] == 'passed' for a in card['acceptance']), 'Executed required acceptance')
            require(isinstance(card['accepted_delivery'], list) and card['accepted_delivery'], 'Accepted proof required')
            require(repo in {p['repository'] for p in card['accepted_delivery']}, 'Accepted primary delivery')
            require(len(card['accepted_delivery']) == len({p['repository'] for p in card['accepted_delivery']})
                    and all(p['repository'] in {h['repository'] for h in historical.values()} for p in card['accepted_delivery']), 'Unique canonical accepted repositories')
            for proof in card['accepted_delivery']:
                validate_proof(proof, proof['repository'])
        else:
            require(card['accepted_delivery'] is None and all(a['result'] == 'not_run' for a in card['acceptance']), 'No fabricated pending acceptance')
        if card['status'] not in {'planned', 'blocked'}:
            require(set(dependencies) <= done and issue is not None, 'Accepted dependencies before activation')
    require(set(new) <= set(current['G44']['dependencies']), 'All platform gates feed full release')
    order = plan['recommended_order']
    require(len(order) == len(current) and set(order) == set(current), 'One complete execution order')
    visited = set(accepted)
    for gid in order:
        require(set(current[gid]['dependencies']) <= visited, 'Acyclic dependency-before-execution order')
        visited.add(gid)
    active, checked = set(), set()
    def visit(gid):
        if gid in accepted or gid in checked:
            return
        require(gid not in active, 'Conditional dependency cycle')
        active.add(gid)
        card = current[gid]
        for dep in card['dependencies'] + [d for group in card['conditional_dependencies'].values() for d in group]:
            visit(dep)
        active.remove(gid)
        checked.add(gid)
    for gid in current:
        visit(gid)


def api(endpoint):
    require(endpoint.startswith('repos/eylema-dev/'), 'Canonical read-only API')
    result = subprocess.run(['gh', 'api', '--method', 'GET', endpoint], capture_output=True, text=True, timeout=60, check=False)
    require(result.returncode == 0, 'GitHub metadata unavailable: ' + endpoint)
    return json.loads(result.stdout)


def audit_card(card):
    issue = card['issue']
    require(issue is not None, 'Current issue not materialized: ' + card['id'])
    remote = api(f"repos/{card['repository']}/issues/{issue['number']}")
    marker = f"<!-- eylema-platform-goal:{card['id']}:r{card['plan_card_revision']} -->"
    require('pull_request' not in remote and remote['html_url'] == issue['url']
            and marker in (remote['body'] or ''), 'Actual current issue/card binding')
    require(remote['state'] == ('closed' if card['status'] == 'accepted' else 'open'), 'Current issue state')
    for proof in card['accepted_delivery'] or []:
        repo = proof['repository']
        pr = api(f"repos/{repo}/pulls/{proof['pr'].rsplit('/', 1)[1]}")
        require(pr['merged'] and pr['head']['sha'] == proof['head'] and pr['merge_commit_sha'] == proof['main'], 'Actual merged delivery')
        for field in ('head', 'main'):
            require(api(f"repos/{repo}/commits/{proof[field]}")['commit']['tree']['sha'] == proof['tree'], 'Equal reviewed and merged trees')
        run = api(f"repos/{repo}/actions/runs/{proof['main_ci']['id']}")
        require(run['head_sha'] == proof['main'] and run['status'] == 'completed' and run['conclusion'] == 'success', 'Actual accepted-main CI')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='GET current issue bindings and exact accepted proof')
    args = parser.parse_args()
    try:
        plan, index, tracking = [json.loads((ROOT / 'records' / name).read_text()) for name in ('platform-goal-plan.json', 'goal-index.json', 'goal-tracking.json')]
        validate_plan(plan, index, tracking)
        if args.fetch:
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(audit_card, plan['goals']))
        print(f"PASS: {len(plan['accepted_goal_ids'])} preserved accepted Goals; {len(plan['goals'])} current cards; nine roles and required release gates")
        print('Scope: metadata only; independent review truth, authority, native models and performance require their own evidence.')
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        print('FAIL: ' + str(exc))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
