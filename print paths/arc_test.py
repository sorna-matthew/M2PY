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
mp.move(mg, x = 70, y = 120, z = -169.15)
mp.wait(mg, seconds = 5)
mp.move(mg, x = -30)
mp.ch1on(mg)
mp.move(mg, x = 30)

for x in range(1):
    mp.arc(mg, i = 40)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 35)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 30)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 25)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 20)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 15)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 10)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -2.5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 7.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 12.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 17.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 22.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 27.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 32.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    
    mp.arc(mg, i = 37.5)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -5)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)

mp.alloff(mg)
mp.mclose(mg)