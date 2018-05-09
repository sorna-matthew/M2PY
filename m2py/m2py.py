# M2PY -- Python library used to control the Makergear M2 Pneumatic Control System [M2PCS]
# Developed in the Architected Materials Laboratory at the University of Pennsylvania
# Author: Matthew Sorna [sorna@seas.upenn.edu]

# Importing of necessary dependent modules
import os
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Module Function Definitions

# Serial communication commands
def mopen(com, baud, printout = 1, fid = os.path.abspath('path_vis_temp.txt')):
    """
	Returns the necessary handle (serial object if printout = 1, or temporary file if printout = 0). If printout = 1, this function will instantiate a serial object used by all subsequent function calls to send serial commands to the specified printer. If printout = 0, this function will store all revelant coordinate changes (move and arc commands) to a temporary file that can then be used to visualize print paths before sending commands to the printer. By default, printout = 1.
    """
    global pflag
    if printout == 1:
        pflag = 1
        handle = serial.Serial(com, baud, timeout = 1)
        time.sleep(2) # Make sure to give it enough time to initialize
        print('Serial port connected')
        for x in range(21): # Reads in all 21 lines of initialization text for the M2
            handle.readline()
        return handle
        
    elif printout == 0:
        global print_dir
        global coord_sys
        print_dir = fid 
        coord_sys = 'abs'
        
        pflag = 0
        handle = open(fid, "w")
        return handle
       
def mclose(handle):
	"""
	Closes the specified handle. If in mopen printout = 1, this function will close the necessary serial object. If prinout = 0, this function will close the specified temporary file and plot a visualization of all relevant movement commands. Visualization function will use whatever coordinate system you explicity designate using coord. If coord isn't explicitly called, the coordinate system used by the visualization tool will be absolute.
	"""
    global pflag
    if pflag == 1:
        print("Serial port disconnected")
        handle.close()
        
    elif pflag == 0:
        global print_dir
        global coord_sys
        handle.close()
        path_vis(fid = print_dir, coord = coord_sys)

def path_vis(fid, coord = 'abs'):
	"""
	Takes the (x, y, z) coordinates generated from mp.mopen(printout = 0), and plots them into a 3D line graph to check a print path before actually sending commands to the Makergear. Visualization function will use whatever coordinate system you explicity designate using coord. If coord isn't explicitly called, the coordinate system used by the visualization tool will be absolute. When using path_vis, the file directory of the path coordinates needs to be explicity set, unlike when it is implictly called inside mclose.
	"""
    coord_array = np.zeros([1, 3])
    
    if coord == 'abs':
        with open(fid, "r") as data:
            for line in data:
                raw = line.split(' ')
                coords = [float(raw[0]), float(raw[1]), float(raw[2])]
                coord_array = np.append(coord_array, [coords[0], coords[1], coords[2]])
        coord_array.shape = (int(len(coord_array)/3), 3)
        
    elif coord == 'rel':
        old_coords = [0,0,0]
        with open(fid, "r") as data:
            for line in data:
                raw = line.split(' ')
                coords = [float(raw[0]), float(raw[1]), float(raw[2])]
                coord_array = np.append(coord_array, [coords[0] + old_coords[0], coords[1] + old_coords[1], coords[2] + old_coords[2]])
                old_coords =  [coords[0] + old_coords[0], coords[1] + old_coords[1], coords[2] + old_coords[2]]
        coord_array.shape = (int(len(coord_array)/3), 3)
    
    x_coord = coord_array[:,0]
    y_coord = coord_array[:,1]
    z_coord = coord_array[:,2]
    
    xmin = np.min(x_coord)
    xmax = np.max(x_coord)
    ymin = np.min(y_coord)
    ymax = np.max(y_coord)
    
    fig = plt.figure()
    ax = fig.gca(projection=Axes3D.name)
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylim3d(ymin, ymax)
    ax.set_zlim3d(0, 203)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.plot(x_coord, y_coord, z_coord, color = 'g', linewidth = 1.0, label = 'Print path visualization')
    ax.legend()
    plt.show()           
        
def prompt(com, baud):
    """
	Allows for quick, native GCode serial communication with the M2, provided that the proper com port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type exit in the IPython console.
    """
    escape = 0;
    cmd = ''
    
    #Create and define serial port parameters
    handle = serial.Serial(com, baud, timeout = 0)
    time.sleep(2) # Make sure to give it enough time to initialize
    print("Enter a GCode command. To exit, type \'exit\'")
    
    handle.write(str.encode('M17\n'))
    
    x = 0
    y = 0
    z = 0
    
    xval = 0
    yval = 0
    zval = 0
    
    while escape == 0:
        cmd = input('>> ')
        if cmd == 'exit':
            handle.close();
            print("Serial port disconnected")
            escape = 1;
        else:
            handle.write(str.encode('{}\n'.format(cmd)))
            
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

def file_read(fid, com, baud):
    """
	Reads in a text file of GCode line by line, and waits for the M2 to acknowledge that it received the command before sending another, maintaining print accuracy.
    """
    #Create and define serial port parameters
    handle = serial.Serial(com, baud, timeout = 100)
    time.sleep(2) # Make sure to give it enough time to initialize
    
    print('Serial port initialized')
    for x in range(21): # Reads in all 21 lines of initalization text for the M2
        handle.readline()
    print('Beginning print')
    with open(fid, "r") as gcode:
        for line in gcode:
            split_line = line.split(';') # chops off comments
            if split_line[0] != '':      # makes sure it's not a comment-only line of GCode
                handle.write(str.encode('{}\n'.format(split_line[0]))) #Reads in text file (GCode) line by line and sends commands to M2
                print(split_line[0])
                read = handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = handle.readline()
                
    print('Print complete!\nSerial port closed')
    handle.close() #Closes serial port

# GCode wrappers

# G0/G1       
def move(handle, x = 0, y = 0, z = 0, track = 1):
	"""
	Moves to the specified point, keeping in mind the coordinate system (relative / absolute)
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('G1 X{} Y{} Z{}\n'.format(x, y, z)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Move to ({}, {}, {})'.format(x, y, z))
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
            
    elif pflag == 0 and track == 1:
        handle.write('{} {} {}\n'.format(x, y, z))


def speed(handle, speed = 30):
	"""
	Sets the movement speed of the printer to the specified speed in [mm/s] (default 30 mm/sec)
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('G1 F{}\n'.format(speed*60)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Changing movement speed to {} mm/s'.format(speed))
    
# G2/G3
def arc(handle, x = 0, y = 0, z = 0, i = 0, j = 0, direction = 'ccw'):
	"""
	Moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as 'cw' or 'ccw' (default 'ccw')
	"""
    global pflag
    if pflag == 1:
        if direction == 'ccw':
            handle.write(str.encode('G3 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
            read = handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
            print('CCW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))
        elif direction == 'cw':
            handle.write(str.encode('G2 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
            read = handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
            print('CW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))
    
    elif pflag == 0:
        handle.write('{} {} {}\n'.format(x, y, z))
        
# G4
def wait(handle, seconds = 0):
	"""
	Waits for the specified amount of time (default 0 seconds)
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('G4 S{}\n'.format(seconds)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
        print('Waiting for {} seconds'.format(seconds))

# G28
def home(handle, axes = 'X Y Z'):
	"""
	Homes the specified axes (default 'X Y Z')
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('G28 {}\n'.format(axes)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
        print('{} axes homed'.format(axes))
        
# G90/G91
def coord(handle, coord = 'abs'):
	"""
	Sets the coordinate system of the printer [relative or absolute] (default 'abs')
	"""
    global coord_sys
    coord_sys = coord
    
    global pflag
    if pflag == 1:
        if coord == 'abs':
            handle.write(str.encode('G90\n'))
            read = handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
            print('Set to absolute coordinates')
            
        elif coord == 'rel':
            handle.write(str.encode('G91\n'))
            read = handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = handle.readline()
                time.sleep(0.06)
            print('Set to relative coordinates')  

# G92       
def set_coords(handle, x = 0, y = 0, z = 0):
	"""
	Sets the current position to the specified (x, y, z) point (keeping in mind the current coordinate system)
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('G92 X{} Y{} Z{}\n'.format(x, y, z)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Changed current position to ({}, {}, {})'.format(x, y, z))        

# CORE SHELL SPECIFIC FUNCTIONS
def allon(handle):
	"""
	Turns pneumatic CHANNEL 1, 2, 3 ON
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M3\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        handle.write(str.encode('M5\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        handle.write(str.encode('M7\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('All Channels ON')

def alloff(handle):
	"""
	Turns pneumatic CHANNEL 1, 2, 3 OFF
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M4\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        handle.write(str.encode('M6\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        handle.write(str.encode('M8\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('All Channels OFF') 

# M3    
def ch1on(handle):
	"""
	Turns pneumatic CHANNEL 1 ON
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M3\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 1 ON')

# M4
def ch1off(handle):
	"""
	Turns pneumatic CHANNEL 1 OFF
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M4\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 1 OFF')

# M5    
def ch2on(handle):
	"""
	Turns pneumatic CHANNEL 2 ON
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M5\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 2 ON')

# M6
def ch2off(handle):
	"""
	Turns pneumatic CHANNEL 2 OFF
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M6\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 2 OFF')

# M7
def ch3on(handle):
	"""
	Turns pneumatic CHANNEL 3 ON
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M7\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 3 ON')

# M8
def ch3off(handle):
	"""
	Turns pneumatic CHANNEL 3 OFF
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M8\n'))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel 3 OFF')
    
def delay_set(handle, delay = 50):
	"""
	Sets the delay time (in ms) between a channel turning on and the execution of another command. Can be used to fine tune under extrusion effects, depending on ink viscosity.
	"""
    global pflag
    if pflag == 1:
        handle.write(str.encode('M50 S{}\n'.format(delay)))
        read = handle.readline()
        while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
            read = handle.readline()
            time.sleep(0.06)
        print('Channel ON delay time changed to {} ms'.format(delay))

def clip(handle, clip_height = 1, radius = 0.5):
	"""
	This subroutine automatically turns off all channels, and performs a quick arc/z-translation to shear excess material away from nozzle before continuing with print path.
	"""
    global pflag
    if pflag == 1:
        alloff(handle)
        arc(handle, z = clip_height, i = radius)
        print('Print clipped')

def change_tool(handle, dx = 0, dy = 0, change_height = 10):
	"""
	This subroutine automatically turns off all channels, and performs a predetermined z translation of z = change_height, and then moves (x,y) = (dx, dy) to allow for change between multiple nozzles. It also automatically lowers back to the z height it was at previously, continuing printing after switching active tools
	"""
    global pflag
    if pflag == 1:
        alloff(handle)
        move(handle, z = change_height)
        move(handle, x = dx, y = dy)
        move(handle, z = -change_height)
        print('Tool change to ({}, {})'.format(dx, dy))