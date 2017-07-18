#!/bin/bash

set -euo pipefail

if [ "$RUN_OPENSTACK_CI" != "true" ]; then
    echo RUN_OPENSTACK_CI is set to false, skipping the openstack end to end test.
    exit
fi

KEYPAIR_NAME="travis-ci-$TRAVIS_BUILD_NUMBER"

openstack keypair delete "$KEYPAIR_NAME" || true
openstack stack delete --wait --yes openshift.example.com || true
