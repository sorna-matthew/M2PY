file = 'C:/Users/University of Penn/Desktop/size3_body4_pre.gcode'
file2 = 'C:/Users/University of Penn/Desktop/size3_body4_post.gcode'

flag = 0
with open(file2, 'w') as f_all:
    with open(file, "r") as gcode:
            for line in gcode:
                if flag == 0:
                    f_all.write(line)
                else:
                    split = line.split(' ')
                    if split[4][1] == '7':
                        f_all.write('M5\n')
                    elif split[4][1] == '1':
                        f_all.write('M3\n')
                    flag = 0
            
                if line == 'G1 E-0.5000 F1500\n':
                    flag = 1
                
                
#%%    
import m2py as mp
mp.file_read(file2, 'COM3', 115200, 0, 0)

