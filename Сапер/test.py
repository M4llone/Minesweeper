import random

board = [[0 for i in range(10)] for i in range(10)]
count = 0
while count != 10:
    coord1 = random.randint(0,9)
    coord2 = random.randint(0,9)
    if board[coord1][coord2] != -1:
        board[coord1][coord2] = -1
        count += 1

for row in range(10):
    for col in range(10):
        if board[row][col] != -1:
            count = 0
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if (0 <= r < 10 and 0 <= c < 10):
                        if board[r][c] == -1:
                            count += 1
            board[row][col] = count
        


for row in board:
    print(' '.join(str(cell).rjust(2) for cell in row))