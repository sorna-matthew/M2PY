# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:49:27 2018

@author: Matthew
"""

import m2py as mp
mg = mp.mopen('COM7',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 30)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = 30, y = 140, z = -151.5)
mp.wait(mg, seconds = 5)


for layers in range(5):
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.4)
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.4)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = -10)
    mp.move(mg, x = 0.4, z = -1)
    
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.4)
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.4)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = 10)
    mp.move(mg, y = -0.4, z = -1)
    
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.4)
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.4)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = -10)
    mp.move(mg, x = -0.4, z = -1)
    
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.4)
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.4)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = 10)
    mp.move(mg, y = -10, z = -1 + 0.4)

mp.alloff(mg)
mp.mclose(mg)