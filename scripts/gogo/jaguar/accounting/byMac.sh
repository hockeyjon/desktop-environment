#!/bin/bash
if [ $# -eq 0 ];then
    rows=1
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

mac=`cat macaddress` 
echo "serching for pedmac: $mac"
echo "-------------------------------------"
idsstring=`sqlite3 /var/acctd/cache.sqlite "SELECT id FROM record_cache where pedmac=\"$mac\" order by id desc limit $rows;"`
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
    echo "id:       $id"
    echo "ctime:    $ctime"
    echo "type:     $type"
    echo "resource: $resource"
    echo "pedmac:   $pedmac"
    echo "appname:  $appname"
    echo "unit:     $unit"
    echo "amount:   $amount"
    echo "start:    $start"
    echo "end:      $end"
    echo "-------------------------------------"
done
echo
echo "Date: `date`"
