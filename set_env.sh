#!/bin/bash

# TODOs:
# chmod +x set_env.sh
# source set_env.sh
# Installation:
#   a. On Ubuntu/Debian
#     sudo apt-get update
#     sudo apt-get install gettext
#   b. On macOS
#     brew install gettext
#     brew link --force gettext
#   c. On CentOS/RHEL
#     sudo yum install gettext
# envsubst < deployment.yaml | kubectl apply -f - -n $ENVIRONMENT
#


ENVIRONMENT=$(grep 'environment:' values.yaml | awk '{print $2}')
VERSION=$(grep 'version:' values.yaml | awk '{print $2}')


export ENVIRONMENT
export VERSION

echo "export ENVIRONMENT=${ENVIRONMENT}"
echo "export VERSION=${VERSION}"
