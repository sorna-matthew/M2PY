import m2py as mp

xl = 40             # x length of box mm
yl = 40             # y lenth of box mm
dx = 2              # delta between x lines mm
dy = 2              # delta between y lines mm
dz = 0.41*0.7      # delta between z layers mm
nx = int(xl/(2*dx)) # number of iterations on each layer in x direction
ny = int(yl/(2*dy)) # number of iterations on each layer in y direction
layers = 15         # total number of layers
zl = layers*dz*2      # overall z height based on dz and number of layers mm
zraise = 2          # distance clip function travels 
ms = 45             # movement speed in mm/sec

#%%
mg = mp.mopen('COM6',115200)

# Run setup command sequence
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = ms)    # mm/s
mp.home(mg, axes = 'X Y Z')
p0 = [110, 100, -157.7]         # for use again below
mp.move(mg, x = p0[0], y = p0[1], z = p0[2]) # Moves to start position of print
mp.wait(mg, seconds = 2) #Gives yourself time to adjust!

for l in range(layers):
    mp.ch1on(mg)
    for m in range(nx):
        mp.move(mg, y = yl)
        mp.move(mg, x = dx)
        mp.move(mg, y = -yl)
        mp.move(mg, x = dx)
    
    mp.clip(mg, clip_height = zraise, radius = 0.2)
    mp.change_tool(mg, dx = -28.2 , dy = -0.2)
    mp.move(mg, x = -dx*2*nx)
    mp.move(mg, z = -(zraise - dz))
    
    mp.ch2on(mg)
    for m in range(ny):
        mp.move(mg, x = xl)
        mp.move(mg, y = dy)
        mp.move(mg, x = -xl)
        mp.move(mg, y = dy)
    
    mp.clip(mg, clip_height = zraise, radius = 0.2)
    mp.change_tool(mg, dx = 28.2 , dy = 0.2)
    mp.move(mg, y = -dy*2*ny)
    mp.move(mg, z = -(zraise - dz))

mp.alloff(mg)
mp.mclose(mg)     