import m2py as mp

num_body_layers = 37
num_support_layers = 17

with open('D:\\M2PY\\trunk\\JM_slicer\\output\\Size3_all2.txt', 'w') as f_all:
    f_all.write('G28\n')
    f_all.write('G91\n')
    f_all.write('G1 F750\n')
    f_all.write('G1 X50 Y50 Z-74.6\n')
    for i in range(num_body_layers):
        fileid = 'D:\\M2PY\\trunk\\JM_slicer\\output\\Size3_body2_{}.cnc'.format(i)
        f1 = open(fileid, 'r')
        for line in f1:
            f_all.write(line)
        f1.close()
        
        if i <= (num_support_layers-1):
            fileid = 'D:\\M2PY\\trunk\\JM_slicer\\output\\Size3_support2_{}.cnc'.format(i)
            f2 = open(fileid, 'r')
            for line in f2:
                f_all.write(line)
            f2.close()
            
fileid = 'D:\\M2PY\\trunk\\JM_slicer\\output\\Size3_all2.txt'
#mp.file_read(fileid, 'COM3',115200, -36.1, 0)