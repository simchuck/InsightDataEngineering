#!/bin/bash

PEG_ROOT='~/Desktop/InsightDataEngineering/pegasus'
PEG_ROOT=$(dirname ${BASH_SOURCE})/../..

# Consumers
CLUSTER_NAME='cs1-consumers'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/consumers.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka
