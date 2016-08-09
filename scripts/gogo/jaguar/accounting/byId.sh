#!/bin/bash

id=$1 
ctime=`sqlite3 /var/acctd/cache.sqlite "SELECT ctime FROM record_cache where id=\"$id\";" | xargs -I {} date -d @{}`
type=`sqlite3 /var/acctd/cache.sqlite "SELECT type FROM record_cache where id=\"$1\";"`
resource=`sqlite3 /var/acctd/cache.sqlite "SELECT resource FROM record_cache where id=\"$1\";"`
pedmac=`sqlite3 /var/acctd/cache.sqlite "SELECT pedmac FROM record_cache where id=\"$1\";"`
appname=`sqlite3 /var/acctd/cache.sqlite "SELECT appname FROM record_cache where id=\"$1\";"`
unit=`sqlite3 /var/acctd/cache.sqlite "SELECT unit FROM record_cache where id=\"$1\";"`
start=`sqlite3 /var/acctd/cache.sqlite "SELECT starttime FROM record_cache where id=\"$id\" order by id desc limit 1;" | xargs -I {} date -d @{}`
end=`sqlite3 /var/acctd/cache.sqlite "SELECT endtime FROM record_cache where id=\"$id\" order by id desc limit 1;" | xargs -I {} date -d @{}`
amount=`sqlite3 /var/acctd/cache.sqlite "SELECT amount FROM record_cache where id=\"$id\" order by id desc limit 1;"`
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
