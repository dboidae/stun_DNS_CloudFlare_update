#!/bin/bash
#
#here you must specify AWS account, VPC and subnet settings
export AWS_PROFILE=my_profile
export VPC_ID=
export SUBNET_ID_A=
export SUBNET_ID_B=

serverless deploy -v --aws-profile $AWS_PROFILE --force
