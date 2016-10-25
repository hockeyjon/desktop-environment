#! /bin/sh

i="0"
while [ $i -lt 200 ]
do
   faulttool -T critical -t HW -c 3456 -- Error number: $i
   sleep 1
   i=$[$i+1]
done
