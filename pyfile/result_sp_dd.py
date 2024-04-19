import pickle
import osmnx as ox
import random
import matplotlib.pyplot as plt

city = '세종특별자치시'
sample_num = 100
k = 10

with open(f"./fewest_turn_paths/{city}_ftp_{sample_num}_{k}.pkl", 'rb') as file1, \
    open(f"../graph_data/{city}_graph_default.pkl", 'rb') as file2, \
    open(f"./shortest_paths/{city}_sp_{sample_num}_{k}.pkl", 'rb') as file3, \
    open(f"./quickest_paths/{city}_qp_{sample_num}_{k}.pkl", 'rb') as file4, \
    open(f"./smart_paths/{city}_smp_{sample_num}_{k}.pkl", 'rb') as file5:
    ftps  = pickle.load(file1)
    G     = pickle.load(file2)
    sps   = pickle.load(file3)
    qps   = pickle.load(file4)
    smps  = pickle.load(file5)


# random_numbers = random.sample(range(0, 100), 10)

random_numbers = [82]

for idx in random_numbers:
    
    ftp = ftps[idx]
    sp  =  sps[idx]
    qp  =  qps[idx]
    smp = smps[idx]

    if ftp == []:
        continue

    start_node = sp[0] 
    end_node   = sp[-1]  

    s_node_lat = G.nodes[start_node]['y']
    s_node_lon = G.nodes[start_node]['x'] 
    t_node_lat = G.nodes[end_node]['y']
    t_node_lon = G.nodes[end_node]['x'] 


    fig, ax = ox.plot_graph_route(G, sp, route_color='b', \
                        route_alpha = 0.7, route_linewidth=3, edge_alpha = 0.6, \
                        edge_linewidth=0.2, node_color='black', bgcolor='white', node_size=0, figsize=(10, 10))
    
    ax.plot([s_node_lon, t_node_lon], [s_node_lat, t_node_lat], color='red', linewidth=3, linestyle='--')

    fig.savefig(f'./{city}_sp_drone_{idx}.pdf')