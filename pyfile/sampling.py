import pickle
import random
from algorithms import Preset
import sys


def sampling(G, city):
    # sample_num = [1000, 2000, 4000, 8000]
    # sample_num = [1000]
    sample_num = [100]
    nodes      = list(G.nodes())

    for num in sample_num:
        attempts     = 0
        sample_nodes = []

        while attempts < num:
            random_nodes = tuple(random.sample(nodes, 2))
            if random_nodes not in sample_nodes:
                sample_nodes.append(random_nodes)
                attempts += 1

        # 체크용
        print(city, len(sample_nodes))
        
        with open(f'../sample_data/{city}_sample_{num}.pkl', 'wb') as file:
            pickle.dump(sample_nodes, file)


def get_graph(city):
    with open(f'../graph_data/{city}_graph_default.pkl', 'rb') as file:
        G = pickle.load(file)

    return G


def main(txt_file):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)

    for city in cities:
        G = get_graph(city)
        sampling(G, city)


if __name__ == '__main__':
    main(sys.argv[1])