import heapq

def dijkstra(graph, start):

    distances = {node: float("inf") for node in graph}
    previous = {}

    distances[start] = 0

    pq = [(0, start)]

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.get(current_node, {}).items():

            if neighbor not in distances:
                distances[neighbor] = float("inf")

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(
                    pq,
                    (distance, neighbor)
                )

    return distances, previous