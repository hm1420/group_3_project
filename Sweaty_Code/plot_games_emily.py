import pandas as pd  # noqa F401   
import numpy as np  # noqa F401
import string  # noqa F401
import random  # noqa F401


class tictactoe:  # Main Class
    def __init__(self, strategyX = 'random', strategyO = 'random'):  # Initialises new array for board
        self.board = []
        self.strategyX = strategyX
        self.strategyO = strategyO

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
        nr=0
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=='-':
                    nr+=1
        if nr>5:
            return False
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
        #this strategy is choosing the move in a random way
        free=True
        while free==True:
            row = random.randint(1, 3)
            col = random.randint(1, 3)
            if self.board[row-1][col-1]=='-':
                free=False
                return row-1, col-1
                break
    
    def strategy1(self):
        #checking for rows and columns which have 2 same pieces
        #so that the next move will be in the 3rd free space (for both players)
        #checking rows
        for i in range(3):
            if self.board[i][0]== self.board[i][1] and self.board[i][2]=='-':
                return i, 2
            else:
                if self.board[i][0]==self.board[i][2] and self.board[i][1]=='-':
                    return i, 1
                else:
                    if self.board[i][1]==self.board[i][2] and self.board[i][0]=='-':
                        return i, 0
                    
        #checking for columns
        for i in range(3):
            if self.board[0][i]== self.board[1][i] and self.board[2][i]=='-':
                return 2,i
            else:
                if self.board[0][i]==self.board[2][i] and self.board[1][i]=='-':
                    return 1, i
                else:
                    if self.board[1][i]==self.board[2][i] and self.board[0][i]=='-':
                        return 0,i
        #checking for diagonals
        if self.board[0][0]==self.board[1][1] and self.board[2][2]=='-':
            return 2,2
        else:
            if self.board[0][0]==self.board[2][2] and self.board[1][1]=='-':
                return 1,1
            else:
                if self.board[1][1]==self.board[2][2] and self.board[0][0]=='-':
                    return 0,0
        if self.board[0][2]==self.board[1][1] and self.board[2][0]=='-':
            return 2,0
        else:
            if self.board[0][2]==self.board[0][2] and self.board[1][1]=='-':
                return 1,1
            else:
                if self.board[1][1]==self.board[2][0] and self.board[0][2]=='-':
                    return 0,2
        return False
    
    def take_turn(self, strategy):
        if strategy == 'random':
            return self.free_space()
        elif strategy == 'smart':
            return self.strategy1()
        else:
            return self.free_space()

    def startgame(self):  # Call other functions in here to run the game.
        self.__init__() # added this so you can continually initiate game
        self.setBoard()
        print(self.board)

        computer = 'X' if self.firstTurn() == 1 else 'O'
        while True:
            print(computer, "turn")
            if computer == 'X':
                i, j = self.take_turn(self.strategyX)
            else:
                i, j = self.take_turn(self.strategyO)
            self.placement(i, j, computer)
            self.showBoard()

            # You can add this check only if number of turns is greater than 5 here (add a counter)
            # Check if the current player wins
            if self.winner(computer):
                print("Player", computer, "wins the game!")
                return computer
                break
            
            # if you have a counter here you don't need to check the board is full but break after 9 turns
            # Check if the board is full
            if self.is_board_filled():
                print("Draw match!")
                break

            # Change players
            computer = self.swap_player_turn(computer)

        print()
        
        self.showBoard()


t = tictactoe()
t.startgame()

#next task: make x play with random startegy and O with strategy1 and plot the sample of wins
#for 100 games
N = 1000
a=np.zeros(N)
b=np.zeros(N)
winsX=0
winsO=0

t = tictactoe()
for i in range(1,N):
    computer=t.startgame()
    if computer:
        if computer=='X':
            winsX+=1
        else:
            winsO+=1
    a[i]=winsX
    b[i]=winsO

from matplotlib import pyplot as plt
plt.plot(range(N), a, label='X wins')
plt.plot(range(N), b, label='O wins')
plt.legend()