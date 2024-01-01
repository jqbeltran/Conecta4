###
####
####
#####    main.py contains a simple version of the game. 
#####    It prints the board on the console.
####
####
###


import numpy as np
from Conecta4.Utilities import *
from Conecta4.Search import *


board = np.full((6, 7), '.', dtype=str)

## Game loop (PC vs Player)
'''
for i in range(42):
    if i % 2 == 0:
        # PC
        move = Best_move(board, 'R')
        board = move
    else:
        # Player
        move = int(input("Select column (0-6): "))
        for j in range(6):
            if board[j][move] == '.':
                board[j][move] = 'A'
                break
    for j in range(5, -1, -1):
        for k in range(7):
            print(board[j][k], end=" ")
        print()
    print("\n")
    result = Utility(board, 'R')
    if result is not None:
        if result == 1:
            print("PC wins!")
        elif result == -1:
            print("Player wins!")
        else:
            print("It's a tie!")
        break
'''


## Game loop (PC vs PC)
for i in range(42):
    if i % 2 == 0:
        # PC 1
        move = Best_move(board, 'R')
        board = move
    else:
        # PC 2
        move_2 = Best_move(board, 'A')
        board = move_2
    for j in range(5, -1, -1):
        for k in range(7):
            print(board[j][k], end=" ")
        print()
    print("\n")
    result = Utility(board, 'R')
    if result is not None:
        if result == 1:
            print("PC 1 wins!")
        elif result == -1:
            print("PC 2 wins!")
        else:
            print("It's a tie!")
        break