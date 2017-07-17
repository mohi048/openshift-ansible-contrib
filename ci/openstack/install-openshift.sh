#!/bin/bash

set -euo pipefail

# Do we have ssh keys?

export INVENTORY="$PWD/playbooks/provisioning/openstack/sample-inventory"


echo INSTALL OPENSHIFT

ansible-playbook --become --timeout 180 --user openshift --private-key ~/.ssh/id_rsa -i "$INVENTORY" ../openshift-ansible/playbooks/byo/config.yml
