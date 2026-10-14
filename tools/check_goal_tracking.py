"""Development-only snapshot validation and opt-in read-only GitHub audit."""
import argparse
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from github_identity import canonical_endpoint, canonical_repository, canonical_url

ROOT = Path(__file__).resolve().parents[1]
STATES = {'backlog', 'ready', 'implementing', 'verification', 'review', 'ready_for_maintainer', 'accepted'}
RUST_REPOS = {'eylema-dev/eylema', 'eylema-dev/eylema-examples', 'eylema-dev/eylema-evals'}


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}', value)


def validate_tracking(index, tracking, management, proposal):
    require(tracking['format_version'] == management['format_version'] == proposal['format_version'] == 1, 'Version')
    require(tracking['source_cards'] == 'records/goal-index.json', 'Frozen card binding')
    require(set(tracking['states']) == STATES and len(tracking['states']) == len(STATES), 'State inventory')
    cards = {g['id']: g for g in index['goals']}
    goals = tracking['goals']
    require(len(goals) == len(cards) == 47 and {g['id'] for g in goals} == set(cards), 'All 47 unique Goal identities')
    by_id = {g['id']: g for g in goals}
    urls = set()
    require(sum(g['status'] == 'implementing' for g in goals) <= 1, 'Only one implementing Goal')
    repos = management['repositories']
    require(set(repos) == {'eylema-dev/' + name for name in ('eylema','devguide','eylema-docs-en','eylema-docs-tr','.github','eylema-examples','eylema-evals','eylema-models','eylema-training','eylemadotdev')}, 'Ten repository observations')
    for goal in goals:
        card = cards[goal['id']]
        repo = goal['repository']
        require(repo == card['repository'] and repo in repos, 'Goal owner')
        number = goal['issue']['number']
        url = goal['issue']['url']
        require(type(number) is int and number > 0 and url == f'https://github.com/{repo}/issues/{number}' and url not in urls, 'Unique owned issue URL')
        urls.add(url)
        require(goal['dependencies'] == card['dependencies'] and goal['conditional_dependencies'] == card['conditional_dependencies'] and goal['related_eyl'] == card['related_eyl'], 'Frozen dependency/EYL identity')
        require(goal['status'] in STATES, 'Goal state')
        milestone = goal['milestone']
        require(milestone['id'] == card['milestone'] and type(milestone['number']) is int and milestone['number'] > 0 and milestone['title'].startswith(milestone['id'] + ' — ') and milestone['url'] == f"https://github.com/{repo}/milestone/{milestone['number']}", 'Owned logical/numeric milestone')
        labels = goal['labels']
        require(len(labels) == len(set(labels)) and {x for x in labels if x.startswith('status:')} == {'status:' + goal['status']} and {'goal', 'milestone:' + milestone['id'], 'priority:unranked'} <= set(labels), 'State/Goal/milestone labels')
        require({'planning:' + x for x in goal['related_eyl']} <= set(labels), 'Planning ID labels')
        if goal['status'] != 'backlog':
            require(all(by_id[d]['status'] == 'accepted' for d in goal['dependencies']), 'Accepted dependencies before activation')
        delivery = goal['accepted_delivery']
        if goal['status'] != 'accepted':
            require(delivery is None, 'No premature accepted proof')
            continue
        require(isinstance(delivery, list) and delivery and repo in {p['repository'] for p in delivery}, 'Accepted primary delivery')
        require(len(delivery) == len({p['repository'] for p in delivery}), 'Unique delivery repositories')
        for proof in delivery:
            owner = proof['repository']
            require(owner in repos and all(sha(proof[k]) for k in ('head','main','tree')), 'Immutable accepted revisions')
            require(bool(re.fullmatch(re.escape('https://github.com/' + owner + '/pull/') + r'[1-9][0-9]*', proof['pr'])), 'Owned PR')
            ci, review = proof['main_ci'], proof['review']
            require(type(ci['id']) is int and ci['id'] > 0 and ci['url'] == f"https://github.com/{owner}/actions/runs/{ci['id']}" and ci['head'] == proof['main'] and ci['status'] == 'passed', 'Exact accepted-main CI')
            require(review['status'] == 'passed' and review['reviewed_head'] == proof['head'] and bool(review['reviewer']) and 'unassigned' not in review['reviewer'], 'Separate review binding')
    require(set(proposal['repositories']) == set(repos), 'Protection proposal coverage')
    require(proposal['status'] == 'prepared; separately authorized administration write required', 'Proposal is not enforcement/authority')
    for repo, proposed in proposal['repositories'].items():
        observation = repos[repo]
        require(sha(observation['main']) and proposed['source_main'] == observation['main'], 'Observed-main proposal binding')
        expected = {'repository-checks'} | ({'rust-checks'} if repo in RUST_REPOS else set())
        sources = proposed['required_check_sources']
        require(len(sources) == len(expected) and {c['name'] for c in sources} == expected, 'Role-scoped check inventory')
        for source in sources:
            require(source in observation['checks'] and source['head'] == observation['main'] and source['status'] == 'completed' and source['conclusion'] == 'success' and source['app_id'] == 15368 and source['app_slug'] == 'github-actions', 'Observed successful Actions check source')
        request = proposed['request']
        require(set(request) == {'required_status_checks','enforce_admins','required_pull_request_reviews','restrictions','required_conversation_resolution','allow_force_pushes','allow_deletions','required_linear_history','lock_branch','allow_fork_syncing'}, 'No hidden protection request fields')
        checks = request['required_status_checks']
        require(checks['strict'] is True and checks['contexts'] == [] and len(checks['checks']) == len(expected) and {c['context'] for c in checks['checks']} == expected and all(c['app_id'] == 15368 for c in checks['checks']), 'Required checks bind observed app')
        review = request['required_pull_request_reviews']
        require(request['enforce_admins'] is True and request['required_conversation_resolution'] is True and request['allow_force_pushes'] is False and request['allow_deletions'] is False and request['restrictions'] is None, 'Protection boundaries')
        require(review == {'dismiss_stale_reviews':True,'require_code_owner_reviews':False,'required_approving_review_count':0,'require_last_push_approval':False}, 'Single-account PR/review boundary')
        require(request['lock_branch'] is False and request['allow_fork_syncing'] is False and request['required_linear_history'] is False, 'No hidden lock/history change')


def api(endpoint):
    """GET only; never accept credentials, arbitrary host or mutation arguments."""
    endpoint = canonical_endpoint(endpoint)
    result = subprocess.run(['gh', 'api', '--method', 'GET', endpoint], capture_output=True, text=True, timeout=120, check=False)
    require(result.returncode == 0, 'GitHub read failed: ' + endpoint)
    return json.loads(result.stdout)


def protection(repo):
    repo = canonical_repository(repo)
    result = subprocess.run(['gh', 'api', '--method', 'GET', 'repos/' + repo + '/branches/main/protection'], capture_output=True, text=True, timeout=120, check=False)
    if result.returncode == 0:
        return json.loads(result.stdout)
    require('HTTP 404' in result.stderr, 'Protection read unavailable: ' + repo)
    return None


def audit_goal(goal):
    repo = goal['repository']
    issue = api(f"repos/{repo}/issues/{goal['issue']['number']}")
    require('pull_request' not in issue and canonical_url(issue['html_url']) == canonical_url(goal['issue']['url']) and ('<!-- eylema-goal:' + goal['id'] + ':v1 -->') in (issue['body'] or ''), 'Actual Goal issue identity')
    require(issue['state'] == ('closed' if goal['status'] == 'accepted' else 'open'), 'Issue state differs from snapshot: ' + goal['id'])
    actual = {label['name'] for label in issue['labels']}
    require(set(goal['labels']) <= actual and {label for label in actual if label.startswith('status:')} == {'status:' + goal['status']}, 'Issue labels differ: ' + goal['id'])
    require(issue['milestone'] and issue['milestone']['number'] == goal['milestone']['number'] and issue['milestone']['title'] == goal['milestone']['title'], 'Issue milestone differs: ' + goal['id'])
    for proof in goal['accepted_delivery'] or []:
        prefix = 'repos/' + proof['repository']
        pr = api(prefix + '/pulls/' + proof['pr'].rsplit('/', 1)[1])
        require(pr['merged'] and pr['head']['sha'] == proof['head'] and pr['merge_commit_sha'] == proof['main'], 'Actual merged delivery differs')
        for revision in ('head','main'):
            require(api(prefix + '/commits/' + proof[revision])['commit']['tree']['sha'] == proof['tree'], 'Reviewed/main trees differ')
        run = api(prefix + '/actions/runs/' + str(proof['main_ci']['id']))
        require(run['head_sha'] == proof['main'] and run['status'] == 'completed' and run['conclusion'] == 'success' and canonical_url(run['html_url']) == canonical_url(proof['main_ci']['url']), 'Actual accepted-main CI differs')
    return goal['id']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='GET public GitHub metadata; fail on issue/accepted-proof drift')
    args = parser.parse_args()
    try:
        index, tracking, management, proposal = [json.loads((ROOT / 'records' / filename).read_text()) for filename in ('goal-index.json','goal-tracking.json','github-work-management.json','github-protection-proposal.json')]
        validate_tracking(index, tracking, management, proposal)
        if args.fetch:
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(audit_goal, tracking['goals']))
            for repo, observed in management['repositories'].items():
                require(protection(repo) == observed['classic_protection'], 'Classic protection differs from observed snapshot: ' + repo)
                require(api('repos/' + repo + '/rules/branches/main') == observed['applied_rules'] and api('repos/' + repo + '/rulesets') == observed['rulesets'], 'Rules differ from observed snapshot: ' + repo)
                runs = api('repos/' + repo + '/commits/' + observed['main'] + '/check-runs?per_page=100')['check_runs']
                for source in proposal['repositories'][repo]['required_check_sources']:
                    require(any(c['name'] == source['name'] and c['head_sha'] == source['head'] and canonical_url(c['html_url']) == canonical_url(source['url']) and c['status'] == 'completed' and c['conclusion'] == 'success' and c['app']['id'] == source['app_id'] and c['app']['slug'] == source['app_slug'] for c in runs), 'Observed check source differs')
            print('PASS: read-only GitHub issue/milestone/labels, accepted merged trees/CI and exact-main Actions sources')
        print('PASS: 47 versioned Goal mappings and 10 prepared protection requests; separate administration authority and live readback still required')
        print('Scope: planning/metadata only; separate AI review truth, permissions, runtime/GPU/model/training are not established by this checker')
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        print('FAIL: ' + str(exc))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
