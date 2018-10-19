# Print Path Visualization
import m2py as mp
mk = mp.Makergear('COM3',115200,printout = 0)
mk.coord_sys(coord_sys = 'rel')
mk.set_tool_coords(tool = 1, x = 0, y = 0, z = 0)
mk.set_tool_coords(tool = 2, x = -35, y = 0, z = 0)
mk.set_tool_coords(tool = 3, x = -70, y = 0, z = 0)


for _ in range(5):
    mk.on(1)
    mk.move(x = 10)
    mk.move(y = 10)
    mk.move(x = -10)
    mk.move(y = -10)
    mk.off(1)
    mk.move(z = 2)

mk.on(2)
mk.move(x = 10, y = 10)
mk.off(2)
mk.move(x = -10)
mk.on(3)
mk.move(x = 10, y = -10)
mk.off(3)
mk.move(x = -10)

mk.change_tool(change_to = 2)
mk.move(z = 1)

for _ in range(5):
    mk.on(2)
    mk.move(x = 7.5)
    mk.move(y = 7.5)
    mk.move(x = -7.5)
    mk.move(y = -7.5)
    mk.off(2)
    mk.move(z = 2)

mk.on(3)
mk.move(x = 7.5, y = 7.5)
mk.off(3)
mk.move(x = -7.5)
mk.on(1)
mk.move(x = 7.5, y = -7.5)
mk.off(1)
mk.move(x = -7.5)

mk.change_tool(change_to = 3)
mk.move(z = 1)

for _ in range(5):
    mk.on(3)
    mk.move(x = 5)
    mk.move(y = 5)
    mk.move(x = -5)
    mk.move(y = -5)
    mk.off(3)
    mk.move(z = 2)

mk.on(1)
mk.move(x = 5, y = 5)
mk.off(1)
mk.move(x = -5)
mk.on(2)
mk.move(x = 5, y = -5)
mk.off(2)
mk.move(x = -5)

mk.close()