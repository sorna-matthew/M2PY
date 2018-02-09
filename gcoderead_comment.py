# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:28:34 2018

@author: Matthew Sorna
"""

import serial
import time

fd = 'C:/Users/lab/Desktop/Users/Matt/m2-python/trunk/comment_test.txt'

#Create and define serial port parameters

ser = serial.Serial('COM7', 115200, timeout = 100)
nordson = serial.Serial('COM5', 115200)
time.sleep(2) # Make sure to give it enough time to initialize

print('Serial port initialized')
for x in range(21): # Reads in all 21 lines of initalization text for the M2
    init = ser.readline()
    #print(init)
print('Beginning print')
with open(fd, "r") as gcode:
    for line in gcode:
        if line[0:1] == '$':
            brk = line.split('$')
            cmd = brk[1]
            if cmd == 'NT':
                nordson.write(b'\x02\x30\x38\x44\x49\x30\x42\x03') #If the command after the $ escape character is NT, toggle the nordson pressure regulator
        else:
            ser.write(str.encode('{}\r\n'.format(line))) #Reads in text file (GCode) line by line and sends commands to M2
            read = b''
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = ser.readline()
            
print('Print complete!\nSerial port closed')
ser.close() #Closes serial port