#[M2PCS] Movement Tool
from tkinter import Tk, Label, Button, Entry, DoubleVar
from tkinter.ttk import Combobox
import serial.tools.list_ports
import m2py_old as mp


window = Tk()
window.title('[M2PCS] Movement Tool')
window.geometry('640x415')

xcoord = DoubleVar()
ycoord = DoubleVar()
zcoord = DoubleVar()

lbl_xy = Label(text = 'X/Y', font = ('Courier New',12))
lbl_xy.grid(column = 1, row = 1)

btn_yp = Button(text = '↑', font = ('Courier New',18), bg = 'light blue', state = 'disabled')
btn_yp.grid(column = 1, row = 0, pady = (20, 0))

btn_ym = Button(text = '↓', font = ('Courier New',18), bg = 'light blue', state = 'disabled')
btn_ym.grid(column = 1, row = 2)

btn_xp = Button(text = '→', font = ('Courier New',18), bg = 'light blue', state = 'disabled')
btn_xp.grid(column = 2, row = 1)

btn_xm = Button(text = '←', font = ('Courier New',18), bg = 'light blue', state = 'disabled')
btn_xm.grid(column = 0, row = 1, padx = (20, 0))

lbl_z = Label(text = 'Z', font = ('Courier New',12))
lbl_z.grid(column = 0, row = 6, sticky = 'E', rowspan = 2)

btn_zp = Button(text = '↑', font = ('Courier New',18), bg = 'light green', state = 'disabled')
btn_zp.grid(column = 1, row = 6)

btn_zm = Button(text = '↓', font = ('Courier New',18), bg = 'light green', state = 'disabled')
btn_zm.grid(column = 1, row = 7)

lbl_x = Label(text = 'X:', font = ('Courier New',12))
lbl_x.grid(column = 3, row = 3)
entry_x = Entry(fg = 'red', width = 6)
entry_x.insert(0, '***')
entry_x.grid(column = 4, row = 3)
lbl_xpm = Label(text = '±:', font = ('Courier New',12))
lbl_xpm.grid(column = 5, row = 3)
combo_xpm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100), state = 'disabled')
combo_xpm.grid(column = 6, row = 3)
combo_xpm.current(3)

lbl_y = Label(text = 'Y:', font = ('Courier New',12))
lbl_y.grid(column = 3, row = 4)
entry_y = Entry(fg = 'red', width = 6)
entry_y.insert(0, '***')
entry_y.grid(column = 4, row = 4)
lbl_ypm = Label(text = '±:', font = ('Courier New',12))
lbl_ypm.grid(column = 5, row = 4)
combo_ypm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100), state = 'disabled')
combo_ypm.grid(column = 6, row = 4)
combo_ypm.current(3)

lbl_z = Label(text = 'Z:', font = ('Courier New',12))
lbl_z.grid(column = 3, row = 5)
entry_z = Entry(fg = 'red', width = 6)
entry_z.insert(0, '***')
entry_z.grid(column = 4, row = 5)
lbl_zpm = Label(text = '±:', font = ('Courier New',12))
lbl_zpm.grid(column = 5, row = 5)
combo_zpm = Combobox(width = 6, values = (0.1, 0.5, 1, 5, 10, 20, 50, 100), state = 'disabled')
combo_zpm.grid(column = 6, row = 5)
combo_zpm.current(3)

#Channel Control Buttons
btn_ch1 = Button(text = 'CH 1', font = ('Courier New',12), state = 'disabled', relief = 'raised', bg = 'lightgray')
btn_ch1.grid(row = 6, column = 7)

btn_ch2 = Button(text = 'CH 2', font = ('Courier New',12), state = 'disabled', relief = 'raised', bg = 'lightgray')
btn_ch2.grid(row = 6, column = 8)

btn_ch3 = Button(text = 'CH 3', font = ('Courier New',12), state = 'disabled', relief = 'raised', bg = 'lightgray')
btn_ch3.grid(row = 6, column = 9)

btn_allon = Button(text = 'ALL ON', font = ('Courier New',12), state = 'disabled', relief = 'raised', bg = 'lightgray')
btn_allon.grid(row = 5, column = 8)

btn_alloff = Button(text = 'ALL OFF', font = ('Courier New',12), state = 'disabled', relief = 'raised', bg = 'lightgray')
btn_alloff.grid(row = 7, column = 8)


#Homing Buttons
btn_home_all = Button(text = 'Home All', font = ('Courier New',12), state = 'disabled', bg = 'lightgray')
btn_home_all.grid(column = 7, row = 0, columnspan = 3)

btn_home_x = Button(text = 'Home X', font = ('Courier New',12), state = 'disabled', bg = 'lightgray')
btn_home_x.grid(column = 7, row = 1)

btn_home_y = Button(text = 'Home Y', font = ('Courier New',12), state = 'disabled', bg = 'lightgray')
btn_home_y.grid(column = 8, row = 1)

btn_home_z = Button(text = 'Home Z', font = ('Courier New',12), state = 'disabled', bg = 'lightgray')
btn_home_z.grid(column = 9, row = 1)

#COMPORT
lbl_com = Label(window, text = 'COMPORT: ****',font = ("Courier New", 8), fg = 'red')
lbl_com.grid(column = 0, row = 9, sticky = 'W', columnspan = 3, pady = (20, 0))
comm_data = serial.tools.list_ports.comports()
comm_list = []
for i in range(len(comm_data)):
    comm_list.append(comm_data[i].device)
comm_tuple = tuple(comm_list)
combo_com = Combobox(window, font = ("Courier New", 8))
combo_com.grid(column = 3, row = 9,columnspan = 3, padx = (10, 0))
combo_com['values'] = comm_tuple
btn_com_set = Button(window, text = 'SET', font = ("Courier New", 8), bg = 'lightgray')
btn_com_set.grid(column = 6, row = 9)

#SPEED
lbl_speed = Label(window, text = 'BAUDRATE: ****** BPS',font = ("Courier New", 8), fg = 'red')
lbl_speed.grid(column = 0, row = 10, sticky = 'W', columnspan = 3)
combo_speed = Combobox(window, font = ("Courier New", 8))
combo_speed.grid(column = 3, row = 10, columnspan = 3, padx = (10, 0))
combo_speed['values'] = (9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000)
combo_speed.current(5)
btn_speed_set = Button(window, text = 'SET', font = ("Courier New", 8), bg = 'lightgray')
btn_speed_set.grid(column = 6, row = 10)

btn_connect = Button(text = 'Connect', bg = 'lightgreen', font = ("Courier New", 20), state = 'disabled')
btn_connect.grid(column = 7, row = 9, columnspan = 3, rowspan = 2)

#FUNCTION DEFINITIONS

def set_com():
    global connect_status
    global comport
    comport = combo_com.get()
    lbl_com.configure(text = 'COMPORT: {}'.format(comport), fg = 'blue')
    btn_connect.configure(text = 'Connect', bg = 'lightgreen', font = ("Courier New", 20), command = lambda: connect(), state = 'normal')
btn_com_set.config(command = set_com)

#SET SPEED
def set_speed():
    global speed
    speed = combo_speed.get()
    lbl_speed.configure(text = 'BAUDRATE: {} BPS'.format(speed), fg = 'blue')    
btn_speed_set.config(command = set_speed)

def connect():
    global connect_status
    global mg
    global comport
    global speed
    mg = mp.mopen(comport, speed)
    mp.coord(mg, coord = 'rel')
    mp.delay_set(mg, delay = 1)
    connect_status = 1
    btn_connect.configure(text = 'Disconnect', bg = 'salmon', font = ("Courier New", 20), command = lambda: disconnect())
    btn_xp.configure(state = 'normal')
    btn_xm.configure(state = 'normal')
    btn_yp.configure(state = 'normal')
    btn_ym.configure(state = 'normal')
    btn_zp.configure(state = 'normal')
    btn_zm.configure(state = 'normal')
    btn_home_all.configure(state = 'normal')
    btn_home_x.configure(state = 'normal')
    btn_home_y.configure(state = 'normal')
    btn_home_z.configure(state = 'normal')
    combo_xpm.configure(state = 'normal')
    combo_ypm.configure(state = 'normal')
    combo_zpm.configure(state = 'normal')
    btn_ch1.configure(state = 'normal')
    btn_ch2.configure(state = 'normal')
    btn_ch3.configure(state = 'normal')
    btn_allon.configure(state = 'normal')
    btn_alloff.configure(state = 'normal')
    
def disconnect():
    global connect_status
    global mg
    mp.mclose(mg)
    connect_status = 0
    btn_connect.configure(text = 'Connect', bg = 'lightgreen', font = ("Courier New", 20), command = lambda: connect())

def home(axes = ''):
    global mg
    mp.home(mg, axes = axes)
    
    if axes == 'X Y Z':
        xcoord.set(0.0)
        ycoord.set(0.0)
        zcoord.set(0.0)
    elif axes == 'X':
        xcoord.set(0.0)
    elif axes == 'Y':
        ycoord.set(0.0)
    elif axes == 'Z':
        zcoord.set(0.0)
    
    entry_x.configure(textvariable = xcoord, fg = 'black')
    entry_y.configure(textvariable = ycoord, fg = 'black')
    entry_z.configure(textvariable = zcoord, fg = 'black')
        
btn_home_all.configure(command = lambda: home('X Y Z'))
btn_home_x.configure(command = lambda: home('X'))
btn_home_y.configure(command = lambda: home('Y'))
btn_home_z.configure(command = lambda: home('Z'))

def update_coord(dx = 0, dy = 0, dz = 0):
    global mg
    mp.move(mg, x = dx, y = dy, z = dz)
    xcoord.set(round(xcoord.get() + float(dx), 1))
    ycoord.set(round(ycoord.get() + float(dy), 1))
    zcoord.set(round(zcoord.get() + float(dz), 1))
    entry_x.configure(textvariable = xcoord, fg = 'black')
    entry_y.configure(textvariable = ycoord, fg = 'black')
    entry_z.configure(textvariable = zcoord, fg = 'black')
    
btn_xp.configure(command = lambda: update_coord(dx = combo_xpm.get()))
btn_xm.configure(command = lambda: update_coord(dx = -float(combo_xpm.get())))
btn_yp.configure(command = lambda: update_coord(dy = combo_ypm.get()))
btn_ym.configure(command = lambda: update_coord(dy = -float(combo_ypm.get())))
btn_zp.configure(command = lambda: update_coord(dz = -float(combo_zpm.get())))
btn_zm.configure(command = lambda: update_coord(dz = combo_zpm.get()))

def channel_on(channels = 0):
    global mg
    if channels == 1:
        mp.ch1on(mg)
        btn_ch1.configure(relief = 'sunken', command = lambda: channel_off(channels = 1))
    elif channels == 2:
        mp.ch2on(mg)
        btn_ch2.configure(relief = 'sunken', command = lambda: channel_off(channels = 2))
    elif channels == 3:
        mp.ch3on(mg)
        btn_ch3.configure(relief = 'sunken', command = lambda: channel_off(channels = 3))
    elif channels == 4:
        mp.allon(mg)
        btn_ch1.configure(relief = 'sunken', command = lambda: channel_off(channels = 1))
        btn_ch2.configure(relief = 'sunken', command = lambda: channel_off(channels = 2))
        btn_ch3.configure(relief = 'sunken', command = lambda: channel_off(channels = 3))
        
def channel_off(channels = 0):
    global mg
    if channels == 1:
        mp.ch1off(mg)
        btn_ch1.configure(relief = 'raised', command = lambda: channel_on(channels = 1))
    elif channels == 2:
        mp.ch2off(mg)
        btn_ch2.configure(relief = 'raised', command = lambda: channel_on(channels = 2))
    elif channels == 3:
        mp.ch3off(mg)
        btn_ch3.configure(relief = 'raised', command = lambda: channel_on(channels = 3))
    elif channels == 4:
        mp.alloff(mg)
        btn_ch1.configure(relief = 'raised', command = lambda: channel_on(channels = 1))
        btn_ch2.configure(relief = 'raised', command = lambda: channel_on(channels = 2))
        btn_ch3.configure(relief = 'raised', command = lambda: channel_on(channels = 3))

btn_ch1.configure(command = lambda: channel_on(channels = 1))
btn_ch2.configure(command = lambda: channel_on(channels = 2))
btn_ch3.configure(command = lambda: channel_on(channels = 3))
btn_allon.configure(command = lambda: channel_on(channels = 4))
btn_alloff.configure(command = lambda: channel_off(channels = 4))
        
window.mainloop()