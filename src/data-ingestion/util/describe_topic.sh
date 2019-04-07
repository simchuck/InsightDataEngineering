#!/usr/bin/env bash

topic=${1:-weather-test}

# Query Kafka cluster for information about specified topic
echo -e "Description of topic: ${topic}..."
kafka-topics.sh \
	--zookeeper 'localhost:2181' \
	--describe \
	--topic ${topic}
