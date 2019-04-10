#! /usr/bin/env python3
"""
Data ingestion and extraction from Kafka topics.

Command line options allow specification as producer or consumer, along with specification
of the topic of interest.

Ingestion options include from web API call, or from AWS S3 bucket.  API/url for either
option is currently hard-coded in this file.  Records are extracted from the source,
transformed (as appropriate), then published to the specified Kafka topic.

Generic consumption routines are provided to extract from the specified Kafka topic.

Kafka cluster IP addresses for brokers are hard-coded here for specific infrastructure
used during the Insight 19A-SEA Data Engineering cohort.
"""

import argparse
#import logging
import sys

from kafka import KafkaProducer,KafkaConsumer
from smart_open import smart_open

#logger = logging.basicConfig(level=logging.DEBUG)

# AWS private IP addresses for the Kafka cluster.
brokers = [
    'ip-10-0-0-165',
    'ip-10-0-0-125',
    'ip-10-0-0-150',
    'ip-10-0-0-166',
    ]
brokers = ':9092,'.join(brokers) + ':9092'

# AWS S3 bucket containing static data sources used for simulation.
s3_bucket = 's3://csimchick-insight-static-data'

# Specify ingestion data stream info, including topic name and source location on S3.
STREAM_INFO = {
    'weather': {'folder': 'weather', 'file': 'weather.dat'},
    'demand': {'folder': 'mis-data', 'file': 'mains.dat'},
    'price': {'folder': 'energy-price', 'file': 'pjm_rt_fivemin_hrl_lmps.csv'},
#    'resource_capacity', {'folder': '', 'file': ''},
    }
S = STREAM_INFO     # set alias for clarity in following step
for k,v in S.items():
    S[k]['url'] = '/'.join([s3_bucket, S[k]['folder'], S[k]['file']])

# Specify insgestion web API info, including topic name and web API string.
### TODO: NOT YET IMPLEMENTED ###
API_INFO = {
    'weather': {'api_url': '', 'query_string': ''},
    'cpu_demand': {'api_url': '', 'query_string': ''},
    'energy_price': {'api_url': '', 'query_string': ''},
#    'resource_capacity', {'api_url': '', 'query_string': ''},
    }
A = API_INFO        # set alias for clarity in following step
for k,v in A.items():
    A[k]['url'] = '/'.join([A[k]['api_url'], A[k]['query_string']])


### DEBUG: PROBLEM APPEARS TO BE IN THIS ROUTINE -- RETURNING A GENERATOR OBJECT
### DEBUG: ON CALLS INSTEAD OF STRING OBJECT.
def query_file(source_url):
    """
    Yield each line of the specified file resource.
    """
    def __init__(self, source_url):
        print(' 68: Within query_file().__init__()')        ### DEBUG:
        f = smart_open(source_url, 'r')
        print(' 70: after smart_open() call')               ### DEBUG:

    print(' 72: Within query_file(), before loop with ', type(source_url), source_url)   ### DEBUG:
    for line in f.read().strip().encode('utf-8'):
    #while True:
    #    line = f.read().strip().encode('utf-8')
        print(' 76: In query_file(), type is ', type(line))      ### DEBUG:
        yield line


def query_api(url):
    """
    Submit query to web API and return response.
    """
    pass        ### TODO: NOT YET IMPLEMENTED ###
    sys.exit('ERROR: function `query_api()` is not yet implemented')
    #return response


def produce_record(source, brokers, topic):
    """
    ETL ingestion to Kafka topics.

    Hard-coded ETL pipeline allows for filtering and transformation of the source data
    before publishing to the Kafka topic.

    Input:
        source  dict with 'url' for data source location
        topic   string representing the Kafka topic name
    """

    # Instantiate Kafka producer
    try:
        producer = KafkaProducer(bootstrap_servers=brokers)
    except Exception as e:
        print('ERROR: Could not instantiate producer at {0}'.format(brokers))

    # Extract: get data from source
    print('108: source.startswith(): ',source[:4]); print(source.startswith('http'), source.startswith('s3'))        ### DEBUG:
    if source.startswith('http'):
        record = query_api(source)
    elif source.startswith('s3'):
        print('112: Before query_file(), type is ')     ### DEBUG:
        record = query_file(source)
        print('114: After query_file(), type is ', type(record))     ### DEBUG:
    else:
        sys.exit('ERROR: Data source is not valid.')

    # Transform: filtering, aggregations, and simulation adjustments as appropriate
    ### TODO: NEED TO ADJUST STATIC DATA FILE TIMESTAMPS FOR SIMULATION
    pass

    # Load: publish to Kafka topic
    print('123: ', type(topic), topic)       ### DEBUG:
    print('124: ', type(record), record)     ### DEBUG:
    try:
        producer.send(topic, record)
#        producer.flush()       ### IS THIS NECESSARY?
    except Exception as e:
        print('ERROR: Could not publish to topic {0}'.format(topic))
        raise e

    return record


def consume_record(brokers, topic):
    """
    Read a single record from the specified Kafka topic and return.
    """

    # Instantiate Kafka consmer
    try:
        consumer = KafkaConsumer (
            topic,
            bootstrap_servers=brokers
            #auto_offset_reset='earliest'
            )
    except Exception as e:
        print('ERROR: Could not instantiate consumer at {0}'.format(brokers))

    for record in consumer:
        yield record


def simulate_topic_stream(topic, source_data):
    """
    Wrapper around produce_record() to provide output to STDOUT.
    """

    print('\nStarting Kafka producer test with\n' \
        '\tsource: \t{0}\n' \
        '\ttopic:  \t{1}\n'.format(source_data, topic))

    print('163: ', type(source_data), source_data)   ### DEBUG:
    print('164: ', type(brokers), brokers)           ### DEBUG:
    print('165: ', type(topic), topic)               ### DEBUG:
    try:
        record = produce_record(source_data, brokers, topic)
        #print(record)
        print('.',)
    except Exception as e:
        print('ERROR: Could not publish to topic {0}'.format(topic))
        raise e


def consume_topic_stream(topic):
    """
    Wrapper around consume_record() to provide output to STDOUT.
    """

    print('\nStarting Kafka consumer test with\n' \
        '\ttopic:  \t{0}\n'.format(topic))

    try:
        record = consume_record(brokers, topic)
        print('185: ', record)      ### DEBUG:
        return record
    except Exception as e:
        print('ERROR: Could not consume from topic {0}'.format(topic))
        raise e


#def simulate_streams_for_resource_node(topic):
#
#    for stream in STREAM_INFO:
#
#        try:
#            produce_record(stream['url'], brokers, topic)
#            #produce_record(s3_source, brokers, topic)
#        except Exception as e:
#            print('ERROR: Could not publish to topic {0}'.format(topic))
#            raise e
#
#    return
#
#
#def consume_streams_for_resource_node():
#
#    #logger.debug('\nStarting Kafka consumer test\n')
#    print('\nStarting Kafka consumer test\n')
#
#    for stream in STREAM_INFO:
#        print(stream)
#        print(type(stream))
#        for (topic, directory, filename) in stream:
#            try:
#                consume_record(brokers, topic)
#                # maths here
#            except Exception as e:
#                print('Could not read from topic {0}'.format(topic))
#                raise e
#
#    return


if __name__ == '__main__':
    """
    Command line execution of producers and consumers.
    """

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Producer/Consumer for Kafka cluster.')
    parser.add_argument('-m', '--mode', help='Specify producer/consumer mode')
    parser.add_argument('-t', '--topic', help='Specify Kafka topic')
    args = parser.parse_args()

    ### TODO: NEED TO MAKE THIS MORE GENERIC TO HANDLE ANY SPECIFIED RESOURCE NODE
    if args.mode == 'producer':
        #simulate_streams_for_resource_node(topic)
        if args.topic == 'all':
            for topic, source in STREAM_INFO.items():
                print('241: ', type(topic), topic)       ### DEBUG:
                print('242: ', type(source), source)     ### DEBUG:
                simulate_topic_stream(topic, source['url'])
        else:
            simulate_topic_stream(args.topic, STREAM_INFO['args.topic']['url'])

    elif args.mode == 'consumer':
        #consume_streams_for_resource_node()
        if args.topic == 'all':
            for topic, source in STREAM_INFO.items():
                print('251: ', type(topic), topic)       ### DEBUG:
                record = consume_topic_stream(topic)
        else:
            record = consume_topic_stream(args.topic)
