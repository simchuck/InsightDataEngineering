#!/bin/bash

topic=${1}

# Start console producer to publish to the specified Kafka topic
echo -e "Publishing to topic: ${topic}..."
kafka-console-producer.sh \
	--bootstrap-server localhost:9092 \
	--topic ${topic}
