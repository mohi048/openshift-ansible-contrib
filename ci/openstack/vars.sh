#!/bin/bash

if [ "${RUN_OPENSTACK_CI:-}" == true ]
then
    # TODO(shadower): Can we only run this when the project admin asked for it?

    git fetch origin master:master

    echo Modified files:
    git diff --name-only master
    echo ==========

    WHITELIST_REGEX='^(.travis.yml|ci|roles|playbooks\/provisioning)'

    if git diff --name-only master | grep -qE "$WHITELIST_REGEX"; then
        RUN_OPENSTACK_CI=true
    else
        RUN_OPENSTACK_CI=false
    fi
fi

export RUN_OPENSTACK_CI
