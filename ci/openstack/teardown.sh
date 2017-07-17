#!/bin/bash

set -euo pipefail

openstack stack delete --wait --yes openshift.example.com
