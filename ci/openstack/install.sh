#!/bin/bash

set -euo pipefail

git clone https://github.com/openshift/openshift-ansible ../openshift-ansible

pip install ansible shade dnspython python-openstackclient

curl -L -o oc.tgz https://github.com/openshift/origin/releases/download/v1.5.1/openshift-origin-client-tools-v1.5.1-7b451fc-linux-64bit.tar.gz
tar -xf oc.tgz
mv openshift-origin-client-tools-v1.5.1-7b451fc-linux-64bit bin
