#!/bin/bash

set -euo pipefail

git clone https://github.com/openshift/openshift-ansible ../openshift-ansible

pip install ansible shade dnspython python-openstackclient

