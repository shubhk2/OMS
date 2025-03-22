# import time
# start_time = None
# from sqlitin import get_db_connection
#
#
#
# def create_task():
#     db=get_db_connection()
#
# def checkin():
#     global start_time
#     start_time = time.time()
#     return "Timer started"
# def checkout():
#     global start_time
#     if start_time is None:
#         return  "Timer not started"
#     elapsed_time = time.time() - start_time
#     start_time = None
#     return elapsed_time
# # print(checkin())
# # time.sleep(10)
# # print(checkout())
# def count_words(sen):
#     count=0
#     for i in sen:
#         if i == ' ':
#             count += 1
#     return count+1

import heapq


def dijkstra(source, graph,all_nodes):
    distances = {node: float('inf') for node in all_nodes}  # Initialize distances to infinity
    distances[source] = 0  # Distance from start to itself is 0
    priority_queue = [(0, source)]  # Priority queue (distance, node)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we've already found a shorter path, skip
        if current_distance > distances[current_node]:
            continue
        print(current_node,distances)
        if current_node not in graph:

            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If we found a shorter path to the neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


if __name__ == "__main__":
    # adj = {}
    adj = {'A': {'B': -1}, 'B': {'C': -2}, 'C': {'A': -3}}
    # adj[1].append((4, 6))

    # adj[2] = {3: 2}
    # adj[2].append((4, 1))
    # adj[2].append((6, 3))

    #
    # adj[4] = {6: 3}
    # # adj[4].append((2, 1))
    #
    # # adj[5].append((3, 10))
    # adj[5] = {6: 3}
    all_nodes=['A','B','C']

    # adj[6].append((2, 3))
    # adj[6].append((5, 4))

    res = dijkstra('A', adj,all_nodes)

    print()

    for i in all_nodes:
        if  res[i] == float('inf'):
            print("-1 ", end="")
        else:
            print(res[i], end=" ")
        # print(f"Distance of Vertex {i}: {d[i]}")
