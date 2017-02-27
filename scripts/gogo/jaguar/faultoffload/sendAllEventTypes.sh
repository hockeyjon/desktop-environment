#!/usr/bin/env bash

faulttool -T critical -t HW -c 1111 -- Critical HW Event
echo "faulttool -T critical -t HW -c 1111 -- Critical HW Event"
faulttool -T abnormal -t HW -c 1112 -- Abnormal HW Event
echo "faulttool -T abnormal -t HW -c 1112 -- Abnormal HW Event"
faulttool -T event -t HW -c 1113 -- Normal HW Event
echo "faulttool -T event -t HW -c 1113 -- Normal HW Event"
faulttool -T health -t HW -c 1114 -- Health HW Event
echo "faulttool -T health -t HW -c 1114 -- Health HW Event"