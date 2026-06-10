class Graph:

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def h(self, n):
        H = {
            'a': 14,
            'b': 14,
            'c': 11,
            'd': 6,
            'e': 4,
            'f': 11,
            'z': 0
        }
        return H[n]

    def a_star_algorithm(self, start_node, goal_node):

        frontier_set = set([start_node])
        expanded_set = set([])

        g = {}
        g[start_node] = 0

        parents = {}
        parents[start_node] = start_node

        while len(frontier_set) > 0:

            n = None

            for v in frontier_set:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n == goal_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)
                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            for (m, weight) in self.get_neighbors(n):

                if m not in frontier_set and m not in expanded_set:
                    frontier_set.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in expanded_set:
                            expanded_set.remove(m)
                            frontier_set.add(m)

            frontier_set.remove(n)
            expanded_set.add(n)

        print('Path does not exist!')
        return None


if __name__ == "__main__":
    adjacency_list = {
        'a': [('b', 4), ('c', 3)],
        'b': [('a', 4), ('f', 5), ('e', 12)],
        'c': [('a', 3), ('d', 7), ('e', 10)],
        'd': [('c', 7), ('e', 2)],
        'e': [('b', 12), ('c', 10), ('d', 2), ('z', 5)],
        'f': [('b', 5), ('z', 16)],
        'z': [('f', 16), ('e', 5)]
    }

    graph1 = Graph(adjacency_list)
    graph1.a_star_algorithm('a', 'z')
    input()