#!/bin/bash

# Usage: create_topic <topic_name>

topic=${1}

# Create the specified topic on the Kafka cluster
echo -e "Creating topic: ${topic}..."
kafka-topics.sh \
    --zookeeper 'localhost:2181' \
    --create \
    --topic ${topic} \
    --partitions 4 \
    --replication-factor 2
