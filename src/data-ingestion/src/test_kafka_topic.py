#! /usr/bin/env python3
"""
Test code for simple producer.

Reads from specified S3 bucket and writes each line to Kafka topic.
"""

### May have some issues with data files due to Windows line endings `\r\n`

import argparse
#import logging

from kafka import KafkaProducer,KafkaConsumer

#logger = logging.basicConfig(level=logging.DEBUG)

brokers = [
    'ip-10-0-0-165',
    'ip-10-0-0-125',
    'ip-10-0-0-150',
    'ip-10-0-0-166',
    ]
brokers = ':9092,'.join(brokers) + ':9092'

s3_bucket = 's3://csimchick-insight-static-data'

STREAM_INFO = {
    'weather': {'folder': 'weather', 'file': 'weather.dat'},
    'cpu_demand': {'folder': 'mis-data', 'file': 'mains.dat'},
    'energy_price': {'folder': 'energy-price', 'file': 'pjm_rt_fivemin_hrl_lmps.csv'},
#    'resource_capacity', {'folder': '', 'file': ''},
    }
S = STREAM_INFO     # set alias for clarity in following step
for k,v in S.items():
    S[k]['url'] = '/'.join([s3_bucket, S[k]['folder'], S[k]['file']])


def produce_record(source, brokers, topic):
    """
    Read each line from specified source, small transformation, and publish to topic.
    """

    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    import json

    from smart_open import smart_open

    # DEBUG: can I move the instantiation outside of the loop to improve throughput?
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
#        yield (record.timestamp, record.value)


def simulate_streams_for_resource_node(topic):

    for stream in STREAM_INFO:
    #for (topic, s3_directory, s3_filename) in STREAM_INFO:

        #s3_source = '/'.join([s3_bucket, s3_directory, s3_filename])

        #logger.debug('\nStarting Kafka producer test with\n' \
        #print('\nStarting Kafka producer test with\n' \
        #    '\tsource: \t{0}\n' \
        #    '\ttopic:  \t{1}\n' \
        #    '\tbrokers:\t{2}\n'.format(s3_source, topic, brokers))

        try:
            produce_record(stream['url'], brokers, topic)
            #produce_record(s3_source, brokers, topic)
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
        #record, value = consume_record(brokers, topic)
        consume_record(brokers, topic)
    except Exception as e:
        print('ERROR: Could not read from topic {0}'.format(topic))
        raise e

    #yield record, value
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


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test Producer/Consumer for Kafka cluster.')
    parser.add_argument('-m', '--mode', help='Specify producer/consumer mode')
    parser.add_argument('-t', '--topic', help='Specify Kafka topic')
    args = parser.parse_args()

    if args.mode == 'producer':
        if args.topic == 'weather':
            s3_url = s3_bucket + '/weather/weather.dat'
        elif args.topic == 'price':
            s3_url = s3_bucket + '/energy-price/pjm_rt_fivemin_hrl_lmps.csv'
        elif args.topic == 'demand':
            s3_url = s3_bucket + '/mis-data/mains.dat'
        simulate_topic_stream(args.topic, s3_url)
        #simulate_streams_for_resource_node(topic)
    elif args.mode == 'consumer':
        record = consume_topic_stream(args.topic)
        #consume_streams_for_resource_node()
