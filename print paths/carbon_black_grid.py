#Carbon Black
import m2py as mp

mk = mp.Makergear('COM3',115200, printout = 1)
mk.coord_sys(coord_sys = 'rel')
mk.speed(speed = 30)
mk.home()
mk.move(x = 20, y = 45, z = -82.4, track = 0)
mk.speed(speed = 3)
mk.on(1)
for _ in range(5):
    mk.move(y = 50)
    mk.move(x = 5)
    mk.move(y = -50)
    mk.move(x = 5)

mk.off(1)
mk.move(x = -50)
mk.on(1)    
for _ in range(5):
    mk.move(x = 50)
    mk.move(y = 5)
    mk.move(x = -50)
    mk.move(y = 5)    
mk.off(1)

mk.close()