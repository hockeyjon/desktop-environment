#!/bin/bash
FILE=sqlite.out
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
    sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache ORDER BY id DESC LIMIT $rows;" > $FILE
    
    idx=0
    while read line
    do
        rows[$idx]=$line
        ((idx++))
    done <$FILE


    echo -e " ID   |\tCTIME\t\t\t     |  LRUID\t     |\tTYPE    | RSRC |  MACADDR\t   |   APPNAME  |  UNIT | AMT |   START TIME\t\t     |  END TIME"
    rowIdx=0
    while [ "$rowIdx" -lt ${#rows[@]} ];do
       #echo "row $idx:  ${rows[$rowIdx]}"
       out=""
       colIdx=0
       IFS='|' read -a cols <<< "${rows[$rowIdx]}"
       while [ "$colIdx" -lt ${#cols[@]} ];do
            if [ "$colIdx" -eq "1" ] || [ "$colIdx" -eq "9" ] || [ "$colIdx" -eq "10" ];then
               colVal=`echo ${cols[$colIdx]} | xargs -I {} date -d @{}`   
            elif [ "$colIdx" -eq "4" ] || [ "$colIdx" -eq "6" ] || [ "$colIdx" -eq "8" ];then
               colVal=`echo -e "${cols[$colIdx]}\t"`
            else
               colVal=${cols[$colIdx]}   
            fi
            out+="$colVal | "   
            ((colIdx++))
       done
       echo $out
       ((rowIdx++))
    done

fi
