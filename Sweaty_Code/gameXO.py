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
            if ok==1:
                
                return True

        # Checking on columns
        for i in range(3):
            ok = 1
            for j in range(3):
                if self.board[j][i] != player:
                    ok = 0
                    break
            if ok==1:
                return True
                    

        # Checking the diagonals
        for i in range(3):
            ok = 1
            if self.board[i][i] != player:
                ok = 0
                break
        if ok==1:
            return True
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
            row = random.randint(0, 2)
            
            col = random.randint(0, 2)
            if self.board[row][col]=='-':
                free=False
                return row, col
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
        return -1, -1
    
    def strategy2(self, player):
        #first move should be in a corner and the second one should be on a line
        #that has the first piece on (blocking a line for the first player)
        
        #computing a counter (as we can't use the one in the startgame function)
        counter=9
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=='-':
                    counter-=1
        #choosing first move to be in a corner
        if counter==0:
            row = random.randint(0,1)
            col = random.randint(0,1)
            if row==1:
                row=2
            if col==1:
                col=2
            return row, col
        elif counter==1:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]!='-':
                        break
            
            while True:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
                if row== i or col==j:
                    return row, col
                elif i==j and row==col:
                    return row, col
                elif i+j==2 and row+col==2:
                    return row, col
        
        #checking for rows and columns which have 2 same pieces
        #so that the next move will be in the 3rd free space (for both players)
        #prefers to occupy a spot that wins rather one that stops the opponent from winning
        #checking rows
        a=-1
        b=-1
        for i in range(3):
            if self.board[i][0]== self.board[i][1] and self.board[i][2]=='-':
                if self.board[i][0]==player:
                    return i, 2
                else:
                    a=i
                    b=2
            else:
                if self.board[i][0]==self.board[i][2] and self.board[i][1]=='-':
                    if self.board[i][0]== player:
                        return i, 1
                    else:
                        a=i
                        b=1
                else:
                    if self.board[i][1]==self.board[i][2] and self.board[i][0]=='-':
                        if self.board[i][1]==player:
                            return i, 0
                        else:
                            a=i
                            b=0
                    
        #checking for columns
        for i in range(3):
            if self.board[0][i]== self.board[1][i] and self.board[2][i]=='-':
                if self.board[0][i]==player:
                    return 2,i
                else:
                    a=2
                    b=i
            else:
                if self.board[0][i]==self.board[2][i] and self.board[1][i]=='-':
                    if self.board[0][i]==player:
                        return 1,i
                    else:
                        a=1
                        b=i
                else:
                    if self.board[1][i]==self.board[2][i] and self.board[0][i]=='-':
                        if self.board[1][i]==player:
                            return 0,i
                        else:
                            a=0
                            b=i
        #checking for diagonals
        if self.board[0][0]==self.board[1][1] and self.board[2][2]=='-':
            if self.board[0][0]==player:
                return 2,2
            else:
                a=2
                b=2
        else:
            if self.board[0][0]==self.board[2][2] and self.board[1][1]=='-':
                if self.board[0][0]==player:
                    return 1,1
                else:
                    a=1
                    b=1
            else:
                if self.board[1][1]==self.board[2][2] and self.board[0][0]=='-':
                    if self.board[1][1]==player:
                        return 0,0
                    else:
                        a=0
                        b=0
        if self.board[0][2]==self.board[1][1] and self.board[2][0]=='-':
            if self.board[0][2]==player:
                return 2,0
            else:
                a=2
                b=0
        else:
            if self.board[0][2]==self.board[0][2] and self.board[1][1]=='-':
                if self.board[0][2]==player:
                    return 1,1
                else:
                    a=1
                    b=1
            else:
                if self.board[1][1]==self.board[2][0] and self.board[0][2]=='-':
                    if self.board[1][1]==player:
                        return 0,2
                    else:
                        a=0
                        b=2
        
        if a>=0 and b>=0:
            return a, b
        return -1, -1
    
            
                
        
        
    
    def take_turn(self, strategy, computer):
        if strategy == 1:               #'random':
            print("random")
            return self.free_space()
        elif strategy == 2:     # == 'smart_2':
            print("medium")
            return self.strategy1()
        elif strategy == 3:             # == 'smart_3':
            print("smart")
            return self.strategy2(computer)
        else:
            print ('No strategy chosen defaulting to random')
            return self.free_space()

    def startgame(self, strategyIndexX, strategyIndexO):  # Call other functions in here to run the game.
        self.__init__() # added this so you can continually initiate game

        self.setBoard()
        print(self.board)

        count=0
        computer = 'X' if self.firstTurn() == 1 else 'O' # randomly get first player
        while True:
            print (computer, "turn")
            count += 1
            if computer == 'X':
                i, j = self.take_turn(strategyIndexX, computer)
            else:
                i, j = self.take_turn(strategyIndexO, computer)
            if i==-1 and j==-1:
                i, j= self.free_space() 
                
            self.placement(i, j, computer)
        # while True:
        #     print(computer, "turn")
        #     count+=1
        #     if computer == 'X':
        #         if strategyIndexX == 1:
        #             i, j = self.take_turn(self.free_space())
        #         elif strategyIndexX==2:
        #             i, j = self.take_turn(self.strategy1())
        #         else: 
        #             i,j= self.take_turn(self.strategy2('X'))
        #     else:
        #         if strategyIndexO == 1:
        #             i, j = self.take_turn(self.free_space())
        #         elif strategyIndexO==2:
        #             i, j = self.take_turn(self.strategy1())
        #         else: 
        #             i,j= self.take_turn(self.strategy2('X'))
        #     self.placement(i, j, computer)
            
            self.showBoard()

            # You can add this check only if number of turns is greater than 5 here (add a counter)
            # Check if the current player wins
            if count>4:
                if self.winner(computer):
                    print("Player", computer, "wins the game!")
                    return computer
                    break
            
            # if you have a counter here you don't need to check the board is full but break after 9 turns
            # Check if the board is full
            if count==9:
                print("Draw match!")
                break

            # Change players
            computer = self.swap_player_turn(computer)

        print()
        
        self.showBoard()


t = tictactoe()
t.startgame(3,1)

#next task: make an even better strategy, even closer to how a human in playing

#next task: make x play with random startegy and O with strategy1 and plot the sample of wins

N = 1000
a=np.zeros(N)
b=np.zeros(N)
winsX=0
winsO=0

t = tictactoe()
for i in range(1,N):
    # 3 = 'smart_2'
    # 2 = 'smart_1'
    # 1 = 'random'
    computer=t.startgame(2,1) # first position fives strategy of X, second position gives strategy of O
    if computer:
        if computer=='X':
            winsX+=1
        else:
            winsO+=1
    a[i]=winsX
    b[i]=winsO

from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
    
plt.plot(range(N), a, label='X wins')
plt.plot(range(N), b, label='O wins')
plt.xlabel('Number of wins')
plt.ylabel('Number of games played')
plt.title('X-medium strategy, O- random strategy')
plt.legend()
