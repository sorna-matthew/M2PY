import m2py as mp

mg = mp.mopen('COM6',115200, printout = 1)
mp.coord(mg, coord = 'rel')
mp.home(mg, axes = 'Y Z')
mp.move(mg, y = 60, z = -182.2, track = 0)
mp.delay_set(mg, delay = 1)

for _ in range(5):
    mp.speed(mg, speed = 10)
    mp.ch3on(mg)
    mp.move(mg, y = 50)
    mp.move(mg, x = 0.5)
    mp.move(mg, y = -50)
    mp.ch3off(mg)
    mp.move(mg, x = 0.5)
    
    mp.speed(mg, speed = 25)
    mp.ch1on(mg)
    mp.move(mg, y = 50)
    mp.move(mg, x = 0.5)
    mp.move(mg, y = -50)
    mp.ch1off(mg)
    mp.move(mg, x = 0.5)
    
    mp.speed(mg, speed = 30)
    mp.ch2on(mg)
    mp.move(mg, y = 50)
    mp.move(mg, x = 0.5)
    mp.move(mg, y = -50)
    mp.ch2off(mg)
    mp.move(mg, x = 0.5)


mp.alloff(mg)
mp.mclose(mg)