### 
####
#####   Utilities.py contains some of the functions used in the game.
####
###


## Test_terminal is a function that checks if the board is terminal
def Test_terminal(board):
    if Winner(board, 'R') or Winner(board, 'A') or Full(board):
        return True
    else:
        return False
    

## Utility is a function that returns a simple utility of a board
def Utility(board, color):
    winner = Winner(board, color)
    loser = Winner(board, Invert_color(color))

    if winner:
        return 1
    elif loser:
        return -1
    elif Full(board):
        return 0
    else:
        return None
    

## Invert_color is a function that returns the opposite color
def Invert_color(color):
    return 'R' if color == 'A' else 'A'


## Winner is a function that checks if the current board has a winner
def Winner(board, color):
    def In_line(directions):    # Check if there are 4 in line
        for dir_r, dir_c in directions:
            for row in range(6):
                for column in range(7):
                    for i in range(4):
                        new_row = row + i * dir_r
                        new_column = column + i * dir_c

                        if 0 <= new_row < 6 and 0 <= new_column < 7:    # Verify that the position is inside the board
                            if board[new_row, new_column] != color:
                                break
                        else:
                            break
                    else:
                        return True
        return False

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal /, Diagonal \

    return In_line(directions)


## Full is a function that checks if the board is full
def Full(board):
    return not any(board[5, column] == '.' for column in range(7))


## Successors is a function that returns a list of the possible boards after a move
def Successors(board, color):
    successor = board.copy()
    successors = []
    for i in range(7):
        for j in range(6):
            if successor[j][i] == '.':
                temp = successor.copy()
                temp[j][i] = color
                successors.append(temp)
                break
    return successors