#!/usr/bin/env python

import sys
from kafka import KafkaProducer
from smart_open import smart_open

KAFKA_BUCKET = 's3://csimchick-insight-static-data/weather/weather.dat'
KAFKA_TOPIC = 'weather-test'
#brokers = 'ec2-52-39-178-192.us-west-2.compute.amazonaws.com,ec2-35-163-191-58.us-west-2.compute.amazonaws.com,ec2-52-39-228-217.us-west-2.compute.amazonaws.com,ec2-34-213-64-75.us-west-2.compute.amazonaws.com'
brokers = [
    'ip-10-0-0-165',
    'ip-10-0-0-125',
    'ip-10-0-0-150',
    'ip-10-0-0-166',
    ]
KAFKA_BROKERS = ':9092,'.join(brokers) + ':9092'

def produce(bucket, brokers, topic):

    producer = KafkaProducer(bootstrap_servers = brokers)

    for line in smart_open(bucket, 'r'):
        producer.send(topic, line.strip().encode('utf-8'))
        producer.flush()

def main():
    produce(KAFKA_BUCKET, KAFKA_BROKERS, KAFKA_TOPIC)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
