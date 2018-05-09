#Visualization Testing

import m2py as mp

mg = mp.mopen('COM6',115200, printout = 0)
mp.coord(mg, coord = 'rel')

dx = 5
dy = 5
x = 20
y = 20

for l in range(4):
    mp.move(mg, x = dx)
    mp.move(mg, y = y)
    mp.move(mg, x = dx)
    mp.move(mg, y = -y)

mp.move(mg, x = -2*x, y = y)

for l in range(4):
    mp.move(mg, x = 2*x)
    mp.move(mg, y = -dy)
    
mp.mclose(mg)