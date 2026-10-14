"""Current harness plan preserves history and rejects unsafe execution metadata."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from check_platform_plan import validate_plan, validate_proof


class PlatformPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan, self.index, self.tracking = [
            json.loads((ROOT / 'records' / name).read_text())
            for name in ('platform-goal-plan.json', 'goal-index.json', 'goal-tracking.json')
        ]

    def check_bad(self, change):
        bad = copy.deepcopy(self.plan)
        change(bad)
        with self.assertRaises(ValueError):
            validate_plan(bad, self.index, self.tracking)

    def test_current_plan_and_complete_original_coverage(self):
        validate_plan(self.plan, self.index, self.tracking)

    def test_history_cannot_be_rewritten(self):
        tracking = copy.deepcopy(self.tracking)
        tracking['goals'][0]['accepted_delivery'][0]['main'] = 'a' * 40
        with self.assertRaises(ValueError):
            validate_plan(self.plan, self.index, tracking)

    def test_missing_duplicate_and_unknown_goals_fail(self):
        self.check_bad(lambda p: p['goals'].pop())
        self.check_bad(lambda p: p['goals'].append(copy.deepcopy(p['goals'][0])))
        self.check_bad(lambda p: p['goals'][0]['dependencies'].append('G99'))

    def test_original_required_dependency_cannot_be_waived(self):
        self.check_bad(lambda p: p['goals'][1]['dependencies'].clear())

    def test_cycles_and_reordered_dependency_execution_fail(self):
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G46')['dependencies'].append('G54'))
        self.check_bad(lambda p: p['recommended_order'].reverse())

    def test_release_keeps_all_platform_and_original_gates(self):
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G44')['dependencies'].remove('G58'))
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'W01')['conditional_dependencies'].clear())

    def test_scope_escape_and_unbounded_budget_fail(self):
        self.check_bad(lambda p: p['goals'][0]['allowed_paths'].append('../other'))
        self.check_bad(lambda p: p['goals'][0]['allowed_paths'].append('/private/other'))
        self.check_bad(lambda p: p['goals'][0]['budget'].update(active_minutes=None))
        self.check_bad(lambda p: p['goals'][0]['budget'].update(max_targeted_repairs=999))

    def test_local_rust_and_external_authority_boundaries_fail_closed(self):
        for key, value in [('local_inference', 'hidden_backend'),
                           ('hidden_inference_engine', True),
                           ('model_output_is_authority', True),
                           ('external_production_rust_crates', True),
                           ('private_reasoning_collection', True)]:
            with self.subTest(key=key):
                self.check_bad(lambda p: p['policy'].update({key: value}))

    def test_memory_scope_authority_and_backend_policy_fail_closed(self):
        for key, value in [('default', 'shared'), ('derivative_permissions_inherited', False),
                           ('authority', 'memory_grants_authority'), ('backend_policy', 'hidden_sql_engine')]:
            with self.subTest(key=key):
                self.check_bad(lambda p: p['memory_policy'].update({key: value}))
        self.check_bad(lambda p: p['memory_policy']['kinds'].remove('knowledge_graph'))
        for gid, dependency in [('G72', 'G88'), ('G71', 'G88'), ('G74', 'G87'),
                                ('G75', 'G87'), ('G79', 'G89'), ('G82', 'G89'),
                                ('G87', 'G63'), ('G88', 'G70'), ('G89', 'G33'), ('G90', 'G89')]:
            with self.subTest(goal=gid, dependency=dependency):
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == gid)['dependencies'].remove(dependency))

    def test_g40_does_not_gain_a_new_trial_or_repair_allowance(self):
        for key, value in [('active_minutes', 15), ('new_provider_calls', 1), ('max_targeted_repairs', 1)]:
            with self.subTest(key=key):
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G40')['budget'].update({key: value}))
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G40').update(status='implementing'))

    def test_acceptance_or_activation_cannot_be_fabricated(self):
        self.check_bad(lambda p: p['goals'][0].update(status='accepted'))
        blocked_activation = copy.deepcopy(self.plan)
        next(g for g in blocked_activation['goals'] if g['id'] == 'G44')['status'] = 'implementing'
        with self.assertRaisesRegex(ValueError, 'Accepted dependencies before activation'):
            validate_plan(blocked_activation, self.index, self.tracking)
        self.check_bad(lambda p: p['goals'][0]['acceptance'][0].update(result='passed'))

    def test_issue_identity_and_model_role_coverage_fail_closed(self):
        self.check_bad(lambda p: p['goals'][0].update(issue={'number': 1, 'url': 'https://github.com/other/repo/issues/1'}))
        self.check_bad(lambda p: p['roles'].pop())

    def test_separate_audio_vision_and_project_private_derivatives(self):
        self.check_bad(lambda p: p['capability_profiles'].remove('text_to_speech'))
        self.check_bad(lambda p: p['capability_profiles'].remove('speech_to_text'))
        self.check_bad(lambda p: p['data_policy'].update(default='public'))
        self.check_bad(lambda p: p['data_policy'].update(derivative_permissions_inherited=False))
        self.check_bad(lambda p: p['data_policy'].update(automatic_private_sharing=True))

    def test_native_improvement_and_investment_cannot_be_silently_widened(self):
        self.check_bad(lambda p: p['policy'].update(native_training='external_runtime'))
        self.check_bad(lambda p: p['improvement_methods'].remove('held_out_evaluation'))
        self.check_bad(lambda p: p.update(capacity_planning='automatic procurement'))
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G72')['dependencies'].remove('G73'))
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G72')['dependencies'].append('G60'))

    def test_training_candidate_limit_rejects_unbounded_and_wrong_types(self):
        for value in [None, -1, 2, 999, True, False, '1']:
            with self.subTest(value=value):
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G84')['budget'].update(training_candidate_limit=value))
        self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == 'G40')['budget'].update(training_candidate_limit=1))

    def test_placeholder_reviewer_cannot_claim_passed_review(self):
        proof = copy.deepcopy(next(g for g in self.tracking['goals'] if g['status'] == 'accepted')['accepted_delivery'][0])
        validate_proof(proof, proof['repository'])
        for actor in ['', '   ', None, 12, 'unassigned; separate context and exact reviewed SHA required', 'pending', 'TBD', 'unknown', 'TODO']:
            with self.subTest(actor=actor):
                proof['review']['reviewer'] = actor
                with self.assertRaises(ValueError):
                    validate_proof(proof, proof['repository'])

    def test_original_acceptance_cannot_be_removed_rewritten_or_duplicated(self):
        for gid in ['G44', 'G35']:
            with self.subTest(gid=gid):
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == gid)['acceptance'].pop())
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == gid)['acceptance'][-1].update(requirement='Weakened evidence'))
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == gid)['acceptance'][-1].update(check='Only static check'))
                self.check_bad(lambda p: next(g for g in p['goals'] if g['id'] == gid)['acceptance'].append(copy.deepcopy(next(g for g in p['goals'] if g['id'] == gid)['acceptance'][-1])))


if __name__ == '__main__':
    unittest.main()
