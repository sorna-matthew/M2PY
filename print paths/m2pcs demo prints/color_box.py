# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:49:27 2018

@author: Matthew
"""

dx12 = 18.5
dy12 = -0.8

import m2py as mp
mg = mp.mopen('COM6',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 32)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = 60, y = 160, z = -170.2)
mp.wait(mg, seconds = 5)

# Bottom Quad
for layers in range(4):
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.41)
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.41)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = dx12, dy = dy12)
    mp.move(mg, x = 0.41, z = -1)
    
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.41)
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.41)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = -dx12, dy = -dy12)
    mp.move(mg, y = -0.41, z = -1)
    
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.41)
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.41)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = dx12, dy = dy12)
    mp.move(mg, x = -0.41, z = -1)
    
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.41)
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.41)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    if layers < 3:
        mp.change_tool(mg, dx = -dx12, dy = -dy12)
    mp.move(mg, y = 0.41, z = -1 + 0.41)

#Upper Quad
for layers in range(4):
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.41)
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.41)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = -dx12, dy = -dy12)
    mp.move(mg, x = 0.41, z = -1)
    
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.41)
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.41)
    mp.move(mg, x = 10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = dx12, dy = dy12)
    mp.move(mg, y = -0.41, z = -1)
    
    mp.ch1on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = -0.41)
        mp.move(mg, x = 10)
        mp.move(mg, y = -0.41)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = -dx12, dy = -dy12)
    mp.move(mg, x = -0.41, z = -1)
    
    mp.ch2on(mg)
    for x in range(12):
        mp.move(mg, x = -10)
        mp.move(mg, y = 0.41)
        mp.move(mg, x = 10)
        mp.move(mg, y = 0.41)
    mp.move(mg, x = -10)
    
    mp.clip(mg)
    mp.change_tool(mg, dx = dx12, dy = dy12)
    mp.move(mg, y = 0.41, z = -1 + 0.41)


mp.alloff(mg)
mp.mclose(mg)