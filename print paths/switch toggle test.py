# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:49:27 2018

@author: Matthew
"""

import m2py as mp
mg = mp.mopen('COM6',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 30)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = 90, y = 90, z = -169.15)
mp.wait(mg, seconds = 5)
mp.move(mg, x = -30)
mp.ch1on(mg)
mp.move(mg, x = 30)

for x in range(5):
    mp.move(mg, x = 60)
    mp.move(mg, y = 60)
    mp.move(mg, x = -60)
    mp.move(mg, y = -60)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 10, y = 10)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    mp.move(mg, x = 40)
    mp.move(mg, y = 40)
    mp.move(mg, x = -40)
    mp.move(mg, y = -40)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 10, y = 10)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    mp.move(mg, x = 20)
    mp.move(mg, y = 20)
    mp.move(mg, x = -20)
    mp.move(mg, y = -20)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -20, y = -20)
    mp.ch1on(mg)

mp.alloff(mg)
mp.mclose(mg)