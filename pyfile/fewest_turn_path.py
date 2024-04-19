import pickle
import algorithms
import multiprocessing
from algorithms import Preset
import sys


def get_fewest_turn_path(tup):

    city, num, samples, graph, k = tup

    print(f"Processing sample number = {num} in {city}")

    paths   = []

    for sample_tup in samples:
        source = sample_tup[0]
        target = sample_tup[1]

        path = algorithms.fewest_turn_path_dijkstra(graph, source, target)

        paths.append(path)

    with open(f'./fewest_turn_paths/{city}_ftp_{num}_{k}.pkl', 'wb') as file:
        pickle.dump(paths, file)


def main(k, txt_file):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    samples  = get_data.get_sample(cities)
    dict_G   = get_data.get_dict_graph(cities, k)

    file_infos = []

    # sample_num = [1000, 2000, 4000, 8000]
    # sample_num = [1000]
    sample_num = [100]
    for city in cities:
        graph = dict_G[city]

        for num in sample_num:
            sample_list = samples[f'{city}_sample_{num}']
            tup         = (city, num, sample_list, graph, k)
            # get_fewest_turn_path(tup)
            file_infos.append(tup)

    # processes 10하면 메모리 터지는듯
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(get_fewest_turn_path, file_infos)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
    # main(10, 'intl')