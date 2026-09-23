import random

def display_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_win(board, player):
    # Added all 8 winning combinations: 3 rows, 3 columns, 2 diagonals
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[cell] == player for cell in combo) for combo in win_conditions)

def check_draw(board):
    return all(cell in ['X', 'O'] for cell in board)

def play_tic_tac_toe():
    board = [str(i + 1) for i in range(9)]
    human = 'X'
    computer = 'O'
    
    print("Welcome to Tic-Tac-Toe!")
    display_board(board)
    
    turn = random.choice(['Human', 'Computer'])
    print(f"{turn} goes first!")
    
    while True:
        if turn == 'Human':
            move = input("Enter your move (1-9): ")
            if not move.isdigit() or int(move) < 1 or int(move) > 9 or board[int(move) - 1] in ['X', 'O']:
                print("Invalid move. Try again.")
                continue
            idx = int(move) - 1
            board[idx] = human
            display_board(board)
            
            if check_win(board, human):
                print("You win!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            turn = 'Computer'
        else:
            print("Computer is thinking...")
            available_moves = [i for i, cell in enumerate(board) if cell not in ['X', 'O']]
            idx = random.choice(available_moves)
            board[idx] = computer
            display_board(board)
            
            if check_win(board, computer):
                print("Computer wins!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            turn = 'Human'

if __name__ == "__main__":
    play_tic_tac_toe()