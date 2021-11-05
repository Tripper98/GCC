import os
import json
import time
import numpy as np 
import multiprocessing
from Dynamic_programming import knapSack
from ortools.algorithms import pywrapknapsack_solver

def test():
    path = ".\\benchmark instance\instances_01_KP\large_scale"
    cmp = 0
    filenames = []
    # filenames = os.walk(path)
    for (_, _, filename) in os.walk(path):
        cmp += 1
        filenames.extend(filename)
    print(len(filenames))
    # print(cmp)
    # print(filenames)

def get_files(path = ".\\benchmark instance\instances_01_KP\large_scale"):
    path = path
    filenames = []
    paths = []
    # filenames = os.walk(path)
    for (_, _, filename) in os.walk(path):
        filenames.extend(filename)

    for file in filenames:
        paths.append(os.path.join(path, file))

    print(len(paths))
    return paths
    

    # return filenames



def read_instance():
    INSTANCES = []
    paths = get_files()

    for path in paths:

        datContent = [i.strip().split() for i in open(path).readlines()]
        # print(datContent[:101])

        number_of_items = int(datContent[0][0])
        values = [int(el[0]) for el in datContent[1:number_of_items+1] ]
        weights = [[int(el[1]) for el in datContent[1:number_of_items+1]] ]
        max_capacity = [int(datContent[0][1])]

        INSTANCES.append([path, values, weights, max_capacity])

    print(INSTANCES[9][2][0])
    # print(INSTANCES[9][2])
    return INSTANCES

def solver(process, method, values, weights, capacities):
    output = {}

    if method == 'O':
        m = 'CBC Based Solver'
        start_time = time.time()
        output['Optimal solution'] = knapSack(capacities[0], weights[0], values, len(values))
        output['Time of Execution'] = time.time() - start_time
        process.send(output)

    
    packed_items = []
    packed_weights = []
    total_weight = 0

    if method == 'C':
        print('I am here ! ')
        m = 'CBC Based Solver'
        solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'KnapsackExample')

    if method == 'D':
        m = 'DYNAMIC PROGRAMMING'
        solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER, 'KnapsackExample')

    if method == 'B':
        m = 'BRANCH & BOUND'
        solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    start_time = time.time()

    # max_time = time.time() + 900
 
    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    

    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    # print("--- %s seconds ---" % (time.time() - start_time))
    # output['Instance'] = instance
    output['Method'] = m 
    output['Optimal solution'] = computed_value
    output['Total weight'] = total_weight
    output['Packed items'] = packed_items
    output['Packed_weights'] = packed_weights
    output['Time of Execution'] = time.time() - start_time
    
    print('Total value =', output['Optimal solution'])
    print('Total weight:', output['Total weight'])
    print('Packed items:', output['Packed items'])
    print('Packed_weights:', output['Packed_weights'])
    print('Time of Execution (s)', output['Time of Execution'])
    process.send(output)
    # return output

def main():
    # D for dynamic Programming 
    # B for Branch & Bound 
    INSTANCES = read_instance()  # len(INSTANCES)
    # print(len(INSTANCES))
    methods = ['D', 'B', 'C', 'O']
    cmp = 0
    for method in methods:
        outputs = {}    
        if method == 'D' or method == 'B' or method == 'C':
            continue

        for instance in INSTANCES: 
            # print(method)
            file_name, values , weights, capacities = instance[0], instance[1], instance[2], instance[3] 
            # not_corr = ['large_scale\knapPI_3_2000_1000_1', 'large_scale\knapPI_3_10000_1000_1', 'large_scale\knapPI_3_5000_1000_1']
            # if file_name[37:] in not_corr :
            #     continue
            print(f"Solution for instance: {file_name[37:]}")

            ## New Approach 
            parent_conn, child_conn = multiprocessing.Pipe()
            p = multiprocessing.Process(target= solver, name="solver", args=(child_conn, method, values, weights, capacities))
            start_time = time.time()
            p.start()
            # time.sleep(5)
            # p.join(30)
            output = parent_conn.recv()
            p.terminate()
            p.join()
            ###########

            # output = solver(method, values , weights, capacities)

            # Save result as JSON File 
            outputs[file_name[37:]] = output
            output_name = method+'_'+'results.json'
            with open(output_name, 'w') as fp:
                json.dump(outputs, fp)
        


if __name__ == '__main__' : 
    # p = multiprocessing.Process(target= main, name="main")
    main()
    # p.start()

    # read_instance()
    # start_time = time.time()
    # # Wait 10 seconds for foo
    # time.sleep(30)

    # if(time.time() - start_time > 30 ):
    #     print('I Got it ! ')
    #     p.terminate()

    # Terminate foo
    # p.terminate()

    # # Cleanup
    # p.join()


    # s = "instance\instances_01_KP\large_scale\knapPI_3_500_1000_1"
    # print(s[37:])
    # test()
    # get_files()



# start_time = time.time()
# main()
# print("--- %s seconds ---" % (time.time() - start_time))