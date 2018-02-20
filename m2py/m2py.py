# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:59:06 2018

@author: Matthew Sorna
"""

# Importing of necessary dependent modules
import serial
import time

def prompt(COM, BAUD):
    """
    Creates a serial connection with the printer found at the specified COM and at the given BAUD, and allows for GCode commands to be sent
    """
    escape = 0;
    cmd = ''
    
    #Create and define serial port parameters
    ser = serial.Serial(COM, BAUD, timeout = 0)
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

def fread(fid, COM, BAUD):
    """
    Reads in and sends an entire GCode txt file to the specified printer at the given BAUD 
    """
    #Create and define serial port parameters
    ser = serial.Serial(COM, BAUD, timeout = 100)
    time.sleep(2) # Make sure to give it enough time to initialize
    
    print('Serial port initialized')
    for x in range(21): # Reads in all 21 lines of initalization text for the M2
        ser.readline()
    print('Beginning print')
    with open(fid, "r") as gcode:
        for line in gcode:
            ser.write(str.encode('{}\r\n'.format(line))) #Reads in text file (GCode) line by line and sends commands to M2
            read = b''
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = ser.readline()
                
    print('Print complete!\nSerial port closed')
    ser.close() #Closes serial port