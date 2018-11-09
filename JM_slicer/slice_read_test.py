# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 13:24:02 2018

@author: University of Penn
"""

import m2py as mp

for i in range(30):
    mp.file_read('D:\\M2PY\\trunk\\computer vision\\JM_slicer\\output\\Size3_support_{}.cnc'.format(i),'COM3',115200)