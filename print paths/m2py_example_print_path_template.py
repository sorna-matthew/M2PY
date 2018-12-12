import m2py as mp # Imports the M2PY library, and gives it a shorter name, mp
start = [50, 70, 0] # The starting global coordinates of the tool_head
mk = mp.Makergear('COM3', 115200, printout = 0) # Initializes the printer, and when printout = 1, the printer gets sent command. printout = 0 just plots the coordinates in the visualizer
mk.coord_sys(coord_sys = 'rel') # Sets coordinate system to relative
mk.speed(speed = 45) # Movement speed in mm/s
mk.home(axes = 'X Y Z') # Homes all axes to global (0,0,0)
mk.move(x = start[0], y = start[1], z = start[2], track = 0) # Moves the tool head to the start location, relative to (0,0,0)

# Now any movement commands are relative from the starting location, with the nozzle at the build plate.

# Examples of commands
mk.on(1)
mk.move(x = 10)
mk.arc(x = 10, y = 0, i = 5, j = 0)
mk.off(1)

# Your code here:

    

mk.close() # This always needs to be called at the end of every script