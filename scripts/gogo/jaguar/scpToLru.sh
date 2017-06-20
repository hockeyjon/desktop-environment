#!/usr/bin/env bash

echo "cd ~/git/myWorkspace"
cd ~/git/myWorkspace
echo "git pull"
git pull
echo "tar cvzf scripts.tar.gz scripts"
tar cvzf scripts.tar.gz scripts
echo "docker cp scripts.tar.gz maint-cli:/tmp/."
docker cp scripts.tar.gz maint-gui:/tmp/.
echo "docker exec -it maint-gui scp /tmp/scripts.tar.gz gogo-maint@172.20.1.1:."
docker exec -it maint-gui scp /tmp/scripts.tar.gz gogo-maint@172.20.1.1:.
