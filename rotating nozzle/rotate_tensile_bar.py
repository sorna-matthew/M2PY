import m2py as mp
import numpy as np
mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord_sys(coord_sys = 'rel')
mk.home()
mk.move(x = 60, y = 120, z = -133.5, track = 0)
mk.set_current_coords(x = 0, y = 0, z = 0)
mk.coord_sys(coord_sys = 'abs')
mk.speed(speed = 28)
coords = np.loadtxt('D:/Downloads/tensile_bar_coord.csv', delimiter = ',', usecols=range(2), skiprows = 1)

dz = 0.7
zheight = 0

mk.wait(seconds = 1)
mk.rotate(speed = -80)

mk.on(1)
for _ in range(2):
    for pts in coords:
        mk.move(x = pts[0], y = pts[1], z = zheight)
    
    zheight = zheight + dz
    
    for pts in np.flip(coords, axis = 0):
        mk.move(x = pts[0], y = pts[1], z = zheight)

    zheight = zheight + dz

mk.rotate(speed = 0)
mk.off(1)
mk.close()