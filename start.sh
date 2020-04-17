#!/bin/bash
#
#export AWS_PROFILE=my_profile
for i in `cat environment.sh` 
	do 
		export $i 
	done
./l-start.py
