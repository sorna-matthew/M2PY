#[M2PCS] GCode Tool
from tkinter import Tk, Label, Button, Entry
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
import m2py_old as mp
import serial.tools.list_ports
import os

window = Tk()
window.title('[M2PCS] GCode Tool')
window.geometry('400x110')

#COMPORT
lbl_com = Label(window, text = 'COMPORT: ****',font = ("Courier New", 8), fg = 'red')
lbl_com.grid(column = 0, row = 0, sticky = 'W')
comm_data = serial.tools.list_ports.comports()
comm_list = []
for i in range(len(comm_data)):
    comm_list.append(comm_data[i].device)
comm_tuple = tuple(comm_list)
combo_com = Combobox(window, font = ("Courier New", 8))
combo_com.grid(column = 1, row = 0)
combo_com['values'] = comm_tuple
btn_com_set = Button(window, text = 'SET', font = ("Courier New", 8), bg = 'lightgray')
btn_com_set.grid(column = 2, row = 0)

#SPEED
lbl_speed = Label(window, text = 'BAUDRATE: ****** BPS',font = ("Courier New", 8), fg = 'red')
lbl_speed.grid(column = 0, row = 1, sticky = 'W')
combo_speed = Combobox(window, font = ("Courier New", 8))
combo_speed.grid(column = 1, row = 1)
combo_speed['values'] = (9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000)
combo_speed.current(5)
btn_speed_set = Button(window, text = 'SET', font = ("Courier New", 8), bg = 'lightgray')
btn_speed_set.grid(column = 2, row = 1)

#OPEN FILE
btn_open_file = Button(window, text = 'Open File',font = ("Courier New", 8), bg = 'lightgray')
btn_open_file.grid(column = 0, row = 2)
entry_file_directory = Entry(window, width = 30, font = ("Courier New", 8))
entry_file_directory.grid(column = 1, row = 2, rowspan = 2, sticky = 'W')

#READ FILE
btn_read_file = Button(window, text = 'Print File',font = ("Courier New", 8), state = 'disabled', bg = 'lightgray')
btn_read_file.grid(column = 0, row = 3)

#FUNCTION DEFINITIONS
def set_com():
    global comport
    comport = combo_com.get()
    lbl_com.configure(text = 'COMPORT: {}'.format(comport), fg = 'blue')
btn_com_set.config(command = set_com)

#SET SPEED
def set_speed():
    global speed
    speed = combo_speed.get()
    lbl_speed.configure(text = 'BAUDRATE: {} BPS'.format(speed), fg = 'blue')    
btn_speed_set.config(command = set_speed)

def open_file():
    global file_dir
    current_cwd = os.getcwd()
    file_dir = askopenfilename(initialdir = current_cwd, title = "Select GCode File",filetypes = (("Text files","*.txt"),("GCode files","*.gcode"),("All files","*.*")))
    entry_file_directory.insert(0, file_dir)
    btn_read_file.config(state = 'active')
btn_open_file.config(command = open_file)

def print_file():
    global file_dir
    global comport
    global speed
    mp.file_read(fid = file_dir, com = comport, baud = speed)
btn_read_file.config(command = print_file)

window.mainloop()