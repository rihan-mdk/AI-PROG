graph = {
    'A': {'children': [('B', 1), [('C', 1), ('D', 1)]]},
    'B': {'children': [('E', 1), ('F', 1)]},
    'C': {'children': [('G', 1), [('H', 1), ('I', 1)]]},
    'D': {'children': [('J', 1)]},
    'E': {'children': []},
    'F': {'children': []},
    'G': {'children': []},
    'H': {'children': []},
    'I': {'children': []},
    'J': {'children': []},
}

heuristic = {
    'A': 6, 'B': 5, 'C': 3, 'D': 4,
    'E': 10, 'F': 11, 'G': 3, 'H': 0, 'I': 0, 'J': 1
}

cost           = {n: heuristic[n] for n in heuristic}
solved         = {n: False for n in graph}
best_connector = {}
solution_graph = {}
parents        = {n: [] for n in graph}


def is_and_group(connector):
    return isinstance(connector, list)


def build_parent_map():
    for node, data in graph.items():
        for connector in data['children']:
            if is_and_group(connector):
                for child, _ in connector:
                    if node not in parents[child]:
                        parents[child].append(node)
            else:
                child, _ = connector
                if node not in parents[child]:
                    parents[child].append(node)


def connector_cost_estimate(connector):
    if is_and_group(connector):
        return sum(e + cost[c] for c, e in connector)
    else:
        child, edge = connector
        return edge + cost[child]


def evaluate_node(node):
    if not graph[node]['children']:
        return heuristic[node], None, True

    best_cost = float('inf')
    best_conn = None
    is_solved = False

    for connector in graph[node]['children']:
        c = connector_cost_estimate(connector)
        if is_and_group(connector):
            conn_solved = all(solved[child] for child, _ in connector)
        else:
            child, _ = connector
            conn_solved = solved[child]
        if c < best_cost:
            best_cost = c
            best_conn = connector
            is_solved = conn_solved

    return best_cost, best_conn, is_solved


def add_children_to_frontier(conn, frontier):
    """Add unsolved children of a connector to the frontier."""
    if is_and_group(conn):
        for child, _ in conn:
            if not solved.get(child, False) and child not in frontier:
                frontier.append(child)
    else:
        child, _ = conn
        if not solved.get(child, False) and child not in frontier:
            frontier.append(child)


def back_propagate(node, frontier):
    queue   = list(parents[node])
    visited = set()

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        old_cost  = cost[current]
        old_solved = solved[current]
        old_conn  = best_connector.get(current)

        new_cost, new_conn, new_solved = evaluate_node(current)

        if new_cost != old_cost or new_solved != old_solved:
            cost[current]           = new_cost
            best_connector[current] = new_conn
            solved[current]         = new_solved
           

            # If best connector changed, queue new children for exploration
            if new_conn != old_conn and new_conn is not None:
                add_children_to_frontier(new_conn, frontier)

            for parent in parents[current]:
                if parent not in visited:
                    queue.append(parent)


def ao_star(start):
    for node in graph:
        solved[node] = not bool(graph[node]['children'])
        cost[node]   = heuristic[node]

    build_parent_map()
    frontier = [start]

    while frontier:
        node = frontier.pop(0)

        if solved.get(node, False):
            continue

       
        new_cost, best_conn, is_solved = evaluate_node(node)
        cost[node]           = new_cost
        best_connector[node] = best_conn
        solved[node]         = is_solved

        if best_conn is None:
            continue

        add_children_to_frontier(best_conn, frontier)
        back_propagate(node, frontier)

    return cost[start]


def build_solution(node):
    if node not in best_connector or best_connector[node] is None:
        return
    conn = best_connector[node]
    if is_and_group(conn):
        children = [c for c, _ in conn]
        solution_graph[node] = {'type': 'AND', 'children': children}
        for child in children:
            build_solution(child)
    else:
        child, _ = conn
        solution_graph[node] = {'type': 'OR', 'children': [child]}
        build_solution(child)


# Run
result = ao_star('A')
build_solution('A')

print("\n")
print("Minimum cost:", result)
print("\nSolution Graph:")
for n in sorted(solution_graph.keys()):
    info = solution_graph[n]
    print(f"  {n} ({info['type']}) → {info['children']}")

input()