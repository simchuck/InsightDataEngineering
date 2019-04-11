#!/bin/bash

# Run this script on the Kafka master node to delete the specified topics,
# for each of the specified resource nodes.
#
# Assumes consecutive nodes starting from index 1.
#
# Usage: delete_rn_topics <num>

NUM_NODES=$1

# Repeat for each resource node
for node in $(seq 1 $NUM_NODES); do

    echo -e "Deleting topics for resource node RN00${node}:"
    for topic in {capacity,load,weather,energy-price,demand,resource-price,summary}; do
        rn_topic=RN00${node}-${topic}
        kafka-topics.sh \
            --zookeeper 'localhost:2181' \
            --delete \
            --topic ${rn_topic}
    done

done
