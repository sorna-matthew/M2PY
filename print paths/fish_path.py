# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 17:25:49 2018

@author: Matthew
"""

import numpy as np
import matplotlib.pyplot as plt
import m2py as mp

# Defining x values
dx = 0.41
dz = 0.41
x = np.arange(-20, 20, dx)
x2 = np.arange(-7, 7, dx)
x3 = np.arange(19.5, 28, dx)
x4 = np.arange(-10, -4, dx)


# Equations for upper / lower curves
f1 = (1/2)*np.sqrt(400 - x**2)
f2 = -(1/2)*np.sqrt(400 - x**2)
f3 = 15 - 0.1*x2**2
f4 = (1/2)*np.sqrt(400 - x2**2)
f5 = (1.5*x3 - 28)
f6 = -(1.5*x3 - 28)
f7 = 5 - np.sqrt(-40 - 14*x4 - x4**2)
f8 = 5 + np.sqrt(-40 - 14*x4 - x4**2)


# Initializing coordinate vectors
xcoord = np.repeat(x, 2)
ycoord = np.zeros(0)

xcoord2 = np.repeat(x2, 2)
ycoord2 = np.zeros(0)

xcoord3 = np.repeat(x3, 2)
ycoord3 = np.zeros(0)

xcoord4 = np.repeat(x4, 2)
ycoord4 = np.zeros(0)


# Filling coordinate vectors for infill paths
for i in range(len(x)-1):
    if i%2 == 0:
        ycoord = np.append(ycoord, f1[i])
        ycoord = np.append(ycoord, f1[i + 1]) 
    
    if i%2 != 0:
        ycoord = np.append(ycoord, f2[i])
        ycoord = np.append(ycoord, f2[i + 1])
    

xcoord = xcoord[1:-1]

for i in range(len(x2)-1):
    if i%2 == 0:
        ycoord2 = np.append(ycoord2, f3[i])
        ycoord2 = np.append(ycoord2, f3[i + 1]) 
    
    if i%2 != 0:
        ycoord2 = np.append(ycoord2, f4[i])
        ycoord2 = np.append(ycoord2, f4[i + 1])
    
xcoord2 = xcoord2[1:-1]

for i in range(len(x3)-1):
    if i%2 == 0:
        ycoord3 = np.append(ycoord3, f5[i])
        ycoord3 = np.append(ycoord3, f5[i + 1]) 
    
    if i%2 != 0:
        ycoord3 = np.append(ycoord3, f6[i])
        ycoord3 = np.append(ycoord3, f6[i + 1])
    
xcoord3 = xcoord3[1:-1]

for i in range(len(x4)-1):
    if i%2 == 0:
        ycoord4 = np.append(ycoord4, f7[i])
        ycoord4 = np.append(ycoord4, f7[i + 1]) 
    
    if i%2 != 0:
        ycoord4 = np.append(ycoord4, f8[i])
        ycoord4 = np.append(ycoord4, f8[i + 1])
    
xcoord4 = xcoord4[1:-1]


# Plot print paths for various sections
plt.plot(xcoord*2, ycoord*2, xcoord2*2, ycoord2*2, xcoord3*2, ycoord3*2, xcoord4*2, ycoord4*2)

coords1 = np.column_stack((xcoord, ycoord))*2
coords2 = np.column_stack((xcoord2, ycoord2))*2
coords3 = np.column_stack((xcoord3, ycoord3))*2
coords4 = np.column_stack((xcoord4, ycoord4))*2


#%% Begin M2PY Control

mg = mp.mopen('COM7',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 30)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = 30, y = 140, z = -151.5)
mp.coord(mg, coord = 'abs')
mp.wait(mg, seconds = 5)

# Fish body
mp.set_coords(mg, x = coords1[0][0] - 10, y = coords1[0][1])
mp.ch1on(mg)
for lines in coords1:
    mp.move(mg, x = lines[0], y = lines[1])
mp.ch1off(mg)
mp.move(mg, z = dz)

# Fish fin
mp.move(mg, x = coords2[0][0] - 10, y = coords2[0][1])
mp.move(mg, z = -dz)
mp.ch1on(mg)
for lines in coords2:
    mp.move(mg, x = lines[0], y = lines[1])
mp.ch1off(mg)
mp.move(mg, z = dz)

# Fish tail
mp.move(mg, x = coords3[0][0], y = coords3[0][1])
mp.move(mg, z = -dz)
mp.ch1on(mg)
for lines in coords3:
    mp.move(mg, x = lines[0], y = lines[1])
mp.ch1off(mg)
mp.move(mg, z = dz)

# Fish eye
mp.move(mg, x = coords4[0][0], y = coords4[0][1])
mp.ch1on(mg)
for lines in coords4:
    mp.move(mg, x = lines[0], y = lines[1])
    
mp.alloff(mg)
mp.mclose(mg)