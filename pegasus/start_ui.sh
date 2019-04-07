#!/bin/bash

PEG_ROOT='~/Desktop/InsightDataEngineering/pegasus'
PEG_ROOT=$(dirname ${BASH_SOURCE})/../..

# UI
CLUSTER_NAME='cs1-ui'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/ui.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
