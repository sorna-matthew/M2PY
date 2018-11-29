import m2py as mp
import numpy as np
import matplotlib.pyplot as plt

# intersection function
def box_intersect(minpt, maxpt, p0, p1):
    n1 = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]
    n2 = [[-1, 0, 0],[0, -1, 0],[0, 0, -1]]
    intersect = False
    
    for normal1 in n1:
            intpt = isect_line_plane_v3(p0, p1, maxpt, normal1)
            if type(intpt) == tuple:
                intpt = list(intpt)
                if np.logical_and(np.less_equal(minpt, intpt), np.less_equal(intpt, maxpt)).all() and np.logical_and(np.less_equal(p0, intpt), np.less_equal(intpt, p1)).all():
                    intersect = True
                    plt.scatter(intpt[0], intpt[1], intpt[2], marker = 'x', color = 'r', linewidth = 8)
                    
    for normal2 in n2:
            intpt = isect_line_plane_v3(p0, p1, minpt, normal2)
            if type(intpt) == tuple:
                intpt = list(intpt)
                if np.logical_and(np.less_equal(minpt, intpt), np.less_equal(intpt, maxpt)).all() and np.logical_and(np.less_equal(p0, intpt), np.less_equal(intpt, p1)).all():
                    intersect = True
                    plt.scatter(intpt[0], intpt[1], intpt[2], marker = 'x', color = 'r', linewidth = 8)

            
    return intersect
    

def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=1e-6):
    """
    p0, p1: define the line
    p_co, p_no: define the plane:
        p_co is a point on the plane (plane coordinate).
        p_no is a normal vector defining the plane direction;
             (does not need to be normalized).

    return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        # the factor of the point between p0 -> p1 (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # otherwise:
        #  < 0.0: behind p0.
        #  > 1.0: infront of p1.
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = mul_v3_fl(u, fac)
        return add_v3v3(p0, u)
    else:
        # The segment is parallel to plane
        return None

# ----------------------
# generic math functions

def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
        )


def sub_v3v3(v0, v1):
    return (
        v0[0] - v1[0],
        v0[1] - v1[1],
        v0[2] - v1[2],
        )


def dot_v3v3(v0, v1):
    return (
        (v0[0] * v1[0]) +
        (v0[1] * v1[1]) +
        (v0[2] * v1[2])
        )


def len_squared_v3(v0):
    return dot_v3v3(v0, v0)


def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
        )

def build_path(minpts, maxpts, p0, p1):
    path_found = False
    pstart = p0
    pgoal = p1
    start_path = np.array([pstart])
    goal_path = np.array([pgoal])   

    # First checks to see if you can get from initial start and goal before trying to build RRT path
    iscollision_list = []
    for j in range(minpts.shape[0]):
        iscollision = box_intersect(minpts[j], maxpts[j], p0, p1)
        iscollision_list = np.append(iscollision_list, iscollision)
    
    if iscollision_list.any(axis = 0) == True:
        print('Collision Detected! Building collision-free path!')
    else:
        print('Path found!')
        path_found = True
        foundpath = np.array([pstart, pgoal])
    
    while path_found != True:
        start_add = False
        goal_add = False
        
        prand = [np.random.randint(0,203+1),np.random.randint(0,254+1),np.random.randint(0,203+1)]
        
        # Checks if prand can connect to pstart
        iscollision_list = []
        for j in range(minpts.shape[0]):
            iscollision = box_intersect(minpts[j], maxpts[j], pstart, prand)
            iscollision_list = np.append(iscollision_list, iscollision)
        
        if iscollision_list.any(axis = 0) == False:
            start_add = True
            start_path = np.append(start_path, prand) 
        
        # Checks if prand can connect to pgoal
        iscollision_list = []
        for j in range(minpts.shape[0]):
            iscollision = box_intersect(minpts[j], maxpts[j], prand, pgoal)
            iscollision_list = np.append(iscollision_list, iscollision)
        
        if iscollision_list.any(axis = 0) == False:
            goal_add = True
            goal_path = np.append(prand, goal_path)
        
        if start_add and goal_add:
            print('Path found!')
            path_found = True
            foundpath = np.append(start_path, goal_path)
            foundpath.shape = (int(len(foundpath)/3),3)
    
    print(foundpath)
    
    return foundpath
    
mk = mp.Makergear('COM3',115200, printout = 0)
mk.coord_sys(coord_sys = 'abs')
zheight = 0
dz = 0.4
coords_5 = np.array([[0,0], [9,0], [9,9], [3,9], [3,12], [9,12], [9,15], [0,15], [0,6], [6,6], [6,3], [0,3], [0,0]])*5 + [15,50]
coords_2 = (np.array([[0,0], [-9,0], [-9,9], [-3,9], [-3,12], [-9,12], [-9,15], [0,15], [0,6], [-6,6], [-6,3], [0,3], [0,0]]) + [21,0])*5 + [15,50]
coords_0 = (np.array([[0,0], [9,0], [9,15], [0,15], [0,0], [3,0], [3,3], [6,3], [6,12], [3,12], [3,3], [3,0], [0,0], [-24,0]]) + [24,0])*5 + [15,50]
mk.on(1)

for _ in range(7):
    for coord in coords_5:
        mk.move(x = coord[0], y = coord[1], z = zheight)
    for coord in coords_2:
        mk.move(x = coord[0], y = coord[1], z = zheight)
    for coord in coords_0:
        mk.move(x = coord[0], y = coord[1], z = zheight)
        
    zheight = zheight + dz
    mk.move(x = coord[0], y = coord[1], z = zheight)    
mk.close()
minpts, maxpts = mk.obs_gen(ds = 0.4)

p0 = [20,60,0.4]
p1 = [85, 115, 0.4]
fillpts = np.array([[20,60,0.4], [50, 60, 0.4], [50, 90, 0.4], [20, 90, 0.4], [20, 115, 0.4], [50, 115, 0.4], [85, 115, 0.4], [115, 115, 0.4], [115, 85, 0.4], [85, 85, 0.4], [85, 60, 0.4], [115, 60, 0.4], [140, 60, 0.4], [140, 120, 0.4], [170, 120, 0.4], [170, 60, 0.4], [155, 60, 0.4]])

path = p0
for j in range(fillpts.shape[0]-1):
    pathj = build_path(minpts, maxpts, fillpts[j], fillpts[j+1])
    path = np.vstack((path,pathj))

fig = plt.figure(3)
ax1 = fig.add_subplot(111, projection='3d')
ax1.plot(path[:,0], path[:,1], path[:,2])
for j in range(minpts.shape[0]):
        ax1.bar3d(minpts[j][0],minpts[j][1], minpts[j][2], maxpts[j][0]-minpts[j][0], maxpts[j][1]-minpts[j][1], maxpts[j][2]-minpts[j][2], color = 'b')
        ax1.set_xlim(0, 203)
        ax1.set_ylim(0, 254)
        ax1.set_zlim(0, 203)
        ax1.set_xlabel('X axis [mm]')
        ax1.set_ylabel('Y axis [mm]')
        ax1.set_zlabel('Z axis [mm]')


