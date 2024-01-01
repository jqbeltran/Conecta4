###
####
##### main_pygame.py contains the game with a graphical interface.
####
###


import numpy as np
import pygame
import sys
import math
from Conecta4.Utilities import Winner, Full
from Conecta4.Search import Best_move


## Create_board returns a board with all the positions empty
def Create_board():
    board = np.full((ROW_COUNT,COLUMN_COUNT), '.', dtype=str)
    return board


## Drop_piece drops a piece in the board in the given position and color
def Drop_piece(board, row, col, piece):
    board[row][col] = piece


## Is_valid_location checks if the given column is valid (not full)
def Is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == '.'


## Get_next_open_row returns the next open row in the given column
def Get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == '.':
            return r


## Draw_board draws the current board on the screen
def Draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, PURPLE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))   # Draw the board
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)   # Draw the circles of the board

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 'R':
                pygame.draw.circle(screen, PINK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)   # Draw the pink pieces (R for Rosa)
            elif board[r][c] == 'A': 
                pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)   # Draw the blue pieces (A for Azul)
    pygame.display.update()


## Play_game_1 is a function that contains the game loop for a local vs local game
def Play_game_1():
    board = Create_board()
    game_over = False
    turn = 0

    Draw_board(board)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))   # Draw the black rectangle on top of the board
    pygame.display.update()

    myfont = pygame.font.Font(None, 100)    # Font for the labels

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # If the user closes the window, the game ends
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # If the user presses B, it goes back to the main menu
                    Main_menu()
                elif event.key == pygame.K_r:   # If the user presses R, it restarts the game
                    board = Create_board()
                    game_over = False
                    turn = 0
                    Draw_board(board)
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    pygame.display.update()

            if event.type == pygame.MOUSEMOTION:    # If the user moves the mouse, it draws a circle on top of the board
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:    # If the user clicks, it drops a piece in the board
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if Is_valid_location(board, col):
                        row = Get_next_open_row(board, col)
                        Drop_piece(board, row, col, 'R')
                        drop_sound.play()
                        if Winner(board, 'R'):
                            label = myfont.render("Player 1 Wins!", 1, PINK)
                            label_rect = label.get_rect()
                            label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center  # Center the label
                            screen.blit(label, label_rect)
                            win_sound.play()
                            pygame.time.delay(500)
                            game_over = True
                        else:
                            turn = 1
                    else:
                        turn == 0
                else:               
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if Is_valid_location(board, col):
                        row = Get_next_open_row(board, col)
                        Drop_piece(board, row, col, 'A')
                        drop_sound.play()
                        if Winner(board, 'A'):
                            label = myfont.render("Player 2 Wins!", 1, BLUE)
                            label_rect = label.get_rect()
                            label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                            screen.blit(label, label_rect)
                            win_sound.play()
                            pygame.time.delay(500)
                            game_over = True
                        else:
                            turn = 0
                    else:
                        turn == 1

                Draw_board(board)

                if Full(board):    # If the board is full, it's a tie
                    label = myfont.render("It's a tie!", 1, PURPLE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    pygame.display.update()
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True

                if game_over:
                    pygame.time.wait(3000)


## Play_game_2 is a function that contains the game loop for a local vs AI game
def Play_game_2():
    board = Create_board()
    game_over = False
    turn = 0

    Draw_board(board)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))   # Draw the black rectangle on top of the board
    pygame.display.update()

    myfont = pygame.font.Font(None, 100)    # Font for the labels

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # If the user closes the window, the game ends
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: # If the user presses B, it goes back to the main menu
                    Main_menu()
                elif event.key == pygame.K_r:   # If the user presses R, it restarts the game
                    board = Create_board()
                    game_over = False
                    turn = 0
                    Draw_board(board)
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    pygame.display.update()

            if turn == 0:
                if event.type == pygame.MOUSEMOTION:    # If the user moves the mouse, it draws a circle on top of the board
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE / 2)), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:    # If the user clicks, it drops a piece in the board
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if Is_valid_location(board, col):
                        row = Get_next_open_row(board, col)
                        Drop_piece(board, row, col, 'R')
                        drop_sound.play()
                        if Winner(board, 'R'):
                            label = myfont.render("You Win!", 1, PINK)
                            label_rect = label.get_rect()
                            label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                            screen.blit(label, label_rect)
                            win_sound.play()
                            pygame.time.delay(500)
                            game_over = True
                        else:
                            turn = 1

            elif turn == 1:   # AI
                move = Best_move(board, 'A')
                board = move
                drop_sound.play()
                if Winner(board, 'A'):
                    label = myfont.render("AI Wins!", 1, BLUE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True
                else:
                    turn = 0

            Draw_board(board)

            if Full(board):   # If the board is full, it's a tie
                    label = myfont.render("It's a tie!", 1, PURPLE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    pygame.display.update()
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True

            if game_over:
                pygame.time.wait(3000)


## Play_game_3 is a function that contains the game loop for an AI vs local game
def Play_game_3():
    board = Create_board()
    game_over = False
    turn = 0

    Draw_board(board)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))   # Draw the black rectangle on top of the board
    pygame.display.update()

    myfont = pygame.font.Font(None, 100)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # If the user closes the window, the game ends
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: # If the user presses B, it goes back to the main menu
                    Main_menu()
                elif event.key == pygame.K_r:   # If the user presses R, it restarts the game
                    board = Create_board()
                    game_over = False
                    turn = 0
                    Draw_board(board)
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    pygame.display.update()

            if turn == 1:
                if event.type == pygame.MOUSEMOTION:    # If the user moves the mouse, it draws a circle on top of the board
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE / 2)), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:    # If the user clicks, it drops a piece in the board
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if Is_valid_location(board, col):
                        row = Get_next_open_row(board, col)
                        Drop_piece(board, row, col, 'R')
                        drop_sound.play()
                        if Winner(board, 'R'):
                            label = myfont.render("You Win!", 1, PINK)
                            label_rect = label.get_rect()
                            label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                            screen.blit(label, label_rect)
                            win_sound.play()
                            pygame.time.delay(500)
                            game_over = True
                        else:
                            turn = 0

            elif turn == 0:  # AI
                move = Best_move(board, 'A')
                board = move
                drop_sound.play()
                if Winner(board, 'A'):
                    label = myfont.render("AI Wins!", 1, BLUE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True
                else:
                    turn = 1

            Draw_board(board)

            if Full(board):  # If the board is full, it's a tie
                    label = myfont.render("It's a tie!", 1, PURPLE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    pygame.display.update()
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True

            if game_over:
                pygame.time.wait(3000)


## Play_game_4 is a function that contains the game loop for an AI vs AI game.
## It was used to test the AI, not used in the final version
'''
def Play_game_4():
    board = Create_board()
    game_over = False
    turn = 0

    Draw_board(board)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    pygame.display.update()

    myfont = pygame.font.Font(None, 75)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    Main_menu()

            if turn == 0:
                move = Best_move(board, 'R')
                board = move
                if Winner(board, 'R'):
                        label = myfont.render("AI 1 Wins!", 1, PINK)
                        label_rect = label.get_rect()
                        label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                        screen.blit(label, label_rect)
                        game_over = True
            else:
                move = Best_move(board, 'A')
                board = move
                if Winner(board, 'A'):
                        label = myfont.render("AI 2 Wins!", 1, BLUE)
                        label_rect = label.get_rect()
                        label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                        screen.blit(label, label_rect)
                        game_over = True

            Draw_board(board)
            turn += 1
            turn = turn % 2

            if Full(board):
                    label = myfont.render("It's a tie!", 1, PURPLE)
                    label_rect = label.get_rect()
                    label_rect.center = pygame.Rect(0, 0, width, SQUARESIZE).center
                    screen.blit(label, label_rect)
                    pygame.display.update()
                    lose_sound.play()
                    pygame.time.delay(500)
                    game_over = True

            if game_over:
                pygame.time.wait(3000)
'''


## Main_menu is a function that contains the main menu of the game
def Main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if button_game_1.collidepoint(pygame.mouse.get_pos()):  # It checks if the mouse is on the button
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # if it's true, the cursor change of shape
                elif button_game_2.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif button_game_3.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_game_1.collidepoint(pygame.mouse.get_pos()):  # It checks if the button was pressed
                    button_sound.play()
                    pygame.time.delay(1000)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Cursor shape becomes to its original form
                    Play_game_1()
                elif button_game_2.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    pygame.time.delay(1000)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    Play_game_2()
                elif button_game_3.collidepoint(pygame.mouse.get_pos()):
                    button_sound.play()
                    pygame.time.delay(1000)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    Play_game_3()

        # The next lines draw the images on the screen
        screen.blit(background_image, (0, 0))
        screen.blit(logo, logo_rect)
        screen.blit(button_image, button_game_1.topleft)
        screen.blit(button_image, button_game_2.topleft)
        screen.blit(button_image, button_game_3.topleft)

        font = pygame.font.Font(None, 36)   # Font for the text
        text_game_1 = font.render("Local vs. Local", True, (255, 255, 255))
        text_game_2 = font.render("Local vs. AI", True, (255, 255, 255))
        text_game_3 = font.render("AI vs. Local", True, (255, 255, 255))

        # Get the positions for center the texts
        text_rect_1 = text_game_1.get_rect()
        text_rect_1.center = button_game_1.center
        text_rect_2 = text_game_2.get_rect()
        text_rect_2.center = button_game_2.center
        text_rect_3 = text_game_3.get_rect()
        text_rect_3.center = button_game_3.center

        # They prints the text on the screen 
        screen.blit(text_game_1, text_rect_1)
        screen.blit(text_game_2, text_rect_2)
        screen.blit(text_game_3, text_rect_3)

        pygame.display.flip()


# Colors
PURPLE = (122,0,255)
BLACK = (0,0,0)
PINK = (255,0,193)
BLUE = (0,184,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100    # size of the imaginary squares on the board
RADIUS = int(SQUARESIZE/2 - 5)  # radius for the circles inside of the squares (where the pieces go in)

width = COLUMN_COUNT * SQUARESIZE   # Screen width
height = (ROW_COUNT + 1) * SQUARESIZE   # Screen height (we are adding 1 to ROW_COUNT because of the black rectangle on the top)
size = (width, height)


pygame.init()

screen = pygame.display.set_mode(size)

# It sets the background
background_image = pygame.image.load('./templates/background.jpg')
background_image = pygame.transform.scale(background_image, (width, height))

# Load the logo and set position
logo = pygame.image.load('./templates/logo.png')
logo = pygame.transform.scale(logo, (350, 350))
logo_rect = logo.get_rect()
logo_rect.centerx = width // 2
logo_rect.y = 0

# Set the feaures use for every button
button_width, button_height = 400, 75
button_image = pygame.image.load('./templates/button.png')
button_image = pygame.transform.scale(button_image, (button_width, button_height))

# Define buttons
button_game_1 = pygame.Rect((width - button_width) // 2, 300, button_width, button_height)
button_game_2 = pygame.Rect((width - button_width) // 2, 400, button_width, button_height)
button_game_3 = pygame.Rect((width - button_width) // 2, 500, button_width, button_height)

# Load sounds
drop_sound = pygame.mixer.Sound("./templates/drop.mp3")
button_sound = pygame.mixer.Sound("./templates/button.mp3")
lose_sound = pygame.mixer.Sound("./templates/lose.mp3")
win_sound = pygame.mixer.Sound("./templates/win.mp3")

Main_menu() # Initialize the game