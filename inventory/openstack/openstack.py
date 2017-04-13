#!/usr/bin/env python2

from __future__ import print_function

import argparse
import json
import os
import sys

from keystoneauth1.identity import generic as ks_id
from keystoneauth1 import session
import heatclient.client


# TODO
STACK_NAME='openshift-test-test'


def keystone_session():
    auth_url = os.environ.get('OS_AUTH_URL')
    username = os.environ.get('OS_USERNAME')
    password = os.environ.get('OS_PASSWORD')
    auth_token = os.environ.get('OS_AUTH_TOKEN')
    project_name = os.environ.get('OS_TENANT_NAME')
    cacert = os.environ.get('OS_CACERT')

    if auth_token:
        auth_inputs = {
            'auth_url': auth_url,
            'token': auth_token,
            'project_name': project_name,
        }
        if auth_url.endswith('v3'):
            auth_inputs['project_domain_id'] = 'default'
        auth = ks_id.Token(**auth_inputs)
    else:
        auth_inputs = {
            'auth_url': auth_url,
            'username': username,
            'password': password,
            'project_name': project_name,
        }
        if auth_url.endswith('v3'):
            auth_inputs['user_domain_id'] = 'default'
            auth_inputs['project_domain_id'] = 'default'
        auth = ks_id.Password(**auth_inputs)
    return session.Session(auth=auth, verify=cacert)


def heat_client():
    session = keystone_session()
    try:
        client = heatclient.client.Client('1', session=session)
    except Exception as e:
        print("Error connecting to Heat: {}".format(e.message),
              file=sys.stderr)
        sys.exit(1)
    return client


def inventory_list():
    heat = heat_client()
    stack = heat.stacks.get(STACK_NAME)
    inventory = {}

    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'OSv3': {
            'children': [
                'infra',
                'masters',
                'nodes',
                'etcd',
            ]
        },
        'masters': {
            'vars': {
                'openshift_schedulable': True,
                'openshift_router_selector': 'region=infra'
            }
        },
    }

    outputs = dict(((output['output_key'], output['output_value'])
                    for output in stack.outputs))

    inventory['masters']['hosts'] = [host['hostname'] for host
                                     in outputs['master_nodes']]

    for output in outputs['master_nodes']:
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_hostname': output['internal_hostname'],
            'openshift_public_hostname': output['hostname'],
        }

    inventory['etcd'] = [host['hostname'] for host
                            in outputs['master_nodes']]

    app_and_infra_nodes = outputs['infra_nodes'] + outputs['app_nodes']
    inventory['nodes'] = [host['hostname'] for host
                            in app_and_infra_nodes]

    for output in outputs['infra_nodes']:
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_node_labels' : "{'region': 'infra', 'zone': 'default'}",
            'openshift_hostname': output['internal_hostname'],
            'openshift_public_hostname': output['hostname'],
            'openshift_ip': output['private_ip'],
        }

    for output in outputs['app_nodes']:
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_node_labels': "{'region': 'primary', 'zone': 'default'}",
            'openshift_hostname': output['internal_hostname'],
            'openshift_public_hostname': output['hostname'],
            'openshift_ip': output['private_ip'],
        }

    print(json.dumps(inventory))


# http://docs.ansible.com/ansible/developing_inventory.html
def inventory_host():
    print('{}')


def main():
    parser = argparse.ArgumentParser(
        description="Ansible inventory for OpenShift on OpenStack")
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store_true')
    args = parser.parse_args()
    if args.list:
        inventory_list()
    elif args.host:
        inventory_host()
    sys.exit(0)


if __name__ == '__main__':
    main()
