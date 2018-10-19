# Switching Nozzles
# Matthew Sorna, M2PY Library

import m2py as mp
#import numpy as np
#import matplotlib.pyplot as plt
start = [100, 100, -74.7]
layers = 5
dx = -36
dy = 0
diam = 0.4
dz = diam*0.8

mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord(coord_sys = 'rel')
mk.delay_set(delay = 300)
mk.speed(speed = 10)
mk.home()
mk.move(x = start[0], y = start[1], z = start[2], track = 0)

mk.on(1)
mk.move(x = 20)
mk.move(y = 20)
mk.move(x = -20, y = -20)
mk.off(1)

mk.change_tool(dx = dx, dy = dy, change_height = 0)

mk.move(x = -40)

mk.on(2)
mk.move(x = 20)
mk.move(y = 20)
mk.move(x = -20)
mk.move(y = -20)
mk.off(2)

mk.close()