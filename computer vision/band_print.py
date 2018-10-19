d1 = 24
d2 = 24.1
r1 = d1/2
r2 = d2/2
diam = 0.4
layers = 5

import m2py as mp
import numpy as np
#import matplotlib.pyplot as plt
theta = np.linspace(0, 2*np.pi, 60);

start = [120, 70, -120]
layers = 10
dz = diam*0.8

mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord(coord_sys = 'rel')
mk.speed(speed = 40)
mk.home()
mk.move(x = start[0], y = start[1], z = start[2], track = 0)
mk.on(2)
mk.coord(coord_sys = 'abs')
mk.set_coords()
zheight = dz
for i in range(layers):
    mk.on(2)
    for j in range(len(theta)):
        mk.move(x = r2*np.cos(theta[j]), y = r2*np.sin(theta[j]), z = zheight)
    zheight = zheight + dz
    mk.off(2)
    mk.move(x = r1*np.cos(theta[0]), y = r1*np.sin(theta[0]), z = zheight)
mk.off(2)

mk.close()