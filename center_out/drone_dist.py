import pickle
from haversine import haversine
import osmnx as ox
import numpy as np
from algorithms import Preset
import sys


def get_drone(cities, graphs, sample_data, option):

    samples = [100]
    for city in cities:
        G     = graphs[city]
        nodes = ox.graph_to_gdfs(G, edges=False)

        for num in samples:
            lat_lons = []
            datas    = sample_data[f'{city}_sample_{num}']

            for data in datas:
                source = data[0]
                target = data[1]
                s_lat  = nodes.iloc[source]['y']
                s_lon  = nodes.iloc[source]['x']
                t_lat  = nodes.iloc[target]['y']
                t_lon  = nodes.iloc[target]['x']

                lat_lons.append([(s_lat, s_lon), (t_lat, t_lon)])
                
            drone_dists = []
            for lat_lon in lat_lons:
                dist = haversine(lat_lon[0], lat_lon[1], unit='m')
                drone_dists.append(dist)

            drone_dists = np.array(drone_dists)
            drone_dists = np.round(drone_dists, 2)

            with open(f'./result/{city}_{option}_drone_{num}.pkl', 'wb') as file:
                pickle.dump(drone_dists, file)


def main(txt_file, option):

    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    samples  = get_data.get_sample(cities, option=option)
    graphs   = get_data.get_raw_graph(cities)

    get_drone(cities, graphs, samples, option)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])