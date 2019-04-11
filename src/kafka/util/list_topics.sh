#!/bin/bash

# Query Kafka cluster for existing topics
echo -e "Topics on Kafka cluster..."
kafka-topics.sh \
	--zookeeper 'localhost:2181' \
	--list
