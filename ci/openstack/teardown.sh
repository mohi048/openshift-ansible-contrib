#!/bin/bash

set -euo pipefail

sudo cp resolv.conf.orig /etc/resolv.conf
openstack stack delete --wait --yes openshift.example.com
