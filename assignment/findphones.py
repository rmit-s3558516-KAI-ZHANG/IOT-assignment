#!/usr/bin/env python3

import bluetooth
import os
import time
from sense_hat import SenseHat
from operate import Database

#instantiate class Database
da = Database()
da.params = None
stmt = 'INSERT INTO MAC_add_info VALUES(%s, %s)'
message = 'Address: %s, Name: %s'

#instantiate SenseHat
sense = SenseHat()

#descover the devices nearby
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Currently: {}".format(da.t))

if len(nearby_devices) > 0:
    print("found %d devices" % len(nearby_devices))
    #insert the Mac Address and name into database
    for addr, name in nearby_devices:
        da.params = (addr, name)
        da.insert(stmt, message)
        #send the notification
        temp = da.temp_calibrated
        sense = SenseHat()
        if temp < 20:
            sense.show_message("Hi, %s! Current Temp is %.2f*C, please wear warmly!"%(name, temp), scroll_speed=0.1)
        elif temp > 35:
            sense.show_message("Hi, %s! Current Temp is %.2f*C, you need ice cream!"%(name, temp), scroll_speed=0.1)
        else:
            sense.show_message("Hi, %s! Current Temp is %.2f*C, please wear warmly!"%(name, temp), scroll_speed=0.1)
else:
    print("No devices found!")
    sense.show_message("No device found")
