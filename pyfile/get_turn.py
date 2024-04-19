import pickle
import numpy as np
import algorithms
import multiprocessing
from algorithms import Preset
import sys


def get_graphs(graphs, cities):
    dict_G = {}

    for city in cities:
        G = graphs[city]
        graph_dict = algorithms.get_nested_dict_graph(G)

        dict_G[city] = graph_dict

    return dict_G


def get_paths(cities, path_name, k):
    # samples = [1000, 2000, 4000, 8000]
    # samples = [1000]
    samples = [100]
    paths_data = {}

    if path_name == 'sp':
        dir = 'shortest_paths'
    elif path_name == 'qp':
        dir = 'quickest_paths'
    elif path_name == 'ftp':
        dir = 'fewest_turn_paths'
    elif path_name == 'smp':
        dir = 'smart_paths'

    for city in cities:
        for num in samples:
            with open(f'./{dir}/{city}_{path_name}_{num}_{k}.pkl', 'rb') as file:
                data = pickle.load(file)                

            paths_data[f'{city}_sample_{num}'] = data
            
    return paths_data


def get_turn(tup):
    city, num, paths, G, path_name, k = tup

    print(f"Processing sample number = {num} in {city}")

    threshold = 0.5 # cos60

    turns = []
    
    for path in paths:
        turn = 0

        for i in range(len(path)-2):
            current_vec = G[path[i]][path[i+1]]['vector']
            next_vec    = G[path[i+1]][path[i+2]]['vector']

            if np.dot(current_vec, next_vec) < threshold:
                turn += 1
        
        turns.append(turn)
    
    turns = np.array(turns)

    with open(f'../result/{city}_{path_name}_turns_{num}_{k}.pkl', 'wb') as file:
        pickle.dump(turns, file)



def main(k, path_name, txt_file):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    
    if k != -1:
        graphs = get_data.get_nxGraph(cities, k)
    else:
        graphs = get_data.get_raw_graph(cities)

    dict_G     = get_graphs(graphs, cities)


    file_infos = []
    # sample_num = [1000, 2000, 4000, 8000]
    # sample_num = [1000]
    sample_num = [100]

    paths_data = get_paths(dict_G, path_name, k)
    
    for city in cities:
        G = dict_G[city]

        for num in sample_num:
            paths = paths_data[f'{city}_sample_{num}']
            file_infos.append((city, num, paths, G, path_name, k))

    with multiprocessing.Pool(processes=10) as pool:
        pool.map(get_turn, file_infos)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])