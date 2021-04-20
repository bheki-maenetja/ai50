"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(arr.count("X") for arr in board)
    o_count = sum(arr.count("O") for arr in board)
    if x_count > o_count:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return [(i, j) for i, arr in enumerate(board) for j, elem in enumerate(arr) if board[i][j] == EMPTY]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    current_player = player(board_copy)
    i, j = action
    if board_copy[i][j] == EMPTY:
        board_copy[i][j] = current_player
        return board_copy
    else:
        raise NameError("Can't make that move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        row = board[i]
        column = [ arr[i] for arr in board ]
    
        if column.count("X") == 3 or row.count("X") == 3:
            return "X"
        
        if column.count("O") == 3 or row.count("O") == 3:
            return "O"
    
    first_diag = [ board[0][0], board[1][1], board[2][2] ]
    second_diag = [ board[0][2], board[1][1], board[2][0] ]

    if first_diag.count("X") == 3 or second_diag.count("X") == 3:
        return "X"
    
    if first_diag.count("O") == 3 or second_diag.count("O") == 3:
        return "O"
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if sum(arr.count(EMPTY) for arr in board) == 0 or winner(board):
        return True
    return False

    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == "X":
        return 1
    elif game_winner == "O":
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if current_player == "X":
        action_values = [(action, min_value(result(board, action))) for action in actions(board)]
        return max(action_values, key=lambda x: x[1])[0]
    elif current_player == "O":
        action_values = [(action, max_value(result(board, action))) for action in actions(board)]
        return min(action_values, key=lambda x: x[1])[0]

def max_value(board):
    """
    Returns the highest possible utility value from a given board
    """
    v = -math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    """
    Returns the lowest possible utility value from a given board
    """
    v = math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
