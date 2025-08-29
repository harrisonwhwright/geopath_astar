import heapq
import math
import networkx as nx

EARTH_RADIUS_METERS = 6371 * 1000

# https://en.wikipedia.org/wiki/Haversine_formula
def haversine_distance(graph: nx.MultiDiGraph, node1: int, node2: int) -> float:
    lat1, lon1 = graph.nodes[node1]['y'], graph.nodes[node1]['x']
    lat2, lon2 = graph.nodes[node2]['y'], graph.nodes[node2]['x']

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = EARTH_RADIUS_METERS * c
    return distance

# https://en.wikipedia.org/wiki/A*_search_algorithm
def astar_path(graph: nx.MultiDiGraph, start_node: int, end_node: int) -> list[int] | None:
    # open set
    priority_queue = [(0, start_node)]
    
    came_from = {}

    # cost from start to this node.
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0

    # estimated total cost
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = haversine_distance(graph, start_node, end_node)

    while priority_queue:
        # get lowest f_score from priority queue
        _, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            return path[::-1] # return path

        for neighbor_node in graph.neighbors(current_node):
            road_segment_length = graph[current_node][neighbor_node][0]['length']
            
            tentative_g_score = g_score[current_node] + road_segment_length

            if tentative_g_score < g_score[neighbor_node]:
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + haversine_distance(graph, neighbor_node, end_node)
                
                heapq.heappush(priority_queue, (f_score[neighbor_node], neighbor_node))
                
    return None # return no path