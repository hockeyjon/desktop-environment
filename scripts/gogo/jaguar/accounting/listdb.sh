#!/bin/bash
if [ $# -eq 0 ];then
    rows=0
else
   case $1 in
       ''|*[!0-9]*)
            echo "invalid input."
            exit 1
            ;;
       *) 
            rows=$1
            ;;
   esac
fi

if [ $rows -eq 0 ]; then
    sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache;" 
else 
    sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache ORDER BY id DESC LIMIT $rows;" 
fi
