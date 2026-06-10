class TreeNode:

    def __init__(self, element, action=None, parent=None):
        self.element = element
        self.action = action
        self.parent = parent
        self.firstChild = None
        self.nextSibling = None
        self.is_goal = (element[0] == 2)
        self.is_repeat = False


def apply_actions(state):
    x, y = state
    results = []
    if x < 4:
        results.append(('A1: Fill 4-litre', (4, y)))
    if y < 3:
        results.append(('A2: Fill 3-litre', (x, 3)))
    if x > 0:
        results.append(('A3: Empty 4-litre', (0, y)))
    if y > 0:
        results.append(('A4: Empty 3-litre', (x, 0)))
    if x + y >= 4 and y > 0:
        results.append(('A5: Pour 3→4 (fill 4)', (4, y - (4 - x))))
    if x + y >= 3 and x > 0:
        results.append(('A6: Pour 4→3 (fill 3)', (x - (3 - y), 3)))
    if 0 < x + y <= 4:
        results.append(('A7: Pour all 3→4', (x + y, 0)))
    if 0 < x + y <= 3:
        results.append(('A8: Pour all 4→3', (0, x + y)))
    return results


def is_repeat(state, generated_set):
    return state in generated_set


def solve(initial_state=(0, 0)):

    print("\n")
    print("  BACKTRACKING — Depth-First Node Generation")
    print("\n")

    generated_set = set()

    root = TreeNode(initial_state, action=None, parent=None)
    generated_set.add(initial_state)

    if root.is_goal:
        print(f"\n    Root is the goal state!")
        return root, root

    goal_found = [None]

    def backtrack(e_node):

        if goal_found[0] is not None:
            return True

        children_data = apply_actions(e_node.element)
        prev_child = None

        for action, child_state in children_data:
            if goal_found[0] is not None:
                break

            C = TreeNode(child_state, action=action, parent=e_node)

            if prev_child is None:
                e_node.firstChild = C
            else:
                prev_child.nextSibling = C
            prev_child = C

            if C.is_goal:
                goal_found[0] = C
                return True

            if is_repeat(child_state, generated_set):
                C.is_repeat = True
                continue

            generated_set.add(child_state)

            found = backtrack(C)
            if found:
                return True

        return False

    backtrack(root)

    return root, goal_found[0]


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
    if len(parts) != 2:
        raise ValueError("Need exactly two values")
    return (int(parts[0].strip()), int(parts[1].strip()))


def validate_state(state):
    x, y = state
    if not (0 <= x <= 4):
        raise ValueError(f"4-litre jug must be 0–4, got {x}")
    if not (0 <= y <= 3):
        raise ValueError(f"3-litre jug must be 0–3, got {y}")


def main():
    print("\n")

    while True:
        raw = input("\nEnter initial state (default: (0,0)): ").strip()
        if raw == "":
            initial = (0, 0)
            break
        try:
            initial = parse_state(raw)
            validate_state(initial)
            break
        except (ValueError, IndexError) as e:
            print(f"   {e}. Try again.")

    print(f"\n  Initial state: {initial}")

    root, goal_node = solve(initial)

    print("\n")
    if goal_node:
        path = reconstruct_path(goal_node)
        print("  SOLUTION PATH")
        print("\n")
        print(f"\n  States: {[n.element for n in path]}")
    else:
        print("  No solution found.")
    print("\n")

    again = input("\nTry another initial state? (y/n): ").strip().lower()
    if again == 'y':
        main()
    else:
        print("\nGoodbye!\n")


if __name__ == "__main__":
    main()
