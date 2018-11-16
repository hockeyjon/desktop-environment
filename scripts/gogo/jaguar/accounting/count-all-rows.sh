#!/bin/bash
rows=`sqlite3 /var/acctd/cache.sqlite "SELECT COUNT(*) FROM record_cache;"`
echo $rows
