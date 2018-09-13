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

class Makergear:
    def __init__(self, com, baud, printout = 1):
        self.com = com
        self.baud = baud
        self.printout = printout
        self.fid = os.path.abspath('path_vis_temp.txt')

        if self.printout == 1:
            self.handle = serial.Serial(com, baud, timeout = 1)
            time.sleep(2) # Make sure to give it enough time to initialize
            print('Serial port connected')
            for _ in range(21): # Reads in all 21 lines of initialization text for the M2
                self.handle.readline()
        elif self.printout == 0:
            self.coord_sys = 'abs'
            self.handle = open(self.fid, "w")

    def close(self):
        """
        Closes the specified handle. If self.printout = 1, this function will close the necessary serial object. If prinout = 0, this function will close the specified temporary file and plot a visualization of all relevant movement commands. Visualization function will use whatever coordinate system you explicity designate using coord. If coord isn't explicitly called, the coordinate system used by the visualization tool will be absolute.
        """
        if self.printout == 1:
            print("Serial port disconnected")
            self.handle.close()
        elif self.printout == 0:
            self.handle.close()
            self.path_vis()

    def path_vis(self):
        """
        Takes the (x, y, z) coordinates generated from mp.mopen(printout = 0), and plots them into a 3D line graph to check a print path before actually sending commands to the Makergear. Visualization function will use whatever coordinate system you explicity designate using coord. If coord isn't explicitly called, the coordinate system used by the visualization tool will be absolute. When using path_vis, the file directory of the path coordinates needs to be explicity set, unlike when it is implictly called inside mclose.
        """
        coord_array = np.zeros([1, 3])

        if self.coord_sys == 'abs':
            with open(self.fid, "r") as data:
                for line in data:
                    raw = line.split(' ')
                    coords = [float(raw[0]), float(raw[1]), float(raw[2])]
                    coord_array = np.append(coord_array, [coords[0], coords[1], coords[2]])
            coord_array.shape = (int(len(coord_array)/3), 3)

        elif self.coord_sys == 'rel':
            old_coords = [0,0,0]
            with open(self.fid, "r") as data:
                for line in data:
                    raw = line.split(' ')
                    coords = [float(raw[0]), float(raw[1]), float(raw[2])]
                    coord_array = np.append(coord_array, [coords[0] + old_coords[0], coords[1] + old_coords[1], coords[2] + old_coords[2]])
                    old_coords =  [coords[0] + old_coords[0], coords[1] + old_coords[1], coords[2] + old_coords[2]]
            coord_array.shape = (int(len(coord_array)/3), 3)

        x_coord = coord_array[:,0]
        y_coord = coord_array[:,1]
        z_coord = coord_array[:,2]

        fig = plt.figure()
        ax = fig.gca(projection=Axes3D.name)
        ax.set_title('M2PCS Print Visualization')
        ax.set_xlim3d(0, 205)
        ax.set_ylim3d(0, 255)
        ax.set_zlim3d(0, 205)
        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Y [mm]')
        ax.set_zlabel('Z [mm]')
        ax.plot(x_coord, y_coord, z_coord, color = 'g', linewidth = 1.0, label = 'toolhead')
        ax.legend()
        plt.show()

    # GCode wrappers
    # G0/G1
    def move(self, x = 0, y = 0, z = 0, track = 1):
        """
        Moves to the specified point, keeping in mind the coordinate system (relative / absolute)
        """
        if self.printout == 1:
            self.handle.write(str.encode('G1 X{} Y{} Z{}\n'.format(x, y, z)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Move to ({}, {}, {})'.format(x, y, z))
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)

        elif self.printout == 0 and track == 1:
            self.handle.write('{} {} {}\n'.format(x, y, z))


    def speed(self, speed = 30):
        """
        Sets the movement speed of the printer to the specified speed in [mm/s] (default 30 mm/sec)
        """
        if self.printout == 1:
            self.handle.write(str.encode('G1 F{}\n'.format(speed*60)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Changing movement speed to {} mm/s'.format(speed))

    def rotate(self, speed = 20):
            """
            Sets the rotation speed of the motor to the specified speed [0-127] (default 20)
            """
            if self.printout == 1:
                self.handle.write(str.encode('M9 S{}\n'.format(int(speed))))
                read = self.handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
                print('Changing rotation speed to {}'.format(int(speed)))

    # G2/G3
    def arc(self, x = 0, y = 0, z = 0, i = 0, j = 0, direction = 'ccw'):
        """
        Moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as 'cw' or 'ccw' (default 'ccw')
        """
        if self.printout == 1:
            if direction == 'ccw':
                self.handle.write(str.encode('G3 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
                read = self.handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
                print('CCW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))
            elif direction == 'cw':
                self.handle.write(str.encode('G2 X{} Y{} Z{} I{} J{}\n'.format(x, y, z, i, j)))
                read = self.handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
                print('CW arc to ({}, {}, {}), center at ({}, {})'.format(x, y, z, i, j))

        elif self.printout == 0:
            self.handle.write('{} {} {}\n'.format(x, y, z))

    # G4
    def wait(self, seconds = 0):
        """
        Waits for the specified amount of time (default 0 seconds)
        """
        if self.printout == 1:
            self.handle.write(str.encode('G4 S{}\n'.format(seconds)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
            print('Waiting for {} seconds'.format(seconds))

    # G28
    def home(self, axes = 'X Y Z'):
        """
        Homes the specified axes (default 'X Y Z')
        """
        if self.printout == 1:
            self.handle.write(str.encode('G28 {}\n'.format(axes)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
            print('{} axes homed'.format(axes))

    # G90/G91
    def coord(self, coord_sys = 'abs'):
        """
        Sets the coordinate system of the printer [relative or absolute] (default 'abs')
        """
        self.coord_sys = coord_sys

        if self.printout == 1:
            if self.coord_sys == 'abs':
                self.handle.write(str.encode('G90\n'))
                read = self.handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
                print('Set to absolute coordinates')

            elif self.coord_sys == 'rel':
                self.handle.write(str.encode('G91\n'))
                read = self.handle.readline()
                while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                    read = self.handle.readline()
                    time.sleep(0.06)
                print('Set to relative coordinates')

    # G92
    def set_coords(self, x = 0, y = 0, z = 0):
        """
        Sets the current position to the specified (x, y, z) point (keeping in mind the current coordinate system)
        """
        if self.printout == 1:
            self.handle.write(str.encode('G92 X{} Y{} Z{}\n'.format(x, y, z)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Changed current position to ({}, {}, {})'.format(x, y, z))

    # CORE SHELL SPECIFIC FUNCTIONS
    def allon(self):
        """
        Turns pneumatic CHANNEL 1, 2, 3 ON
        """
        if self.prinout == 1:
            self.handle.write(str.encode('M3\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            self.handle.write(str.encode('M5\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            self.handle.write(str.encode('M7\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('All Channels ON')

    def alloff(self):
        """
        Turns pneumatic CHANNEL 1, 2, 3 OFF
        """
        if self.printout == 1:
            self.handle.write(str.encode('M4\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            self.handle.write(str.encode('M6\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            self.handle.write(str.encode('M8\n'))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('All Channels OFF')

    # M3/M5/M7
    def on(self, channel):
        """
        Turns pneumatic CHANNEL ON
        """
        if self.printout == 1:
            if channel == 1:
                schannel = 'M3\n'
            elif channel == 2:
                schannel = 'M5\n'
            elif channel == 3:
                schannel = 'M7\n'
            self.handle.write(str.encode(schannel))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Channel {} ON'.format(channel))

    # M4/M6/M8
    def off(self, channel):
        """
        Turns pneumatic CHANNEL OFF
        """
        if self.printout == 1:
            if channel == 1:
                schannel = 'M4\n'
            elif channel == 2:
                schannel = 'M6\n'
            elif channel == 3:
                schannel = 'M8\n'
            self.handle.write(str.encode(schannel))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Channel {} OFF'.format(channel))

    def delay_set(self, delay = 50):
        """
        Sets the delay time (in ms) between a channel turning on and the execution of another command. Can be used to fine tune under extrusion effects, depending on ink viscosity.
        """
        if self.printout == 1:
            self.handle.write(str.encode('M50 S{}\n'.format(delay)))
            read = self.handle.readline()
            while read[0:2] != b'ok': #Waits for printer to send 'ok' command before sending the next command, ensuring print accuracy
                read = self.handle.readline()
                time.sleep(0.06)
            print('Channel ON delay time changed to {} ms'.format(delay))

    def clip(self, clip_height = 1, radius = 0.5):
        """
        This subroutine automatically turns off all channels, and performs a quick arc/z-translation to shear excess material away from nozzle before continuing with print path.
        """
        if self.printout == 1:
            self.alloff(self.handle)
            self.arc(self.handle, z = clip_height, i = radius)
            print('Print clipped')

    def change_tool(self, dx = 0, dy = 0, change_height = 10):
        """
        This subroutine automatically turns off all channels, and performs a predetermined z translation of z = change_height, and then moves (x,y) = (dx, dy) to allow for change between multiple nozzles. It also automatically lowers back to the z height it was at previously, continuing printing after switching active tools
        """
        if self.printout == 1:
            self.alloff()
            self.move(z = change_height)
            self.move(x = dx, y = dy)
            self.move(z = -change_height)
            print('Tool change to ({}, {})'.format(dx, dy))

#Additional functions outside of the M2 CLASS
def prompt(com, baud):
    """
    Allows for quick, native GCode serial communication with the M2, provided that the proper com port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type exit in the IPython console.
    """
    escape = 0
    cmd = ''
    #Create and define serial port parameters
    handle = serial.Serial(com, baud, timeout = 0)
    time.sleep(2) # Make sure to give it enough time to initialize
    print("Enter a GCode command. To exit, type \'exit\'")
    handle.write(str.encode('M17\n'))
    x = y = z = 0
    xval = yval = zval = 0
    while escape == 0:
        cmd = input('>> ')
        if cmd == 'exit':
            handle.close()
            print("Serial port disconnected")
            escape = 1
        else:
            handle.write(str.encode('{}\n'.format(cmd)))
            if cmd =='G28':
                x = y = z = 0
                xval = yval = zval = 0
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
    for _ in range(21): # Reads in all 21 lines of initalization text for the M2
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