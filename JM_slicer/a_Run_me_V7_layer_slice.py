# Slice STL
from __future__ import division
import sys
sys.dont_write_bytecode = True
def ucopy(inList):
    if isinstance(inList, list):
        return list( map(ucopy, inList) )
    return inList
from b_slice__main_V4 import command_line

'''
Initialization of 3D Printer
'''
import m2py_py27 as mp
mk = mp.Makergear('COM3',115200, printout = 0, verbose = True)
mk.speed(speed = 15)
mk.coord_sys(coord_sys = 'rel')
mk.home(axes = 'X Y Z')
mk.move(x = 25, y = 40, z = -82.7, track = 0)
mk.set_current_coords(x = 0, y = 0, z = 0)
dz = 0.4*0.85 # mm
linespace = 0.4 # mm

'''
BODY SLICING
'''
file = 'Size3_body3.stl' # Beats30x30x10   Country30x20x10   HolePlate50x20x10   Square30x30x10
file2 = 'Size3_support3.stl' # Beats30x30x10   Country30x20x10   HolePlate50x20x10   Square30x30x10
subdir_models = "models"
subdir_output = "output"
layer_thickness = dz
width = 46.1123205      # X
height = 46.103381999999996      # Y
scale = False # True means that the part is NOT being scaled
svg2 = False
dxf = False
verbose = False
quiet = False

xsize_b, ysize_b, paths_all_b = command_line(file, subdir_models, subdir_output, layer_thickness, width, height, scale, svg2, dxf, verbose, quiet)

'''
SUPPORT SLICING
'''
subdir_models = "models"
subdir_output = "output"
layer_thickness = dz
width = 37.060593      # X
height = 37.060347      # Y
scale = False # True means that the part is NOT being scaled
svg2 = False
dxf = False
verbose = False
quiet = False
# Support material XY resolution
linespace_s = 2 # mm

xsize_s, ysize_s, paths_all_s = command_line(file2, subdir_models, subdir_output, layer_thickness, width, height, scale, svg2, dxf, verbose, quiet)

num_layers = len(paths_all_b)

for curr_layer in range(num_layers):
    layer_path = [paths_all_b[curr_layer]]
    channel = 1
    # TSP settings
    depot = 0 # == starting point
    
    # Line search options
    endp = [False, 15, -2147483647]   # Status, endnode, distance to depot
    best_endp = [False, -2147483647]    # Find the best endpoint automatically, distance to depot
    kPenalty = 2147483647  # Penalty for all points. If penalty is lower than a specific distance, the point is skipped
    ind_layers = True     # Independent layers treats all layers individually: starting point independent of the previous layer. This option overrides the 'endp' option for all but the first [0] layer if False.
    best_start_and_end_pt = False    # Finds the best start and endpoint
    
    gcode_rel = True    # True: relative coordinates, False: absolute
    
    importance_init_dist = 1.5   # 0: all initial distances are equal, 1: actual initial distances, >1: increased effect. Switch completely off to show how the FDM process path would look like (lots of jumps - start/stops). Increase this value if "jumps" over large distances are discovered.
    dir_neighbor = 4       # Direct (hor/ver) neighbours. Multiplies all but the direct distances.
    indir_neighbor = 16      # Indirect (diagonal) neighbours. Multiplies all but the direct and indirect distances.
    cont_multiplier = 16     # multiplies each distance that is NOT a contour
    hor_multiplier = 50     # multiplies each distance that is NOT horizontal
    ver_multiplier = 2    # 1 multiplies each distance that is NOT vertical
    deleteallbut =  2   # 2 Delete all nodes but none (0), 2, 3, 4, or 5 near the edges. Only works with a high hor_multiplier
    shortendeldist = 10000000   # Decrease distance of the nodes to the left and right of deleted nodes to each other by x/factor. This factor is important when inner nodes away from the contour are selected.
    
    plotlayer = 0
    
    # Error/logic checks
    if endp[0] == True and ind_layers == False:
        sys.exit("CAUTION #1: If layers are dependent, selecting an end point doesn't make sense.")
    if endp[0] == True and best_endp[0] == True:
        sys.exit("CAUTION #2: If the best endpoint is searched, it cannot be specified.")
    if best_start_and_end_pt == True and ind_layers == False:
        sys.exit("CAUTION #3: Layers cannot be dependent if the starting point is searched automatically. It needs to be selected based on the previous layer.")
    if ind_layers == False and best_endp[0] == False:
        sys.exit("CAUTION #4: If layers are dependent, the best endpoint needs to be active.")
    if best_start_and_end_pt == True and best_endp[0] == True:
        sys.exit("CAUTION #5: If 'best start and end point' is selected, the search for the 'best endpoint' is already included.")
    if best_start_and_end_pt == True and endp[0] == True:
        sys.exit("CAUTION #6: If 'best start and end point' is selected, the endpoint will be found automatically and cannot be selected.")
    if best_start_and_end_pt == True and depot != 0:
        sys.exit("CAUTION #7: If 'best start and end point' is selected, the depot needs to be at '0'.")
    
    # Timer
    import time
    start_time = time.time()
    elapsed_time = ['Timer [s]']
    
    # Grid
    from c_grid import grid_overlay
    grid, min_x, max_x, min_y, max_y = grid_overlay(layer_path, linespace)
    max_x_body = max_x
    max_y_body = max_y
    
    elapsed_time.append('Grid: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()
    
    import numpy as np
    import scipy.spatial
    distances = []
    for idxi, i in enumerate(grid):
        a = np.array(grid[idxi])
        temp = scipy.spatial.distance.cdist(a,a)
    distances.append(temp.tolist())
    
    elapsed_time.append('Distances: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()   
    
    ''' ####################################################################### '''
    ''' Start of additional line fill algorithm '''
    ''' ####################################################################### '''
    
    rem_indices = []
    grid_del = [[] for i in range(len(grid))]
    for idxi, i in enumerate(grid):
        for idxii, ii in enumerate(i):
            ls1 = 1*linespace
            ls2 = 2*linespace
            ls3 = 3*linespace
            ls4 = 4*linespace
            ls5 = 5*linespace
            if deleteallbut == 2:
                if [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i:
                    rem_indices.append([idxi, idxii])
                    grid_del[idxi].append(grid[idxi][idxii])
            if deleteallbut == 3:
                if [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i:
                    rem_indices.append([idxi, idxii])
                    grid_del[idxi].append(grid[idxi][idxii])
            if deleteallbut == 4:
                if [round(ii[0]-ls4, 3), ii[1]] in i and [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i and [round(ii[0]+ls4, 3), ii[1]] in i:
                    rem_indices.append([idxi, idxii])
                    grid_del[idxi].append(grid[idxi][idxii])
            if deleteallbut == 5:
                if [round(ii[0]-ls5, 3), ii[1]] in i and [round(ii[0]-ls4, 3), ii[1]] in i and [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i and [round(ii[0]+ls4, 3), ii[1]] in i and [round(ii[0]+ls5, 3), ii[1]] in i:
                    rem_indices.append([idxi, idxii])
                    grid_del[idxi].append(grid[idxi][idxii])
    
    dist_multipl_rem_ends = []
    for i in distances:
        temp = []
        for ii in i:
            temp.append([1]*len(ii))
        dist_multipl_rem_ends.append(temp)
    
    for i in rem_indices:
        if [round(grid[i[0]][i[1]][0]-linespace, 3), grid[i[0]][i[1]][1]] not in grid_del[i[0]]:
            startpoint = i
            pointbeforestartpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]-linespace, 3), grid[i[0]][i[1]][1]])]
            count = 1
            currentpoint = startpoint 
            while [round(grid[i[0]][i[1]][0]+count*linespace, 3), grid[i[0]][i[1]][1]] in grid_del[i[0]]:
                currentpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]+count*linespace, 3), grid[i[0]][i[1]][1]])]
                count +=1
            endpoint = currentpoint 
            pointafterendpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]+count*linespace, 3), grid[i[0]][i[1]][1]])]
    
            dist_multipl_rem_ends[i[0]][pointbeforestartpoint[1]][pointafterendpoint[1]] = -shortendeldist
            dist_multipl_rem_ends[i[0]][pointafterendpoint[1]][pointbeforestartpoint[1]] = -shortendeldist
    
    for i in sorted(rem_indices, reverse=True):
        del grid[i[0]][i[1]]
        for idxj, j in enumerate(distances[i[0]]):
            del distances[i[0]][idxj][i[1]]
            del dist_multipl_rem_ends[i[0]][idxj][i[1]]
    
    for i in sorted(rem_indices, reverse=True):
        del distances[i[0]][i[1]]
        del dist_multipl_rem_ends[i[0]][i[1]]
    
    for idxi, i in enumerate(dist_multipl_rem_ends):
        for idxii, ii in enumerate(i):
            for idxiii, iii in enumerate(ii):
                if iii == 1:
                    dist_multipl_rem_ends[idxi][idxii][idxiii] = shortendeldist
                elif iii == -shortendeldist:
                    dist_multipl_rem_ends[idxi][idxii][idxiii] = 1
    
    ''' ------------------------------------- 
        End of additional line fill algorithm
        -------------------------------------   '''
    
    elapsed_time.append('Delete grid points: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()
    
    dist_multipl_neigh_dir = []
    dist_multipl_neigh_indir = []
    for i in distances:
        temp1 = []
        temp2 = []
        for ii in i:
            temp1.append([1]*len(ii))
            temp2.append([1]*len(ii))
        dist_multipl_neigh_dir.append(temp1)
        dist_multipl_neigh_indir.append(temp2)
    
    diag_dist = (2*linespace**2)**0.5 
    node_neighbours = []
    node_neighbours_vectors = []   
    for idxi, i in enumerate(distances):
        node_neighbours_temp1 = []
        node_neighbours_vectors_temp1 = []
        for idxii, ii in enumerate(i):
            node_neighbours_temp2 = []
            node_neighbours_vectors_temp2 = []
            x1 = grid[idxi][idxii][0]
            y1 = grid[idxi][idxii][1]
            for idxiii, iii in enumerate(ii):
                if (iii < diag_dist+0.001 and idxii != idxiii): 
                    node_neighbours_temp2.append(idxiii)
                    x2 = grid[idxi][idxiii][0]
                    y2 = grid[idxi][idxiii][1]
                    if (x2-x1)/linespace != 0:
                        temp_abs_x = (x2-x1)/linespace * abs((x2-x1)/linespace)**(-1)
                    else:
                        temp_abs_x = 0
                    if (y2-y1)/linespace != 0:
                        temp_abs_y = (y2-y1)/linespace * abs((y2-y1)/linespace)**(-1)   
                    else: 
                        temp_abs_y = 0
                    node_neighbours_vectors_temp2.append([temp_abs_x, temp_abs_y])
                if iii > linespace + 0.01:  # Direct neighbours; 
                    dist_multipl_neigh_dir[idxi][idxii][idxiii] *= dir_neighbor
                if iii > diag_dist+0.001:  # Indirect neighbours
                    dist_multipl_neigh_indir[idxi][idxii][idxiii] *= indir_neighbor
            node_neighbours_temp1.append(node_neighbours_temp2)
            node_neighbours_vectors_temp1.append(node_neighbours_vectors_temp2)
        node_neighbours.append(node_neighbours_temp1)
        node_neighbours_vectors.append(node_neighbours_vectors_temp1)
    
    elapsed_time.append('Modify distances of direct and indirect neighbours: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()
    
    ''' ################################# '''
    ''' CONTOUR, HORIZONTAL, and VERTICAL '''
    ''' ################################# '''
    
    dist_multipl_cont = []
    dist_multipl_dir_hor = []
    dist_multipl_dir_ver = []
    for i in distances:
        dist_multipl_cont_temp = []
        dist_multipl_dir_hor_temp = []
        dist_multipl_dir_ver_temp = []
        for ii in i:
            dist_multipl_cont_temp.append([cont_multiplier]*len(ii))
            dist_multipl_dir_hor_temp.append([hor_multiplier]*len(ii))
            dist_multipl_dir_ver_temp.append([ver_multiplier]*len(ii))
        dist_multipl_cont.append(dist_multipl_cont_temp)
        dist_multipl_dir_hor.append(dist_multipl_dir_hor_temp)
        dist_multipl_dir_ver.append(dist_multipl_dir_ver_temp)
    null_vectors = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1], [0,1]]
    del dist_multipl_cont_temp, dist_multipl_dir_hor_temp, dist_multipl_dir_ver_temp
    
    for idxi, i in enumerate(node_neighbours_vectors):
        for idxii, ii in enumerate(i):
            for idxj, j in enumerate(null_vectors[0:8]):
                if idxj != len(null_vectors)-1:
                    if (j in ii and null_vectors[idxj+1] not in ii):
                        ind_temp = node_neighbours[idxi][idxii][ii.index(j)]
                        dist_multipl_cont[idxi][idxii][ind_temp] = 1
                    elif (null_vectors[idxj+1] in ii and j not in ii):
                        ind_temp = node_neighbours[idxi][idxii][ii.index(null_vectors[idxj+1])]
                        dist_multipl_cont[idxi][idxii][ind_temp] = 1
            if [1,0] in ii:
                ind_temp = node_neighbours[idxi][idxii][ii.index([1,0])]
                dist_multipl_dir_hor[idxi][idxii][ind_temp] = 1
            if [-1,0] in ii:
                ind_temp = node_neighbours[idxi][idxii][ii.index([-1,0])]
                dist_multipl_dir_hor[idxi][idxii][ind_temp] = 1            
            if [0,1] in ii:
                ind_temp = node_neighbours[idxi][idxii][ii.index([0,1])]
                dist_multipl_dir_ver[idxi][idxii][ind_temp] = 1
            if [0,-1] in ii:
                ind_temp = node_neighbours[idxi][idxii][ii.index([0,-1])]
                dist_multipl_dir_ver[idxi][idxii][ind_temp] = 1
    
    dist_multipl_init_dist = []
    for idxi, i in enumerate(distances):
        temp1 = []
        for idxii, ii in enumerate(i):
            temp2 = []
            for idxiii, iii in enumerate(ii):
                if iii == 0:
                    temp2.append(1)
                else:
                    temp3 = (linespace+(distances[idxi][idxii][idxiii]-linespace)*importance_init_dist)/distances[idxi][idxii][idxiii]
                    temp2.append(temp3)
            temp1.append(temp2)
        dist_multipl_init_dist.append(temp1)
    
    for idxi, i in enumerate(distances):
        for idxii, ii in enumerate(i):
            for idxiii, iii in enumerate(ii):
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_rem_ends[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_neigh_dir[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_neigh_indir[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_cont[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_dir_hor[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_dir_ver[idxi][idxii][idxiii]
                distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_init_dist[idxi][idxii][idxiii]
    
    ''' ####################################################################### '''
    ''' Normalize list for TSP input '''
    ''' ####################################################################### '''
    maxval = 2147483647*0.1 # Max C++ long value
    for idxi, i in enumerate(distances):
        for idxii, ii in enumerate(i):
            distances[idxi][idxii] = [float(i)/max(distances[idxi][idxii])*maxval for i in distances[idxi][idxii]]
    
    elapsed_time.append('Contour: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()
    
    if endp[0] == True:
        for idxi, i in enumerate(distances):
            distances[idxi][endp[1]][depot] = endp[2]
    
    if best_start_and_end_pt:
        for idxi, i in enumerate(distances):
            distzero = [0]*len(i)
            distances[idxi].insert(0, distzero)
            for idxii, ii in enumerate(i):
                distances[idxi][idxii].insert(0, 0)
    
    def closest_node(node, nodes):
        nodes = np.asarray(nodes)
        dist_2 = np.sum((nodes - node)**2, axis=1)
        return np.argmin(dist_2)
        
    elapsed_time.append('Start and end points: ' + str(round(time.time()-start_time, 3)))
    start_time = time.time()
    
    ''' ####################################################################### '''
    ''' Run TSP solver '''
    ''' ####################################################################### '''
    route = []
    print '_________________________'
    for idxi, DistMatrix in enumerate(distances):
        if best_endp[0] == True:
            for idxii, ii in enumerate(DistMatrix):
                distances[idxi][idxii][depot] = best_endp[1]
        from d_TSP_V4 import TSP
        route_temp = TSP(DistMatrix, depot, kPenalty)
        if (endp[0] == True) or (best_endp[0] == True):
            del route_temp[-1]
        if (ind_layers == False and idxi != len(distances)-1):
            depot = closest_node(grid[idxi][route_temp[-1]], grid[idxi+1]) 
        route.append(route_temp)
        print 'Starting node: ' + str(route_temp[0])
        print 'Ending node: ' + str(route_temp[-1])
        print 'Number of nodes: ' + str(len(distances[idxi]))
        print '_________________________'
    
    elapsed_time.append('TSP solver: ' + str(round(time.time()-start_time, 3)))
    elapsed_time.append('_________________________')
    print("\n".join(elapsed_time))
    
    if best_start_and_end_pt:
        for idxi, i in enumerate(route):
            rem_idx = []
            for idxii, ii in enumerate(i):
                if ii == 0: 
                    rem_idx.append(idxii)
                else:
                    route[idxi][idxii] -= 1
            if len(rem_idx) > 0:
                for j in reversed(rem_idx):
                    del route[idxi][j]
    if best_start_and_end_pt:
        for idxi, i in enumerate(sorted(distances, reverse=True)):
            for idxj, j in enumerate(distances[idxi]):
                del distances[idxi][idxj][0]
        for idxi, i in enumerate(sorted(distances, reverse=True)):
            del distances[idxi][0]
    
    route_rem = []
    for idxi, i in enumerate(route):
        for idxii, ii in enumerate(i):
            if idxii != 0 and idxii != len(route[idxi])-1:
                coord_x_prev = grid[idxi][route[idxi][idxii-1]][0]
                coord_x_curr = grid[idxi][route[idxi][idxii]][0]
                coord_x_next = grid[idxi][route[idxi][idxii+1]][0]
                coord_y_prev = grid[idxi][route[idxi][idxii-1]][1]
                coord_y_curr = grid[idxi][route[idxi][idxii]][1]
                coord_y_next = grid[idxi][route[idxi][idxii+1]][1]
                if coord_x_prev == coord_x_curr == coord_x_next or coord_y_prev == coord_y_curr == coord_y_next:
                    route_rem.append([idxi, idxii])
    for i in sorted(route_rem, reverse=True):
        del route[i[0]][i[1]]
    
    route_xy = []
    for idxi, i in enumerate(route):
        route_xy_temp = []
        for ii in range(0, len(route[idxi])-1):
            x0 = grid[idxi][route[idxi][ii]][0]
            x1 = grid[idxi][route[idxi][ii+1]][0]
            y0 = grid[idxi][route[idxi][ii]][1]
            y1 = grid[idxi][route[idxi][ii+1]][1]
            route_xy_temp.append([x0, x1, y0, y1])
        route_xy.append(route_xy_temp)

    xi = route_xy[0][0][0]
    yi = route_xy[0][0][2]      

    mk.move(x = xi, y = yi)        
    
    for line in route_xy:
        mk.on(channel)
        for pts in line:
            mk.move(x = pts[1]-pts[0], y = pts[3]-pts[2])
        mk.off(channel)

    coords = mk.return_current_coords()
    print(coords)
    mk.move(x = -coords[0], y = -coords[1]) 
        
    from c_gcode import generate_gcode
    
    num_layers_s = len(paths_all_s)
    if curr_layer < num_layers_s:
        mk.move(x = (xsize_b - xsize_s)/2, y = (ysize_b - ysize_s)/2)
        channel = 1
        gcode = generate_gcode(route_xy, channel, False, 0, 0, 0, layer_thickness, gcode_rel, subdir_output, curr_layer, file)
        channel = 2
        
        layer_path = [paths_all_s[curr_layer]]
        # TSP settings
        depot = 0 # == starting point
        
        # Line search options
        endp = [False, 15, -2147483647]   # Status, endnode, distance to depot
        best_endp = [False, -2147483647]    # Find the best endpoint automatically, distance to depot
        kPenalty = 2147483647  # Penalty for all points. If penalty is lower than a specific distance, the point is skipped
        ind_layers = True     # Independent layers treats all layers individually: starting point independent of the previous layer. This option overrides the 'endp' option for all but the first [0] layer if False.
        best_start_and_end_pt = False    # Finds the best start and endpoint
        
        gcode_rel = True    # True: relative coordinates, False: absolute
        
        importance_init_dist = 1   # 0: all initial distances are equal, 1: actual initial distances, >1: increased effect. Switch completely off to show how the FDM process path would look like (lots of jumps - start/stops). Increase this value if "jumps" over large distances are discovered.
        dir_neighbor = 4       # Direct (hor/ver) neighbours. Multiplies all but the direct distances.
        indir_neighbor = 4      # Indirect (diagonal) neighbours. Multiplies all but the direct and indirect distances.
        cont_multiplier = 16     # multiplies each distance that is NOT a contour
        hor_multiplier = 8     # multiplies each distance that is NOT horizontal
        ver_multiplier = 8    # 1 multiplies each distance that is NOT vertical
        deleteallbut =  0   # 2 Delete all nodes but none (0), 2, 3, 4, or 5 near the edges. Only works with a high hor_multiplier
        shortendeldist = 10000000   # Decrease distance of the nodes to the left and right of deleted nodes to each other by x/factor. This factor is important when inner nodes away from the contour are selected.
        
        plotlayer = 0
        
        # Error/logic checks
        if endp[0] == True and ind_layers == False:
            sys.exit("CAUTION #1: If layers are dependent, selecting an end point doesn't make sense.")
        if endp[0] == True and best_endp[0] == True:
            sys.exit("CAUTION #2: If the best endpoint is searched, it cannot be specified.")
        if best_start_and_end_pt == True and ind_layers == False:
            sys.exit("CAUTION #3: Layers cannot be dependent if the starting point is searched automatically. It needs to be selected based on the previous layer.")
        if ind_layers == False and best_endp[0] == False:
            sys.exit("CAUTION #4: If layers are dependent, the best endpoint needs to be active.")
        if best_start_and_end_pt == True and best_endp[0] == True:
            sys.exit("CAUTION #5: If 'best start and end point' is selected, the search for the 'best endpoint' is already included.")
        if best_start_and_end_pt == True and endp[0] == True:
            sys.exit("CAUTION #6: If 'best start and end point' is selected, the endpoint will be found automatically and cannot be selected.")
        if best_start_and_end_pt == True and depot != 0:
            sys.exit("CAUTION #7: If 'best start and end point' is selected, the depot needs to be at '0'.")
        
        # Timer
        start_time = time.time()
        elapsed_time = ['Timer [s]']
        
        # Grid
        grid, min_x, max_x, min_y, max_y = grid_overlay(layer_path, linespace_s)
        
        elapsed_time.append('Grid: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()
        
        distances = []
        for idxi, i in enumerate(grid):
            a = np.array(grid[idxi])
            temp = scipy.spatial.distance.cdist(a,a)
        distances.append(temp.tolist())
        
        elapsed_time.append('Distances: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()   
        
        ''' ####################################################################### '''
        ''' Start of additional line fill algorithm '''
        ''' ####################################################################### '''
        
        rem_indices = []
        grid_del = [[] for i in range(len(grid))]
        for idxi, i in enumerate(grid):
            for idxii, ii in enumerate(i):
                ls1 = 1*linespace_s
                ls2 = 2*linespace_s
                ls3 = 3*linespace_s
                ls4 = 4*linespace_s
                ls5 = 5*linespace_s
                if deleteallbut == 2:
                    if [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i:
                        rem_indices.append([idxi, idxii])
                        grid_del[idxi].append(grid[idxi][idxii])
                if deleteallbut == 3:
                    if [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i:
                        rem_indices.append([idxi, idxii])
                        grid_del[idxi].append(grid[idxi][idxii])
                if deleteallbut == 4:
                    if [round(ii[0]-ls4, 3), ii[1]] in i and [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i and [round(ii[0]+ls4, 3), ii[1]] in i:
                        rem_indices.append([idxi, idxii])
                        grid_del[idxi].append(grid[idxi][idxii])
                if deleteallbut == 5:
                    if [round(ii[0]-ls5, 3), ii[1]] in i and [round(ii[0]-ls4, 3), ii[1]] in i and [round(ii[0]-ls3, 3), ii[1]] in i and [round(ii[0]-ls2, 3), ii[1]] in i and [round(ii[0]-ls1, 3), ii[1]] in i and [round(ii[0]+ls1, 3), ii[1]] in i and [round(ii[0]+ls2, 3), ii[1]] in i and [round(ii[0]+ls3, 3), ii[1]] in i and [round(ii[0]+ls4, 3), ii[1]] in i and [round(ii[0]+ls5, 3), ii[1]] in i:
                        rem_indices.append([idxi, idxii])
                        grid_del[idxi].append(grid[idxi][idxii])
        
        dist_multipl_rem_ends = []
        for i in distances:
            temp = []
            for ii in i:
                temp.append([1]*len(ii))
            dist_multipl_rem_ends.append(temp)
        
        for i in rem_indices:
            if [round(grid[i[0]][i[1]][0]-linespace_s, 3), grid[i[0]][i[1]][1]] not in grid_del[i[0]]:
                startpoint = i
                pointbeforestartpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]-linespace_s, 3), grid[i[0]][i[1]][1]])]
                count = 1
                currentpoint = startpoint 
                while [round(grid[i[0]][i[1]][0]+count*linespace_s, 3), grid[i[0]][i[1]][1]] in grid_del[i[0]]:
                    currentpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]+count*linespace_s, 3), grid[i[0]][i[1]][1]])]
                    count +=1
                endpoint = currentpoint 
                pointafterendpoint = [i[0], grid[i[0]].index([round(grid[i[0]][i[1]][0]+count*linespace_s, 3), grid[i[0]][i[1]][1]])]
        
                dist_multipl_rem_ends[i[0]][pointbeforestartpoint[1]][pointafterendpoint[1]] = -shortendeldist
                dist_multipl_rem_ends[i[0]][pointafterendpoint[1]][pointbeforestartpoint[1]] = -shortendeldist
        
        for i in sorted(rem_indices, reverse=True):
            del grid[i[0]][i[1]]
            for idxj, j in enumerate(distances[i[0]]):
                del distances[i[0]][idxj][i[1]]
                del dist_multipl_rem_ends[i[0]][idxj][i[1]]
        
        for i in sorted(rem_indices, reverse=True):
            del distances[i[0]][i[1]]
            del dist_multipl_rem_ends[i[0]][i[1]]
        
        for idxi, i in enumerate(dist_multipl_rem_ends):
            for idxii, ii in enumerate(i):
                for idxiii, iii in enumerate(ii):
                    if iii == 1:
                        dist_multipl_rem_ends[idxi][idxii][idxiii] = shortendeldist
                    elif iii == -shortendeldist:
                        dist_multipl_rem_ends[idxi][idxii][idxiii] = 1
        
        ''' ------------------------------------- 
            End of additional line fill algorithm
            -------------------------------------   '''
        
        elapsed_time.append('Delete grid points: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()
        
        dist_multipl_neigh_dir = []
        dist_multipl_neigh_indir = []
        for i in distances:
            temp1 = []
            temp2 = []
            for ii in i:
                temp1.append([1]*len(ii))
                temp2.append([1]*len(ii))
            dist_multipl_neigh_dir.append(temp1)
            dist_multipl_neigh_indir.append(temp2)
        
        diag_dist = (2*linespace_s**2)**0.5 
        node_neighbours = []
        node_neighbours_vectors = []   
        for idxi, i in enumerate(distances):
            node_neighbours_temp1 = []
            node_neighbours_vectors_temp1 = []
            for idxii, ii in enumerate(i):
                node_neighbours_temp2 = []
                node_neighbours_vectors_temp2 = []
                x1 = grid[idxi][idxii][0]
                y1 = grid[idxi][idxii][1]
                for idxiii, iii in enumerate(ii):
                    if (iii < diag_dist+0.001 and idxii != idxiii): 
                        node_neighbours_temp2.append(idxiii)
                        x2 = grid[idxi][idxiii][0]
                        y2 = grid[idxi][idxiii][1]
                        if (x2-x1)/linespace_s != 0:
                            temp_abs_x = (x2-x1)/linespace_s * abs((x2-x1)/linespace_s)**(-1)
                        else:
                            temp_abs_x = 0
                        if (y2-y1)/linespace_s != 0:
                            temp_abs_y = (y2-y1)/linespace_s * abs((y2-y1)/linespace_s)**(-1)   
                        else: 
                            temp_abs_y = 0
                        node_neighbours_vectors_temp2.append([temp_abs_x, temp_abs_y])
                    if iii > linespace_s + 0.01:  # Direct neighbours; 
                        dist_multipl_neigh_dir[idxi][idxii][idxiii] *= dir_neighbor
                    if iii > diag_dist+0.001:  # Indirect neighbours
                        dist_multipl_neigh_indir[idxi][idxii][idxiii] *= indir_neighbor
                node_neighbours_temp1.append(node_neighbours_temp2)
                node_neighbours_vectors_temp1.append(node_neighbours_vectors_temp2)
            node_neighbours.append(node_neighbours_temp1)
            node_neighbours_vectors.append(node_neighbours_vectors_temp1)
        
        elapsed_time.append('Modify distances of direct and indirect neighbours: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()
        
        ''' ################################# '''
        ''' CONTOUR, HORIZONTAL, and VERTICAL '''
        ''' ################################# '''
        
        dist_multipl_cont = []
        dist_multipl_dir_hor = []
        dist_multipl_dir_ver = []
        for i in distances:
            dist_multipl_cont_temp = []
            dist_multipl_dir_hor_temp = []
            dist_multipl_dir_ver_temp = []
            for ii in i:
                dist_multipl_cont_temp.append([cont_multiplier]*len(ii))
                dist_multipl_dir_hor_temp.append([hor_multiplier]*len(ii))
                dist_multipl_dir_ver_temp.append([ver_multiplier]*len(ii))
            dist_multipl_cont.append(dist_multipl_cont_temp)
            dist_multipl_dir_hor.append(dist_multipl_dir_hor_temp)
            dist_multipl_dir_ver.append(dist_multipl_dir_ver_temp)
        null_vectors = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1], [0,1]]
        del dist_multipl_cont_temp, dist_multipl_dir_hor_temp, dist_multipl_dir_ver_temp
        
        for idxi, i in enumerate(node_neighbours_vectors):
            for idxii, ii in enumerate(i):
                for idxj, j in enumerate(null_vectors[0:8]):
                    if idxj != len(null_vectors)-1:
                        if (j in ii and null_vectors[idxj+1] not in ii):
                            ind_temp = node_neighbours[idxi][idxii][ii.index(j)]
                            dist_multipl_cont[idxi][idxii][ind_temp] = 1
                        elif (null_vectors[idxj+1] in ii and j not in ii):
                            ind_temp = node_neighbours[idxi][idxii][ii.index(null_vectors[idxj+1])]
                            dist_multipl_cont[idxi][idxii][ind_temp] = 1
                if [1,0] in ii:
                    ind_temp = node_neighbours[idxi][idxii][ii.index([1,0])]
                    dist_multipl_dir_hor[idxi][idxii][ind_temp] = 1
                if [-1,0] in ii:
                    ind_temp = node_neighbours[idxi][idxii][ii.index([-1,0])]
                    dist_multipl_dir_hor[idxi][idxii][ind_temp] = 1            
                if [0,1] in ii:
                    ind_temp = node_neighbours[idxi][idxii][ii.index([0,1])]
                    dist_multipl_dir_ver[idxi][idxii][ind_temp] = 1
                if [0,-1] in ii:
                    ind_temp = node_neighbours[idxi][idxii][ii.index([0,-1])]
                    dist_multipl_dir_ver[idxi][idxii][ind_temp] = 1
        
        dist_multipl_init_dist = []
        for idxi, i in enumerate(distances):
            temp1 = []
            for idxii, ii in enumerate(i):
                temp2 = []
                for idxiii, iii in enumerate(ii):
                    if iii == 0:
                        temp2.append(1)
                    else:
                        temp3 = (linespace_s+(distances[idxi][idxii][idxiii]-linespace_s)*importance_init_dist)/distances[idxi][idxii][idxiii]
                        temp2.append(temp3)
                temp1.append(temp2)
            dist_multipl_init_dist.append(temp1)
        
        for idxi, i in enumerate(distances):
            for idxii, ii in enumerate(i):
                for idxiii, iii in enumerate(ii):
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_rem_ends[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_neigh_dir[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_neigh_indir[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_cont[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_dir_hor[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_dir_ver[idxi][idxii][idxiii]
                    distances[idxi][idxii][idxiii] = distances[idxi][idxii][idxiii] * dist_multipl_init_dist[idxi][idxii][idxiii]
        
        ''' ####################################################################### '''
        ''' Normalize list for TSP input '''
        ''' ####################################################################### '''
        maxval = 2147483647*0.1 # Max C++ long value
        for idxi, i in enumerate(distances):
            for idxii, ii in enumerate(i):
                distances[idxi][idxii] = [float(i)/max(distances[idxi][idxii])*maxval for i in distances[idxi][idxii]]
        
        elapsed_time.append('Contour: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()
        
        if endp[0] == True:
            for idxi, i in enumerate(distances):
                distances[idxi][endp[1]][depot] = endp[2]
        
        if best_start_and_end_pt:
            for idxi, i in enumerate(distances):
                distzero = [0]*len(i)
                distances[idxi].insert(0, distzero)
                for idxii, ii in enumerate(i):
                    distances[idxi][idxii].insert(0, 0)
        
        def closest_node(node, nodes):
            nodes = np.asarray(nodes)
            dist_2 = np.sum((nodes - node)**2, axis=1)
            return np.argmin(dist_2)
            
        elapsed_time.append('Start and end points: ' + str(round(time.time()-start_time, 3)))
        start_time = time.time()
        
        ''' ####################################################################### '''
        ''' Run TSP solver '''
        ''' ####################################################################### '''
        route = []
        print '_________________________'
        for idxi, DistMatrix in enumerate(distances):
            if best_endp[0] == True:
                for idxii, ii in enumerate(DistMatrix):
                    distances[idxi][idxii][depot] = best_endp[1]
    
            route_temp = TSP(DistMatrix, depot, kPenalty)
            if (endp[0] == True) or (best_endp[0] == True):
                del route_temp[-1]
            if (ind_layers == False and idxi != len(distances)-1):
                depot = closest_node(grid[idxi][route_temp[-1]], grid[idxi+1]) 
            route.append(route_temp)
            print 'Starting node: ' + str(route_temp[0])
            print 'Ending node: ' + str(route_temp[-1])
            print 'Number of nodes: ' + str(len(distances[idxi]))
            print '_________________________'
        
        elapsed_time.append('TSP solver: ' + str(round(time.time()-start_time, 3)))
        elapsed_time.append('_________________________')
        print("\n".join(elapsed_time))
        
        if best_start_and_end_pt:
            for idxi, i in enumerate(route):
                rem_idx = []
                for idxii, ii in enumerate(i):
                    if ii == 0: 
                        rem_idx.append(idxii)
                    else:
                        route[idxi][idxii] -= 1
                if len(rem_idx) > 0:
                    for j in reversed(rem_idx):
                        del route[idxi][j]
        if best_start_and_end_pt:
            for idxi, i in enumerate(sorted(distances, reverse=True)):
                for idxj, j in enumerate(distances[idxi]):
                    del distances[idxi][idxj][0]
            for idxi, i in enumerate(sorted(distances, reverse=True)):
                del distances[idxi][0]
        
        route_rem = []
        for idxi, i in enumerate(route):
            for idxii, ii in enumerate(i):
                if idxii != 0 and idxii != len(route[idxi])-1:
                    coord_x_prev = grid[idxi][route[idxi][idxii-1]][0]
                    coord_x_curr = grid[idxi][route[idxi][idxii]][0]
                    coord_x_next = grid[idxi][route[idxi][idxii+1]][0]
                    coord_y_prev = grid[idxi][route[idxi][idxii-1]][1]
                    coord_y_curr = grid[idxi][route[idxi][idxii]][1]
                    coord_y_next = grid[idxi][route[idxi][idxii+1]][1]
                    if coord_x_prev == coord_x_curr == coord_x_next or coord_y_prev == coord_y_curr == coord_y_next:
                        route_rem.append([idxi, idxii])
        for i in sorted(route_rem, reverse=True):
            del route[i[0]][i[1]]
        
        route_xy = []
        for idxi, i in enumerate(route):
            route_xy_temp = []
            for ii in range(0, len(route[idxi])-1):
                x0 = grid[idxi][route[idxi][ii]][0]
                x1 = grid[idxi][route[idxi][ii+1]][0]
                y0 = grid[idxi][route[idxi][ii]][1]
                y1 = grid[idxi][route[idxi][ii+1]][1]
                route_xy_temp.append([x0, x1, y0, y1])
            route_xy.append(route_xy_temp)
        
        gcode = generate_gcode(route_xy, channel, True, (xsize_b - xsize_s)/2, (ysize_b - ysize_s)/2, dz, layer_thickness, gcode_rel, subdir_output, curr_layer, file2)
    
        xi = route_xy[0][0][0]
        yi = route_xy[0][0][2]      
    
        mk.move(x = xi, y = yi)        
        
        for line in route_xy:
            mk.on(channel)
            for pts in line:
                mk.move(x = pts[1]-pts[0], y = pts[3]-pts[2])
            mk.off(channel)
    
        coords = mk.return_current_coords()
        print(coords)
        mk.move(x = -coords[0], y = -coords[1])
        mk.move(z = dz)
        #mk.move(x = (xsize_b - xsize_s)/2, y = (ysize_b - ysize_s)/2)
    else:
        channel = 1
        gcode = generate_gcode(route_xy, channel, False, 0, 0, dz, layer_thickness, gcode_rel, subdir_output, curr_layer, file)
        mk.move(z = dz)
    
mk.close()