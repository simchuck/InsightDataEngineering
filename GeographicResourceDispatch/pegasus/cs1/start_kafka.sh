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
#peg sshcmd-cluser ${CLUSTER_NAME} "sudo apt install bc"    # 2019.04.03 pulled Curtis' `awk over bc` commit for config/zookeeper/setup_single.sh
peg install ${CLUSTER_NAME} environment
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka
