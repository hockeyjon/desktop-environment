#!/bin/bash

mac=`cat macaddress` 
#sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache where pedmac=\"mac\";"
sqlite3 /var/acctd/cache.sqlite "PRAGMA table_info(record_cache);"
#sqlite3 /var/acctd/cache.sqlite ".tables"
#sqlite3 /var/acctd/cache.sqlite ""
 
