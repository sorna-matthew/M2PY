import m2py as mp

xl = 15             # x length of box mm
yl = 30
dx = 1             # delta between x lines mm
dz = 0.41      # delta between z layers mm
nx = int(xl/(2*dx)) # number of iterations on each layer in x direction
layers = 10         # total number of layers
zl = layers*dz*2      # overall z height based on dz and number of layers mm
zraise = 2          # distance clip function travels 
ms = 50             # movement speed in mm/sec

#%%
mg = mp.mopen('COM6',115200)

# Run setup command sequence
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = ms)    # mm/s
mp.home(mg, axes = 'Y Z')
p0 = [0, 200, -166.2]         # for use again below
mp.move(mg, x = p0[0], y = p0[1], z = p0[2]) # Moves to start position of print
mp.wait(mg, seconds = 4) #Gives yourself time to adjust!

for l in range(layers):
    mp.allon(mg)
    for m in range(nx):
        mp.move(mg, y = yl)
        mp.move(mg, x = dx)
        mp.ch1off(mg)
        mp.move(mg, y = -yl)
        mp.move(mg, x = dx)
        mp.ch1on(mg)
    
    mp.clip(mg, clip_height = zraise, radius = 0.2)
    mp.move(mg, x = -dx*2*nx)
    mp.move(mg, z = -(zraise - dz))
    
mp.alloff(mg)
mp.mclose(mg)     