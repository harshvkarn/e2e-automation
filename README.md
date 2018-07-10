# e2e-automation

This repo is initialised with Ansible Playbook and python scripts that automates the result from playbook to testrail and raises Github Issue upon test failures.

### Authors
[@harshvkarn](https://github.com/harshvkarn/) 
[@shiveshabhishek](https://github.com/shiveshabhishek/) 
[@chandankumar4](https://github.com/chandankumar4/) 

## Jenkins Shell Configuration

```bash
#!/bin/bash

cd ${JENKINS_HOME}/openebs/e2e/ansible/
ansible-playbook ../../../dummy-test/main.yml -vv --extra-vars "BUILD_NUMBER=$BUILD_NUMBER"
ansible-playbook ../../../dummy-test/dtest.yml -vv --extra-vars "build_number=$BUILD_NUMBER"
ansible-playbook ../../../dummy-test/dtest-fail.yml -vv --extra-vars "build_number=$BUILD_NUMBER"
ansible-playbook ../../../dummy-test/logtorail.yml -vv --extra-vars "build_number=$BUILD_NUMBER"

```

