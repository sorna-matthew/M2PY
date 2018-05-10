from tkinter import Tk, Label, Button, Entry
import m2py as mp

global mg
mg = ''

window = Tk()
window.title('Makergear M2 Pneumatic Control System GUI')
window.geometry('845x230')

lbl_title = Label(window, text = 'Makergear M2', font = ("Arial Bold", 10))
lbl_title.grid(column = 0, row = 0)
lbl_title2 = Label(window, text = 'Pneumatic Control System', font = ("Arial Bold", 10))
lbl_title2.grid(column = 0, row = 1)

lbl_com = Label(window, text = 'COMPORT: ###',font = ("Arial", 10), fg = 'red')
lbl_com.grid(column = 0, row = 2)
entry_com = Entry(window, width = 10)
entry_com.grid(column= 1, row = 2)
btn_com_set = Button(window, text = 'SET')
btn_com_set.grid(column = 2, row = 2)

lbl_speed = Label(window, text = 'BAUDRATE: ### bps',font = ("Arial", 10), fg = 'red')
lbl_speed.grid(column = 0, row = 3)
entry_speed = Entry(window, width = 10)
entry_speed.grid(column= 1, row = 3)
btn_speed_set = Button(window, text = 'SET')
btn_speed_set.grid(column = 2, row = 3)

btn_connect = Button(window, bg = 'green', text = 'CONNECT')
btn_connect.grid(column = 3, row = 3)
    
#Homing buttons
lbl_home = Label(window, text = 'HOMING:',font = ("Arial", 10))
lbl_home.grid(column = 0, row = 4)
btn_homeall= Button(window, text='Home All Axes', bg = 'light gray')
btn_homex= Button(window, text='Home X Axis', bg = 'light gray')
btn_homey= Button(window, text='Home Y Axis', bg = 'light gray')
btn_homez= Button(window, text='Home Z Axis', bg = 'light gray')
btn_homeall.grid(column=1, row=4)
btn_homex.grid(column=2, row=4)
btn_homey.grid(column=3, row=4)
btn_homez.grid(column=4, row=4)

#Coordinate system buttons
lbl_coord_sys = Label(window, text = 'COORD SYS:',font = ("Arial", 10))
lbl_coord_sys.grid(column = 0, row = 5)
btn_rel = Button(window, text='Relative', bg = 'light gray')
btn_rel.grid(column = 1, row = 5)
btn_abs = Button(window, text='Absolute', bg = 'light gray')
btn_abs.grid(column = 2, row = 5)

lbl_manual_move = Label(window, text = 'MOVE:', font = ("Arial", 10))
lbl_manual_move.grid(column = 0, row = 6)

lbl_dx = Label(window, text = 'dx', font = ("Arial", 10))
lbl_dx.grid(column = 1, row = 6)
entry_dx = Entry(window, width = 4)
entry_dx.insert(0, '10')
entry_dx.grid(column = 2, row = 6)

lbl_dy = Label(window, text = 'dy', font = ("Arial", 10))
lbl_dy.grid(column = 1, row = 7)
entry_dy = Entry(window, width = 4)
entry_dy.insert(0, '10')
entry_dy.grid(column = 2, row = 7)

lbl_dz = Label(window, text = 'dz', font = ("Arial", 10))
lbl_dz.grid(column = 1, row = 8)
entry_dz = Entry(window, width = 4)
entry_dz.insert(0, '10')
entry_dz.grid(column = 2, row = 8)

# Manual movement buttons
#Up

lbl_xy_space = Label(window, text = '        ')
lbl_xy_space.grid(column = 6, row = 5)

btn_up = Button(window, text = ' ^ ', bg = 'cyan')
btn_up.grid(column = 7, row = 4)
#Down
btn_down = Button(window, text = ' v ', bg = 'cyan')
btn_down.grid(column = 7, row = 6)
#Left
btn_left = Button(window, text = ' < ', bg = 'cyan')
btn_left.grid(column = 6, row = 5)
#Right
btn_right = Button(window, text = ' > ', bg = 'cyan')
btn_right.grid(column = 8, row = 5)

lbl_xy = Label(window, text = 'X/Y')
lbl_xy.grid(column = 7, row = 5)

btn_zup = Button(window, text = ' ^ ', bg = 'cyan')
btn_zup.grid(column = 12, row = 4)

lbl_zspace = Label(window, text = '       ')
lbl_zspace.grid(column = 11, row = 5)

lbl_z = Label(window, text = 'Z')
lbl_z.grid(column = 12, row = 5)

btn_zdown = Button(window, text = ' v ', bg = 'cyan')
btn_zdown.grid(column = 12, row = 6) 

#Coordinate location label
lbl_coords = Label(window, text = '    Current coordinates: (#, #, #)', font = ("Arial Bold", 10), fg = 'red')
lbl_coords.grid(column = 13, row = 5)

#SET COMPORT
def set_com():
    global xcoord
    xcoord = 0
    global ycoord
    ycoord = 0
    global zcoord
    zcoord = 0
    global comport
    comport = entry_com.get()
    lbl_com.configure(text = 'COMPORT: {}'.format(comport), fg = 'blue')
btn_com_set.config(command = set_com)

#SET SPEED
def set_speed():
    global speed
    speed = entry_speed.get()
    lbl_speed.configure(text = 'BAUDRATE: {} bps'.format(speed), fg = 'blue')    
btn_speed_set.config(command = set_speed)

def home_all():
    global mg
    global xcoord
    global ycoord
    global zcoord
    xcoord = 0
    ycoord = 0
    zcoord = 0
    mp.home(mg, axes = 'X Y Z')
    lbl_coords.configure(text = '    Current coordinates: ({}, {}, {})'.format(xcoord, ycoord, zcoord), fg = 'blue')
btn_homeall.config(command = home_all)

def home_x():
    global xcoord
    global ycoord
    global zcoord
    global mg
    xcoord = 0
    mp.home(mg, axes = 'X')
    lbl_coords.configure(text = '    Current coordinates: ({}, {}, {})'.format(xcoord, ycoord, zcoord), fg = 'blue')
btn_homex.config(command = home_x)

def home_y():
    global xcoord
    global ycoord
    global zcoord
    global mg
    ycoord = 0
    mp.home(mg, axes = 'Y')
    lbl_coords.configure(text = '    Current coordinates: ({}, {}, {})'.format(xcoord, ycoord, zcoord),fg = 'blue')
btn_homey.config(command = home_y)

def home_z():
    global xcoord
    global ycoord
    global zcoord
    global mg
    zcoord = 0
    mp.home(mg, axes = 'Z')
    lbl_coords.configure(text = '    Current coordinates: ({}, {}, {})'.format(xcoord, ycoord, zcoord),fg = 'blue')
btn_homez.config(command = home_z)

def set_coord_system(coord_sys = 'abs'):
    global mg
    mp.coord(mg, coord = coord_sys)
    
    if coord_sys == 'abs':
        btn_abs.config(bg = 'blue')
        btn_rel.config(bg = 'light gray')
    elif coord_sys == 'rel':
        btn_rel.config(bg = 'blue')
        btn_abs.config(bg = 'light gray')
btn_abs.config(command = lambda: set_coord_system(coord_sys = 'abs'))
btn_rel.config(command = lambda: set_coord_system(coord_sys = 'rel'))

#CONNECT PRINTER
def connect_printer():
    global status
    global comport
    global speed
    global mg
    status = 1
    mg = mp.mopen(com = comport, baud = int(speed))
    mp.coord(mg, coord = 'rel')
    btn_connect.config(text = 'DISCONNECT', command = disconnect_printer, bg = 'red')
btn_connect.config(command = connect_printer)
    
#DISCONNECT PRINTER
def disconnect_printer():
    global status
    global mg
    status = 0
    mp.mclose(mg)
    btn_connect.config(bg = 'green', text = 'CONNECT',command = connect_printer)

def update_coords(dx = 0, dy = 0, dz = 0):
    global mg
    global xcoord
    global ycoord
    global zcoord
    
    if mg != '':
        mp.move(mg, x = dx, y = dy, z = dz)
        xcoord = xcoord + dx
        ycoord = ycoord + dy
        zcoord = zcoord + dz
        lbl_coords.configure(text = '    Current coordinates: ({}, {}, {})'.format(xcoord, ycoord, zcoord), fg = 'blue')
    
btn_up.configure(command = lambda: update_coords(dy = int(entry_dy.get())))
btn_down.configure(command = lambda: update_coords(dy = -int(entry_dy.get())))
btn_right.configure(command = lambda: update_coords(dx = int(entry_dx.get())))
btn_left.configure(command = lambda: update_coords(dx = -int(entry_dx.get())))
btn_zup.configure(command = lambda: update_coords(dz = -int(entry_dz.get())))
btn_zdown.configure(command = lambda: update_coords(dz = int(entry_dz.get())))

window.mainloop()