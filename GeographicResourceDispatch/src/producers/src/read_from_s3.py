#!/usr/bin/python3
"""
Read data record from S3 bucket and publish to a topic on the Kafka cluster.

This code runs on the `producers` instance within the AWS subnet.
"""

import argparse
#from time import sleep

from kafka import KafkaProducer
#from kafka.errors import KafkaError
from smart_open import smart_open

s3_bucket = 's3://csimchick-insight-static-data'
s3_directory = 'weather'
s3_filename = 'weather.dat'

s3_url = '/'.join([s3_bucket, s3_directory, s3_filename])

KAFKA_TOPIC = 'weather-test'
brokers = [
    'ip-10-0-0-165',
    'ip-10-0-0-125',
    'ip-10-0-0-150',
    'ip-10-0-0-166',
    ]
KAFKA_BROKERS = ':9092,'.join(brokers) + ':9092'

def produce(bucket, brokers, topic):
    """
    Read lines from the specified AWS S3 bucket and publish to the appropriate
    topic on the Kafka cluster
    """

    # Instantiate the producer object
    producer = KafkaProducer(bootstrap_servers = brokers)

    # Read individual lines from the S3 file and publish to the Kafka topic
    for line in smart_open(s3_url, 'rb'):

        fields = line.strip().encode('utf8').split(',')
        message = ','.join(fields[0], fields[2])

        # FUTURE: insert control loop to simulate rate of ingestion
        producer.send(topic, message)
        #producer.flush()


if __name__ == '__main__':
    # Parse command line arguements
    parser = argparse.ArgumentParser(description='xxx')
    parser.add_argument('-h', '--host', default=KAFKA_BROKERS, help='Kafka broker ip')
    parser.add_argument('-t', '--topic', default=KAFKA_TOPIC, help='Kafka topic name')
    parser.add_argument('-p', '--port', default='9092', help='Kafka port number (default 9092)')
    args = parser.parse_args()

    source = s3_url
    brokers = KAFKA_BROKERS
    topic = KAFKA_TOPIC

    #
    try:
        produce(source, brokers, topic)
    except as e:
        print('Could not publish to {0}.'.format(topic))

