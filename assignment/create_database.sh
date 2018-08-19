#!/bin/bash

DATABASE="HumAndTemps_DB"
RESULT=`sudo mysqlshow --user=root --password=|grep -c $DATABASE`

if [ $RESULT -gt 0 ]; then
echo This database has already exist
else
sudo mysql --user=root --password=  <<EOF
  create database $DATABASE;
EOF
echo Create successfully!
fi

