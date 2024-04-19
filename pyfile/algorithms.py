import heapq
import numpy as np
import pickle


class Preset:
    def get_cities(self, txt_name):
        # txt_name = input('txt file name? : ')

        cities = []
        with open(f'../txt/{txt_name}.txt', 'r', encoding='UTF-8') as txt_file:
            for line in txt_file:
                city = line.strip().split(',')[0]
                cities.append(city)

        return cities
    
    def get_sample(self, cities):
        # sample_num  = [1000, 2000, 4000, 8000]
        # sample_num = [1000]
        sample_num = [100]
        sample_data = {}

        for city in cities:
            for num in sample_num:
                with open(f'../sample_data/{city}_sample_{num}.pkl', 'rb') as file:
                    data = pickle.load(file)

                sample_data[f'{city}_sample_{num}'] = data

        return sample_data

    def get_dict_graph(self, cities, k):
        graphs = {}

        for city in cities:
            with open(f'../graph_data/{city}_graph_{k}.pkl', 'rb') as file:
                G          = pickle.load(file)
                graph_dict = get_nested_dict_graph(G)

            graphs[city] = graph_dict

        return graphs

    def get_raw_graph(self, cities):
        graphs = {}

        for city in cities:
            with open(f'../graph_data/{city}_graph_default.pkl', 'rb') as file:
                G = pickle.load(file)
                graphs[city] = G
        
        return graphs
            
    def get_nxGraph(self, cities, k):
        graphs = {}

        for city in cities:
            with open(f'../graph_data/{city}_graph_{k}.pkl', 'rb') as file:
                G = pickle.load(file)
                graphs[city] = G
        
        return graphs


def smart_path_dijkstra(graph, source, target, k=0.5):
    distances    = {node: float('inf') for node in graph}
    travel_times = {node: float('inf') for node in graph}
    k_calculates = {node: float('inf') for node in graph}
    parents      = {node: None for node in graph}
    distances[source]    = 0
    travel_times[source] = 0
    k_calculates[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:
        current_k_calculate, current_node = heapq.heappop(priority_queue)

        if current_node == target:  # 대상 노드에 도달하면 중지하고 결과 반환
            break

        if current_k_calculate > k_calculates[current_node]:
            continue

        for neighbor, edge_info in graph[current_node].items():
            length      = edge_info['length']
            travel_time = edge_info['travel_time']

            k_calculate = (1-k) * length + (k * travel_time)

            new_k_calculate = current_k_calculate + k_calculate
            new_distance    = distances[current_node] + length
            new_travel_time = travel_times[current_node] + travel_time

            if new_k_calculate < k_calculates[neighbor]:
                distances[neighbor]    = new_distance
                travel_times[neighbor] = new_travel_time
                k_calculates[neighbor] = new_k_calculate
                parents[neighbor]      = current_node
                heapq.heappush(priority_queue, (new_k_calculate, neighbor))

    path = []
    current_node = target
    while current_node is not None:
        path.append(current_node)
        current_node = parents[current_node]
    path.reverse()

    if distances[target] != float('inf'):
        return path
    else:
        return []  # 대상까지 경로가 없는 경우
    
# ======================================================================= # 

def first_inter_vec(graph, source):
    dot_dict        = {}
    min_dot_product = float('inf')

    for first_neighbor, edge_info in graph[source].items():
        inter_vec = edge_info['vector']

        for second_neighbor, second_edge_info in graph[first_neighbor].items():
            second_inter_vec = second_edge_info['vector']

            # 활성화 함수 처럼 y = -x + 1 적용
            # 유닛 벡터 내적값은 -1 ~ 1 사이기 떄문에, 값이 작을수록 weight를 크게 줘야하기 때문에 이렇게 함.
            temp_dot = -np.dot(inter_vec, second_inter_vec) + 1

            dot_dict[temp_dot] = (source, first_neighbor, second_neighbor, second_inter_vec, temp_dot)

    if dot_dict:
        min_dot_product = min(dot_dict.keys())
        min_s_t         = dot_dict[min_dot_product]

        return min_s_t
    
    else:
        return None


def fewest_turn_path_dijkstra(graph, source, target):
    dot_products         = {node: float('inf') for node in graph}
    parents              = {node: None for node in graph}
    dot_products[source] = 0

    priority_queue = []

    result = first_inter_vec(graph, source)

    if result is not None:
        start_point, first_neighbor, second_neighbor, second_inter_vec, temp_dot = result

        dot_products[first_neighbor]  = 0
        dot_products[second_neighbor] = temp_dot

        parents[first_neighbor]  = start_point
        parents[second_neighbor] = first_neighbor
        
        heapq.heappush(priority_queue, (temp_dot, second_neighbor, second_inter_vec))
    else:
        return []

    while priority_queue:
        current_dot_product, current_node, std_vec = heapq.heappop(priority_queue)

        if current_node == target:
            break

        if dot_products[current_node] < current_dot_product:
            continue

        for neighbor, edge_info in graph[current_node].items():
            inter_vec   = edge_info['vector']
            dot_product = -np.dot(std_vec, inter_vec) + 1
            final_vec   = current_dot_product + dot_product

            if final_vec < dot_products[neighbor]:
                dot_products[neighbor] = final_vec
                parents[neighbor]      = current_node

                heapq.heappush(priority_queue, (final_vec, neighbor, inter_vec))

    path = []
    current_node = target
    while current_node is not None:
        path.append(current_node)
        current_node = parents[current_node]
    path.reverse()

    if dot_products[target] != float('inf'):
        return path
    else:
        return []  # 대상까지 경로가 없는 경우

# ======================================================================= #


def get_nested_dict_graph(G):
    # 그래프를 딕셔너리로 변환
    graph_dict = {}

    for node in G.nodes():
        edges_data = {}

        for neighbor in G.successors(node):
            length_time_vec = {}

            edge_data = G.get_edge_data(node, neighbor)
            edge_data = list(edge_data.values())[0]

            length      = edge_data['length']
            travel_time = edge_data['travel_time']
            vector      = edge_data['vector']

            length_time_vec['length']      = length
            length_time_vec['travel_time'] = travel_time
            length_time_vec['vector']      = vector

            edges_data[neighbor] = length_time_vec

        graph_dict[node] = edges_data

    return graph_dict