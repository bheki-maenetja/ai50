from tictactoe import winner

EMPTY = None

board = [["X", "X", "O"],
            ["O", "O", EMPTY],
            ["O", "O", "X"]]

print(winner(board))
