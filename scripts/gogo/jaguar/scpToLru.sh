#!/usr/bin/env bash

cd ~/git/myWorkspace
git pull
tar cvzf scripts.tar.gz scripts
docker cp scripts.tar.gz maint-cli:/tmp/.
docker exec -it maint-cli scp /tmp/scripts.tar.gz root@172.20.1.1:.