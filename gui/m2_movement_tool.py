#[M2PCS] GCode Tool
from tkinter import Tk, Label, Button, Entry
from tkinter.ttk import Combobox
import m2py as mp


window = Tk()
window.title('[M2PCS] Movement Tool')
window.geometry('400x600')

btn_yp = Button(text = '↑', font = ('Courier New',18), bg = 'light blue')
btn_yp.grid(column = 1, row = 0)

btn_ym = Button(text = '↓', font = ('Courier New',18), bg = 'light blue')
btn_ym.grid(column = 1, row = 2)

btn_xp = Button(text = '→', font = ('Courier New',18), bg = 'light blue')
btn_xp.grid(column = 2, row = 1)

btn_xm = Button(text = '←', font = ('Courier New',18), bg = 'light blue')
btn_xm.grid(column = 0, row = 1)

btn_zp = Button(text = '↑', font = ('Courier New',18), bg = 'light green')
btn_zp.grid(column = 1, row = 6)

btn_zm = Button(text = '↓', font = ('Courier New',18), bg = 'light green')
btn_zm.grid(column = 1, row = 8)

lbl_x = Label(text = 'X:', font = ('Courier New',12))
lbl_x.grid(column = 3, row = 3)
entry_x = Entry(fg = 'red', width = 6)
entry_x.insert(0, '***')
entry_x.grid(column = 4, row = 3)
lbl_xpm = Label(text = '±:', font = ('Courier New',12))
lbl_xpm.grid(column = 5, row = 3)
combo_xpm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100))
combo_xpm.grid(column = 6, row = 3)
combo_xpm.current(3)

lbl_y = Label(text = 'Y:', font = ('Courier New',12))
lbl_y.grid(column = 3, row = 4)
entry_y = Entry(fg = 'red', width = 6)
entry_y.insert(0, '***')
entry_y.grid(column = 4, row = 4)
lbl_ypm = Label(text = '±:', font = ('Courier New',12))
lbl_ypm.grid(column = 5, row = 4)
combo_ypm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100))
combo_ypm.grid(column = 6, row = 4)
combo_ypm.current(3)

lbl_z = Label(text = 'Z:', font = ('Courier New',12))
lbl_z.grid(column = 3, row = 5)
entry_z = Entry(fg = 'red', width = 6)
entry_z.insert(0, '***')
entry_z.grid(column = 4, row = 5)
lbl_zpm = Label(text = '±:', font = ('Courier New',12))
lbl_zpm.grid(column = 5, row = 5)
combo_zpm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100))
combo_zpm.grid(column = 6, row = 5)
combo_zpm.current(3)

#Homing Buttons
btn_home_all = Button(text = 'Home All')
btn_home_all.grid(column = 7, row = 0)

btn_home_x = Button(text = 'Home X')
btn_home_x.grid(column = 7, row = 1)

btn_home_y = Button(text = 'Home Y')
btn_home_y.grid(column = 7, row = 2)

btn_home_z = Button(text = 'Home Z')
btn_home_z.grid(column = 7, row = 3)
#FUNCTION DEFINITIONS


window.mainloop()