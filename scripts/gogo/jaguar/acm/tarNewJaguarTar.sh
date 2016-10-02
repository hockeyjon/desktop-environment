#!/bin/bash
cd acm/var/jaguar/configs/active
sha1sum *.json > manifest.txt
cd ~/acm
tar cvzf jaguar.tar.gz var
