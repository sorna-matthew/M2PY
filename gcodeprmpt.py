# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 13:33:28 2018

@author: Matthew
"""

import serial
import time

escape = 0;
cmd = ''

#Create and define serial port parameters
ser = serial.Serial('COM7', 115200, timeout = 0)
time.sleep(2) # Make sure to give it enough time to initialize
print("Enter a GCode command. To exit, type \'exit\'")

while escape == 0:
    cmd = input('>> ')
    if cmd == 'exit':
        ser.close();
        print("Serial port disconnected!")
        escape = 1;
    else:
        ser.write(str.encode('{}\r\n'.format(cmd)))
