## We put CFR Coded Algorithm here!

import pandas as pd
import numpy as np

import string
import random


class tictactoe: #Main Class

    def __init__(self): #Initialises new array for board
        self.board = []

    def setBoard(self): #Sets the 3 rows into a 2-D array
        for x in range (3):
            row = []
            for i in range (3):
                row.append('-')
            self.board.append(row)

    def showBoard(self): #Visual display for board when called
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def firstTurn(self): #Determines the 1st turn being either 'X' or 'O'
        first=random.randint(0,1)
        return first

    def placement(self, row, col, computer): #Sets the row and column position from the computer input
        self.board[row][col] = computer



    def startgame(self): #Call other functions in here to run the game.
        
        self.setBoard()
        print(self.board)

        
        computer = 'X' if self.firstTurn() == 0 else 'O'
        
        self.showBoard()
        
        row = random.randint(1,3)   #Random move from the computer adding a piece to the board
        col = random.randint(1,3)
        
        self.placement(row - 1, col - 1, computer)

        print(row,col)

        print()
        self.showBoard()
            


t = tictactoe()
t.startgame()
