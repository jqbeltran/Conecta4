###
####
#####    Search.py contains the functions used in the search algorithm (Alpha-Beta Pruning).
####
###


import numpy as np
from .Utilities import *


## Best_move is a function that returns the best move for a board in a given depth (default = 5)
def Best_move(board, color, depth = 5):
    best_value = float('-inf')
    best_move = None
    for move in Successors(board, color):
        value = Search_alpha_beta(move, color, depth)   # Get the value of the move
        if value > best_value:  # If the value is greater than the current best value, it becomes the new best value
            best_value = value
            best_move = move
    return best_move


## Search_alpha_beta is a function that returns the value of a board using the Alpha-Beta Pruning algorithm
def Search_alpha_beta(board, color, depth):
    v = Min_value(board, -np.inf, np.inf, color, depth)
    return v


## Max_value returns the maximum value of the Successors of a board (Don't modify index)
def Max_value(board, alpha, beta, color, depth, index = 0):
    if index == depth:
        return Heuristic(board, color)
    if Test_terminal(board):
        return Heuristic(board, color)
    v = -np.inf
    for s in Successors(board, color):
        v = max(v, Min_value(s, alpha, beta, color, depth, index + 1))  # It checks if the minimum of the Successors is greater than the current value
        alpha = max(alpha, v)
        if v >= beta:   # if the value is greater or equal to beta, it prunes
            return v
    return v


## Min_value returns the minimum value of the Successors of a board (Don't modify index)
def Min_value(board, alpha, beta, color, depth, index = 0):
    if index == depth:
        return Heuristic(board, color)
    if Test_terminal(board):
        return Heuristic(board, color)
    v = np.inf
    for s in Successors(board, Invert_color(color)):
        v = min(v, Max_value(s, alpha, beta, color, depth, index + 1))    # It checks if the maximum of the Successors is less than the current value
        beta = min(beta, v)
        if v <= alpha:   # If the value is less or equal to alpha, it prunes
            return v
    return v


## Heuristic is a function that returns the utility of a board. 
## It gives a score to each disk in the board depending on its position. 
## The score is higher if the disk is in the center of the board (more combinations to form a 4-line)
## The final score is the sum of the scores of all the disks of the player minus the sum of the scores of all the disks of the opponent
def Heuristic(board, color):
    column_value = [1, 2, 3, 4, 3, 2, 1]
    row_value = [1, 2, 3, 3, 2, 1]
    diagonal_value = [[1, 1, 1, 2, 1, 1, 1], [1, 2, 3, 4, 3, 2, 1], [1, 3, 5, 6, 5, 3, 1], [1, 3, 5, 6, 5, 3, 1], [1, 2, 3, 4, 3, 2, 1], [1, 1, 1, 2, 1, 1, 1]]
    utility_disk = 0
    utility_disk_opponent = 0

    for row in range(6):
        for column in range(7):
            if board[row][column] == color:
                utility_disk += column_value[column] + row_value[row] + diagonal_value[row][column]
            elif board[row][column] == Invert_color(color):
                utility_disk_opponent += column_value[column] + row_value[row] + diagonal_value[row][column]

    if Test_terminal(board):    # Penalty for losing or reward for winning
        if Winner(board, color):
            return 1000
        elif Winner(board, Invert_color(color)):
            return -1000
        else:
            return 0

    return utility_disk - utility_disk_opponent