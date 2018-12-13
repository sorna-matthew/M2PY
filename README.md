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
**m2py.Makergear**(*com*, *baud*, *printout=0*, *verbose=True*): If printout = 1, this function will instantiate a serial object used by all subsequent function calls to send serial commands to the specified printer. If printout = 0, this function will store all relevant coordinate changes (move and arc commands) to a temporary file that can then be used to visualize print paths before sending commands to the printer. By default, printout = 0. The flag verbose controls the print statements to the console. With verbose = True, all print statements are printed. With verbose = False, all print statements are suppressed. 
```python
import m2py as mp
mk = mp.Makergear('COM3',115200)
```

```python
import m2py as mp
mk = mp.Makergear('COM3',115200, printout = 1, verbose = False)
```

**close**(): closes the specified Makergear object. If printout = 1, this function will close the necessary serial object. If printout = 0, this function will close the specified temporary file and plot a visualization of all relevant movement commands. Visualization function will use whatever coordinate system you explicitly designate using **coord**. If **coord** isn't explicitly called, the coordinate system used by the visualization tool will be *absolute*.

```python
import m2py as mp
mk = mp.Makergear('COM3', 115200)
mk.close()
```
#### GCode wrappers
##### G0 / G1
**move**(*x=0*, *y=0*, *z=0*): moves to the specified point, keeping in mind the coordinate system (relative / absolute)

```python
import m2py as mp
mk = mp.Makergear('COM3',115200)
mk.move(x = 10, y = -5) # x, y, z arguments are all keyword arguments, and default to 0 when not called
mk.close()
```
**speed**(*speed=0*): sets the movement speed of the printer to the specified speed in [mm/s] (default `0` mm/sec)

```python
mk.speed(speed = 40) # sets the movement speed of the printer to 40 mm/s
```

**rotate**(*speed=0*):sets the rotation speed of the motor to the specified speed (default 0)

```python
mk.rotate(speed = 30) # sets the rotation speed of the motor to 30
```

**ramp**(*start=0*,*stop=0*,*seconds=1*): sets the rotation speed of the motor from the start speed to the specified stop speed over a given time in seconds [0-127] (default 0 --> 0)

```python
mk.ramp(start = 0, stop = 0, seconds = 1) # ramps the rotation speed from 0 to 30 in 1 second
```

##### G2 / G3
**arc**(*x=0*, *y=0*, *i=0*, *j=0*, *direction='ccw'*): moves to the specified x-y point, with the i-j point as the center of the arc, with direction specified as `'cw'` or `'ccw'` (default `'ccw'`)

```python
mk.arc(x = 10, y = -5, i = 2, j = 3, direction = 'ccw') 
```
##### G4
**wait**(*seconds=0*): waits for the specified amount of time (default `0` seconds)

```python
mk.wait(seconds = 5) # causes the printer to wait for 5 seconds 
```
##### G28
**home**(*axes='X Y Z'* ): homes the specified axes (default `'X Y Z'`)

```python
mk.home(axes = 'X Y Z') # homes all three axes
mk.home() # homes all three axes
mk.home(axes = 'X Z') # homes only the specified axes
```
##### G90 / G91
**coord_sys**(*coord_sys='abs'* ): sets the coordinate system of the printer [relative or absolute] (default `'abs'`)

```python
mk.coord_sys(coord_sys = 'abs') # sets coordinate system to absolute
mk.coord_sys(coord_sys = 'rel') # sets coordinate system to relative
mk.mclose()
```
##### G92
**set_current_coords**(*x=0*, *y=0*, *z=0* ): sets the current position to the specified (x, y, z) point (keeping in mind the current coordinate system)

```python
mk.move(x = 10)
mk.set_current_coords(x = 0) # sets this new position to x = 0
mk.mclose()
```

**return_current_coords**( ): returns the current stored coordinates of the Makergear object

```python
mk.move(x = 10)
coords = mk.return_current_coords( ) # returns current coords
print(coords)
mk.mclose()
```

**set_tool_coords**(*tool=1*, *x=0*, *y=0*, *z=0*): sets internally stored coordinates of each tool, used in switching commands, relative to tool 1 which is defined at [0,0,0]

**change_tool**(*change_to=1*): This subroutine automatically switches from the current to specified tool
 
  ```python
mk.set_tool_coords(tool = 1, x = 0, y = 0, z = 0)
mk.set_tool_coords(tool = 2, x = 10, y = 10, z = 0)
mk.on(1)
mk.move(x = 10)
mk.off(1)
mk.change_tool(change_to = 2)
mk.on(2)
mk.move(x = 10)
mk.off(2)
```
**set_bed_temp**(*temp=25*, *wait='off'*): Sets the temperature of the heated bed to the specified temp in deg C. If the wait argument is set to `'on'`, the printer will wait for temp to be reached before excecuting other commands. If `'off'` the printer will set the temp without waiting.
```python
mk.set_bed_temp(temp = 50, wait = 'on')
mk.on(1)
mk.move(x = 10)
mk.off(1)
```

---
#### Makergear M2 Pressure Control System (M2PCS) specific functions
##### M3 - M8
**on**(*channel*): Turns pneumatic channel ON \
**off**(*channel*): Turns pneumatic channel OFF
```python
mk.on(1)
mk.move(x = 10)
mk.off(1)
```

**set_channel_delay**(*delay=50*): sets the delay time (in ms) between a channel turning on and the execution of another command. Can be used to fine tune under extrusion effects, depending on ink viscosity.
```python
mk.set_channel_delay(delay = 50)
mk.on(3)
mk.move(x = 10)
mk.move(x = -10)
mk.off(3)
```

#### Simultaneous functions
**allon**(): Turns all three pneumatic channels ON \
**alloff**(): Turns all three pneumatic channels OFF
 ```python
mk.allon()
mk.move(x = 10)
mk.alloff()
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