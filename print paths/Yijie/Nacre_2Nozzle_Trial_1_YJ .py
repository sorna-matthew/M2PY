import m2py as mp 
# Imports the M2PY library, and gives it a shorter name, mp
start = [50, 70, -100] 
# The starting global coordinates of the tool_head
mk = mp.Makergear('COM3', 115200, printout = 0) 
# Initializes the printer, and when printout = 1, the printer gets sent command. printout = 0 just plots the coordinates in the visualizer
mk.coord_sys(coord_sys = 'rel')
# Sets coordinate system to relative
mk.speed(speed = 25)
# Movement speed in mm/s
mk.home(axes = 'X Y Z') 
# Homes all axes to global (0,0,0)
mk.move(x = start[0], y = start[1], z = start[2], track = 0) 
# Moves the tool head to the start location, relative to (0,0,0)

# Now any movement commands are relative from the starting location, with the nozzle at the build plate.

mk.set_tool_coords(tool=1,x=0,y=0,z=0)
mk.set_tool_coords(tool=2,x=30,y=0,z=0)

dx=0.6*1.1
dz=0.6*0.7
layer=6
col=5*2
row=5

nH=12
nS=4



for Li in range(layer):
	mk.on(1)
	mk.move(y=(row*(nH+nS)-1)*dx)
	
	for ci in range(col//2):
		mk.move(x=dx)
		for ri in range(row):
			if ri==1:
				mk.move(y=-(nS/2-1)*dx)
			else:
				mk.move(y=-(nS/2)*dx)
			mk.off(1)
			mk.change_tool(change_to=2)
			mk.on(2)
			mk.move(y=-nH*dx)
			mk.off(2)
			mk.change_tool(change_to=1)
			mk.on(1)
			mk.move(y=-nS/2*dx)

		mk.move(x=dx)
		mk.move(y=(row*(nH+nS)-1)*dx)

		mk.off(1)
		mk.change_tool(change_to=2)
		mk.move(x=dx)
		mk.on(2)
		for ri in range(row):
			if ri==1:
				mk.move(y=-(nH/2-1)*dx)
			else:
				mk.move(y=-(nH/2)*dx)
			mk.off(2)
			mk.change_tool(change_to=1)
			mk.on(1)
			mk.move(y=-nS*dx)
			mk.off(1)
			mk.change_tool(change_to=2)
			mk.on(2)
			mk.move(y=-nH/2*dx)

		mk.off(2)
		mk.change_tool(change_to=1)
		mk.on(1)
		mk.move(x=dx)
		mk.move(y=(row*(nH+nS)-1)*dx)
	
	mk.off(1)
	mk.move(z=dz)
	mk.move(x=-(col*2)*dx, y=-(row*(nH+nS)-1)*dx)

mk.move(x=-5, y=-5)

mk.close() # This always needs to be called at the end of every script