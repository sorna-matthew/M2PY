def generate_gcode(channel, route_xy, layer_thickness, gcode_rel, subdir_output, curr_layer, file):
    if gcode_rel: # relative coordinates
        gcode = []
        gcode.append('G91')
    
        for idxi, i in enumerate(route_xy):
            for idxii, ii in enumerate(i):
                if idxii == 0:
                    gcode.append('G1 X' + str(route_xy[0][0][0]) + ' Y' + str(route_xy[0][0][2]))
                    gcode.append('M{}'.format(channel*2 + 1))
                    gcode.append('G1 X' + str(ii[1]-ii[0]) + ' Y' + str(ii[3]-ii[2]))
                else:
                    gcode.append('G1 X' + str(ii[1]-route_xy[idxi][idxii-1][1]) + ' Y' + str(ii[3]-route_xy[idxi][idxii-1][3]))
            if (len(route_xy) > 1 and idxi != len(route_xy)-1):
                gcode.append('G1 X' + str(route_xy[idxi+1][0][0]-ii[1]) + ' Y' + str(route_xy[idxi+1][0][2]-ii[3]) + 'Z' + str(layer_thickness))
    else: # absolute coordinates
        gcode = []
        gcode.append('G90')
        for idxi, i in enumerate(route_xy):
            gcode.append('G1 X' + str(i[0][0]) + ' Y' + str(i[0][2]))
            for ii in i:
                gcode.append('G1 X' + str(ii[1]) + ' Y' + str(ii[3]))
            if idxi != len(route_xy)-1:
                gcode.append('G1 Z' + str(layer_thickness*(idxi+1)))

    gcode.append('M{}'.format(channel*2 + 2))
    gcode.append('G1 X-' + str(route_xy[0][-1][1]) + ' Y-' + str(route_xy[0][-1][3]))
    import os
    f=open(os.path.splitext(os.path.dirname(os.path.realpath(__file__)) + "\\" + subdir_output +"\\"  + os.path.basename(file))[0] + '_' + str(curr_layer) + '.cnc','w') 
    for i in gcode: 
        f.write(i + '\n') 
    f.close()

    return gcode