#!/usr/bin/python3

import MySQLdb
import datetime
import os
import re
from sense_hat import SenseHat

class Database:
    #create a SenseHat object
    sense = SenseHat()
    #invoke get_humidity() method to get the humidity
    hum = sense.get_humidity()
    #invoke get_temperature() method to get the temperature
    temp = sense.get_temperature()
    #using shell command to get the cpu temperature, and calculate the correct
    #temperature by using the formula
    result = '/opt/vc/bin/vcgencmd measure_temp'
    cpu_temp_str = os.popen(result).read()
    cpu_temp = float(re.search("\d+(\.\d+)?",cpu_temp_str).group())
    temp_calibrated = temp -((cpu_temp-temp)/1.5)
    #get the date and time and format them
    d = datetime.datetime.now().strftime("%Y-%m-%d")
    t = (datetime.datetime.now()+datetime.timedelta(hours=10)).strftime("%H:%M:%S")
    #this parameters is used for preventing SQL injection
    params = (d,t,hum,temp_calibrated)

    #__init__ method
    def __init__(self,con_host='localhost',user='root',password='',db='HumAndTemps_DB'):
        self.con_host = con_host
        self.user = user
        self.password = password
        self.db = db
        self.con = MySQLdb.connect(self.con_host,self.user,self.password,self.db)
        self.cur = self.con.cursor()

    #create table method which is used for creating a database named 'HumAndTemp_data'
    def create(self,stmt):
        try:
            self.cur.execute(stmt)
            self.con.commit()
            print("Talbe create successfully!")
            self.sense.show_message("Table create successfully!", scroll_speed=0.1)
        except:
            print("ERROR: This table is already exist, the database is being rolled back!")
            self.sense.show_message("Create table failed!", scroll_speed=0.1)
            self.con.rollback()

    #insert the value into the database by using parameters avoiding SQL injection
    def insert(self,stmt,message):
        try:
            self.cur.execute(stmt,self.params)
            self.con.commit()
            print("Insert successfully!")
            self.sense.show_message(message%(self.params), scroll_speed=0.05)
        except:
            print("ERROR: Insert failed, the database is being rolled back!")
            self.sense.show_message("Insert failed!", scroll_speed=0.1)
            self.con.rollback()

    #read all of the data from database
    def read(self):
        try:
            self.cur.execute("SELECT * FROM HumAndTemp_data")
            print("\nDate       Time         Humidity    Temperature")
            print("======================================================")
            for reading in self.cur.fetchall():
                print(str(reading[0])+" "+str(reading[1])+"     "+str(reading[2])+"       "+str(reading[3]))
        except:
            print("ERROR: read data failed!")
