import numpy as np
import random

class TicTacToeError(Exception):
    """Base exception for Tic Tac Toe game errors."""
    pass

class InvalidMoveError(TicTacToeError):
    """Exception raised when a move is invalid (e.g. out of bounds or bad format)."""
    pass

class CellOccupiedError(TicTacToeError):
    """Exception raised when a player tries to select a cell that is already taken."""
    pass

def initialize_board() -> np.ndarray:
    """Returns a new 3x3 numpy array filled with zeros (representing empty cells)."""
    return np.zeros((3, 3), dtype=int)

def print_board(board: np.ndarray):
    """
    Prints the 3x3 board.
    Empty cells display their 1-9 positional numbers to guide players.
    X is represented in red, and O is represented in blue.
    """
    display_board = []
    for r in range(3):
        row_display = []
        for c in range(3):
            val = board[r, c]
            pos_num = r * 3 + c + 1
            if val == 1:
                row_display.append("\033[91mX\033[0m")  # Red 'X'
            elif val == -1:
                row_display.append("\033[94mO\033[0m")  # Blue 'O'
            else:
                row_display.append(str(pos_num))        # Gray/default positional number
        display_board.append(row_display)
    
    print("\n")
    print(f" {display_board[0][0]} | {display_board[0][1]} | {display_board[0][2]} ")
    print("---+---+---")
    print(f" {display_board[1][0]} | {display_board[1][1]} | {display_board[1][2]} ")
    print("---+---+---")
    print(f" {display_board[2][0]} | {display_board[2][1]} | {display_board[2][2]} ")
    print("\n")

def make_move(board: np.ndarray, position_str: str, player: int):
    """
    Attempts to place the player's marker (1 for X, -1 for O) at the 1-based position (1-9).
    
    Raises:
        InvalidMoveError: If position is not a valid number between 1 and 9.
        CellOccupiedError: If the selected cell is already taken.
    """
    try:
        position = int(position_str)
    except ValueError:
        raise InvalidMoveError(f"Invalid input '{position_str}'. Please enter a number between 1 and 9.")

    if position < 1 or position > 9:
        raise InvalidMoveError(f"Number {position} is out of bounds. Choose a number between 1 and 9.")
    
    r = (position - 1) // 3
    c = (position - 1) % 3
    
    if board[r, c] != 0:
        raise CellOccupiedError(f"Cell {position} is already occupied. Please choose an empty cell.")
        
    board[r, c] = player

def check_winner(board: np.ndarray) -> int | None:
    """
    Checks if there is a winner on the board using NumPy vector sums.
    
    Returns:
        1: Player X wins
       -1: Player O wins
     None: No winner yet
    """
    # Rows sum
    row_sums = board.sum(axis=1)
    # Columns sum
    col_sums = board.sum(axis=0)
    # Diagonals sum
    diag_sum1 = board.trace()
    diag_sum2 = np.fliplr(board).trace()
    
    # Combine all sum groups
    all_sums = np.concatenate([row_sums, col_sums, [diag_sum1, diag_sum2]])
    
    if 3 in all_sums:
        return 1
    elif -3 in all_sums:
        return -1
    return None

def is_board_full(board: np.ndarray) -> bool:
    """Returns True if there are no empty cells left on the board."""
    return not np.any(board == 0)

def get_ai_move(board: np.ndarray, ai_player: int) -> int:
    """
    Determines the best move for the AI.
    1. Looks for a winning move for itself.
    2. Looks to block the opponent's winning move.
    3. Prefers the center cell (5) if empty.
    4. Chooses randomly from the remaining empty cells.
    """
    opponent = -ai_player
    empty_cells = []
    for pos in range(1, 10):
        r = (pos - 1) // 3
        c = (pos - 1) % 3
        if board[r, c] == 0:
            empty_cells.append(pos)
            
    # 1. Can AI win in one move?
    for pos in empty_cells:
        temp_board = board.copy()
        r = (pos - 1) // 3
        c = (pos - 1) % 3
        temp_board[r, c] = ai_player
        if check_winner(temp_board) == ai_player:
            return pos
            
    # 2. Can opponent win in one move? Block them.
    for pos in empty_cells:
        temp_board = board.copy()
        r = (pos - 1) // 3
        c = (pos - 1) % 3
        temp_board[r, c] = opponent
        if check_winner(temp_board) == opponent:
            return pos
            
    # 3. Choose center if available
    if 5 in empty_cells:
        return 5
        
    # 4. Choose random corner or side
    return random.choice(empty_cells)

def get_valid_input(prompt: str, valid_choices: list[str] = None) -> str:
    """Helper to get non-empty user input, supporting exit commands."""
    while True:
        try:
            choice = input(prompt).strip().lower()
            if choice == 'q' or choice == 'quit':
                print("Exiting game. Goodbye!")
                exit(0)
            if valid_choices and choice not in valid_choices:
                print(f"Invalid choice. Please select from: {', '.join(valid_choices)}")
                continue
            return choice
        except (KeyboardInterrupt, EOFError):
            print("\nExiting game. Goodbye!")
            exit(0)

def play_game():
    print("=" * 35)
    print("      NUMPY TIC TAC TOE GAME       ")
    print("=" * 35)
    print("Type 'q' or 'quit' at any prompt to exit.\n")
    
    while True:
        # Step 1: Game Mode Selection
        print("Select Game Mode:")
        print(" 1. Player vs Player (PvP)")
        print(" 2. Player vs Computer (AI)")
        mode_choice = get_valid_input("Enter choice (1 or 2): ", ["1", "2"])
        
        vs_computer = (mode_choice == "2")
        ai_player = -1  # Computer plays as 'O'
        human_marker = 1  # Human plays as 'X'
        
        # If Player vs Computer, decide who goes first
        go_first = "1"
        if vs_computer:
            print("\nWho should go first?")
            print(" 1. Player (X)")
            print(" 2. Computer (O)")
            go_first = get_valid_input("Enter choice (1 or 2): ", ["1", "2"])
            
        board = initialize_board()
        # X starts the game (1 represented as 1, O represented as -1)
        current_turn = 1
        
        # If computer goes first, computer is X (1) and player is O (-1)
        if vs_computer and go_first == "2":
            ai_player = 1
            human_marker = -1
            
        print("\nGame started! Let's play!")
        
        while True:
            print_board(board)
            
            # Determine markers names
            current_symbol = "X" if current_turn == 1 else "O"
            
            is_computer_turn = vs_computer and (current_turn == ai_player)
            
            if is_computer_turn:
                print(f"Computer's turn ({current_symbol})... thinking...")
                pos = get_ai_move(board, ai_player)
                make_move(board, str(pos), ai_player)
                print(f"Computer placed marker on cell {pos}.")
            else:
                player_name = "Player" if not vs_computer else ("Player (X)" if human_marker == 1 else "Player (O)")
                while True:
                    pos_input = get_valid_input(f"{player_name}'s turn ({current_symbol}). Enter cell (1-9): ")
                    try:
                        make_move(board, pos_input, current_turn)
                        break  # Move successful, break current prompt loop
                    except TicTacToeError as e:
                        print(f"\033[93mError: {e}\033[0m")
            
            # Check for winner
            winner = check_winner(board)
            if winner is not None:
                print_board(board)
                winner_symbol = "X" if winner == 1 else "O"
                if vs_computer:
                    if winner == human_marker:
                        print("\033[92m🎉 Congratulations! You beat the computer! 🎉\033[0m")
                    else:
                        print("\033[91m🤖 Game Over! The computer won! 🤖\033[0m")
                else:
                    print(f"\033[92m🎉 Player {winner_symbol} wins the game! 🎉\033[0m")
                break
                
            # Check for draw
            if is_board_full(board):
                print_board(board)
                print("\033[93m🤝 It's a draw! Well played! 🤝\033[0m")
                break
                
            # Switch turns
            current_turn = -current_turn
            
        # Replay Option
        replay = get_valid_input("\nDo you want to play again? (y/n): ", ["y", "n", "yes", "no"])
        if replay in ["n", "no"]:
            print("Thanks for playing! Goodbye!")
            break
        print("\n" * 2)

if __name__ == "__main__":
    play_game()