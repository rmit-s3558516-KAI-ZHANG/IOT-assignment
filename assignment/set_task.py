#!/usr/bin/python3

from operate import Database
from crontab import CronTab

da = Database()
cron = CronTab(user='root')

#main menu, chose the the task you want to set
print("1. set recording data CronTab Job")
print("2. set show data CronTab Job")
print("3. remove all jobs")

opt = int(input("Please enter the option: "))
#recording the humidity and the temperature to the database and send the notification
#if necessary
if opt == 1:
    set_time = int(input("Please enter the time interval(uints:minute): "))
    job = cron.new(command='/home/pi/IOT_assighment/job1.py')
    job.minute.every(set_time)
    cron.write()
#display the data from HumAndTemp_data periodically
if opt == 2:
    set_time = int(input("Please enter the time interval(uints:minute): "))
    job = cron.new(coimmand='/home/pi/IOT_assighment/job2.py')
    job.minute.every(set_time)
    cron.write()
#remove all the crontab task
if opt == 3:
    cron.remove_all()
    cron.write()
