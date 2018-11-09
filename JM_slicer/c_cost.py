def calculate_cost(route_xy):
    actual_cost = []
    for i in route_xy:
        actual_cost_temp = 0
        for ii in i:
            actual_cost_temp += ((ii[1]-ii[0])**2+(ii[3]-ii[2])**2)**0.5
        actual_cost.append(actual_cost_temp)
    print ('Actual solution cost of the layers: ') + str(actual_cost)
    
    return actual_cost