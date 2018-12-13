import m2py as mp
mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord_sys(coord_sys = 'rel')
mk.home()
mk.move(x = 10, y = 65, z = -130, track = 0)
mk.speed(speed = 15)

speeds = [40, 60, 80, 100, 120]

for s in speeds:
    mk.rotate(speed = s)
    mk.wait(seconds = 1)
    mk.on(1)
    mk.move(x = 30)
    mk.off(1)
    mk.move(x = -30, y = 10)

mk.rotate(speed = 0)
mk.close()
    