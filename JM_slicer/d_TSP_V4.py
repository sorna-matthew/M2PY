def TSP(DistMatrix, depot, kPenalty):
    from ortools.constraint_solver import pywrapcp
    from ortools.constraint_solver import routing_enums_pb2
    
    tsp_size = len(DistMatrix)
    
    def Distance(i, j):
        return DistMatrix[i][j]

    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, 1, depot)
    
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit_ms = 2500 # Use this when using metaheuristics to limit time

        routing.SetArcCostEvaluatorOfAllVehicles(Distance)

        for order in range(1, routing.nodes() ):
            routing.AddDisjunction([order], kPenalty)

        assignment = routing.Solve()
        if assignment:
            print ('Solution cost: ') + str((assignment.ObjectiveValue()))
            route_number = 0
            node = routing.Start(route_number)
            route = ''
            route2 = []
            while not routing.IsEnd(node):
                route += str(node) + ' -> '
                route2.append(node)
                node = assignment.Value(routing.NextVar(node))
            route += '0'
            route2.append(0)
            print(route)
        else:
            print('No solution found.')
    else:
        print('Specify an instance greater than 0.')

    return route2

if __name__ == '__main__':
  route = TSP(DistMatrix, depot, kPenalty)