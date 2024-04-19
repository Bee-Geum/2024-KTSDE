import pickle
import multiprocessing
from algorithms import Preset
import networkx as nx
import sys


def calculate(tup):
    city, num, sample_list, G, k = tup

    print(f"Processing sample number = {num} in {city}")

    qps     = []

    for sample_tup in sample_list:
        source = sample_tup[0]
        target = sample_tup[1]

        try:
            qp = nx.shortest_path(G=G, source=source, target=target, weight='travel_time')
        except nx.NetworkXNoPath:
            qp = []
        
        qps.append(qp)

    with open(f'./quickest_paths/{city}_qp_{num}_{k}.pkl', 'wb') as file:
        pickle.dump(qps, file)


def main(k, txt_file):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    samples  = get_data.get_sample(cities)
    graphs   = get_data.get_nxGraph(cities, k)

    file_infos = []

    # sample_num = [1000, 2000, 4000, 8000]
    # sample_num = [1000]
    sample_num = [100]
    for city in cities:
        graph = graphs[city]

        for num in sample_num:
            sample_list = samples[f'{city}_sample_{num}']
            file_infos.append((city, num, sample_list, graph, k))

    with multiprocessing.Pool(processes=10) as pool:
        pool.map(calculate, file_infos)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])