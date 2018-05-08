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
    ser = serial.Serial(com, baud, timeout = 1)
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
    
    ser.write(str.encode('M17\n'))
    
    x = 0
    y = 0
    z = 0
    
    xval = 0
    yval = 0
    zval = 0
    
    while escape == 0:
        cmd = input('>> ')
        if cmd == 'exit':
            ser.close();
            print("Serial port disconnected")
            escape = 1;
        else:
            ser.write(str.encode('{}\n'.format(cmd)))
            
            if cmd =='G28':
                x = 0
                y = 0
                z = 0
                
                xval = 0
                yval = 0
                zval = 0
            
            cmd_split = cmd.split(' ')
            
            for a in cmd_split:
                xchar = a.split('X')
                ychar = a.split('Y')
                zchar = a.split('Z')
                if xchar[0] == '' and len(xchar) > 1 and xchar[1] != '':
                    xval = float(xchar[1])
                    x = x + xval
                if ychar[0] == '' and len(ychar) > 1 and ychar[1] != '':
                    yval = float(ychar[1])
                    y = y + yval
                if zchar[0] == '' and len(zchar) > 1 and zchar[1] != '':
                    zval = float(zchar[1])
                    z = z + zval
            print('Currently at ({}, {}, {})'.format(x, y, z))

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
            ser.write(str.encode('{}\n'.format(line))) #Reads in text file (GCode) line by line and sends commands to M2
            read = ser.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = ser.readline()
                
    print('Print complete!\nSerial port closed')
    ser.close() #Closes serial port

# GCode wrappers

# G0/G1
#global move_count
#move_count = 0
        
def move(ser, x = 0, y = 0, z = 0):
    ser.write(str.encode('G1 X{} Y{} Z{}\n'.format(x, y, z)))
    read = ser.readline()
#    global move_count
#    move_count = move_count + 1;
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Move to ({}, {}, {})'.format(x, y, z))
#    if move_count > 20:
#        ser.write(str.encode('M400\n')) # Added buffer pacing command to let in chunks of code in groups of 20 lines at a time
#        read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
#        move_count = 0;

def speed(ser, speed = 30):
    ser.write(str.encode('G1 F{}\n'.format(speed*60)))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Changing movement speed to {} mm/s'.format(speed))
    
# G2/G3
def arc(ser, x = 0, y = 0, z = 0, i = 0, j = 0, direction = 'ccw'):
    if direction == 'ccw':
        ser.write(str.encode('G3 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
        read = ser.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
        print('CCW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))
    elif direction == 'cw':
        ser.write(str.encode('G2 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
        read = ser.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
        print('CW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))
        
# G4
def wait(ser, seconds = 0):
    ser.write(str.encode('G4 S{}\n'.format(seconds)))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
    print('Waiting for {} seconds'.format(seconds))

# G28
def home(ser, axes = 'X Y Z'):
    ser.write(str.encode('G28 {}\n'.format(axes)))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
    print('{} axes homed'.format(axes))
        
# G90/G91
def coord(ser, coord = 'abs'):
    if coord == 'abs':
        ser.write(str.encode('G90\n'))
        read = ser.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
        print('Set to absolute coordinates')
        
    elif coord == 'rel':
        ser.write(str.encode('G91\n'))
        read = ser.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = ser.readline()
            time.sleep(0.06)
        print('Set to relative coordinates')  

# G92       
def set_coords(ser, x = 0, y = 0, z = 0):
    ser.write(str.encode('G92 X{} Y{} Z{}\n'.format(x, y, z)))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Changed current position to ({}, {}, {})'.format(x, y, z))        

# CORE SHELL SPECIFIC FUNCTIONS

def allon(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M3\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    ser.write(str.encode('M5\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    ser.write(str.encode('M7\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('All Channels ON')

def alloff(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M4\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    ser.write(str.encode('M6\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    ser.write(str.encode('M8\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('All Channels OFF') 

# M3    
def ch1on(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M3\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 1 ON')

# M4
def ch1off(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M4\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 1 OFF')

# M5    
def ch2on(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M5\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 2 ON')

# M6
def ch2off(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M6\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 2 OFF')

# M7
def ch3on(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M7\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 3 ON')

# M8
def ch3off(ser):
#    global move_count
#    move_count = 0
    ser.write(str.encode('M8\n'))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel 3 OFF')
    
def delay_set(ser, delay = 50):
    ser.write(str.encode('M50 S{}\n'.format(delay)))
    read = ser.readline()
    while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
        read = ser.readline()
        time.sleep(0.06)
    print('Channel ON delay time changed to {} ms'.format(delay))

def clip(ser, clip_height = 1, radius = 0.5):
    alloff(ser)
    arc(ser, z = clip_height, i = radius)
    print('Print clipped')

def change_tool(ser, dx = 0, dy = 0, change_height = 10):
    alloff(ser)
    move(ser, z = change_height)
    move(ser, x = dx, y = dy)
    move(ser, z = -change_height)
    print('Tool change to ({}, {})'.format(dx, dy))