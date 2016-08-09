#!/bin/bash

mac=`cat macaddress` 
echo "serching for $mac"
sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache where pedmac=\"$mac\";"
