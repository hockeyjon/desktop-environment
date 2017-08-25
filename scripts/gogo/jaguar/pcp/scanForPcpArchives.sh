#! /bin/bash

#. Get the date that the last PCP archived was started (which is
#   represented in the name of archive file (YYYYMMDD.HH.MM.tar.zx)
#   by executing the following commands on the LRU's CLI: ::
#   * ``cd /var/log/pcp/pmlogger/jaguar/
#   * ``ls -l *xz | awk '{print $9}'| tail -n1``


#. Ensure that the latest file is a valid PCP archive file by perfoming
#   the following commands on the LRUs CLI: ::
#   * ``tar --xz -xvf <YYYMMDD.HH.MM>.tar.xz``
#   * ``pmlogsummary -a <YYYMMDD.HH.MM>.0 psoc.now.status | wc -l
#   and verifying that the last command returns a value that is greater
#   than 0.

#. Verify that the pcp archive file offload was attempted at least once
#   after the most recent reboot by executing the following command on
#    the LRU's CLI: ::
#   * ``pushd /var/log/pcp/pmlogger/jaguar/ && file=`ls -l *xz |
#      awk '{print $9}'| tail -n1`;journalctl -b0 -u datapusher |
#      grep Pushing | grep "$file to datastore" | wc -l``