#!/bin/bash

# Text UI for Real Time Dispatch 
# 
# 2019.04.17
# Charles Simchick
# Insight Data Engineering, 19A-SEA

# Text files will be written from my python application with spacing, formatting as appropriate
# include all necessary headers, etc

# This file will loop continuously (perhaps with some sleep delay),
# read from the files to reorganize, rearrange, cut, etc
# clear screen and write update


while true; do

    clear

    echo -e "Real Time Dispatch                                   Charles Simchick, Insight Data Engineering"
    echo -e "-----------------------------------------------------------------------------------------------"
    
    
    echo -e "Resource Node Status"
    echo -e "\tNode\t\tprice\t\tcapacity\t\tload\t\tjobs[]"
    cat node_status_headers.out
    cat node_status.out
    
    echo -e "\n"
    echo -e "Job Queue"
    cat job_queue_headers.out
    cat job_queue.out
    
    echo -e "\n"
    echo -e "Job Summary"
    cat job_summary.out
    
    echo -e "\n"
    echo -e "Node Stream"
    cat node_steream_headers.out
    cat node_stream.out
    
    sleep 0.1

done
    
