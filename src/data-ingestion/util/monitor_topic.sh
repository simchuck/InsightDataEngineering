#!/usr/bin/env bash

topic=${1:-weather-test}

# Start console consumer to monitor specified Kafka topic
echo -e "Monitoring topic: ${topic}..."
kafka-console-consumer.sh \
	--bootstrap-server localhost:9092 \
	--topic ${topic}
