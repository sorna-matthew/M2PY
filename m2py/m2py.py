# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:59:06 2018

@author: Matthew Sorna
"""

# Importing of necessary dependent modules
import serial
import time

# Module Function Definitions

# Serial communication commands
def mopen(com, baud):
    ser = serial.Serial(com, baud, timeout = 0)
    time.sleep(2) # Make sure to give it enough time to initialize
    print('Serial port connected')
    for x in range(21): # Reads in all 21 lines of initialization text for the M2
        ser.readline()
    return ser
    
def mclose(ser):
    print("Serial port disconnected")
    ser.close()
    
def prompt(com, baud):
    """
    Creates a serial connection with the printer found at the specified com and at the given baud, and allows for GCode commands to be sent
    """
    escape = 0;
    cmd = ''
    
    #Create and define serial port parameters
    ser = serial.Serial(com, baud, timeout = 0)
    time.sleep(2) # Make sure to give it enough time to initialize
    print("Enter a GCode command. To exit, type \'exit\'")
    
    while escape == 0:
        cmd = input('>> ')
        if cmd == 'exit':
            ser.close();
            print("Serial port disconnected")
            escape = 1;
        else:
            ser.write(str.encode('{}\r\n'.format(cmd)))

def fileread(fid, com, baud):
    """
    Reads in and sends an entire GCode txt file to the specified printer at the given baud 
    """
    #Create and define serial port parameters
    ser = serial.Serial(com, baud, timeout = 100)
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

# GCode wrappers

# G0/G1        
def move(ser, x = 0, y = 0, z = 0):
    ser.write(str.encode('G1 X{} Y{} Z{}\r\n'.format(x, y, z)))
    print('Move to ({}, {}, {})'.format(x, y, z))

def speed(ser, speed):
    ser.write(str.encode('G1 F{}\r\n'.format(speed*60)))
    print('Changing movement speed to {} mm/s'.format(speed))
    
# G2/G3
def arc(ser, x = 0, y = 0, i = 0, j = 0, direction = 'ccw'):
    if direction == 'ccw':
        ser.write(str.encode('G3 X{} Y{} I{} J{}\r\n'.format(x, y, i, j)))
        print('CCW arc to ({}, {}), center at ({}, {})'.format(x, y, i, j))
    elif direction == 'cw':
        ser.write(str.encode('G2 X{} Y{} I{} J{}\r\n'.format(x, y, i, j)))
        print('CW arc to ({}, {}), center at ({}, {})'.format(x, y, i, j))
        
# G4
def wait(ser, seconds):
    ser.write(str.encode('G4 S{}\r\n'.format(seconds)))
    print('Waiting for {} seconds'.format(seconds))

# G28
def home(ser, axes = 'X Y Z'):
    ser.write(str.encode('G28 {}\r\n'.format(axes)))
    print('{} axes homed'.format(axes))
        
# G90/G91
def coord(ser, coord = 'abs'):
    if coord == 'abs':
        ser.write(str.encode('G90\r\n'))
        print('Set to absolute coordinates')
        
    elif coord == 'rel':
        ser.write(str.encode('G91\r\n'))
        print('Set to relative coordinates')    