# app.py

import streamlit as st
import math
import time

# --- Constants and Game Logic ---
# Players are now emojis
AI_PLAYER, HUMAN_PLAYER = '🤖', '😊'

def check_winner(board):
    """Checks for a winner. Returns the emoji of the winner or None."""
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ': return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ': return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ': return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ': return board[0][2]
    return None

def is_board_full(board):
    """Checks if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def get_available_moves(board):
    """Returns a list of (row, col) tuples for empty spots."""
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']

# --- AI's Brain: The Minimax Algorithm ---

def minimax(board, is_maximizing):
    """Minimax algorithm implementation."""
    winner = check_winner(board)
    if winner == AI_PLAYER: return 10
    if winner == HUMAN_PLAYER: return -10
    if is_board_full(board): return 0

    if is_maximizing:
        best_score = -math.inf
        for r, c in get_available_moves(board):
            board[r][c] = AI_PLAYER
            score = minimax(board, False)
            board[r][c] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for r, c in get_available_moves(board):
            board[r][c] = HUMAN_PLAYER
            score = minimax(board, True)
            board[r][c] = ' '
            best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Finds the best possible move for the AI."""
    best_score = -math.inf
    best_move = None
    for r, c in get_available_moves(board):
        board[r][c] = AI_PLAYER
        score = minimax(board, False)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

# --- Streamlit Web App Interface ---

st.set_page_config(page_title="Emoji Tic-Tac-Toe AI", layout="centered")
st.title("Emoji Tic-Tac-Toe AI")

# Explicitly state who is who
st.markdown("### You are player 😊. The AI is player 🤖.")

# Expander explaining the AI model
with st.expander("How does this AI work? (It's not a pretrained model!)"):
    st.markdown("""
    This AI uses the **Minimax algorithm**, a classic logic-based approach for two-player games. It does not use a pretrained model like GPT.

    **Here’s how it works:**
    1.  **Looks Ahead:** It explores every possible future move down to the end of the game.
    2.  **Assigns Scores:** It gives a score to each final outcome (+10 for an AI win, -10 for a human win, 0 for a draw).
    3.  **Assumes You're Smart:** It assumes you will always make the best possible move to beat it.
    4.  **Finds the Optimal Path:** It chooses the move that guarantees the best possible score for itself, no matter what you do.

    Because Tic-Tac-Toe is a "solved game," Minimax can calculate a provably perfect move every time, making it **unbeatable**.
    """)

# --- Game State Initialization ---
def new_game():
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.player_turn = HUMAN_PLAYER
    st.session_state.game_over = False
    st.session_state.winner = None

if 'board' not in st.session_state:
    new_game()

# --- Display Game Board and Handle Clicks ---
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        button_key = f"cell_{r}_{c}"
        cell_content = st.session_state.board[r][c]
        
        # Display bigger emojis on buttons
        if cols[c].button(cell_content if cell_content != ' ' else '  ', key=button_key, use_container_width=True,
                          disabled=(cell_content != ' ' or st.session_state.game_over)):
            
            st.session_state.board[r][c] = HUMAN_PLAYER
            st.session_state.player_turn = AI_PLAYER
            
            winner = check_winner(st.session_state.board)
            if winner or is_board_full(st.session_state.board):
                st.session_state.game_over = True
                st.session_state.winner = winner
            st.rerun()

# --- AI's Turn Logic ---
if st.session_state.player_turn == AI_PLAYER and not st.session_state.game_over:
    with st.spinner("AI is thinking..."):
        time.sleep(0.5)
        ai_move = find_best_move(st.session_state.board)
        if ai_move: st.session_state.board[ai_move[0]][ai_move[1]] = AI_PLAYER
        
        winner = check_winner(st.session_state.board)
        if winner or is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = winner
        st.session_state.player_turn = HUMAN_PLAYER
        st.rerun()

# --- Game Status and New Game Button ---
st.markdown("---")
if st.session_state.game_over:
    winner = st.session_state.winner
    if winner: st.success(f"🎉 Winner is {winner}! 🎉")
    else: st.warning("🤝 It's a draw! 🤝")

st.button("✨ New Game", on_click=new_game)