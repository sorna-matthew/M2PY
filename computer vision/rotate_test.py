import m2py as mp

start = [20, 55, -115.3]
rotate_speed = [0, 31, 63, 93, 127]

mk = mp.Makergear('COM3',115200)
mk.speed(speed = 20)
mk.coord(coord_sys = 'rel')
mk.home()
mk.move(x = start[0], y = start[1], z = start[2])

mk.rotate(speec = 50)
mk.wait(seconds = 5)
mk.rotate(speed = 0)

for r in range(len(rotate_speed)-1):
    mk.move(z = 5)
    mk.ramp(start = rotate_speed[r], stop = rotate_speed[r+1], seconds = 5)
    mk.move(z = -5)
    
    mk.on(2)
    mk.move(x = 20)
    mk.off(2)
    
    mk.move(y = 5)
    mk.move(x = -20)
    
mk.close()