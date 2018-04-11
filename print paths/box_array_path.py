# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:17:40 2018

@author: Matthew
"""
import numpy as np
import matplotlib.pyplot as plt
import m2py as mp
import math

box_area = 25 # mm^2
sl = math.sqrt(box_area)
dx = 0.4
dy = 0.4
dz = 0.5
nxl = int(sl/dx)
nyl = int(sl/dy)
nzl = int(sl/dz)

nxb = 10
nyb = 5

ch1 = 1
ch2 = 2

coords = np.zeros((1,4))

for k in range(3):
    for j in range(nxb):
        for i in range(nyb):
            if i%2 == 0:
                coords = np.append(coords,coords[-1] + [[0, 0, 0, 1]], axis = 0)
            elif i%2 == 1:
                coords = np.append(coords,coords[-1] + [[0, 0, 0, 2]], axis = 0)
                
            for j in range(int(nxl/2)):
                coords = np.append(coords,coords[-1] + [[sl, 0, 0, 0]], axis = 0)
                coords = np.append(coords,coords[-1] + [[0 , dy, 0, 0]], axis = 0)
                coords = np.append(coords,coords[-1] + [[-sl, 0, 0, 0]], axis = 0)
                coords = np.append(coords,coords[-1] + [[0 , dy, 0, 0]], axis = 0)
        
            if i%2 == 0:
                coords = np.append(coords,coords[-1] + [[0, 0, 0, -1]], axis = 0)
            elif i%2 == 1:
                coords = np.append(coords,coords[-1] + [[0, 0, 0, -2]], axis = 0)
        
        coords = np.append(coords,coords[-1] + [[sl + dx, -nyl*dy*nyb, 0, 0]], axis = 0)
    
    coords = np.append(coords,coords[-1] + [[-(sl + dx)*nxb, 0, dz, 0]], axis = 0)

xcoords = coords[..., 0]
ycoords = coords[..., 1]
zcoords = coords[..., 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xcoords, ycoords, zcoords)

#%%
mg = mp.mopen('COM6',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'abs')
mp.speed(mg, speed = 32)
mp.home(mg, axes = 'X Y Z')