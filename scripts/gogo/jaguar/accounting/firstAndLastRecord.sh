#!/bin/bash
echo "-------- First Record ---------"
idsstring=`sqlite3 /var/acctd/cache.sqlite "SELECT id FROM record_cache order by id asc limit 1;"`
ids=(${idsstring// / })
for (( i=${#ids[@]}-1 ; i>=0 ; i-- ))
do
    id=${ids[i]}
    ctime=`sqlite3 /var/acctd/cache.sqlite "SELECT ctime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    type=`sqlite3 /var/acctd/cache.sqlite "SELECT type FROM record_cache where id=\"$id\";"`
    resource=`sqlite3 /var/acctd/cache.sqlite "SELECT resource FROM record_cache where id=\"$id\";"`
    pedmac=`sqlite3 /var/acctd/cache.sqlite "SELECT pedmac FROM record_cache where id=\"$id\";"`
    appname=`sqlite3 /var/acctd/cache.sqlite "SELECT appname FROM record_cache where id=\"$id\";"`
    unit=`sqlite3 /var/acctd/cache.sqlite "SELECT unit FROM record_cache where id=\"$id\";"`
    start=`sqlite3 /var/acctd/cache.sqlite "SELECT starttime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    end=`sqlite3 /var/acctd/cache.sqlite "SELECT endtime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    amount=`sqlite3 /var/acctd/cache.sqlite "SELECT amount FROM record_cache where id=\"$id\";"`
    echo "id:  $id    ctime: $ctime    type: $type    amount: $amount   start: $start    end:  $end"
done
echo "-------------------------------------"
echo
echo "Total number of rows: `sqlite3 /var/acctd/cache.sqlite "SELECT count(*) FROM record_cache;"`"
echo
echo "-------- Last Record ---------"
idsstring=`sqlite3 /var/acctd/cache.sqlite "SELECT id FROM record_cache order by id desc limit 1;"`
ids=(${idsstring// / })
for (( i=${#ids[@]}-1 ; i>=0 ; i-- ))
do
    id=${ids[i]}
    ctime=`sqlite3 /var/acctd/cache.sqlite "SELECT ctime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    type=`sqlite3 /var/acctd/cache.sqlite "SELECT type FROM record_cache where id=\"$id\";"`
    resource=`sqlite3 /var/acctd/cache.sqlite "SELECT resource FROM record_cache where id=\"$id\";"`
    pedmac=`sqlite3 /var/acctd/cache.sqlite "SELECT pedmac FROM record_cache where id=\"$id\";"`
    appname=`sqlite3 /var/acctd/cache.sqlite "SELECT appname FROM record_cache where id=\"$id\";"`
    unit=`sqlite3 /var/acctd/cache.sqlite "SELECT unit FROM record_cache where id=\"$id\";"`
    start=`sqlite3 /var/acctd/cache.sqlite "SELECT starttime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    end=`sqlite3 /var/acctd/cache.sqlite "SELECT endtime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    amount=`sqlite3 /var/acctd/cache.sqlite "SELECT amount FROM record_cache where id=\"$id\";"`
    echo "id:  $id    ctime: $ctime    type: $type    amount: $amount   start: $start    end:  $end"
done
echo
echo "Date: `date`"
