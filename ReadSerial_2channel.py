# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:36:13 2020

@author: chengjw
"""

import keyboard
import matplotlib.pyplot as plt

plt.ion()
fig=plt.figure()

import serial

ser = serial.Serial('COM21', 9600)
ser.close()
ser.open()

i=0
x=list()
y1=list()
y2=list()
readdata = list()
num_points = 500

while True:
    
    if keyboard.is_pressed("q"):
        print("Exit")
        ser.close()
        break
    
    plt.clf()
    data = ser.readline()
    data_unicode = data.decode()
    print(data_unicode)
    
    data_split = data_unicode.split(';')
    
    x.append(i)
    y1.append(int(data_split[0]))
    y2.append(int(data_split[1].rstrip("\r\n")))
    

    if len(x) < num_points+1:
        plt.xlim(0,(len(x)+1))
        x_plot = x[0:(len(x))]
        y1_plot = y1[0:(len(x))]
        y2_plot = y2[0:(len(x))]
    
    else:
        plt.xlim((len(x)-num_points+1),(len(x)+1))
        x_plot = x[(len(x)-num_points):(len(x))]
        y1_plot = y1[(len(x)-num_points):(len(x))]
        y2_plot = y2[(len(x)-num_points):(len(x))]
    
    
    plt.scatter(x_plot, y1_plot, c = x_plot)
    plt.scatter(x_plot, y2_plot, c = x_plot, cmap = 'inferno')
    plt.xlabel('Time')
    plt.ylabel('AnalogRead')
    

    plt.ylim((min(min(y1_plot), min(y2_plot))*0.5), (max(max(y1_plot), max(y2_plot))*1.5))
    
#    plt.ylim(0, 800)
    
    i += 1
    plt.show()
    plt.pause(0.001)  
    