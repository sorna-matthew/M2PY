output_directory = 'D:\\M2PY\\trunk\\JM_slicer\\output\\'
output_filename = 'A_all'
num_body_layers = 1
body_base_filename = 'A'
support = False
num_support_layers = 13
support_base_filename = 'test_cone_support'

with open('{}{}.txt'.format(output_directory, output_filename), 'w') as f_all:
    f_all.write('G28\n')
    f_all.write('G91\n')
    f_all.write('G1 F750\n') # Specify printing speed in mm/s * 60
    f_all.write('G1 X50 Y50 Z-74.1\n') # Specify starting location relative to fully homed position
    for i in range(num_body_layers):
        fileid = '{}{}_{}.cnc'.format(output_directory, body_base_filename, i)
        f1 = open(fileid, 'r')
        for line in f1:
            f_all.write(line)
        f1.close()
        
        if support:
            if i <= (num_support_layers-1):
                fileid = '{}{}_{}.cnc'.format(output_directory, support_base_filename, i)
                f2 = open(fileid, 'r')
                for line in f2:
                    f_all.write(line)
                f2.close()