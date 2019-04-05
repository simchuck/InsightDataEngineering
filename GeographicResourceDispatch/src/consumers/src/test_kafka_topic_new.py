#! /usr/bin/env python3
"""
Test code for simple producer.

Reads from specified S3 bucket and writes each line to Kafka topic.
"""

### May have issues due to Windows line endings `\r\n`

import argparse
import psycopg2
import sqlite3
from sqlite3 import Error
#import logging

from kafka import KafkaProducer,KafkaConsumer
from smart_open import smart_open

#logger = logging.basicConfig(level=logging.DEBUG)

brokers = [
    'ip-10-0-0-165',
    'ip-10-0-0-125',
    'ip-10-0-0-150',
    'ip-10-0-0-166',
    ]
brokers = ':9092,'.join(brokers) + ':9092'

s3_bucket = 's3://csimchick-insight-static-data'

STREAM_INFO = [
    ['weather', 'weather', 'weather.dat'],
    ['cpu_demand', 'mis-data', 'mains.dat'],
    ['energy_price', 'energy-price', 'pjm_rt_fivemin_hrl_lmps.csv'],
#    ['resource_capacity', 'weather.dat', 'weather'],
    ]
STREAM_INFO = [
    ('weather', 'weather', 'weather.dat'),
    ('cpu_demand', 'mis-data', 'mains.dat'),
    ('energy_price', 'energy-price', 'pjm_rt_fivemin_hrl_lmps.csv'),
#    ('resource_capacity', 'weather.dat', 'weather'),
    ]


def produce_record(source, brokers, topic):
    """
    Read each line from specified source, small transformation, and publish to topic.
    """

    producer = KafkaProducer(bootstrap_servers=brokers)

    for line in smart_open(source, 'r'):
        fields = line.strip().encode('utf-8')
#        fields = line.strip().encode('utf-8').split(',')
#        record = ','.join(fields[0], fields[2])
        producer.send(topic, fields)
#        producer.flush()       ### WHAT DOES THIS DO?


def consume_record(brokers, topic):
    """
    Read each record from topic and print to screen.
    """

    consumer = KafkaConsumer (
        topic,
        bootstrap_servers=brokers
        #auto_offset_reset='earliest'
        )

    for record in consumer:
        print(record.timestamp, record.value)
        print()
        result = [record.timestamp, record.value]
        yield result


def simulate_streams_for_resource_node(topic):

    for (topic, s3_directory, s3_filename) in STREAM_INFO:

        s3_source = '/'.join([s3_bucket, s3_directory, s3_filename])

        #logger.debug('\nStarting Kafka producer test with\n' \
        #print('\nStarting Kafka producer test with\n' \
        #    '\tsource: \t{0}\n' \
        #    '\ttopic:  \t{1}\n' \
        #    '\tbrokers:\t{2}\n'.format(s3_source, topic, brokers))

        try:
            produce_record(s3_source, brokers, topic)
        except Exception as e:
            print('ERROR: Could not publish to topic {0}'.format(topic))
            raise e

    return


def simulate_topic_stream(topic, source_data):

    print('\nStarting Kafka producer test with\n' \
        '\tsource: \t{0}\n' \
        '\ttopic:  \t{1}\n'.format(source_data, topic))

    try:
        produce_record(source_data, brokers, topic)
    except Exception as e:
        print('ERROR: Could not publish to topic {0}'.format(topic))
        raise e

def consume_topic_stream(topic):

    try:
        result = consume_record(brokers, topic)
        key, value = result[0], result[2]
    except Exception as e:
        print('ERROR: Could not read from topic {0}'.format(topic))
        raise e

    return key, value
    #print(result)
    #print()


def consume_streams_for_resource_node():

    #logger.debug('\nStarting Kafka consumer test\n')
    print('\nStarting Kafka consumer test\n')

    for stream in STREAM_INFO:
        print(stream)
        print(type(stream))
        for (topic, directory, filename) in stream:
            try:
                consume_record(brokers, topic)
                # maths here
            except Exception as e:
                print('Could not read from topic {0}'.format(topic))
                raise e

    return


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        query = ''
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test Producer/Consumer for Kafka cluster.')
    parser.add_argument('-m', '--mode', help='Specify producer/consumer mode')
    parser.add_argument('-t', '--topic', help='Specify Kafka topic')
    args = parser.parse_args()

    if args.mode == 'producer':
        if args.topic == 'weather':
            simulate_topic_stream(args.topic, s3_bucket + '/weather/weather.dat')
        elif args.topic == 'price':
            simulate_topic_stream(args.topic, s3_bucket + '/energy-price/pjm_rt_fivemin_hrl_lmps.csv')
        elif args.topic == 'demand':
            simulate_topic_stream(args.topic, s3_bucket + '/mis-data/mains.dat')
        #simulate_streams_for_resource_node(topic)
    elif args.mode == 'consumer':
        create_connection("C:\\sqlite\db\pythonsqlite.db")
        #consume_streams_for_resource_node()
        if args.topic == 'weather':
            ts_weather, val_weather = consume_topic_stream(args.topic)
        elif args.topic == 'price':
            ts_price, val_price = consume_topic_stream(args.topic)
        elif args.topic == 'demand':
            ts_demand, val_demand = consume_topic_stream(args.topic)


