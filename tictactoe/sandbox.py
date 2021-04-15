EMPTY = None

board = [[EMPTY, "X", "O"],
            ["O", EMPTY, EMPTY],
            ["X", "O", EMPTY]]

if sum(arr.count(EMPTY) for arr in board) == 0:
    print("Board full")
elif sum(arr.count(EMPTY) for arr in board) == 9:
    print("Board empty")
    


for i in range(len(board)):
    row = board[i]
    column = [ arr[i] for arr in board ]
    if column.count(column[0]) == 3:
        print("Straight column", column, end="\n")
    
    if row.count(row[0]) == 3:
        print("Straight row", row, end="\n")

first_diag = [ board[0][0], board[1][1], board[2][2] ]
second_diag = [ board[0][2], board[1][1], board[2][0] ]

if first_diag.count(first_diag[0]) == 3 or second_diag.count(second_diag[0]) == 3:
    print("Straight diagonal")