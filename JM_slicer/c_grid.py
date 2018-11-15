def grid_overlay(paths_all, linespace):
    import numpy as np
    grid = []
    for idx, i in enumerate(paths_all):
        paths_all2 = [item for sublist in i for item in sublist]
        min_x, max_x = min([item[0] for item in paths_all2]), max([item[0] for item in paths_all2])
        min_y, max_y = min([item[1] for item in paths_all2]), max([item[1] for item in paths_all2])

        count = 0
        grid_temp = []
        for j in np.arange(min_x,max_x+linespace,linespace):
            for jj in np.arange(min_y,max_y+linespace,linespace):
                grid_temp.append([round(j, 3), round(jj, 3)])
                count += 1
        grid.append(grid_temp)

    import numpy as np
    import matplotlib.path as mplPath
    for idxi, i in enumerate(grid):
        grid_surrounding_polygons = [0] * len(i)
        for idxii, ii in enumerate(i):
            for idxiii, iii in enumerate(paths_all[idxi]):
                bbPath = mplPath.Path(np.array(iii))
                if bbPath.contains_point(ii, radius=-0.0001):
                    grid_surrounding_polygons[idxii] += 1
        grid_idx_rem = []
        for idxj, j in enumerate(grid_surrounding_polygons):
            if j % 2 == 0:
                grid_idx_rem.append(idxj)
        grid[idxi] = [i for j, i in enumerate(grid[idxi]) if j not in grid_idx_rem]

        return grid, min_x, max_x, min_y, max_y