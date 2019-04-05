#!/bin/bash

PEG_ROOT='~/Desktop/InsightDataEngineering/pegasus'
PEG_ROOT=$(dirname ${BASH_SOURCE})/../..

# Kafka cluster
CLUSTER_NAME='cs1-kafka'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/kafka-master.yaml &
peg up ${PEG_ROOT}/examples/cs1/kafka-workers.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka

# Producers
CLUSTER_NAME='cs1-producers'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/producers.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka

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

# Processors
CLUSTER_NAME='cs1-processors'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/processors.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka

# storage
CLUSTER_NAME='cs1-storage'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/storage.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment

# UI
CLUSTER_NAME='cs1-ui'
echo -e "\nCreating ${CLUSTER_NAME}..."

peg up ${PEG_ROOT}/examples/cs1/ui.yaml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} environment
