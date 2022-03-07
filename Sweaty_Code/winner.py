import pandas as pd  # noqa F401   
import numpy as np  # noqa F401
import string  # noqa F401
import random  # noqa F401


class tictactoe:  # Main Class

    def __init__(self):  # Initialises new array for board
        self.board = []

    def setBoard(self):  # Sets the 3 rows into a 2-D array
        for x in range(3):
            self.board.append(['-', '-', '-'])

    def firstTurn(self):  # Determines the 1st turn being either 'X' or 'O'
        first = random.randint(0, 1)
        return first

    def placement(self, row, col, computer):
        # Sets the row and column position from the computer input
        self.board[row][col] = computer

    def winner(self, player):
        # Only after 5 moves, there can be 3 pieces of the same kind
        # Checking on rows
        for i in range(3):
            ok = 1
            for j in range(3):
                if self.board[i][j] != player:
                    ok = 0
                    break

        # Checking on columns
        for i in range(3):
            ok = 1
            for j in range(3):
                if self.board[j][i] != player:
                    ok = 0
                    break

        # Checking the diagonals
        for i in range(3):
            ok = 1
            if self.board[i][i] != player:
                ok = 0
                break
        for i in range(3):
            ok = 1
            if self.board[i][2-i] != player:
                ok = 0
                break
        if ok == 1:
            return True
        return False

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def showBoard(self):  # Visual display for board when called
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()
            
    def free_space(self):
        free=True
        while free==True:
            row = random.randint(1, 3)
            col = random.randint(1, 3)
            if self.board[row-1][col-1]=='-':
                free=False
                return row-1, col-1
                break
            
                   

    def startgame(self):  # Call other functions in here to run the game.
        self.setBoard()
        print(self.board)

        computer = 'X' if self.firstTurn() == 1 else 'O'
        while True:
            print(computer, "turn")


            # Random move from the computer adding a piece to the board
            row = random.randint(1, 3)
            col = random.randint(1, 3)
            i, j= self.free_space()

            self.placement(i, j, computer)
            self.showBoard()

            # Check if the current player wins
            if self.winner(computer):
                print("Player", computer, "wins the game!")
                break

            # Check if the board is full
            if self.is_board_filled():
                print("Draw match!")
                break

            # Change players
            computer = self.swap_player_turn(computer)

        print(row, col)

        print()
        self.showBoard()


t = tictactoe()
t.startgame()
       