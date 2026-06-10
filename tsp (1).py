import heapq
from typing import List, Tuple, Optional

def tsp_greedy_best_first(graph: List[List[float]], start: int = 0) -> Tuple[Optional[List[int]], float]:

    n = len(graph)

    if n < 2:
        return None, float('inf')

    def heuristic(current: int, visited_mask: int) -> float:

        unvisited_costs = []

        for j in range(n):
            if (visited_mask & (1 << j)) == 0:
                cost = graph[current][j]
                if cost < float('inf'):
                    unvisited_costs.append(cost)

        if not unvisited_costs:
            return_cost = graph[current][start]
            return return_cost if return_cost < float('inf') else float('inf')

        unvisited_costs.sort()
        return sum(unvisited_costs)

    pq = []

    initial_mask = 1 << start
    initial_h = heuristic(start, initial_mask)

    heapq.heappush(pq, (initial_h, 0, start, [start], initial_mask))

    best_cost = float('inf')
    best_path = None

    while pq:

        h, g, current, path, visited_mask = heapq.heappop(pq)

        if len(path) == n:
            return_cost = graph[current][start]

            if return_cost < float('inf'):
                total_cost = g + return_cost

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path + [start]

            continue

        for next_city in range(n):
            if (visited_mask & (1 << next_city)) == 0:

                edge_cost = graph[current][next_city]

                if edge_cost < float('inf'):

                    new_g = g + edge_cost
                    new_path = path + [next_city]
                    new_mask = visited_mask | (1 << next_city)
                    new_h = heuristic(next_city, new_mask)

                    heapq.heappush(
                        pq,
                        (new_h, new_g, next_city, new_path, new_mask)
                    )

    return best_path, best_cost


INF = float('inf')

sample_graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

if __name__ == "__main__":

    print("=== TSP using Greedy Best-First Search ===")

    path, cost = tsp_greedy_best_first(sample_graph, start=0)

    if path:
        print("Path:", " -> ".join(map(str, path)))
        print("Total Cost:", cost)
    else:
        print("No valid tour found.")

    input()