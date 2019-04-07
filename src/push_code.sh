#! /usr/bin/env bash

USAGE="Usage:  push_to.sh <aws_node_name> <file_or_directory>"
PROJECT_BASE="~/Desktop/InsightDataEngineering/projects"

[[ $# != 2 ]] && echo $USAGE && exit 1

node=${1}

case $node in 
    kafka)
        node_ip='52.34.181.201' ;;
    producers)
        node_ip='54.203.3.199' ;;
    processors)
        node_ip='54.68.226.170' ;;
    consumers)
        node_ip='35.167.90.164' ;;
    storage)
        node_ip='34.208.100.1' ;;
    ui)
        node_ip='35.160.236.29' ;;
    *)
        echo $USAGE && exit 2
        ;;
esac

[[ ! -d $2 ]] && [[ ! -f $2 ]] && echo $USAGE && exit 3

push_from=${2}
push_to="ubuntu@${node_ip}:~/${push_from}"

echo -e "FROM:\t$(pwd)/${push_from}"
echo -e "TO:\t${push_to}"
exit 0

# Push all source code to remote
scp -r -i ~/.ssh/CSimchick-IAM-keypair.pem "$(pwd)/${push_from}" "${push_to} 
