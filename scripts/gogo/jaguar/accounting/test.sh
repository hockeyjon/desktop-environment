#!/bin/bash

mac=`cat macaddress` 
sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache where pedmac=\"mac\";"
 
