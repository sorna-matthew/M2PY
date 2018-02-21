# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:58:33 2018

@author: Matthew Sorna
"""
import numpy as np
import math

speed = 2400 #mm/min
total = 0

cmds = np.loadtxt('C:/Users/lab/Desktop/Users/Matt/m2-python/trunk/Bistable_Sorna_gcode.txt', dtype = str, delimiter = '\n')
f = open('C:/Users/lab/Desktop/Users/Matt/m2-python/trunk/timing_test2.txt', 'w')

for lines in np.nditer(cmds):
    
    d1 = 0;
    d2 = 0;
    d3 = 0;
    length = 0;
    
    
    splitcmd = np.array_str(lines).split( )
    
    if splitcmd[0] == 'G1':
        if splitcmd[1][0] == 'X':
            d1 = float(splitcmd[1].split('X')[1])
        if splitcmd[1][0] == 'Y':
            d2 = float(splitcmd[1].split('Y')[1])
        if splitcmd[1][0] == 'Z':
            d3 = float(splitcmd[1].split('Z')[1])
        dim = len(splitcmd) - 1
        if dim >= 2:
            if splitcmd[2][0] == 'X':
                d1 = float(splitcmd[2].split('X')[1])
            if splitcmd[2][0] == 'Y':
                d2 = float(splitcmd[2].split('Y')[1])
            if splitcmd[2][0] == 'Z':
                d3 = float(splitcmd[2].split('Z')[1])
        if dim >= 3:
            if splitcmd[3][0] == 'X':
                d1 = float(splitcmd[3].split('X')[1])
            if splitcmd[3][0] == 'Y':
                d2 = float(splitcmd[3].split('Y')[1])
            if splitcmd[3][0] == 'Z':
                d3 = float(splitcmd[3].split('Z')[1])
                
        length = math.sqrt(d1**2 + d2**2 + d3**2)
        total = length/(speed/60) + total 
        f.write(str(total)+'\n')
        
    elif splitcmd[0] != 'G1':
        f.write(str(total)+'\n')
        

    
    
