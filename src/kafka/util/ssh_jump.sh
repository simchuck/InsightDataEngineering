#!/bin/bash

# Jump to nodes in the Kafka cluster using local IP address

# Usage:
#     ssh_jump.sh <node_name>|<node_num>

node=${1}

case $node in
    0|master)
	ip='10.0.0.165'
	;;
    1|worker1)
	ip='10.0.0.125'
	;;
    2|worker2)
	ip='10.0.0.150'
	;;
    3|worker3)
	ip='10.0.0.166'
	;;
    *)
 	;;
esac

ssh ubuntu@${ip}

