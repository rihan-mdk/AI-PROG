class TreeNode:
    def __init__(self, board, row, action=None, parent=None):
        self.board = board[:]
        self.row = row
        self.action = action
        self.parent = parent
        self.firstChild = None
        self.nextSibling = None
        self.is_goal = (row == 8)
        self.is_pruned = False


def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col:
            return False
        if abs(board[i] - col) == abs(i - row):
            return False
    return True


def get_possible_moves(board, row):
    moves = []
    for col in range(1, 9):
        action = f"Row {row+1} → Col {col}"
        new_board = board[:]
        new_board[row] = col
        moves.append((action, new_board, col))
    return moves


def solve():
    global N
    N = 8

    print("\n")
    print("8-QUEENS BACKTRACKING — Permutation Tree")
    print("\n")
    print("Root state: (0, 0, 0, 0, 0, 0, 0, 0)\n")

    root = TreeNode([0] * 8, 0)
    goal_found = [None]

    def backtrack(e_node):
        if goal_found[0] is not None:
            return True

        if e_node.row == 8:
            goal_found[0] = e_node
            return True

        for action, new_board, col in get_possible_moves(e_node.board, e_node.row):
            if goal_found[0] is not None:
                break

            child = TreeNode(new_board, e_node.row + 1, action, e_node)

            if not is_safe(new_board, e_node.row, col):
                child.is_pruned = True
                continue

            if backtrack(child):
                return True

        return False

    backtrack(root)
    return root, goal_found[0]


def main():
    print("8-Queens Problem — Exactly 8 Rows\n")

    root, goal_node = solve()

    print("\n")

    if goal_node:
        print("SOLUTION FOUND!")
        print("Solution (columns for rows 1 to 8):")
        final = [c for c in goal_node.board if c != 0]

        for i, pos in enumerate(final, 1):
            print(f"  Row {i}: Column {pos}")

        print(f"\nFinal 8-tuple: {final}")
    else:
        print("No solution found.")

    print("\n")


if __name__ == "__main__":
    main()
    input()