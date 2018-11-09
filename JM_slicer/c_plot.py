def plot_lines(route_xy, plotlayer):
    import numpy as np
    import matplotlib.pyplot as plt
    print ('Plot layer: ') + str(plotlayer)
    
    for i in route_xy[plotlayer]:
        x = np.array(i)[0:2]
        y = np.array(i)[2:4]
        plt.plot(x, y)

def plot_grid(grid, linespace, min_x, max_x, min_y, max_y, plotlayer, gridcolor, markerstyle):
    import matplotlib.pyplot as plt
    x = [item[0] for item in grid[plotlayer]]
    y = [item[1] for item in grid[plotlayer]]
    plt.plot(x, y,linestyle='',color=gridcolor,marker=markerstyle,markersize=6)
    
    plt.axis([min_x-linespace, max_x+linespace, min_y-linespace, max_y+linespace])
