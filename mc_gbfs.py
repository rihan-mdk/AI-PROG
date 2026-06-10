import heapq

class TreeNode:

    def __init__(self, element, action=None, parent=None):
        self.element = element
        self.action = action
        self.parent = parent
        self.firstChild = None
        self.nextSibling = None
        self.is_goal = (element == (0, 0, 0))
        self.already_reached = False
        self.h = element[0] + element[1]


def is_valid(m, c):
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False
    if m > 0 and c > m:
        return False
    rm, rc = 3 - m, 3 - c
    if rm > 0 and rc > rm:
        return False
    return True


def apply_actions(state):
    m, c, b = state
    results = []
    moves = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]

    if b == 1:
        for bm, bc in moves:
            nm, nc = m - bm, c - bc
            if bm + bc >= 1 and is_valid(nm, nc):
                results.append((f'Move {bm}M+{bc}C →', (nm, nc, 0)))
    else:
        for bm, bc in moves:
            nm, nc = m + bm, c + bc
            if bm + bc >= 1 and is_valid(nm, nc):
                results.append((f'Move {bm}M+{bc}C ←', (nm, nc, 1)))

    return results


def is_reached(state, reached_set):
    return state in reached_set


def solve(initial_state=(3, 3, 1)):

    print("\n")
    print("GREEDY BEST-FIRST SEARCH — Missionaries & Cannibals")
    print("\n")

    reached_set = set()
    counter = [0]

    root = TreeNode(initial_state)
    reached_set.add(initial_state)

    if root.is_goal:
        return root, root

    frontier = []
    counter[0] += 1
    heapq.heappush(frontier, (root.h, counter[0], root))

    goal_found = None

    while frontier:

        h_val, _, e_node = heapq.heappop(frontier)

        if e_node.is_goal:
            goal_found = e_node
            break

        children_data = apply_actions(e_node.element)
        prev_child = None

        for action, child_state in children_data:

            C = TreeNode(child_state, action=action, parent=e_node)

            if prev_child is None:
                e_node.firstChild = C
            else:
                prev_child.nextSibling = C

            prev_child = C

            if is_reached(child_state, reached_set):
                C.already_reached = True
                continue

            reached_set.add(child_state)
            counter[0] += 1
            heapq.heappush(frontier, (C.h, counter[0], C))

    return root, goal_found


def reconstruct_path(goal_node):
    path = []
    cur = goal_node

    while cur:
        path.append(cur)
        cur = cur.parent

    return list(reversed(path))


def parse_state(s):
    s = s.strip().strip('()')
    parts = s.split(',')

    if len(parts) != 3:
        raise ValueError("Need exactly three values: m,c,b")

    return (int(parts[0].strip()),
            int(parts[1].strip()),
            int(parts[2].strip()))


def validate_state(state):
    m, c, b = state

    if not (0 <= m <= 3):
        raise ValueError(f"Missionaries must be 0–3, got {m}")

    if not (0 <= c <= 3):
        raise ValueError(f"Cannibals must be 0–3, got {c}")

    if b not in (0, 1):
        raise ValueError(f"Boat must be 0 or 1, got {b}")

    if not is_valid(m, c):
        raise ValueError(f"State {state} is invalid")


def main():

    print("\nMISSIONARIES & CANNIBALS — Greedy Best-First Search")
    print("State: (missionaries, cannibals, boat) on LEFT bank")
    print("Boat: 1 = left bank, 0 = right bank")
    print("Goal: (0, 0, 0)")
    print("h(n): missionaries + cannibals on left bank\n")

    while True:

        raw = input("Enter initial state (default: (3,3,1)): ").strip()

        if raw == "":
            initial = (3, 3, 1)
            break

        try:
            initial = parse_state(raw)
            validate_state(initial)
            break

        except (ValueError, IndexError) as e:
            print(f"{e}. Try again.")

    print(f"\nInitial state: {initial}")

    root, goal_node = solve(initial)

    print("\n")

    if goal_node:
        path = reconstruct_path(goal_node)
        print("SOLUTION PATH\n")
        print(f"States: {[n.element for n in path]}")
    else:
        print("No solution found.")

    print("\n")

    again = input("Try another initial state? (y/n): ").strip().lower()

    if again == 'y':
        main()
    else:
        print("\nGoodbye!\n")


if __name__ == "__main__":
    main()
