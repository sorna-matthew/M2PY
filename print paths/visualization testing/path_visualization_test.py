# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 17:41:29 2018

@author: Matthew
"""

import m2py_temp as mp
mk = mp.Makergear('COM3',115200, printout = 0)
mk.home()
mk.coord(coord_sys = 'rel')
for _ in range(5):
    
    mk.move(x = -1, y = -1)
    mk.on(3)
    mk.move(x = 22)
    mk.move(y = 22)
    mk.move(x = -22)
    mk.move(y = -22)
    mk.off(3)
    mk.move(x = 1, y = 1)
    
    mk.on(1)
    for _ in range(5):
        mk.move(x = 20)
        mk.move(y = 2)
        mk.move(x = -20)
        mk.move(y = 2)
    mk.off(1)
    mk.move(y = -20)
    mk.on(2)
    for _ in range(5):
        mk.move(y = 20)
        mk.move(x = 2)
        mk.move(y = -20)
        mk.move(x = 2)
    mk.off(2)
    mk.move(x = -20)
    mk.move(z = 3)
    
mk.close()