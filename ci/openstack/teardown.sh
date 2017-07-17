#!/bin/bash

set -euo pipefail

KEYPAIR_NAME="travis-ci-$TRAVIS_BUILD_NUMBER"

openstack keypair delete "$KEYPAIR_NAME" || true
openstack stack delete --wait --yes openshift.example.com || true
