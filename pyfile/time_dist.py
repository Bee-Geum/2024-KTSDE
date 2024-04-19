import pickle
import numpy as np
import multiprocessing
from algorithms import Preset
import sys


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


def get_time_dist(tup):
    city, num, paths, G, path_name, k = tup

    print(f"Processing sample number = {path_name} {num} in {city}")

    results = []

    error_cnt = 0

    for path in paths:
        if path == []:
            results.append([-1, -1])
            continue

        dists = 0
        times = 0

        try:
            for i in range(len(path)-1):
                edge_data = G[path[i]][path[i+1]][0]
                dists += edge_data['length']
                times += edge_data['travel_time']
        except KeyError:
            # print(f"KeyError for node {e} in path calculation for {city}. Path skipped.")
            dists = -1
            times = -1
            error_cnt += 1
        
        times /= 60

        results.append([dists, times])
    
    results = np.array(results)
    results = np.round(results, 2)

    print(f'{city} error {error_cnt}')

    with open(f'../result/{city}_{path_name}dt_{num}_{k}.pkl', 'wb') as file:
        pickle.dump(results, file)


def main(k, path_name, txt_file):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    graphs   = get_data.get_nxGraph(cities, k)

    file_infos = []
    # sample_num = [1000, 2000, 4000, 8000]
    # sample_num = [1000]
    sample_num = [100]

    paths_data = get_paths(cities, path_name, k)

    for city in cities:
        G = graphs[city]

        for num in sample_num:
            paths = paths_data[f'{city}_sample_{num}']

            file_infos.append((city, num, paths, G, path_name, k))

    with multiprocessing.Pool(processes=10) as pool:
        pool.map(get_time_dist, file_infos)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])