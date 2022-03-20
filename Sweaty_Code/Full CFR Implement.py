
#%%
import pandas as pd  # noqa F401   
import numpy as np  # noqa F401
import string  # noqa F401
import random  # noqa F401
import copy
from datetime import datetime
import time

class tictactoe:  # Main Class
    def __init__(self):  # Initialises new array for board
        self.board = []
        self.players = {-1:'O', 1:'X'}
        self.board = np.tile(0, (3,3))

    def firstTurn(self):  # First is always X
        first = 1
        return first

    def WhoseTurn(self):
        Num=0
        for i in range (0, 3):
            for j in range (0,3):
                if self.board[i][j]!=0:
                    Num+=1
        if Num%2 == 0:
            return 1
        else:
            return -1
                
    def ListMoves(self):
        MoveList=[]
        for i in range (0, 3):
            for j in range (0,3):
                if self.board[i][j]==0:
                    MoveList.append([i,j])
        return MoveList


    def GetComputerBoard(self):
        return self.board

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


    def BoardForCFR(self):
        StrArrangement=""
        for i in range (0,3):
            for j in range(0,3):
                if self.board[i,j]==1:
                    StrArrangement += "X"
                elif self.board[i,j]==-1:
                    StrArrangement += "O"
                elif self.board[i,j]==0:
                    StrArrangement += "-"
        return StrArrangement

    
                


##########################################################################################

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
        if player*2 in np.sum(self.board, axis=0):
            # get column(s) with 2 
            row_idy = np.argwhere(np.sum(self.board, axis=0) == player*2 ).squeeze()
            # sample column in the case there is more than 2
            idy = int([np.random.choice(row_idy) if row_idy.shape != () else row_idy][0])
            # get the row axis
            idx = np.argwhere(self.board[:,idy] == 0)[0][0]
            return idx, idy

        # checking on rows
        if player*2 in np.sum(self.board, axis=1):
            # get row(s) with 2
            row_idx = np.argwhere(np.sum(self.board, axis=1) == player*2).squeeze()
            # sample row in the case there is more than 2
            idx = int([np.random.choice(row_idx) if row_idx.shape != () else row_idx][0])
            # add the final piece for winning move
            idy = np.argwhere(self.board[idx,:] == 0)[0][0]
            return idx, idy

        # checking on diagonal1
        if player*2 == np.trace(self.board):
            # get diagonal(s) with 2
            if self.board[0][0] == 0:
                idx, idy = 0, 0
            else:
                idx, idy = 2, 2
            return idx, idy

        # checking on diagonal2
        if player*2 == np.trace(np.rot90(self.board)):
            # get diagonal(s) with 2
            if self.board[0][2] == 0:
                idx, idy = 0, 2
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

    def CFR_Strat(self,KnownArrangements,player):
        if player==1:
            Piece="X"
        else:
            Piece="O"

        Arrangement = "Turn: " + Piece + " Arrangement: " +Game.BoardForCFR()

        CurrentNode=KnownArrangements[Arrangement]
        row=CurrentNode.strategy.argmax()[0]
        col=CurrentNode.strategy.argmax()[0]
        return row, col




##########################################################################################
    
            
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


####################################################################################################################################################################################
#%%



class Node:

    def __init__(self):
        self.NodeName=""
        self.regretSum = np.tile (np.float64(0), (3,3))
        self.strategy = np.tile(np.float64(0), (3,3))
        self.strategySum = np.tile(np.float64(0), (3,3))
    
    def SetNodeName(self,name):
        self.NodeName=name

    def get_strategy(self, ReachProb, Game):

        # GET CURRENT MIXED STRATEGY THROUGH REGRET-MATCHING

        # The code for this function is more or less identical to the one in
        # the Google doc but if you take a look at the page 5, section 2.4 in
        # the paper it is literally just adapting that code to Python.

        # Basically the paper, the Google doc and the guy in the video all
        # adopt the below code.

        available_actions = Game.ListMoves()
        normalisingSum = 0

        for a in available_actions:
            
            arow=a[0]
            acol=a[1]

            if self.regretSum[arow][acol] > 0:
                self.strategy[arow][acol] = self.regretSum[arow][acol]
            else: 
                self.strategy[arow][acol] = 0
            normalisingSum += self.strategy[arow][acol]



        for a in available_actions:
            arow=a[0]
            acol=a[1]

            if normalisingSum > 0:
                self.strategy /= normalisingSum
            else:
                self.strategy[arow][acol] = 1 / len(available_actions)
            self.strategySum[arow][acol] += self.strategy[arow][acol]*ReachProb

        return self.strategy





####################################################################################################################################################################################
#%%


## Inputs: Depth, Node-Child "Reach Probabilities", Our Grid


KnownArrangements={}


### CFR Function

def CounterFactualisedRegret(Game, Depth, Plyr1Prob, Plyr2Prob):

    # Depth: How many nodes deep are we? 0-9

    # Based off depth - Whose turn is it? X always starts.

    Remainder=(Depth%2)
    if Remainder==0:
        TurnNum=1
        TurnPiece="X"
        RelevantProb=Plyr1Prob
        Player1Coeff=1
        Player2Coeff=0
    else:
        TurnNum=-1
        TurnPiece="O"
        RelevantProb=Plyr2Prob
        Player1Coeff=0
        Player2Coeff=1
    # Is there a winner on the board?


    if Game.winner(TurnNum):
        return 1

    # Is the board full?

    if Game.is_board_filled is True:
        return 0


    # Define Node Name via Arrangement: Player : Board i.e. Turn: X Arrangement: -OX -XO ---
    
    NodeArrangement = "Turn: "

    NodeArrangement += TurnPiece
    
    NodeArrangement += " Arrangement: "

    CurrentArrangement = Game.BoardForCFR()

 

    NodeArrangement += CurrentArrangement


    # Question: Does this Node exist already? (Different paths can lead to same state!) Start w Node as Empty

    NODE= None
    
    NodeExists = NodeArrangement in KnownArrangements

    if NodeExists is True:
    # Answer 1: Yes - State Node from Map of Nodes

        NODE = KnownArrangements[NodeArrangement]

    # Answer 2: No - Lets make it exist! Create Node. -> Add the Node to the map!
    elif NodeExists is False:

        NODE=Node()
        NODE.SetNodeName(NodeArrangement)
        KnownArrangements[NodeArrangement] = NODE

    else: print("Broken")


    # Which Node-Child "Reach Probabilities" is relevant?


    # GET-PROBABILITIES FUNC - Find Current Node prob.
#
    ChildProb = NODE.get_strategy(RelevantProb,Game)

    # What are the response moves?
#
    Responses = Game.ListMoves()

    # State Values of Child Nodes to be 0 - There are as many children nodes as there are possible responses

    ChildVals=np.tile (np.float64(0), (3,3))

    # State Node Value to be 0 (until proven otherwise! Via summation of children values*reachprob.)

    NodeVal=0

    # For Each Action:

    for i in Responses:

        irow=i[0]
        icol=i[1]


        # Make a new (temporary) grid for further exploration of path.

        DeeperGrid = copy.deepcopy(Game)

    # Place a point on the grid (apply action)

        DeeperGrid.placement(irow,icol, TurnNum)

    # Premptively increasing depth by one!

        Depth2 = Depth + 1

    # Recursion Time :) - Go another node deeper by recalling the same function. (this will continue until we find a winner down this node route and we can extract a value for this child val (reach probability adjusted summation of grandchildren.))
    # This will be negative version  of current "regret frame" - as moves which are good for X are bad for Y

        ChildVals[irow][icol] = -CounterFactualisedRegret(DeeperGrid,  Depth2, Plyr1Prob + Player1Coeff*ChildProb[irow][icol], Plyr2Prob +Player2Coeff*ChildProb[irow][icol])
        NodeVal = NodeVal + ChildVals[irow][icol] * ChildProb[irow][icol]

    # Find Child Regret (=Vi*RPi-Sum(Vj*RPj)) After iteration above:
    for i in Responses:


            irow=i[0]
            icol=i[1]
            Regret = ChildVals[irow][icol]*ChildProb[irow][icol] -NodeVal
            # Probability of action occuring is prob of previous move:

            NODE.regretSum[irow][icol] += RelevantProb*Regret



    # Redefine node's own value (regret) by resumming children: Sum(Vj*RPj)

    # Spit out Node's Value (utility)

    return NodeVal



def train(iterations):

    Game=tictactoe()

    util = 0

    for i in range(0,iterations):
        util += CounterFactualisedRegret(Game, 0, 1, 1)

        print(i, "iter completed")


####################################################################################################################################################################################

# %%


print("Start Time =", datetime.now().strftime("%H:%M:%S"))
train(2)
print("End Time =", datetime.now().strftime("%H:%M:%S"))

#%%

####################################################################################################################################################################################


Game=tictactoe()

Game.showBoard()
Game.placement(0,0,1)
Game.showBoard()
Game.placement(1,0,-1)
Game.showBoard()
Game.placement(2,2,1)
Game.showBoard()
Game.placement(2,0,-1)
Game.showBoard()





#%%


Piece="X"
Arrangement = "Turn: " + Piece + " Arrangement: " +Game.BoardForCFR()
CurrentNode=KnownArrangements[Arrangement]
row=CurrentNode.strategy.argmax()
print(CurrentNode.strategy)
col=np.unravel_index(CurrentNode.strategy.argmax(), CurrentNode.strategy.shape)
print(col)
#Game.placement(KnownArrangements[Game.BoardForCFR].strategy.argmax()[0],KnownArrangements[Game.BoardForCFR].strategy.argmax()[1],-1)
#Game.showBoard()

# %%
#print(KnownArrangements[Game.BoardForCFR()])
print(Game.BoardForCFR())
#print(KnownArrangements)


# %%

# %%
