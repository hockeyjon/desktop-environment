#!/bin/bash

sqlite3 /var/acctd/cache.sqlite "SELECT * FROM record_cache;" 
