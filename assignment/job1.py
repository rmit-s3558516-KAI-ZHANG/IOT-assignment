#!/usr/bin/python3

import requests
import json
import os
from operate import Database
from sense_hat import SenseHat
from time import sleep

#insert the temperature and humidity into database
sense = SenseHat()
da = Database()
stmt = "INSERT INTO HumAndTemp_data(date,time,hum,temp) VALUES(%s,%s,%s,%s)"
message = "Date: %s, Time: %s, Hum: %.2f, Temp: %.2f C"
da.insert(stmt,message)

temp = da.temp_calibrated
ip_add = os.popen('hostname -I').read()

ACCESS_TOKEN = "o.rwal3V6n3tIxUCMsQ8DVhTef2ulsb0DQ"

#used for sending the notification
def send_notification(title,body):
    data_send = {"type": "note", "title": title, "body": body}
    res = requests.post('https://api.pushbullet.com/v2/pushes',
            data = json.dumps(data_send), headers={'Authorization': 'Bearer '+ ACCESS_TOKEN,
            'Content-Type': 'application/json'})
    if res.status_code != 200:
        sense.show_message("Sending failed!")
        raise Exception('Sending failed!')
    else:
        print('Complete sending!')
        sense.show_message("Complete sending!")

#judge whether the notification shold be sent or which notification should be sent
def monitor_temp():
    if temp < 20:
        send_notification(ip_add, "the temperature is low, please bring a sweater! >_< \nFrom Raspberry Pi")
        for i in range(3):
            sense.low_light = True
            sleep(1)
            sense.show_message("COLD!",text_colour=[0,255,0],back_colour=[255,255,255],scroll_speed=0.5)
            sleep(1)
            sense.low_light = False
            sleep(1)
        sense.clear()
    elif temp > 35:
        send_notification(ip_add, "the temperature is high, you need ice cream! ^_^ \nFrom Raspberry Pi")
        for i in range(3):
            sense.low_light = True
            sleep(1)
            sense.show_message("HOT!!",text_colour=[255,0,0],back_colour=[255,255,255],scroll_speed=0.5)
            sleep(1)
            sense.low_light = False
            sleep(1)
        sense.clear()

#execute monitor_temp
monitor_temp()
