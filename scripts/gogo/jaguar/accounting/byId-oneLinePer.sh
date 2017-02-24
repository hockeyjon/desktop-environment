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

echo "-------------------------------------"
idsstring=`sqlite3 /var/acctd/cache.sqlite "SELECT id FROM record_cache order by id desc limit $rows;"`
ids=(${idsstring// / })
for (( i=${#ids[@]}-1 ; i>=0 ; i-- ))
do
    id=${ids[i]}
    ctime=`sqlite3 /var/acctd/cache.sqlite "SELECT ctime FROM record_cache where id=\"$id\";" | xargs -I {} date +"%T" -d @{}`
    type=`sqlite3 /var/acctd/cache.sqlite "SELECT type FROM record_cache where id=\"$id\";"`
    resource=`sqlite3 /var/acctd/cache.sqlite "SELECT resource FROM record_cache where id=\"$id\";"`
    pedmac=`sqlite3 /var/acctd/cache.sqlite "SELECT pedmac FROM record_cache where id=\"$id\";"`
    appname=`sqlite3 /var/acctd/cache.sqlite "SELECT appname FROM record_cache where id=\"$id\";"`
    unit=`sqlite3 /var/acctd/cache.sqlite "SELECT unit FROM record_cache where id=\"$id\";"`
    start=`sqlite3 /var/acctd/cache.sqlite "SELECT starttime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    end=`sqlite3 /var/acctd/cache.sqlite "SELECT endtime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
    bytes=`sqlite3 /var/acctd/cache.sqlite "SELECT amount FROM record_cache where id=\"$id\";"`
    #mb=`awk "BEGIN {printf \"%.2f\",${bytes}/${i}"`
    #mb=`bc <<< 'scale=2;$((amount))/1024/1024'`
    echo "id: $id  ctime: $ctime  type: $type  resource: $resource  pedmac: $pedmac  appname: $appname  bytes: $bytes mb: $mb       start: $start"
    #echo "ctime:    $ctime"
    #echo "-------------------------------------"
done
echo
echo "Date: `date`"