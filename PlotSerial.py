import keyboard
import matplotlib.pyplot as plt

plt.ion()
fig=plt.figure()

import serial

ser = serial.Serial('COM11', 57600)
ser.close()
ser.open()

i=0
x=list()
y=list()
readdata = list()
num_points = 100

while True:
    
    if keyboard.is_pressed("q"):
        print("Exit")
        ser.close()
        break
    
    plt.clf()
    data = ser.readline()
    data_unicode = data.decode()
    print(data_unicode)
    
    nums = [int(i) for i in data_unicode.split() if i.isdigit()]
    
    x.append(i)
    y.append(nums[0])
    

    if len(x) < num_points+1:
        plt.xlim(0,(len(x)+1))
        x_plot = x[0:(len(x))]
        y_plot = y[0:(len(x))]
    
    else:
        plt.xlim((len(x)-num_points+1),(len(x)+1))
        x_plot = x[(len(x)-num_points):(len(x))]
        y_plot = y[(len(x)-num_points):(len(x))]
    
    
    plt.scatter(x_plot, y_plot, c = x_plot)
    plt.xlabel('Time')
    plt.ylabel('AnalogRead')
    

    plt.ylim((min(y_plot)*0.9), (max(y_plot)*1.1))
    
    i += 1
    plt.show()
    plt.pause(0.001)  
    