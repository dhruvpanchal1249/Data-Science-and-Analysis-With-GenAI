import streamlit as st
import numpy as np
import random

# --------------------------
# Functions
# --------------------------

def initialize_board():
    return np.zeros((3, 3), dtype=int)


def check_winner(board):
    row_sums = board.sum(axis=1)
    col_sums = board.sum(axis=0)

    diag1 = np.trace(board)
    diag2 = np.trace(np.fliplr(board))

    all_sums = np.concatenate([row_sums, col_sums, [diag1, diag2]])

    if 3 in all_sums:
        return 1
    elif -3 in all_sums:
        return -1
    return None


def board_full(board):
    return not np.any(board == 0)


def get_ai_move(board, ai):

    opponent = -ai

    empty = []

    for pos in range(1, 10):
        r = (pos - 1) // 3
        c = (pos - 1) % 3

        if board[r][c] == 0:
            empty.append(pos)

    # Win
    for pos in empty:
        temp = board.copy()
        r = (pos - 1) // 3
        c = (pos - 1) % 3

        temp[r][c] = ai

        if check_winner(temp) == ai:
            return pos

    # Block
    for pos in empty:
        temp = board.copy()
        r = (pos - 1) // 3
        c = (pos - 1) % 3

        temp[r][c] = opponent

        if check_winner(temp) == opponent:
            return pos

    # Center
    if 5 in empty:
        return 5

    return random.choice(empty)


def make_move(position):

    board = st.session_state.board

    r = (position - 1) // 3
    c = (position - 1) % 3

    if board[r][c] != 0:
        return

    board[r][c] = st.session_state.current_player

    winner = check_winner(board)

    if winner is not None:
        st.session_state.game_over = True
        st.session_state.winner = winner
        return

    if board_full(board):
        st.session_state.game_over = True
        st.session_state.winner = 0
        return

    st.session_state.current_player *= -1

    # AI Move
    if (
        st.session_state.mode == "Player vs AI"
        and st.session_state.current_player == st.session_state.ai_player
        and not st.session_state.game_over
    ):

        ai_pos = get_ai_move(board, st.session_state.ai_player)

        r = (ai_pos - 1) // 3
        c = (ai_pos - 1) % 3

        board[r][c] = st.session_state.ai_player

        winner = check_winner(board)

        if winner is not None:
            st.session_state.game_over = True
            st.session_state.winner = winner
            return

        if board_full(board):
            st.session_state.game_over = True
            st.session_state.winner = 0
            return

        st.session_state.current_player *= -1


# --------------------------
# Session State
# --------------------------

if "board" not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.current_player = 1
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.mode = "Player vs Player"
    st.session_state.ai_player = -1

# --------------------------
# UI
# --------------------------

st.title("🎮 Tic Tac Toe")

mode = st.selectbox(
    "Choose Game Mode",
    ["Player vs Player", "Player vs AI"],
)

if mode != st.session_state.mode:
    st.session_state.mode = mode
    st.session_state.board = initialize_board()
    st.session_state.current_player = 1
    st.session_state.game_over = False
    st.session_state.winner = None

if mode == "Player vs AI":
    first = st.radio(
        "Who goes first?",
        ["Player", "Computer"],
    )

    if first == "Player":
        st.session_state.ai_player = -1
    else:
        st.session_state.ai_player = 1

        if np.all(st.session_state.board == 0):
            ai = get_ai_move(st.session_state.board, 1)

            r = (ai - 1) // 3
            c = (ai - 1) % 3

            st.session_state.board[r][c] = 1
            st.session_state.current_player = -1

symbols = {
    1: "❌",
    -1: "⭕",
    0: ""
}

board = st.session_state.board

# --------------------------
# Board
# --------------------------

for i in range(3):
    cols = st.columns(3)

    for j in range(3):

        value = board[i][j]

        if cols[j].button(
            symbols[value] if value != 0 else " ",
            key=f"{i}-{j}",
            use_container_width=True,
            disabled=value != 0 or st.session_state.game_over,
        ):
            make_move(i * 3 + j + 1)
            st.rerun()

# --------------------------
# Status
# --------------------------

st.write("---")

if not st.session_state.game_over:

    turn = "❌" if st.session_state.current_player == 1 else "⭕"

    if (
        mode == "Player vs AI"
        and st.session_state.current_player == st.session_state.ai_player
    ):
        st.info(f"Computer's Turn {turn}")
    else:
        st.info(f"Current Turn: {turn}")

else:

    if st.session_state.winner == 1:
        st.success("❌ Wins!")

    elif st.session_state.winner == -1:
        st.success("⭕ Wins!")

    else:
        st.warning("It's a Draw!")

# --------------------------
# Restart
# --------------------------

if st.button("🔄 Restart Game"):

    st.session_state.board = initialize_board()
    st.session_state.current_player = 1
    st.session_state.game_over = False
    st.session_state.winner = None

    st.rerun()