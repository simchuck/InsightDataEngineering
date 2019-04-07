#!/usr/bin/env bash

topic=${1:-weather-test}

# Delete the specified topic from the Kafka cluster
echo -e "Deleting topic: ${topic}..."
kafka-topics.sh \
	--zookeeper 'localhost:2181' \
	--delete \
	--topic ${topic}
