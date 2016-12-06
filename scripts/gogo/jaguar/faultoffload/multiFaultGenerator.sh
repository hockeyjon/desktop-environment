#!/bin/bash

codes="10001 \
10002 \
10003 \
10004 \
10005 \
10006 \
10007 \
10008 \
10009"

read -a msgCodes <<< "$codes"

for (( i=0 ; i<${#msgCodes[@]}; i++ ))
do 
    faulttool -T critical -t HW -c ${msgCodes[i]} -- Error
    echo "faulttool -T critical -t HW -c ${msgCodes[i]} -- Error"
    sleep 2
done
