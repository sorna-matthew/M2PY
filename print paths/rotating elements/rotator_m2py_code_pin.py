# -*- coding: utf-8 -*-
"""
@author: Lucia

Define parametrized print path array for a rotator geometry and execute those commands using MakerGear.
"""
import numpy as np
import m2py as mp
import matplotlib.pyplot as plt

mg = mp.mopen('COM6',115200)

# Key geometric parameters (mm)
L = 8
ratio = 1.25
R = ratio*L
numLayers = 10 # Actual number of layers will be twice this!

# Supporting geometric parameters (mm)
b = 7           # "Buffer" to allow for R > L case. Also makes room for holding down the element during torsion testing.
s = 4           # Outer support ring thickness
w = 6           # Width of rotator blades
p = 4.78 + 1.00  # Pin width + extrusion thickness at 42 mm/s

dimsum = R + L 
dimdiff = R - L
edge = 2*b + 2*s + 2*R  # Outer edge length
bdiff = b + dimdiff     # Distance between inner edges of support
wdiff = R - w           # R
beam = bdiff + L + w    # Total extrusion length of beam (for better length control)

# Print parameters
z0 = -169           # Starting z position, based on zeroing manually, mm
dz = 0.52 * 0.250   # Layer height based on nozzle diameter, mm
fs = 25             # Frame speed, mm/s
bs = 15             # Beam speed, mm/s

# Define print path array for one layer. Entries are in the form (x,y,z,channel) where the coordinates are relative and the channel command (-1,0,1 correspond to none,off,on respectively) is to be executed after the move command.
# Note that this automatically inserts mp.move(mg, 0,0,0) commands in between consecutive channel commands, unless later down in the execution you overwrite this.
printPath = np.array([
        [0, 0, 0, 1],
        # Outer edge of support
        [0, -edge, 0, -1],       
        [-edge, 0, 0, -1],
        [0, edge, 0, -1],
        [edge, 0, 0, 0],
        # Move to inner edge
        [-(s+b+dimdiff), -(s+b), 0, 1],
        # Inner edges of support
        [0, b, 0, -1],
        [-dimsum, 0, 0, 0],
        [0, -bdiff, 0, 1],
        [-b, 0, 0, -1],
        [0, -dimsum, 0, 0],
        [bdiff, 0, 0, 1],    
        [0, -b, 0, -1],      
        [dimsum, 0, 0, 0],
        [0, bdiff, 0, 1],
        [b, 0, 0, -1],
        [0, dimsum, 0, 0],
        # Move to rotator edge
        [-b, -wdiff, 0, 1],
        # Edges of rotator
        [-R, 0, 0, -1],              #1
        [0, wdiff, 0, 0],
        [-w, 0, 0, 1],   
        [0, -R, 0, -1],              #2
        [-wdiff, 0, 0, 0],
        [0, -w, 0, 1],   
        [R, 0, 0, -1],               #3
        [0, -wdiff, 0, 0],
        [w, 0, 0, 1],  
        [0, R, 0, -1],               #4
        [wdiff, 0, 0, 0],
        # Move to beam
        [b, R, 0, 1],
        [0, 0, 0, 2],        # Speed change to bs
        # Beams
        [-beam, 0, 0, 0],    #1
        [-wdiff, b, 0, 1],         
        [0, -beam, 0, 0],    #2
        [-b, -wdiff, 0, 1],         
        [beam, 0, 0, 0],     #3
        [wdiff, -b, 0, 1],         
        [0, beam, 0, 0],     #4
        # Move to pin hole
        [0, 0, 0, 2],        # Speed change back to fs
        [-(R-p/2), -(w-p/2), 0, 1],
        # Pin hole (square)
        [-p, 0, 0, -1],
        [0, -p, 0, -1],
        [p, 0, 0, -1],
        [0, p, 0, 0],
        ])

# Generate print path in absolute coordinates for display
printPathAbs = np.array([[0, 0, 0]])
for i in range(len(printPath)):
    r = printPath[i]
    a = printPathAbs[i]
    printPathAbs = np.append(printPathAbs, [[r[0] + a[0], r[1] + a[1], r[2] + a[2]]], axis=0)
    
# Verify that print path looks as desired by plotting it
print(printPathAbs[:,:2])
plt.plot(printPathAbs[:,0], printPathAbs[:,1])
plt.gca().set_aspect('equal',adjustable='box')
plt.draw()    
plt.savefig('rotator_L%d_ratio%.2f_b%d_w%d.png' % (L,ratio,b,w))

# Display any warnings relating to print viability at the end so that they are visible without scrolling
if dimdiff > (b - 2): print("Warning: buffer will not resolve well!") # Check that diff is small enough compared to b so as to not give the printer a hard time
if (L/2) > wdiff: print("Warning: interference between buckled beam and rotator blade!") # Check that (L/2) <= wdiff so that the buckled beam doesn't contact the adjacent rotator blade

#%%

# Run setup command sequence
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
curSpeed = fs
mp.speed(mg, speed = curSpeed)    # mm/s
mp.home(mg, axes = 'X Y Z')
p0 = [63, 185, -152.66349]         # for use again below
mp.move(mg, x = p0[0], y = p0[1], z = p0[2]) # Moves to start position of print

mp.wait(mg, seconds = 2) #Gives yourself time to adjust!

# Run print sequence as defined by printPath array
mp.ch1on(mg)  # Initial extrusion of material before making key features helps with bed adhesion, still working on this!
#mp.move(mg, x = 5)
for i in range(numLayers):
    # Print one layer as directed in the coordinate array, move to next layer
    for c in printPath:
        # Execute move command
        mp.move(mg, x = c[0], y = c[1], z = c[2])
        # Turn pressure on/off where necessary
        if c[3] == 0:
            mp.ch1off(mg)
        elif c[3] == 1:
            mp.ch1on(mg)
        elif c[3] == 2:  # Toggle between beam speed and frame speed where necessary
            if curSpeed == bs:
                curSpeed = fs
            elif curSpeed == fs:
                curSpeed = bs
            mp.speed(mg, speed = curSpeed)
    mp.move(mg, x = 0, y = 0, z = dz)
    # Print a second layer backwards (retracing steps to reach start point), move to next layer
    for j in range(len(printPath),0,-1):
        d = printPath[j-1]
        #  Execute inverse of associated channel/speed command
        if d[3] == 0:
            mp.ch1on(mg)
        elif d[3] == 1:
            mp.ch1off(mg)
        elif d[3] == 2:  # Toggle between beam speed and frame speed where necessary
            if curSpeed == bs:
                curSpeed = fs
            elif curSpeed == fs:
                curSpeed = bs
            mp.speed(mg, speed = curSpeed)
        # Execute negative of original move command
        mp.move(mg, x = -d[0], y = -d[1], z = -d[2])
    mp.move(mg, x = 0, y = 0, z = dz)
 
# Run end-of-print command sequence
mp.alloff(mg)
mp.move(mg, x = 0, y = 0, z = 30)  # Separate nozzle from print
mp.mclose(mg)