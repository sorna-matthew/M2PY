# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:49:27 2018

@author: Matthew
"""

import m2py as mp
mg = mp.mopen('COM6',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')

mp.home(mg, axes = 'X')

mp.move(mg, x = 50)
mp.move(mg, z = -5)

mp.speed(mg, 35)

mp.ch1on(mg)

mp.move(mg, x = 20)
mp.move(mg, y = 20)
mp.move(mg, x = -20)
mp.move(mg, y = -20)

mp.move(mg, z = .5)

mp.move(mg, x = 20)
mp.move(mg, y = 20)
mp.move(mg, x = -20)
mp.move(mg, y = -20)

mp.move(mg, z = .5)

mp.ch2on(mg)

mp.move(mg, x = 20)
mp.move(mg, y = 20)
mp.move(mg, x = -20)
mp.move(mg, y = -20)

mp.move(mg, z = .5)

mp.ch1off(mg)

mp.move(mg, x = 20)
mp.move(mg, y = 20)
mp.move(mg, x = -20)
mp.move(mg, y = -20)

mp.alloff(mg)


mp.mclose(mg)