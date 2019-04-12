#!/bin/bash

# Kill processes
if [[ $1 == '-k' ]]; then
    ps_demo_producer=$(cat PS_DEMO_PRODUCER)
    for ps_id in $ps_demo_producer; do
        kill -9 $ps_id
    done
    exit
fi

# Set delay between records
if [[ $1 == '-d' ]]; then
    shift; delay=$1; shift
else
    delay=0         # default to no delay
fi

# Start producer scripts for the demo
topics='weather demand price'
touch PS_DEMO_PRODUCERS
for topic in $topics; do
    python3 ~/src/test_kafka_topic.py -m producer -t ${topic} -d ${delay} &
    echo -e "$!" >> PS_DEMO_PRODUCER
done
