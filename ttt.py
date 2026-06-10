def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_win(board, player):

    win_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True

    return False


def check_draw(board):
    return ' ' not in board


def get_player_move(board):

    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1

            if move < 0 or move > 8:
                print("Invalid position. Please enter a number between 1 and 9.")

            elif board[move] != ' ':
                print("Position already taken! Choose another.")

            else:
                return move

        except ValueError:
            print("Please enter a valid number.")


def play_game():

    board = [' '] * 9
    current_player = 'X'
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    print("Player X goes first.")
    print("Enter numbers 1-9 to make your move.\n")

    while not game_over:

        print_board(board)
        print(f"Player {current_player}'s turn")

        move = get_player_move(board)
        board[move] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} WINS!")
            game_over = True
            continue

        if check_draw(board):
            print_board(board)
            print("It's a DRAW!")
            game_over = True
            continue

        current_player = 'O' if current_player == 'X' else 'X'

    while True:

        play_again = input("Play again? (y/n): ").lower()

        if play_again == 'y':
            play_game()
            break

        elif play_again == 'n':
            print("Thanks for playing!")
            break

        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    play_game()