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
mp.move(mg, x = 75, y = 90, z = -169.15)
mp.wait(mg, seconds = 3)
mp.move(mg, x = -20)
mp.ch1on(mg)
mp.move(mg, x = 20)

for y in range(5):
    for x in range(5):
        mp.move(mg, x = 20)
        mp.move(mg, y = 2)
        mp.move(mg, x = -20)
        mp.move(mg, y = 2)
    
    
    mp.ch1off(mg)
    mp.move(mg, z = .4)
    mp.move(mg, y = -20)
    mp.ch1on(mg)
    
    for x in range(5):
        mp.move(mg, y = 20)
        mp.move(mg, x = 2)
        mp.move(mg, y = -20)
        mp.move(mg, x = 2)
    
    mp.ch1off(mg)
    mp.move(mg, z = .4)
    mp.move(mg, x = -20)
    mp.ch1on(mg)
    
mp.alloff(mg)
mp.mclose(mg)
