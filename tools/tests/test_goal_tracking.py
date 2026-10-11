"""Failure coverage for development-only tracking, without network/admin writes."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from check_goal_tracking import api, audit_goal, protection, validate_tracking


class GoalTrackingTests(unittest.TestCase):
    def setUp(self):
        self.records = [json.loads((ROOT / 'records' / name).read_text()) for name in ('goal-index.json','goal-tracking.json','github-work-management.json','github-protection-proposal.json')]

    def test_reviewed_snapshot_has_complete_mapping(self):
        validate_tracking(*self.records)

    def test_goal_identity_scope_dependencies_and_states_reject_drift(self):
        for mode in ('missing','duplicate','owner','url','bool-number','milestone','eyl','dependencies','conditional','multiple-active','ready','state','labels','premature'):
            data = copy.deepcopy(self.records);goals=data[1]['goals'];g=goals[8]
            if mode=='missing':goals.pop()
            if mode=='duplicate':goals[-1]=copy.deepcopy(goals[0])
            if mode=='owner':g['repository']='outside/eylema'
            if mode=='url':g['issue']['url']='https://github.com/outside/eylema/issues/1'
            if mode=='bool-number':g['issue']['number']=True
            if mode=='milestone':g['milestone']['id']='M7'
            if mode=='eyl':g['related_eyl']=[]
            if mode=='dependencies':g['dependencies']=[]
            if mode=='conditional':goals[-1]['conditional_dependencies']={}
            if mode=='multiple-active':g['status']='implementing';g['labels']=[x for x in g['labels'] if not x.startswith('status:')]+['status:implementing']
            if mode=='ready':g['status']='ready';g['labels']=[x for x in g['labels'] if not x.startswith('status:')]+['status:ready']
            if mode=='state':g['status']='done'
            if mode=='labels':g['labels'].append('status:accepted')
            if mode=='premature':g['accepted_delivery']=copy.deepcopy(goals[0]['accepted_delivery'])
            with self.subTest(mode=mode),self.assertRaises((ValueError,KeyError,TypeError)):validate_tracking(*data)

    def test_accepted_proof_requires_owned_immutable_main_ci_and_review(self):
        for mode in ('missing','foreign','head','tree','pr','ci-head','ci-status','ci-url','review-head','review-status','reviewer'):
            data=copy.deepcopy(self.records);g=data[1]['goals'][0];p=g['accepted_delivery'][0]
            if mode=='missing':g['accepted_delivery']=None
            if mode=='foreign':p['repository']='outside/devguide'
            if mode=='head':p['head']='main'
            if mode=='tree':p['tree']='x'*40
            if mode=='pr':p['pr']='https://github.com/other/devguide/pull/3'
            if mode=='ci-head':p['main_ci']['head']='a'*40
            if mode=='ci-status':p['main_ci']['status']='not_run'
            if mode=='ci-url':p['main_ci']['url']='https://github.com/other/devguide/actions/runs/1'
            if mode=='review-head':p['review']['reviewed_head']='a'*40
            if mode=='review-status':p['review']['status']='pending'
            if mode=='reviewer':p['review']['reviewer']='unassigned'
            with self.subTest(mode=mode),self.assertRaises((ValueError,KeyError,TypeError)):validate_tracking(*data)

    def test_protection_cannot_claim_authority_or_hide_weaker_sources(self):
        for mode in ('coverage','enforced','source','app','check','strict','admin','force','delete','approval','hidden'):
            data=copy.deepcopy(self.records);p=data[3];repo='eylema-dev/eylema';v=p['repositories'][repo];request=v['request']
            if mode=='coverage':p['repositories'].pop(repo)
            if mode=='enforced':p['status']='enforced'
            if mode=='source':v['source_main']='a'*40
            if mode=='app':v['required_check_sources'][0]['app_id']=-1
            if mode=='check':request['required_status_checks']['checks'].pop()
            if mode=='strict':request['required_status_checks']['strict']=False
            if mode=='admin':request['enforce_admins']=False
            if mode=='force':request['allow_force_pushes']=True
            if mode=='delete':request['allow_deletions']=True
            if mode=='approval':request['required_pull_request_reviews']['required_approving_review_count']=1
            if mode=='hidden':request['bypass_pull_request_allowances']={'users':['anyone']}
            with self.subTest(mode=mode),self.assertRaises((ValueError,KeyError,TypeError)):validate_tracking(*data)

    def test_api_is_get_only_and_unavailable_is_not_absent(self):
        response=subprocess.CompletedProcess([],0,'{"ok":true}','')
        with patch('check_goal_tracking.subprocess.run',return_value=response) as run:
            self.assertEqual(api('repos/eylema-dev/devguide/issues/10'),{'ok':True})
            self.assertEqual(run.call_args.args[0][:5],['gh','api','--method','GET','repos/eylema-dev/devguide/issues/10'])
        with patch('check_goal_tracking.subprocess.run') as run,self.assertRaises(ValueError):api('https://outside/permissions')
        run.assert_not_called()
        for status,error in [(1,'HTTP 403'),(1,'offline'),(1,'HTTP 500')]:
            with patch('check_goal_tracking.subprocess.run',return_value=subprocess.CompletedProcess([],status,'',error)),self.assertRaises(ValueError):protection('eylema-dev/devguide')
        with patch('check_goal_tracking.subprocess.run',return_value=subprocess.CompletedProcess([],1,'','HTTP 404')):self.assertIsNone(protection('eylema-dev/devguide'))

    def test_remote_issue_mismatch_fails_before_delivery_network(self):
        goal=self.records[1]['goals'][8]
        issue={'html_url':goal['issue']['url'],'body':'<!-- eylema-goal:'+goal['id']+':v1 -->','state':'open','labels':[{'name':x} for x in goal['labels']],'milestone':goal['milestone']}
        with patch('check_goal_tracking.api',return_value=issue):self.assertEqual(audit_goal(goal),goal['id'])
        for mode in ('pr','body','state','labels','milestone'):
            bad=copy.deepcopy(issue)
            if mode=='pr':bad['pull_request']={}
            if mode=='body':bad['body']='unrelated issue'
            if mode=='state':bad['state']='closed'
            if mode=='labels':bad['labels']=[]
            if mode=='milestone':bad['milestone']=None
            with patch('check_goal_tracking.api',return_value=bad),self.subTest(mode=mode),self.assertRaises(ValueError):audit_goal(goal)


if __name__ == '__main__':unittest.main()
