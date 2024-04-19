import osmnx as ox
import pickle
from algorithms import Preset
import sys


def add_time(graph, k, city):
    # travl_time 추가 위해 필수

    # Fallback 속도를 30km/h로 설정 ( add_edge_speeds가 데이터가 없을 때, default로 속도 30으로 설정 )
    fallback_speed = 30

    # add_edge_speeds 함수 호출
    graph = ox.add_edge_speeds(graph, fallback=fallback_speed)
    graph = ox.add_edge_travel_times(graph)

    # 각 노드에서의 대기시간 더해주기
    w = 20
    # ================================ #
    # k = 10
    # ================================ #
    node_wait_times = {}

    for node, degree in graph.degree():
        if degree <= 2:
            wait_time = w
        else:
            wait_time = w + k * (degree - 2)

        node_wait_times[node] = wait_time

    for s, t, key, data in graph.edges(keys=True, data=True):
        # 도착 vertex만 할당, 나중에 path에서 계산할때는 끝 vertex 시간 빼주기. 시작점과 끝점 시간은 빼주기로 했음
        wait_time = node_wait_times[t]
        data["travel_time"] += wait_time

    with open(f'../graph_data/{city}_graph_{k}.pkl', 'wb') as file:
        pickle.dump(graph, file)


def main(k, txt_file):
    get_data = Preset()
    cities   = get_data.get_cities(txt_file)
    notime_G = get_data.get_raw_graph(cities)

    for city in cities:
        print(k, city)
        
        graph = notime_G[city]
        add_time(graph, k, city)


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])