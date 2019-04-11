#!/bin/bash

# Usage: delete_topic <topic_name>

topic=${1}

# Delete the specified topic from the Kafka cluster
echo -e "Deleting topic: ${topic}..."
kafka-topics.sh \
	--zookeeper 'localhost:2181' \
	--delete \
	--topic ${topic}
