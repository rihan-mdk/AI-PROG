"""
Water Jug Problem — Backtracking with first-Child / next-Sibling Tree
======================================================================
4-litre jug (x), 3-litre jug (y). Goal: x == 2.

TreeNode structure:
    element     : (x, y) tuple
    firstChild  : pointer to first child
    nextSibling : pointer to next sibling

Terminology (from the book by Horowitz & Sahni):
    Live node   : generated node whose children have not all been generated yet
    E-node      : the live node currently being expanded
    Dead node   : generated node not to be expanded further
                  (is_repeat=True  OR  is_goal=True  OR  no children)

Bounding function:
    is_repeat(state) — True if this state value was already generated
                       on the current path or globally. Kills the node
                       immediately (makes it a dead node) without generating
                       any of its children.

Single function solve() does everything:
    - Generates nodes (builds the tree)
    - Tracks live nodes / E-node / dead nodes
    - Backtracks when subtree is fully explored
    - Returns on first answer node found
"""

# ─────────────────────────────────────────────────────────────────────────────
# TreeNode
# ─────────────────────────────────────────────────────────────────────────────

class TreeNode:


    def __init__(self, element, action=None, parent=None):
        self.element     = element    # (x, y) tuple
        self.action      = action     # string label e.g. 'A1: Fill 4-litre'
        self.parent      = parent     # back-pointer for path reconstruction
        self.firstChild  = None       # left-child pointer
        self.nextSibling = None       # right-sibling pointer
        self.is_goal     = (element[0] == 2)
        self.is_repeat   = False      # set by bounding function


# ─────────────────────────────────────────────────────────────────────────────
# Actions
# ─────────────────────────────────────────────────────────────────────────────

def apply_actions(state):
    x, y = state
    results = []
    if x < 4:               results.append(('A1: Fill 4-litre',      (4, y)))
    if y < 3:               results.append(('A2: Fill 3-litre',      (x, 3)))
    if x > 0:               results.append(('A3: Empty 4-litre',     (0, y)))
    if y > 0:               results.append(('A4: Empty 3-litre',     (x, 0)))
    if x+y >= 4 and y > 0:  results.append(('A5: Pour 3→4 (fill 4)', (4, y-(4-x))))
    if x+y >= 3 and x > 0:  results.append(('A6: Pour 4→3 (fill 3)', (x-(3-y), 3)))
    if 0 < x+y <= 4:        results.append(('A7: Pour all 3→4',      (x+y, 0)))
    if 0 < x+y <= 3:        results.append(('A8: Pour all 4→3',      (0, x+y)))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Bounding function
# ─────────────────────────────────────────────────────────────────────────────

def is_repeat(state, generated_set):
    """
    Bounding function: returns True if this state value has already been
    generated. Kills the node — it becomes a dead node immediately without
    generating any children.
    """
    return state in generated_set

# ─────────────────────────────────────────────────────────────────────────────
# solve() — single function: generates nodes + finds solution (backtracking)
# ─────────────────────────────────────────────────────────────────────────────

def solve(initial_state=(0, 0)):
    """
    Depth-first node generation with bounding function (backtracking).

    Process:
      - Root node is generated → becomes first E-node.
      - For each child C of E-node R:
          * C is generated and linked into the tree (firstChild / nextSibling).
          * Bounding function applied: if is_repeat(C) → C is a dead node.
          * If C is goal → solution found, return.
          * Otherwise C becomes the new E-node (recurse into subtree C).
          * When subtree C is fully explored, R becomes E-node again.
      - A node becomes dead when all its children have been generated.

    Returns (root, goal_node) or (root, None).
    """

    print("\n")
    print("  BACKTRACKING — Depth-First Node Generation")
    print("\n")

    generated_set = set()   # globally generated state values
 

    # Generate root 

    root = TreeNode(initial_state, action=None, parent=None)
    generated_set.add(initial_state)

   
    if root.is_goal:		#else Root will become E-node
        print(f"\n    Root is the goal state!")
        return root, root


    # Recursive backtracking

    goal_found = [None]   # mutable so inner function can set it

    def backtrack(e_node):
        """
        e_node : current E-node (its children are being generated).
        Returns True if goal found in this subtree.
        """
        if goal_found[0] is not None:
            return True

        children_data = apply_actions(e_node.element)
        prev_child = None    # for building nextSibling chain

        for action, child_state in children_data:
            if goal_found[0] is not None:
                break

            # ── Generate child C ──────────────────────────────────────────
            
            C = TreeNode(child_state, action=action, parent=e_node)

            # Link into left-child / right-sibling structure
            if prev_child is None:
                e_node.firstChild = C        # first child
            else:
                prev_child.nextSibling = C   # extend sibling chain
            prev_child = C

           

            # ── IS-GOAL check ─────────────────────────────────────────────
            if C.is_goal:
                goal_found[0] = C
                return True

            # ── Bounding function ─────────────────────────────────────────
            if is_repeat(child_state, generated_set):
                C.is_repeat = True
                # C is dead — do not expand, continue to next sibling
                continue

            # ── else C is a live node → mark generated, C becomes new E-node ───
            generated_set.add(child_state)
           
            # ── Recurse: generate subtree rooted at C ────────────────────
            found = backtrack(C)
            if found:
                return True

            # ── Now Subtree of C fully explored: C becomes dead ───────────────
            

        # Now all children of e_node generated → e_node becomes dead; goal state not found
        
        return False

   
    backtrack(root)

    return root, goal_found[0]


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
    if len(parts) != 2: raise ValueError("Need exactly two values")
    return (int(parts[0].strip()), int(parts[1].strip()))


def validate_state(state):
    x, y = state
    if not (0 <= x <= 4): raise ValueError(f"4-litre jug must be 0–4, got {x}")
    if not (0 <= y <= 3): raise ValueError(f"3-litre jug must be 0–3, got {y}")


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

    # Run solve — single function does tree generation + DFS + backtracking
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

    again = input("\nTry another initial state? (y/n): ").strip().lower()
    if again == 'y':
        main()
    else:
        print("\nGoodbye!\n")


if __name__ == "__main__":
    main()
