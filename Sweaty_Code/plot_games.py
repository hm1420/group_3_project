import pandas as pd  # noqa F401   
import numpy as np  # noqa F401
import string  # noqa F401
import random  # noqa F401


class tictactoe:  # Main Class
    def __init__(self):  # Initialises new array for board
        self.board = []
        self.players = {-1:'O', 1:'X'}

    def setBoard(self):  # Sets the 3 rows into a 2-D array
        self.board = np.tile(0, (3,3))

    def firstTurn(self):  # Determines the 1st turn being either 'X' or 'O'
        first = np.random.choice([-1, 1])
        return first

    def placement(self, row, col, computer):
        # Sets the row and column position from the computer input
        self.board[row][col] = computer

    def winner(self, player):
        # checking on row
        if player*3 in np.sum(self.board, axis=0):
            return True

        # # Checking on columns
        if player*3 in np.sum(self.board, axis=1):
            return True
        # Checking the diagonal1
        if player*3 == np.trace(self.board):
            return True
        # checking the diagonal 2
        if player*3 == np.trace(np.rot90(self.board)):
            return True

    def is_board_filled(self):
        if np.where(self.board == 0)[0].shape == 0:
            # no more spaces
            return True
        elif np.where(self.board == 0)[0].shape != 0:
            # there are more spaces
            return False

##########################################################################################

    def swap_player_turn(self, player):
        return player*-1

    def showBoard(self):  # Visual display for board when called
        # convert matrix to 'X' and 'O'
        pieces = {1:'X', -1:'O', 0: '-'}
        for row in self.board:
            for item in row:
                print(pieces[item],  end=" ")
            print()
            
    def free_space(self):
        # this strategy is choosing the move in a random way
        free=True
        while free==True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col]==0:
                free=False
                return row, col
                break
    
    def strategy1(self, player):
        #checking for rows and columns which have 2 same pieces
        #so that the next move will be in the 3rd free space (for either player)

        # checking on columns
        if np.abs(player)*2 in np.abs(np.sum(self.board, axis=0)):
            # get column(s) with 2 
            row_idy = np.argwhere(np.abs(np.sum(self.board, axis=0) )== np.abs(player)*2 ).squeeze()
            # sample column in the case there is more than 2
            idy = int([np.random.choice(row_idy) if row_idy.shape != () else row_idy][0])
            # get the row axis
            idx = np.argwhere(self.board[:,idy] == 0)[0][0]
            return idx, idy

        # checking on rows
        if np.abs(player)*2 in np.abs(np.sum(self.board, axis=1)):
            # get row(s) with 2
            row_idx = np.argwhere(np.abs(np.sum(self.board, axis=1) )== np.abs(player)*2).squeeze()
            # sample row in the case there is more than 2
            idx = int([np.random.choice(row_idx) if row_idx.shape != () else row_idx][0])
            # add the final piece for winning move
            idy = np.argwhere(self.board[idx,:] == 0)[0][0]
            return idx, idy

        # checking on diagonal1
        if np.abs(player)*2 == np.abs(np.trace(self.board)):
            # get diagonal(s) with 2
            if self.board[0][0] == 0:
                idx, idy = 0, 0
            elif self.board[2][2]==0:
                idx, idy = 2, 2
            else:
                idx, idy=1,1
            return idx, idy

        # checking on diagonal2
        if np.abs(player)*2 ==np.abs( np.trace(np.rot90(self.board))):
            # get diagonal(s) with 2
            if self.board[0][2] == 0:
                idx, idy = 0, 2
            elif self.board[1][1]==0:
                idx, idy =1,1     
            else:
                idx, idy = 2, 0
            return idx, idy

        idx, idy = self.free_space()
        return idx, idy
    
    def strategy2(self, player):
        #first move should be in a corner and the second one should be on a line
        #that has the first piece on (blocking a line for the first player)
        
        #computing a counter (as we can't use the one in the startgame function)
        counter=9
        for i in range(3):
            for j in range(3):
                if self.board[i][j]==0:
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
                    if self.board[i][j]!=0:
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
        a=2
        b=2
        
        # checking on columns
        if np.abs(player)*2 in np.abs( np.sum(self.board, axis=0)):
            # get column(s) with 2 
            row_idy = np.argwhere(np.abs(np.sum(self.board, axis=0)) ==np.abs( player)*2 ).squeeze()
            # sample column in the case there is more than 2
            idy = int([np.random.choice(row_idy) if row_idy.shape != () else row_idy][0])
            # get the row axis
            idx = np.argwhere(self.board[:,idy] == 0)[0][0]
            s=0
            for i in range(2):
                s+=self.board[i][idy]
            if s!=player*2:
                a,b=idx, idy
            else:
                return idx, idy

        # checking on rows
        if np.abs(player)*2 in np.abs(np.sum(self.board, axis=1)):
            # get row(s) with 2
            row_idx = np.argwhere(np.abs(np.sum(self.board, axis=1)) == np.abs(player)*2).squeeze()
            # sample row in the case there is more than 2
            idx = int([np.random.choice(row_idx) if row_idx.shape != () else row_idx][0])
            # add the final piece for winning move
            idy = np.argwhere(self.board[idx,:] == 0)[0][0]
            s=0
            for i in range(2):
                s+=self.board[idx][i]
            if s!=player*2:
                a,b=idx, idy
            else:    
                return idx, idy

        # checking on diagonal1
        if np.abs(player)*2 == np.abs(np.trace(self.board)):
            
            # get diagonal(s) with 2
            if self.board[0][0] == 0:
                idx, idy = 0, 0
            elif self.board[2][2]==0:
                idx, idy = 2, 2
            else:
                idx, idy=1,1
            if np.trace(self.board)!=player*2:
                a,b=idx,idy
            else:
                return idx, idy

        # checking on diagonal2
        if np.abs(player)*2 == np.abs(np.trace(np.rot90(self.board))):
            # get diagonal(s) with 2
            if self.board[0][2] == 0:
                idx, idy = 0, 2
            elif self.board[1][1]==0:
                idx,idy=1,1
            else:
                idx, idy = 2, 0
            if player*2!= np.trace(np.rot90(self.board)):
                a,b=idx, idy
            else:
                return idx, idy
        
        if a<2 and b<2:
            return a,b

        idx, idy = self.free_space()
        return idx, idy
    
            
    def take_turn(self, strategy, computer):
        if strategy == 'random':               
            return self.free_space()
        elif strategy == 'smart1':             
            return self.strategy1(computer)
        elif strategy == 'smart2':             
            return self.strategy2(computer)
        else:
            print ('No strategy chosen defaulting to random')
            return self.free_space()

    def startgame(self, strategyIndexX, strategyIndexO):  # Call other functions in here to run the game.
        self.__init__() # added this so you can continually initiate game

        self.setBoard()
        print(self.board)

        count = 0
        player =  self.firstTurn() # randomly get first player
        while True:
            print (self.players[player], "turn")
            strategy = strategyIndexX if player == 1 else strategyIndexO
            i, j = self.take_turn(strategy, player)
            self.placement(i, j, player)
            count += 1
            self.showBoard()

            # You can add this check only if number of turns is greater than 5 here (add a counter)
            # Check if the current player wins
            if count > 4:
                if self.winner(player):
                    print("Player", self.players[player], "wins the game!")
                    return self.players[player]
                    break
            
            # Board full
            if count == 9:
                print("Draw match!")
                break

            # Change players
            player = self.swap_player_turn(player)

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
    computer=t.startgame('smart2','smart1') # first position fives strategy of X, second position gives strategy of O
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
plt.title('X-smart strategy, O- random strategy')
plt.legend()
