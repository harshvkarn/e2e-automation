from testrail import * 
from make_github_issue import *
import pprint
import csv
import sys
import json

#Setting up credentials and URL
client = APIClient('https://xxxxxxx.testrail.com')
client.user = ''
client.password = ''
build_number = sys.argv[1]
resultfile = build_number + '.csv'
logfile = build_number + '.log'

counter=0 #counter will be used to create run only once
with open(resultfile) as csvfile:
    csvfile = csv.DictReader(csvfile)
    for row in csvfile:
        test_name=row['test_name']
        case_id=row['case_id']
        #case_ids.append(case_id)
        suite_id=row['suite_id']
        if(counter==0):
            run=client.send_post(
            'add_run/3',
            {'suite_id': suite_id, 'description': 'Testing for creation via API'}
            )
            run_id=run['id']
            print('Run ID:',run_id)
            counter=1

        result=row['status']
        if str(result)=='Test Passed':
            result=1
        else:
            result=5
        testrail_url=('https://cloudbyte.testrail.com/index.php?/runs/view/'+str(run_id)+'&group_by=cases:section_id&group_order=asc')
        
        #Checking ,if result fails then create one Github Issue
        if result==5:
            ansible_log = open(logfile,'r')
            log_content = ansible_log.read()
            issue_body = '`Case ID: '+case_id+' Suite ID: '+suite_id+'` \nURL: '+testrail_url+'\n **Ansible Log** \n\n ```\n'+log_content+'\n```' 
            assigned_to = ''
            response = make_github_issue(test_name,issue_body,assigned_to, ['e2e'])
            github_issue_url = response['html_url']
        
            add_result=client.send_post(
                'add_result_for_case/'+str(run_id)+'/'+str(case_id),
                {'status_id':result, 'comment': 'URL to Github issue:'+github_issue_url}
            )
        else:
            add_result=client.send_post(
            'add_result_for_case/'+str(run_id)+'/'+str(case_id),
            {'status_id':result, 'comment': 'Test Passed'}
        )

