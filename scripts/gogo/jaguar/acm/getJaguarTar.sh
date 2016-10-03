#!/bin/bash
cd acm
rm -rf *
wget ftp://192.168.1.250/jaguar.tar.gz
tar xvzf jaguar.tar.gz
echo "cd acm/var/jaguar/configs/active"
