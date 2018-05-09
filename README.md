
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
**m2py.mopen**(*com*, *baud*, *printout=1*, *fid=''*): returns the necessary handle (serial object if printout = 1, or temporary file if printout = 0). If printout = 1, this function will instantiate a serial object used by all subsequent function calls to send serial commands to the specified printer. If printout = 0, this function will store all revelant coordinate changes (move and arc commands) to a temporary file that can then be used to visualize print paths before sending commands to the printer. By default, printout = 1. 
```python
import m2py as mp
mg = mp.mopen('COM3',115200)
```

```python
import m2py as mp
mg = mp.mopen('COM3',115200, printout = 0)
```

**m2py.mclose**(*handle*): closes the specified handle. If in **mopen** printout = 1, this function will close the necessary serial object. If prinout = 0, this function will close the specified temporary file and plot a visualization of all relevant movement commands. Visualization function will use whatever coordinate system you explicity designate using **coord**. If **coord** isn't explicitly called, the coordinate system used by the visualization tool will be *absolute*.

```python
import m2py as mp
mg = mp.mopen('COM3', 115200)
mp.mclose(mg)
```
**m2py.path_vis**(*fid=''*, *coord='abs'*): takes the (x, y, z) coordinates generated from mp.mopen(printout = 0), and plots them into a 3D line graph to check a print path before actually sending commands to the Makergear. Visualization function will use whatever coordinate system you explicity designate using **coord**. If **coord** isn't explicitly called, the coordinate system used by the visualization tool will be *absolute*. When using **path_vis**, the file directory of the path coordinates needs to be explicity set, unlike when it is implictly called inside **mclose**.

```python
import m2py as mp
mg = mp.mopen('COM3', 115200, printout = 0, fid = 'C:/Users/Matthew/Documents/test.txt')
mp.move(x = 10)
mp.move(y = 10)
mp.move(x = -10)
mp.move(y = -10)
mp.mclose(mg)
mp.path_vis(fid = 'C:/Users/Matthew/Documents/test.txt', coord = 'rel')
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
**m2py.move**(*handle*, *x=0*, *y=0*, *z=0*): moves to the specified point, keeping in mind the coordinate system (relative / absolute)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.move(mg, x = 10, y = -5) # x, y, z arguments are all keyword arguments, and default to 0 when not called
mp.mclose(mg)
```
**m2py.speed**(*handle*, *speed=30*): sets the movement speed of the printer to the specified speed in [mm/s] (default `30` mm/sec)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.speed(mg, 40) # sets the movement speed of the printer to 40 mm/s
mp.mclose(mg)
```
##### G2 / G3
**m2py.arc**(*handle*, *x=0*, *y=0*, *i=0*, *j=0*, *direction='ccw'*): moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as `'cw'` or `'ccw'` (default `'ccw'`)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.arc(mg, x = 10, y = -5, i = 2, j = 3, direction = 'ccw') 
mp.mclose(mg)
```
##### G4
**m2py.wait**(*handle*, *seconds=0*): waits for the specified amount of time (default `0` seconds)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.wait(mg, 5) # causes the printer to wait for 5 seconds 
mp.mclose(mg)
```
##### G28
**m2py.home**(*handle*, *axes='X Y Z'* ): homes the specified axes (default `'X Y Z'`)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.home(mg, axes = 'X Y Z') # homes all three axes
mp.home(mg) # homes all three axes
mp.home(mg, axes = 'X Z') # homes only the specified axes
mp.mclose(mg)
```
##### G90 / G91
**m2py.coord**(*handle*, *coord='abs'* ): sets the coordinate system of the printer [relative or absolute] (default `'abs'`)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.coord(mg, coord = 'abs') # sets coordinate system to absolute
mp.coord(mg, coord = 'rel') # sets coordinate system to relative
mp.mclose(mg)
```
##### G92
**m2py.set_coords**(*handle*, *x=0*, *y=0*, *z=0* ): sets the current position to the specified (x, y, z) point (keeping in mind the current coordinate system)

```python
import m2py as mp
mg = mp.mopen('COM3',115200)
mp.move(mg, x = 10)
mp.set_coords(mg, x = 0) # sets this new position to x = 0
mp.mclose(mg)
```
---
#### Makergear M2 Pressure Control System (M2PCS) specific functions
##### M3 / M4
**m2py.ch1on**(*handle*): Turns pneumatic Channel 1 ON \
**m2py.ch1off**(*handle*): Turns pneumatic Channel 1 OFF
```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.ch1on(mg)
mp.move(mg, x = 10)
mp.ch1off(mg)
mp.mclose(mg)
```

##### M5 / M6
**m2py.ch2on**(*handle*): Turns pneumatic Channel 2 ON \
**m2py.ch2off**(*handle*): Turns pneumatic Channel 2 OFF
```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.ch2on(mg)
mp.move(mg, x = 10)
mp.ch2off(mg)
mp.mclose(mg)
```

##### M7 / M8
**m2py.ch3on**(*handle*): Turns pneumatic Channel 3 ON \
**m2py.ch3off**(*handle*): Turns pneumatic Channel 3 OFF
```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.ch3on(mg)
mp.move(mg, x = 10)
mp.ch3off(mg)
mp.mclose(mg)
```
**m2py.delay_set**(*handle*, *delay=50*): sets the delay time (in ms) between a channel turning on and the execution of another command. Can be used to fine tune under extrusion effects, depending on ink viscosity.
```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.delay_set(mg, delay = 50)
mp.move(mg, x = 10)
mp.move(mg, x = -10)
mp.ch3off(mg)
mp.mclose(mg)
```

**m2py.clip**(*handle*, *clip_height=1*, *radius=0.5*): This subroutine automatically turns off all channels, and performs a quick arc/z-translation to shear excess material away from nozzle before continuing with print path.
 ```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.ch1on(mg)
mp.move(mg, x = 10)
mp.clip(mg, clip_height = 2, radius = 0.1)
mp.mclose(mg)
```

**m2py.change_tool**(*handle*, *dx=0*, *dy=0*, *change_height=10*): This subroutine automatically turns off all channels, and performs a predetermined z translation of z = change_height, and then moves (x,y) = (dx, dy) to allow for change between multiple nozzles. It also automatically lowers back to the z height it was at previously, continuing printing after switching active tools
 ```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.ch1on(mg)
mp.move(mg, x = 10)
mp.change_tool(mg, dx = 20, dy = 5)
mp.ch2on(mg)
mp.move(mg, x = 10)
mp.mclose(mg)
```

#### Simultaneous functions
---
**m2py.allon**(*handle*): Turns all three pneumatic channels ON \
**m2py.alloff**(*handle*): Turns all three pneumatic channels OFF
 ```python
import m2py as mp
mg = mp.mopen('COM5',115200)
mp.allon(mg)
mp.move(mg, x = 10)
mp.alloff(mg)
mp.mclose(mg)
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