#!/usr/bin/python3
"""

"""

import argparse
from time import sleep

from kafka import KafkaProducer
from kafka.errors import KafkaError
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

for line in smart_open(s3_url, 'rb'):
    print(line)
    for i in range(100000):
        pass
    print('x'*40)

#with smart_open(s3_url, 'rb') as f:
#
#    line = f.read()
#    print(inc, line)
#    fields = line.split(',')
#    timestamp, temperature = fields[0], fields[2]
#
#    print(timestamp, temperature)

#producer = KafkaProducer(bootstrap_servers='ec2-


if __name__ == '__main__':

    # Parse command line arguements
    parser = argparse.ArgumentParser(description='xxx')
    parser.add_argument('-h', '--host', default=KAFKA_BROKERS, help='Kafka broker ip')
    parser.add_argument('-t', '--topic', default=KAFKA_TOPIC, help='Kafka topic name')
    parser.add_argument('-p', '--port', default='9092', help='Kafka port number (default 9092)')
    args = parser.parse_args()

    #

