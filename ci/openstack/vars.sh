#!/bin/bash

if [ "${RUN_OPENSTACK_CI:-}" == true ]; then
    # TODO(shadower): check that the commit changed roles or playbooks/provisioning
    # TODO(shadower): check that a project admin asked for the CI to run
fi

export RUN_OPENSTACK_CI
