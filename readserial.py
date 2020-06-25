# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:41:39 2020

@author: chengjw
"""

import serial

ser = serial.Serial('COM9', 57600)

while(1):
    line = ser.readline()
    decoded = float(line[0:len(line)-1].decode("utf-8"))
    print(decoded)

ser.close()