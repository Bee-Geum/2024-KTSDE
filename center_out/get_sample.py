import pickle
import random


cities = []

with open('../txt/all.txt', 'r') as file:
    for line in file:
        city = line.split(',')[0]
        cities.append(city)


for city in cities:
    with open(f'./nodes/{city}_center_nodes.pkl', 'rb') as file1, \
        open(f'./nodes/{city}_outskirt_nodes.pkl', 'rb') as file2:

        center_nodes   = pickle.load(file1)
        outskirt_nodes = pickle.load(file2)

    num                     = 100
    attempts1, attempts2, attempts3 = 0, 0, 0
    sample_center_nodes     = []
    sample_outskirt_nodes   = []
    sample_center_out_nodes = []


    while attempts1 < num:
        random_nodes = tuple(random.sample(center_nodes, 2))
        if random_nodes not in sample_center_nodes:
            sample_center_nodes.append(random_nodes)
            attempts1 += 1
    

    while attempts2 < num:
        random_nodes = tuple(random.sample(outskirt_nodes, 2))
        if random_nodes not in sample_outskirt_nodes:
            sample_outskirt_nodes.append(random_nodes)
            attempts2 += 1

    while attempts3 < num:
        center_random_node   = random.choice(center_nodes)
        outskirt_random_node = random.choice(outskirt_nodes)
        random_nodes         = (center_random_node, outskirt_random_node)
        if random_nodes not in sample_center_out_nodes:
            sample_center_out_nodes.append(random_nodes)
            attempts3 += 1

    with open(f'./sample_data/{city}_center_sample_100.pkl', 'wb') as file3, \
        open(f'./sample_data/{city}_outskirt_sample_100.pkl', 'wb') as file4, \
        open(f'./sample_data/{city}_center_outskirt_sample_100.pkl', 'wb') as file5:
        pickle.dump(sample_center_nodes, file3)
        pickle.dump(sample_outskirt_nodes, file4)
        pickle.dump(sample_center_out_nodes, file5)

print('done')