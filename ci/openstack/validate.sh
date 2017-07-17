#!/bin/bash

set -euo pipefail

export PATH="$PWD/bin:$PATH"

oc login --insecure-skip-tls-verify=true https://master-0.openshift.example.com:8443 -u test -p password
oc new-project test
oc new-app --template=cakephp-mysql-example

echo Waiting for the pods to come up

STATUS=timeout
for i in $(seq 600); do
    if [ "$(oc status -v | grep 'deployment.*deployed' | wc -l)" -eq 2 ]; then
        STATUS=success
        echo Both pods were deployed
        break
    elif [ "$(oc status -v | grep -i 'error\|fail' | wc -l)" -gt 0 ]; then
        STATUS=error
        echo ERROR: The deployment failed
        break
    else
        sleep 5
    fi
done

if [ "$STATUS" = timeout ]; then
    echo ERROR: Timed out waiting for the pods
fi

echo 'Output of `oc status -v`:'
oc status -v

echo
echo 'Output of `oc logs bc/cakephp-mysql-example`:'
oc logs bc/cakephp-mysql-example

if [ "$STATUS" != success ]; then
    echo "ERROR: The deployment didn't succeed"
    exit 1
fi

set -o pipefail

curl http://cakephp-mysql-example-test.apps.openshift.example.com | grep 'Welcome to your CakePHP application on OpenShift'

echo "SUCCESS \o/"
