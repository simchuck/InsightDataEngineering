#! /usr/bin/env bash

#[[ $# != 1 ]] && exit "Usage: ./push <directory>"

[[ -d $1 ]] && exit "Usage: ./push <directory>"
[[ -f $1 ]] && exit "Usage: ./push <directory>"

push_from=${1}
push_to='ubuntu@54.203.3.199:~/'

# Push all source code to remote
scp -r -i ~/.ssh/CSimchick-IAM-keypair.pem '~/${push_from}/ ${push_to} 
