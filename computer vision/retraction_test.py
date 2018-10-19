# Switching Nozzles
# Matthew Sorna, M2PY Library

import m2py as mp
#import numpy as np
#import matplotlib.pyplot as plt
start = [100, 140, -74.9]
layers = 5
dx = -37
dy = 0
diam = 0.4
dz = diam*0.8

mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord(coord_sys = 'rel')

mk.speed(speed = 22)
mk.home()
mk.move(x = start[0], y = start[1], z = start[2], track = 0)
mk.delay_set(delay = 75)

mk.on(1)
mk.move(x = 25)
mk.move(y = 60)
mk.move(x = -25)
mk.move(y = -60)
mk.off(1)

for _ in range(15):
    mk.move(y = 2)
    mk.on(1)
    mk.move(x = 25)
    mk.off(1)
    mk.move(y = 2)
    mk.change_tool(dx = dx,  dy = 0, change_height = 0)
    mk.on(2)
    mk.move(x = -25)
    mk.off(2)
    mk.change_tool(dx = -dx,  dy = 0, change_height = 0)


mk.close()