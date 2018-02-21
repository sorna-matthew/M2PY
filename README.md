# M2-Python
*Control of the Makergear M2 3D printer using Python*

---

This project allows for the direct control of [Makergear's M2 3D printer](https://www.makergear.com/products/m2) using the [pyserial](https://pythonhosted.org/pyserial/) package for Python, specifically in the Anaconda environment: [https://anaconda.org/](https://anaconda.org/)

---
**m2py** *(a Python module)*
---
#### Basic Commands 
* **m2py.mopen**(*com*, *baud*): opens the specified com port, and returns a serial object, `ser`, which must be used in all other m2py function calls.
```python
import m2py as mp
makergear = mp.mopen('COM3',115200)
```
* **m2py.mclose**(*ser*): closes the specified serial object.

```python
import m2py as mp
makergear = mp.mopen('COM3', 115200)
mp.mclose(makergear)
```
* **m2py.move**(*ser*, *x =*, *y =*, *z =*): moves to the specified point, keeping in mind the coordinate system (relative / absolute).

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.move(makergear, x = 10, y = -5) # x, y, z arguments are all keyword arguments, and default to 0 when not called
mp.mclose(makergear)
```
* **m2py.speed**(*ser*, *speed*): sets the movement speed of the printer to the specified speed in [mm/s].

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.speed(makergear, 2400) # sets the movement speed of the printer to 2400 mm/s
mp.mclose(makergear)
```
* **m2py.home**(*ser*, *axes* = ): homes the specified axes. If none are specifically provided, X, Y & Z are all homed.

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.home(makergear, axes = 'X Y Z') # homes all three axes
mp.home(makergear) # homes all three axes
mp.home(makergear, axes = 'X Z') # homes only the specified axes
mp.mclose(makergear)
```
* **m2py.coord**(*ser*, *coord* = ): sets the coordinate system of the printer (relative or absolute).

```python
import m2py as mp
makgergear = mp.mopen('COM3',115200)
mp.coord(makergear, coord = 'abs') # sets coordinate system to absolute
mp.coord(makergear, coord = 'rel') # sets coordinate system to relative
mp.mclose(makergear)
```
###### Example code of basic commands:
```python
import m2py as mp

makergear = mp.mopen('COM7',115200)
mp.speed(makergear, 2400)
mp.home(makergear)
mp.coord(makergear, coord = 'rel')
mp.coord(makergear, coord = 'abs')
mp.move(makergear)
mp.move(makergear, x = 10)
mp.move(makergear, x = 10, y = 20, z = -5)
mp.move(makergear, z = -20)
mp.speed(makergear, 1600)
mp.home(makergear, 'X Y')
mp.mclose(makergear)
```
---
#### Advanced Commands 
* **m2py.prompt**(*com*, *baud*): allows for quick, native GCode serial communication with the M2, provided that the proper com port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type `exit` in the IPython console.
```python
import m2py as mp
mp.prompt('COM3',115200)
```
* **m2py.fileread**(*fid*, *com*, *baud*): reads in a text file of GCode line by line, and waits for the M2 to acknowledge that it received the command before sending another, maintaining print accuracy.
```python
import m2py
mp.fread('C:/Users/Matthew/Documents/m2-python/trunk/print paths/test_path.txt','COM3',115200)
```
---
