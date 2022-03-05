## We put CFR Coded Algorithm here!

import pandas as pd
import numpy as np

class tictactoe: #Main Class

    def __init__(self): #Initialises empty array for the board
        self.board = []

    def setBoard(self): #Sets the 3 rows into a 2-D array
        for x in range (3):
            row = []
            for i in range (3):
                row.append('-')
            self.board.append(row)

    def showBoard(self): #Visual display for array
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def startgame(self): #Place other other functions in here in the right order for the game
        self.setBoard()
        self.showBoard()

t = tictactoe()
t.startgame()
