#!/bin/bash

### THIS SCRIPT HAS NOT BEEN TESTED

### TODO: Add query template(s) for derived streams
### TODO: Add scripting, etc for combined streams


# This script creates KSQl streams for all of the resource node topics:
#   RN###-weather
#   RN###-demand
#   RN###-energy-price
#   RN###-capacity
#   RN###-load
#   RN###-resource-price
#   RN###-summary

# For now, using the KSQL CLI 
# ref. https://docs.confluent.io/current/ksql/docs/tutorials/examples.html

create_from_topic_query=<<<
DROP STREAM :TOPIC:;
CREATE STREAM :TOPIC: ( :SCHEMA: )
    WITH (
        KAFKA_TOPIC=':TOPIC:',
        VALUE_FORMAT='DELIMITED',
        TIMESTAMP='ts',
        TIMESTAMP_FORMAT=':TS_FORMAT:'
        )
    ;
<<<

### DEBUG: following query is not complete
### DEBUG: trying to make it sufficiently generic to use for all cases
create_from_stream_query=<<<
DROP STREAM :TOPIC:;
CREATE STREAM :TOPIC: AS
    SELECT :ONE:.ts, :ONE:.:VAR_ONE:, :TWO:.ts, :TWO:.:VAR_TWO:
    FROM :TOPIC_ONE: :ONE:, :TOPIC_TWO: :TWO:
    WHERE ABS(:ONE:.ts - :TWO:.ts) < :WINDOW:
    ;
<<<

for rn in RN{001..003}; do

    # 1. Create KSQL streams directly from Kafka topics

    topic='weather'
    schema='ts VARCHAR, id BIGINT, T1 VARCHAR, temperature VARCHAR, T3 VARCHAR, T4 VARCHAR, T5 VARCHAR, T6 VARCHAR, T7 VARCHAR, T8 VARCHAR, T9 VARCHAR
    ts_fmt='yyyy-MM-dd HH:mm:ss'
    ksql http://localhost:8088 < (echo "${create_from_topic_query}" | sed -e "s/:TOPIC:/${rn}-${topic}/g; s/:SCHEMA:/${schema}/g; s/:TS_FMT:/${ts_fmt}/g;")

    topic='demand'
    schema='ts VARCHAR, id BIGINT, kWh VARCHAR, kW VARCHAR, A VARCHAR'
    ts_fmt='yyyy-MM-dd HH:mm:ss'
    ksql http://localhost:8088 < (echo "${create_from_topic_query}" | sed -e "s/:TOPIC:/${rn}-${topic}/g; s/:SCHEMA:/${schema}/g; s/:TS_FMT:/${ts_fmt}/g;")

    ### DEBUG: this one is not working yet -- possibly having to do with interpretation of the timestamp format
    topic='energy-price'
    schema='ts VARCHAR, id BIGINT, loc VARCHAR, V VARCHAR, Tx VARCHAR, load VARCHAR, utility VARCHAR, LMP VARCHAR, p1 VARCHAR, p2 VARCHAR, p3 VARCHAR, B BOOLEAN, n INT'
    ts_fmt='yyyy/MM/dd hh:mm:ss a'
    ksql http://localhost:8088 < (echo "${create_from_topic_query}" | sed -e "s/:TOPIC:/${rn}-${topic}/g; s/:SCHEMA:/${schema}/g; s/:TS_FMT:/${ts_fmt}/g;")
        
    topic='capacity'
    schema='ts VARCHAR, id BIGINT, capacity VARCHAR'
    ts_fmt='yyyy-MM-dd HH:mm:ss'
    ksql http://localhost:8088 < (echo "${create_from_topic_query}" | sed -e "s/:TOPIC:/${rn}-${topic}/g; s/:SCHEMA:/${schema}/g; s/:TS_FMT:/${ts_fmt}/g;")


    # 2. Create KSQL streams by combining existing KSQL streams
    ### these will use the CREATE STREAM .. AS SELECT .. format
    topic='load'
    ksql http://localhost:8088 < 
        (echo "${create_from_topic_query}" | 
        sed -e " \
            s/:TOPIC:/${rn}-${topic}/g; \
            s/:TOPIC_ONE:/${topic_one}/g; s/:ONE:/${one}/g; s/:VAR_ONE:/${var_one}/g; \
            s/:TOPIC_TWO:/${topic_two}/g; s/:TWO:/${two}/g; s/:VAR_TWO:/${var_two}/g; \
            s/:WINDOW:/${window}/g; \
            "
        )

    topic='resource-price'
    topic='summary'

done



# Original approach below, used multiple external template files with schema and timemstamp format
#topics='capacity demand energy-price load resource-price summary weather'
#masks='CAPACITY DEMAND ENERGY-PRICE LOAD RESOURCE-PRICE SUMMARY WEATHER'
## NOTE: .template files use format |TOPIC-STREAM|
#
## KSQL query string is created in memory for each topic; not saved to disk.
#for topic in ${topics}; do
#    mask='|'$(echo ${topic} | tr a-z A-Z)'-STREAM|'
#    ksql http://localhost:8088 < 
#        (cat rn_${topic}_stream.ksql.template | sed -e "s/${mask}/${topic}/g")
#done
