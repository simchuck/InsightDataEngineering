#!/bin/bash

PEG_ROOT='~/Desktop/InsightDataEngineering/pegasus'
PEG_ROOT=$(dirname ${BASH_SOURCE})/../..

# storage
CLUSTER_NAME='cs1-storage'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/storage.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
