# OpenShift and Atomic Platform Ansible Contrib

[![Build
Status](https://travis-ci.org/openshift/openshift-ansible-contrib.svg?branch=master)](https://travis-ci.org/openshift/openshift-ansible-contrib)

This repository contains *unsupported* code that can be used in conjunction with the
[openshift-ansible](https://github.com/openshift/openshift-ansible) repository, namely:
- additional [roles](https://github.com/openshift/openshift-ansible-contrib/tree/master/roles) for OpenShift deployment
- code for provisioning various cloud providers (GCE, AWS, VMWare and [Openstack](https://github.com/openshift/openshift-ansible-contrib/tree/master/playbooks/provisioning/openstack))
- supporting scripts and playbooks for the various [reference architectures](https://github.com/openshift/openshift-ansible-contrib/tree/master/reference-architecture) Red Hat has published

## Running tests locally
We use [tox](http://readthedocs.org/docs/tox/) to manage virtualenvs and run
tests. Alternatively, tests can be run using
[detox](https://pypi.python.org/pypi/detox/) which allows for running tests in
parallel

