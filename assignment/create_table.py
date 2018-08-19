#!/usr/bin/python3

from operate import Database
from time import sleep

stmt1 = 'CREATE TABLE HumAndTemp_data(date CHAR(10), time CHAR(10), hum DECIMAL(5,2), temp DECIMAL(5,2))'
stmt2 = 'CREATE TABLE MAC_add_info(MAC_address CHAR(20),user_name CHAR(20))'
da = Database()
da.create(stmt1)
sleep(5)
da.create(stmt2)
