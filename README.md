# M2-Python
*Control of the Makergear M2 3D printer using Python*

---

This project allows for the direct control of [Makergear's M2 3D printer](https://www.makergear.com/products/m2) using the [pyserial](https://pythonhosted.org/pyserial/) package for Python, specifically in the Anaconda environment: [https://anaconda.org/](https://anaconda.org/)

---
**m2py** *(a Python module)*
*function descriptions*:
* **m2py.prompt**(*COM*, *BAUD*): allows for quick serial communication with the M2, provided that the proper COM port and baud rate are selected, and match what is found in system settings. To exit the command prompt environment, just type `exit` in the IPython console.
```python
import m2py
m2py.prompt('COM3',115200)
```
* **m2py.fread**(*fid*, *COM*, *BAUD*): reads in a text file of gcode line by line, and waits for the M2 to acknowledge that it received the command before sending another, maintaining print accuracy.
```python
import m2py
m2py.fread('C:/Users/Matthew/Documents/m2-python/trunk/print paths/test_path.txt','COM3',115200)
```
---
