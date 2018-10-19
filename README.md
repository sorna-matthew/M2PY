
# M2PYthon
*Control of the Makergear M2 3D printer using Python*

---

This project allows for the direct control of [Makergear's M2 3D printer](https://www.makergear.com/products/m2) using the [pyserial](https://pythonhosted.org/pyserial/) package for Python, specifically in the Anaconda environment: [https://anaconda.org/](https://anaconda.org/)
Additonally, these serial commands have been combined with GCode wrappers into the Python module, **m2py**, outlined below. 

---
**M2PY** *(a Python module)*
---
---
#### Class definition: Makergear
**m2py.Makergear**(*com*, *baud*, *printout=1*): If printout = 1, this function will instantiate a serial object used by all subsequent function calls to send serial commands to the specified printer. If printout = 0, this function will store all revelant coordinate changes (move and arc commands) to a temporary file that can then be used to visualize print paths before sending commands to the printer. By default, printout = 1. 
```python
import m2py as mp
m = mp.Makergear('COM3',115200)
```

```python
import m2py as mp
m = mp.Makergear('COM3',115200, printout = 0)
```

**close**(): closes the specified Makergear object. If printout = 1, this function will close the necessary serial object. If prinout = 0, this function will close the specified temporary file and plot a visualization of all relevant movement commands. Visualization function will use whatever coordinate system you explicity designate using **coord**. If **coord** isn't explicitly called, the coordinate system used by the visualization tool will be *absolute*.

```python
import m2py as mp
m = mp.Makergear('COM3', 115200)
m.close()
```
#### GCode wrappers
##### G0 / G1
**move**(*x=0*, *y=0*, *z=0*): moves to the specified point, keeping in mind the coordinate system (relative / absolute)

```python
import m2py as mp
m = mp.Makergear('COM3',115200)
m.move(x = 10, y = -5) # x, y, z arguments are all keyword arguments, and default to 0 when not called
m.close()
```
**speed**(*speed=30*): sets the movement speed of the printer to the specified speed in [mm/s] (default `30` mm/sec)

```python
m.speed(speed = 40) # sets the movement speed of the printer to 40 mm/s
```
##### G2 / G3
**arc**(*x=0*, *y=0*, *i=0*, *j=0*, *direction='ccw'*): moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as `'cw'` or `'ccw'` (default `'ccw'`)

```python
m.arc(x = 10, y = -5, i = 2, j = 3, direction = 'ccw') 
```
##### G4
**wait**(*seconds=0*): waits for the specified amount of time (default `0` seconds)

```python
m.wait(seconds = 5) # causes the printer to wait for 5 seconds 
```
##### G28
**home**(*axes='X Y Z'* ): homes the specified axes (default `'X Y Z'`)

```python
m.home(axes = 'X Y Z') # homes all three axes
m.home() # homes all three axes
m.home(axes = 'X Z') # homes only the specified axes
```
##### G90 / G91
**coord_sys**(*coord='abs'* ): sets the coordinate system of the printer [relative or absolute] (default `'abs'`)

```python
m.coord_sys(coord_sys = 'abs') # sets coordinate system to absolute
m.coord_sys(coord_sys = 'rel') # sets coordinate system to relative
m.mclose()
```
##### G92
**set_current_coords**(*x=0*, *y=0*, *z=0* ): sets the current position to the specified (x, y, z) point (keeping in mind the current coordinate system)

```python
m.move(x = 10)
m.set_current_coords(x = 0) # sets this new position to x = 0
m.mclose()
```

**return_current_coords**( ): returns the current stored coordinates of the Makergear object

```python
m.move(x = 10)
coords = m.return_current_coords( ) # returns current coords
print(coords)
m.mclose()
```

**set_tool_coords**(*tool=1*, *x=0*, *y=0*, *z=0*): sets internally stored coordinates of each tool, used in switching commands
 ```python
m.on(1)
m.move(x = 10)
m.change_tool(dx = 20, dy = 5)
m.on(2)
m.move(x = 10)
```

**change_tool**(*change_to=1*): This subroutine automatically swiches from the current to speicified tool
 ```python
m.on(1)
m.move(x = 10)
m.change_tool(dx = 20, dy = 5)
m.on(2)
m.move(x = 10)
```

---
#### Makergear M2 Pressure Control System (M2PCS) specific functions
##### M3 - M8
**on**(*channel*): Turns pneumatic channel ON \
**off**(*channel*): Turns pneumatic channel OFF
```python
m.on(1)
m.move(x = 10)
m.off(1)
```

**set_channel_delay**(*delay=50*): sets the delay time (in ms) between a channel turning on and the execution of another command. Can be used to fine tune under extrusion effects, depending on ink viscosity.
```python
m.set_channel_delay(delay = 50)
m.on(3)
m.move(x = 10)
m.move(x = -10)
m.off(3)
```

#### Simultaneous functions
**allon**(): Turns all three pneumatic channels ON \
**alloff**(): Turns all three pneumatic channels OFF
 ```python
m.allon()
m.move(x = 10)
m.alloff()
```
Additional functions outside of the Makergear class definition
---
**mp.prompt**(*com*, *baud*): allows for quick, native GCode serial communication with the M2, provided that the proper com port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type `exit` in the IPython console.
```python
mp.prompt('COM3',115200)
```
**mp.file_read**(*fid*, *com*, *baud*): reads in a text file of GCode line by line, and waits for the M2 to acknowledge that it received the command before sending another, maintaining print accuracy.
```python
mp.file_read('C:/Users/Matthew/Documents/m2-python/trunk/print paths/test_path.txt','COM3',115200)
```