"""
Tic Tac Toe Player
"""

import math

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
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if sum(arr.count(EMPTY) for arr in board) == 0:
        return True
    elif sum(arr.count(EMPTY) for arr in board) == 9:
        return False
    
    for i in range(len(board)):
        row = board[i]
        column = [ arr[i] for arr in board ]
    
        if column.count(column[0]) == 3 or row.count(row[0]) == 3:
            return True
    
    first_diag = [ board[0][0], board[1][1], board[2][2] ]
    second_diag = [ board[0][2], board[1][1], board[2][0] ]

    if first_diag.count(first_diag[0]) == 3 or second_diag.count(second_diag[0]) == 3:
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
