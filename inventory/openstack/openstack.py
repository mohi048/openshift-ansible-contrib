#!/usr/bin/env python2

from __future__ import print_function

import argparse
import json
import os
import sys

from heatclient.v1 import client as heat_client
from keystoneclient.v3 import client as keystone_client


# TODO
STACK_NAME='openshift-test-test'


def get_keystone_client():
    auth_url = os.environ.get('OS_AUTH_URL')
    username = os.environ.get('OS_USERNAME')
    password = os.environ.get('OS_PASSWORD')
    auth_token = os.environ.get('OS_AUTH_TOKEN')
    project_name = os.environ.get('OS_TENANT_NAME')
    cacert = os.environ.get('OS_CACERT')

    if auth_token:
        client = keystone_client.Client(
            auth_url=auth_url,
            username=username,
            token=auth_token,
            project_name=project_name,
            cacert=cacert)
    else:
        client = keystone_client.Client(
            auth_url=auth_url,
            username=username,
            password=password,
            project_name=project_name,
            cacert=cacert)
    client.authenticate()
    return client

def get_heat_client():
    keystone = get_keystone_client()
    endpoint = keystone.service_catalog.url_for(
        service_type='orchestration', endpoint_type='publicURL')
    cacert = os.environ.get('OS_CACERT')
    try:
        client = heat_client.Client(
            endpoint=endpoint,
            token=keystone.auth_token,
            ca_file=cacert)
    except Exception as e:
        print("Error connecting to Heat: {}".format(e.message),
              file=sys.stderr)
        sys.exit(1)
    return client

def inventory_list():
    heat = get_heat_client()
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
        'infra': ['localhost'],
        'dns': ['localhost'],
    }

    outputs = dict(((output['output_key'], output['output_value'])
                    for output in stack.outputs))

    inventory['masters']['hosts'] = [host['hostname'] for host
                                     in outputs['master_nodes'].values()]

    for output in outputs['master_nodes'].values():
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_hostname': output['hostname'],
            'openshift_public_hostname': output['hostname'],
        }

    inventory['etcd'] = [host['hostname'] for host
                            in outputs['master_nodes'].values()]

    app_and_infra_nodes = outputs['infra_nodes'].values() + outputs['app_nodes'].values()
    inventory['nodes'] = [host['hostname'] for host
                            in app_and_infra_nodes]

    for output in outputs['infra_nodes'].values():
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_node_labels' : "{'region': 'infra', 'zone': 'default'}",
            'openshift_hostname': output['hostname'],
            'openshift_public_hostname': output['hostname'],
            'openshift_ip': output['private_ip'],
        }

    for output in outputs['app_nodes'].values():
        inventory['_meta']['hostvars'][output['hostname']] = {
            'openshift_node_labels': "{'region': 'primary', 'zone': 'default'}",
            'openshift_hostname': output['hostname'],
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
