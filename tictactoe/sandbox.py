from tictactoe import minimax


EMPTY = None

board = [[EMPTY, "X", "O"],
            ["X", "X", EMPTY],
            [EMPTY, "O", "O"]]

optimal_action = minimax(board)
print(optimal_action)
