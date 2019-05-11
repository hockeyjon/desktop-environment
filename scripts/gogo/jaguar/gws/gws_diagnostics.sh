#! /bin/bash

function print_key_value() {
    val=`cat $1 | jq ".[]| .${2}"`
    printf "  \"%s\": %s\n" "$2" "$val" >> ${logger}
}

tstamp=`date +%m-%d_%H:%M:%S`
logger="${tstamp}.gwsdiagnostics.$1.log"
printf "Snapshot on %s\n" "`date`" > ${logger}
printf "TESTSTEP: %s\n" "$1" >> ${logger}

printf "Contents of /var/jaguar/bsg:\n" >> ${logger}
bsg_profiles=(/var/jaguar/bsg/lru*)
for profile in "${bsg_profiles[@]}"; do
   printf "%s\n" "`ls -l ${profile}`" >> ${logger}
   print_key_value ${profile} "service.gws.active"
   print_key_value ${profile} "service.gws.partnerID"
   print_key_value ${profile} "service.gws.auth_url"
   print_key_value ${profile} "app.wsi.parameters.C1"
   print_key_value ${profile} "app.wsi.active"
   printf "\n" >> ${logger}
done


printf "Profile settings currently running:\n" >> ${logger}
printf "    \"service.gws.active\": " >> ${logger}
jag config lru -k service.gws.active >> ${logger}
printf "    \"service.gws.partnerID\": " >> ${logger}
jag config lru -k service.gws.partnerID >> ${logger}
printf "    \"service.gws.auth_url\": " >> ${logger}
jag config lru -k service.gws.auth_url >> ${logger}
printf "    \"app.wsi.parameters.C1\": " >> ${logger}
jag config lru -k app.wsi.parameters.C1 >> ${logger}
printf "    \"app.wsi.active\": " >> ${logger}
jag config lru -k app.wsi.active >> ${logger}


jctl_cmd='journalctl -u ground-service --since "10 minutes ago"'
printf "\n%s\n" "$jctl_cmd" >> ${logger}
journalctl -u ground-service --since "10 minutes ago" >> ${logger}
