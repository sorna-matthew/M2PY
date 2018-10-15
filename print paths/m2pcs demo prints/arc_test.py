# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08:49:27 2018

@author: Matthew
"""
start = [45, 70, -120]

import m2py_old as mp
mg = mp.mopen('COM3',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 30)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = start[0], y = start[1], z = start[2], track = 0)
mp.wait(mg, seconds = 2)
mp.ch1on(mg)

for x in range(1):
    mp.arc(mg, i = 40)
    mp.move(mg, z = 0.35)

mp.alloff(mg)
mp.mclose(mg)