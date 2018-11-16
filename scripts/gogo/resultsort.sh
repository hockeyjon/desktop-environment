#!/bin/bash
file=$1
if [ ! -f  $file ]; then
    echo "$file not found!"
fi

cat $file | grep -n "<Begin" > parse.log 
cat $file | grep -n "<End" >> parse.log 
cat $file | grep -n "#@%" >> parse.log
cat $file | grep -n "TESTSTEP" >> parse.log
sort -n parse.log > $file.parsed
rm parse.log
