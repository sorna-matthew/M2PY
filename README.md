# M2-Python
*Control of the Makergear M2 3D printer using Python*

---

This project allows for the direct control of [Makergear's M2 3D printer](https://www.makergear.com/products/m2) using the [pyserial](https://pythonhosted.org/pyserial/) package for Python, specifically in the Anaconda environment: [https://anaconda.org/](https://anaconda.org/)

Additonally, these serial commands have been combined with GCode wrappers into the Python module, **m2py**, outlined below. 

---
**m2py** *(a Python module)*
---
---
#### Serial communication commands 
**m2py.mopen**(*com*, *baud*): opens the specified com port, and returns a serial object, `ser`, which must be used in all other m2py function calls.
```python
import m2py as mp
makergear = mp.mopen('COM3',115200)
```
**m2py.mclose**(*ser*): closes the specified serial object.

```python
import m2py as mp
makergear = mp.mopen('COM3', 115200)
mp.mclose(makergear)
```
**m2py.prompt**(*com*, *baud*): allows for quick, native GCode serial communication with the M2, provided that the proper com port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type `exit` in the IPython console.
```python
import m2py as mp
mp.prompt('COM3',115200)
```
**m2py.fileread**(*fid*, *com*, *baud*): reads in a text file of GCode line by line, and waits for the M2 to acknowledge that it received the command before sending another, maintaining print accuracy.
```python
import m2py
mp.fread('C:/Users/Matthew/Documents/m2-python/trunk/print paths/test_path.txt','COM3',115200)
```
---
#### GCode wrappers
##### G0 / G1
**m2py.move**(*ser*, *x=0*, *y=0*, *z=0*): moves to the specified point, keeping in mind the coordinate system (relative / absolute)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.move(makergear, x = 10, y = -5) # x, y, z arguments are all keyword arguments, and default to 0 when not called
mp.mclose(makergear)
```
**m2py.speed**(*ser*, *speed=30*): sets the movement speed of the printer to the specified speed in [mm/s] (default `30` mm/sec)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.speed(makergear, 40) # sets the movement speed of the printer to 40 mm/s
mp.mclose(makergear)
```
##### G2 / G3
**m2py.arc**(*ser*, *x=0*, *y=0*, *i=0*, *j=0*, *direction='ccw'*): moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as `'cw'` or `'ccw'` (default `'ccw'`)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.arc(makergear, x = 10, y = -5, i = 2, j = 3, direction = 'ccw') 
mp.mclose(makergear)
```
##### G4
**m2py.wait**(*ser*, *seconds=0*): waits for the specified amount of time (default `0` seconds)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.wait(makergear, 5) # causes the printer to wait for 5 seconds 
mp.mclose(makergear)
```
##### G28
**m2py.home**(*ser*, *axes='X Y Z'* ): homes the specified axes (default `'X Y Z'`)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.home(makergear, axes = 'X Y Z') # homes all three axes
mp.home(makergear) # homes all three axes
mp.home(makergear, axes = 'X Z') # homes only the specified axes
mp.mclose(makergear)
```
##### G90 / G91
**m2py.coord**(*ser*, *coord='abs'* ): sets the coordinate system of the printer [relative or absolute] (default `'abs'`)

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.coord(makergear, coord = 'abs') # sets coordinate system to absolute
mp.coord(makergear, coord = 'rel') # sets coordinate system to relative
mp.mclose(makergear)
```

---
#### Makergear M2 Pressure Control System (M2PCS) specific functions
##### M3 / M4
**m2py.ch1on**(*ser*): Turns pneumatic Channel 1 ON \
**m2py.ch1off**(*ser*): Turns pneumatic Channel 1 OFF
```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.ch1on(makergear)
mp.move(makergear, x = 10)
mp.ch1off(makergear)
mp.mclose(makergear)
```

##### M5 / M6
**m2py.ch2on**(*ser*): Turns pneumatic Channel 2 ON \
**m2py.ch2off**(*ser*): Turns pneumatic Channel 2 OFF
```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.ch2on(makergear)
mp.move(makergear, x = 10)
mp.ch2off(makergear)
mp.mclose(makergear)
```

##### M7 / M8
**m2py.ch3on**(*ser*): Turns pneumatic Channel 3 ON \
**m2py.ch3off**(*ser*): Turns pneumatic Channel 3 OFF
```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.ch3on(makergear)
mp.move(makergear, x = 10)
mp.ch3off(makergear)
mp.mclose(makergear)
```

**m2py.clip**(*ser*, *clip_height=1*, *radius=0.5*): This subroutine automatically turns off all channels, and performs a quick arc/z-translation to shear excess material away from nozzle before continuing with print path.
 ```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.ch1on(makergear)
mp.move(makergear, x = 10)
mp.clip(makergear, clip_height = 2, radius = 0.1)
mp.mclose(makergear)
```

**m2py.change_tool**(*ser*, *dx=0*, *dy=0*, *change_height=10*): This subroutine automatically turns off all channels, and performs a predetermined z translation of z = change_height, and then moves (x,y) = (dx, dy) to allow for change between multiple nozzles. It also automatically lowers back to the z height it was at previously, continuing printing after switching active tools
 ```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.ch1on(makergear)
mp.move(makergear, x = 10)
mp.change_tool(makergear, dx = 20, dy = 5)
mp.ch2on(makergear)
mp.move(makergear, x = 10)
mp.mclose(makergear)
```

##### Simultaneous functions
---
**m2py.allon**(*ser*): Turns all three pneumatic channels ON \
**m2py.alloff**(*ser*): Turns all three pneumatic channels OFF
 ```python
import m2py as mp
makergear = mp.mopen('COM5',115200)
mp.allon(makergear)
mp.move(makergear, x = 10)
mp.alloff(makergear)
mp.mclose(makergear)
```
#### Example code of basic commands:
 
```python
import m2py as mp
mg = mp.mopen('COM6',115200)
mp.alloff(mg)
mp.coord(mg, coord = 'rel')
mp.speed(mg, speed = 30)
mp.home(mg, axes = 'X Y Z')
mp.move(mg, x = 90, y = 90, z = -169.15)
mp.wait(mg, seconds = 5)
mp.move(mg, x = -30)
mp.ch1on(mg)
mp.move(mg, x = 30)

for x in range(5):
    mp.move(mg, x = 60)
    mp.move(mg, y = 60)
    mp.move(mg, x = -60)
    mp.move(mg, y = -60)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 10, y = 10)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    mp.move(mg, x = 40)
    mp.move(mg, y = 40)
    mp.move(mg, x = -40)
    mp.move(mg, y = -40)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = 10, y = 10)
    mp.move(mg, z = -0.4)
    mp.ch1on(mg)
    mp.move(mg, x = 20)
    mp.move(mg, y = 20)
    mp.move(mg, x = -20)
    mp.move(mg, y = -20)
    mp.ch1off(mg)
    mp.move(mg, z = 0.4)
    mp.move(mg, x = -20, y = -20)
    mp.ch1on(mg)

mp.alloff(mg)
mp.mclose(mg)
```
---