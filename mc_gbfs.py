"""
Missionaries and Cannibals Problem — Greedy Best-First Search
=============================================================
State: (m, c, b) where
  m = missionaries on LEFT bank (0–3)
  c = cannibals     on LEFT bank (0–3)
  b = boat side     (1 = left,  0 = right)

Goal: (0, 0, 0) — everyone safely on the right bank.

Heuristic: h(n) = m + c  (total people still on left bank)

TreeNode structure (first-child / next-sibling):
    element     : (m, c, b) tuple
    firstChild  : pointer to first child node
    nextSibling : pointer to next sibling node

Terminology (book by Horowitz & Sahni):
    Live node  : generated node whose children have not all been generated yet
    E-node     : the live node currently being expanded (lowest h on frontier)
    Dead node  : generated node not to be expanded further
                 (already_reached=True  OR  is_goal=True  OR  all children generated)

Bounding function:
    is_reached(state) — True if this state has already been generated.
    Kills the node immediately without generating its children.

Single function solve() does everything:
    - Maintains a min-heap frontier ordered by h(n)
    - Pops best node → becomes E-node → generates its children
    - Links children into first-child / next-sibling tree structure
    - Applies bounding function: already_reached nodes become dead immediately
    - Returns on first goal node found
"""

import heapq

# ─────────────────────────────────────────────────────────────────────────────
# TreeNode
# ─────────────────────────────────────────────────────────────────────────────

class TreeNode:

    def __init__(self, element, action=None, parent=None):
        self.element        = element   # (m, c, b) tuple
        self.action         = action    # string label e.g. 'Move 1M+1C →'
        self.parent         = parent    # back-pointer for path reconstruction
        self.firstChild     = None      # left-child pointer
        self.nextSibling    = None      # right-sibling pointer
        self.is_goal        = (element == (0, 0, 0))
        self.already_reached = False    # set by bounding function
        self.h              = element[0] + element[1]   # heuristic value

    


# ─────────────────────────────────────────────────────────────────────────────
# Actions
# ─────────────────────────────────────────────────────────────────────────────

def is_valid(m, c):
    """Check state validity — missionaries never outnumbered on either bank."""
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False
    if m > 0 and c > m:          # left bank unsafe
        return False
    rm, rc = 3 - m, 3 - c
    if rm > 0 and rc > rm:       # right bank unsafe
        return False
    return True


def apply_actions(state):
    """Return list of (action_label, next_state) for all valid moves."""
    m, c, b = state
    results = []
    moves = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]
    if b == 1:                   # boat on left → moves right
        for bm, bc in moves:
            nm, nc = m - bm, c - bc
            if bm + bc >= 1 and is_valid(nm, nc):
                results.append((f'Move {bm}M+{bc}C →', (nm, nc, 0)))
    else:                        # boat on right → moves left
        for bm, bc in moves:
            nm, nc = m + bm, c + bc
            if bm + bc >= 1 and is_valid(nm, nc):
                results.append((f'Move {bm}M+{bc}C ←', (nm, nc, 1)))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Bounding function
# ─────────────────────────────────────────────────────────────────────────────

def is_reached(state, reached_set):
    """
    Bounding function: returns True if this state has already been generated.
    Kills the node — it becomes a dead node immediately without generating
    any of its children.
    """
    return state in reached_set


# ─────────────────────────────────────────────────────────────────────────────
# solve() — single function: generates nodes + GBFS + tree construction
# ─────────────────────────────────────────────────────────────────────────────

def solve(initial_state=(3, 3, 1)):
    """
    Greedy Best-First Search with bounding function.

    Process:
      - Root node is generated → pushed onto frontier (min-heap by h).
      - Loop:
          * Pop node with lowest h → becomes E-node.
          * IS-GOAL? → return solution.
          * For each child C of E-node:
              - C is generated and linked into tree (firstChild / nextSibling).
              - Bounding function: if is_reached(C) → C is dead (skip).
              - Otherwise C is a live node → push onto frontier.
          * E-node's children all generated → E-node becomes dead.
      - Returns (root, goal_node) or (root, None).
    """

    print("\n")
    print("  GREEDY BEST-FIRST SEARCH — Missionaries & Cannibals")
    print("\n")

    reached_set = set()          # globally reached state values
    counter     = [0]            # tie-breaker for heap (insertion order)

    # ── Generate root ───────────────────────────────────────────────────────
    root = TreeNode(initial_state, action=None, parent=None)
    reached_set.add(initial_state)

  

    if root.is_goal:
        return root, root

   

    # frontier is a heap. each frontier node: (h, insertion_order, treenode)
    frontier = []
    counter[0] += 1
    heapq.heappush(frontier, (root.h, counter[0], root))

    goal_found = None

    # ── GBFS main loop ───────────────────────────────────────────────────────
    while frontier:

        h_val, _, e_node = heapq.heappop(frontier)

        # IS-GOAL check on popped node
        if e_node.is_goal:
            goal_found = e_node
            break

        # ── Generate children ────────────────────────────────────────────────
        children_data = apply_actions(e_node.element)
        prev_child    = None

        for action, child_state in children_data:

            # Generate child C
            C = TreeNode(child_state, action=action, parent=e_node)

            # Link into first-child / next-sibling structure
            if prev_child is None:
                e_node.firstChild   = C        # first child
            else:
                prev_child.nextSibling = C     # extend sibling chain
            prev_child = C

            
            # ── Bounding function ────────────────────────────────────────────
            if is_reached(child_state, reached_set):
                C.already_reached = True
                continue

            # ── Live node ─────────────────────────────────────────────────────
            reached_set.add(child_state)
            counter[0] += 1
            heapq.heappush(frontier, (C.h, counter[0], C))
           

        # E-node's children all generated → E-node becomes dead
       

    return root, goal_found




# ─────────────────────────────────────────────────────────────────────────────
# Solution path reconstruction
# ─────────────────────────────────────────────────────────────────────────────

def reconstruct_path(goal_node):
    path = []
    cur = goal_node
    while cur:
        path.append(cur)
        cur = cur.parent
    return list(reversed(path))


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def parse_state(s):
    s = s.strip().strip('()')
    parts = s.split(',')
    if len(parts) != 3: raise ValueError("Need exactly three values: m,c,b")
    return (int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip()))


def validate_state(state):
    m, c, b = state
    if not (0 <= m <= 3): raise ValueError(f"Missionaries must be 0–3, got {m}")
    if not (0 <= c <= 3): raise ValueError(f"Cannibals must be 0–3, got {c}")
    if b not in (0, 1):   raise ValueError(f"Boat must be 0 or 1, got {b}")
    if not is_valid(m, c): raise ValueError(f"State {state} is invalid (missionaries outnumbered)")


def main():
    print("\n")
    print("  MISSIONARIES & CANNIBALS — Greedy Best-First Search")
    print("  State: (missionaries, cannibals, boat) on LEFT bank")
    print("  Boat:  1 = left bank,  0 = right bank")
    print("  Goal:  (0, 0, 0) — everyone on right bank")
    print("  h(n):  missionaries + cannibals on left bank")
    print("\n")

    while True:
        raw = input("  Enter initial state (default: (3,3,1)): ").strip()
        if raw == "":
            initial = (3, 3, 1)
            break
        try:
            initial = parse_state(raw)
            validate_state(initial)
            break
        except (ValueError, IndexError) as e:
            print(f"   {e}. Try again.")

    print(f"\n  Initial state: {initial}")

    # Run solve
    root, goal_node = solve(initial)

   

    # Solution path
    print("\n")
    if goal_node:
        path = reconstruct_path(goal_node)
        print("  SOLUTION PATH")
        print("\n")
        print(f"\n  States: {[n.element for n in path]}")
    else:
        print("  No solution found.")
    print("\n")

    again = input("  Try another initial state? (y/n): ").strip().lower()
    if again == 'y':
        main()
    else:
        print("\n  Goodbye!\n")


if __name__ == "__main__":
    main()
