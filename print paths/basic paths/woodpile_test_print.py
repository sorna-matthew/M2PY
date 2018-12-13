# Wood Pile Test Print
# Matthew Sorna, M2PY Library

import m2py as mp
import math
#import numpy as np
#import matplotlib.pyplot as plt
start = [15, 50, -99.5]
layers = 1
diam = 0.8
dz = diam*0.85

xwidth = 25
dxwidth = 2
yheight = 75
dyheight = 2

xlines = math.ceil((yheight/dxwidth)/2)
ylines = math.ceil((xwidth/dyheight)/2)

mk = mp.Makergear('COM3',115200, printout = 0)
mk.coord_sys(coord_sys = 'rel')
mk.speed(speed = 28)
mk.home()
mk.move(x = start[0], y = start[1], z = start[2], track = 0)

for _ in range(layers):
    mk.on(1)
    for _ in range(xlines):
        mk.move(x = xwidth)
        mk.move(y = dyheight)
        mk.move(x = -xwidth)
        mk.move(y = dyheight)
        
    mk.off(1)
    mk.move(z = dz)
    mk.move(y = -dyheight*xlines*2)

    mk.on(1)
    for _ in range(ylines):
        mk.move(y = yheight)
        mk.move(x = dxwidth)
        mk.move(y = -yheight)
        mk.move(x = dxwidth)
    
    mk.off(1)
    mk.move(z = dz)
    mk.move(x = -dxwidth*ylines*2)
    
mk.close()