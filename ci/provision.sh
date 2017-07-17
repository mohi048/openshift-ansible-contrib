#!/bin/bash

set -euo pipefail

ansible-galaxy install -r playbooks/provisioning/openstack/galaxy-requirements.yaml -p roles
ansible-playbook -i playbooks/provisioning/openstack/sample-inventory/ playbooks/provisioning/openstack/provision.yaml
