
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

        Scores=CurrentNode.strategy

        Options=self.ListMoves()

        AllowedScores=[]


        for i in Options:

            AllowedScores.append(Scores[i[0],i[1]])
        
        
        Biggest=np.argmax(AllowedScores)
        TheOne=Options[Biggest]
        
        
        return TheOne[0],TheOne[1]



##########################################################################################
    
            
    def take_turn(self, strategy, computer, KnownArrangements=0):
        if strategy == 'random':               
            return self.free_space()
        elif strategy == 'smart1':             
            return self.strategy1(computer)
        elif strategy == 'smart2':             
            return self.strategy2(computer)
        elif strategy == 'CFR':
            return self.CFR_Strat(KnownArrangements,computer)
        else:
            print ('No strategy chosen defaulting to random')
            return self.free_space()

    def startgame(self, strategyP1, strategyP2, KnownArrangements=0,Show=True,Winner=True):  # Call other functions in here to run the game.
        self.__init__() # added this so you can continually initiate game

        Plyr1=np.random.choice([-1, 1])
        Plyr2=Plyr1*-1
        
        player=1
        
        count = 0
        # randomly get first player


        while True:

            
            strategy = strategyP1 if player == Plyr1 else strategyP2


            i, j = self.take_turn(strategy, player,KnownArrangements)



            self.placement(i, j, player)
            count += 1

            if Show is True:
                print (self.players[player], "turn")
                self.showBoard()
                print("")
                time.sleep(0.5)

            # You can add this check only if number of turns is greater than 5 here (add a counter)
            # Check if the current player wins
            if count > 4:
                if self.winner(player):
                    if Winner is True:
                        print("Player", self.players[player], " ", strategy ,"wins the game!")
                    return strategy
                    break
            
            # Board full
            if count == 9:
                if Winner is True:
                    print("Draw match!")
                break

            # Change players
            player = self.swap_player_turn(player)
        if Show is True:   
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
                self.strategy[arow][acol] /= normalisingSum
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

    else:
        TurnNum=-1
        TurnPiece="O"
        RelevantProb=Plyr2Prob

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


        #print(ChildVals)

        #print(ChildProb)

        #print("")

        #time.sleep(2)




    # Recursion Time :) - Go another node deeper by recalling the same function. (this will continue until we find a winner down this node route and we can extract a value for this child val (reach probability adjusted summation of grandchildren.))
    # This will be negative version  of current "regret frame" - as moves which are good for X are bad for Y

        if TurnNum==1:
            ChildVals[irow][icol] = -CounterFactualisedRegret(DeeperGrid,  Depth2, Plyr1Prob*ChildProb[irow][icol], Plyr2Prob)
        else: 
            ChildVals[irow][icol] = -CounterFactualisedRegret(DeeperGrid,  Depth2, Plyr1Prob, Plyr2Prob*ChildProb[irow][icol])



        NodeVal = NodeVal + ChildVals[irow][icol] * ChildProb[irow][icol]

        #print(NodeVal)

    # Find Child Regret (=Vi*RPi-Sum(Vj*RPj)) After iteration above:
    for i in Responses:


            irow=i[0]
            icol=i[1]
            Regret = ChildVals[irow][icol] -NodeVal
            # Probability of action occuring is prob of previous move:

            NODE.regretSum[irow][icol] += RelevantProb*Regret





    # Redefine node's own value (regret) by resumming children: Sum(Vj*RPj)

    # Spit out Node's Value (utility)

    return NodeVal






























def train(iterations,Data=True):


    Game=tictactoe()

    util = 0

    for i in range(0,iterations):
        j=i+1

        
        util += CounterFactualisedRegret(Game, 0, 1, 1)


        if round(j-1)==0:
            KnownArrangements1=copy.deepcopy(KnownArrangements)

        if round(j-10)==0:
            KnownArrangements10=copy.deepcopy(KnownArrangements)

        if round(j-20)==0:
            KnownArrangements20=copy.deepcopy(KnownArrangements)


        if round(j-30)==0:
            KnownArrangements30=copy.deepcopy(KnownArrangements)

        if round(j-40)==0:
            KnownArrangements40=copy.deepcopy(KnownArrangements)

        if round(j-50)==0:
            KnownArrangements50=copy.deepcopy(KnownArrangements)


        if round(j-60)==0:
            KnownArrangements60=copy.deepcopy(KnownArrangements)


        if round(j-70)==0:
            KnownArrangements70=copy.deepcopy(KnownArrangements)


        if round(j-80)==0:
            KnownArrangements80=copy.deepcopy(KnownArrangements)


        if round(j-90)==0:
            KnownArrangements90=copy.deepcopy(KnownArrangements)


        if round(j-100)==0:
            KnownArrangements100=copy.deepcopy(KnownArrangements)

    

                

        print(i, "iter completed")

    return [KnownArrangements1, KnownArrangements10, KnownArrangements20, KnownArrangements30 ,KnownArrangements40, KnownArrangements50, KnownArrangements60, KnownArrangements70, KnownArrangements80, KnownArrangements90, KnownArrangements100]


####################################################################################################################################################################################

# %%


print("Start Time =", datetime.now().strftime("%H:%M:%S"))
a1,a10,a20,a30,a40,a50,a60,a70,a80,a90,a100=train(100)
print("End Time =", datetime.now().strftime("%H:%M:%S"))

#%%

####################################################################################################################################################################################

Game=tictactoe()
Game.startgame("CFR","random",KnownArrangements,Show=True)


# %%

Strategy1="CFR"
Strategy2="random"


N = 10000
a=np.zeros(N)
b=np.zeros(N)
winsStrat1=0
winsStrat2=0

Game=tictactoe()
for i in range(1,N):
    computer=Game.startgame(Strategy1,Strategy2,KnownArrangements,Show=False,Winner=False) # first position gives strategy of X, second position gives strategy of O
    if computer:
        if computer==Strategy1:
            winsStrat1+=1
        else:
            winsStrat2+=1
    a[i]=winsStrat1
    b[i]=winsStrat2

from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
    
plt.plot(range(N), a, label=Strategy1+ " wins")
plt.plot(range(N), b, label=Strategy2+ " wins")
plt.ylabel('Number of wins')
plt.xlabel('Number of games played')
plt.title(Strategy1 + ' strategy vs ' + Strategy2 + ' strategy')
plt.legend()
plt.show()

# %%
z=0
x=0
for i in range(1, len(a)):
    if a[i]==a[i-1]:
        z+=1
    if b[i]==b[i-1]:
        x+=1

print("Win Rate ", 1-z/N)
print("Not Loss Rate ", x/N)



#%%



Game=tictactoe()
Game.placement(2,2,1)
#Game.showBoard()
Game.placement(1,1,-1)
#Game.showBoard()
Game.placement(0,1,1)
#Game.showBoard()
Game.placement(1,2,-1)
Game.showBoard()

Game.placement(Game.CFR_Strat(KnownArrangements,1)[0],Game.CFR_Strat(KnownArrangements,1)[1],1)
#Game.showBoard()






# %%


print(KnownArrangements["Turn: " + "X" + " Arrangement: " + "---------"].strategy)
Game=tictactoe()
print((Game.CFR_Strat(KnownArrangements,1)[0],Game.CFR_Strat(KnownArrangements,1)[1],1))

#print(a50["Turn: " + "O" + " Arrangement: " + "XOX------"].strategy-a10["Turn: " + "O" + " Arrangement: " + "XOX------"].strategy)
# %%

Game=tictactoe()
Game.startgame("CFR","random",KnownArrangements)
# %%

Xarr=[1,10,20,30,40,50,60,70,80,90,100]
WinArr=[]
DrawOrWinArr=[]


for NodeList in [a1,a10,a20,a30,a40,a50,a60,a70,a80,a90,a100]:
    Strategy1="CFR"
    Strategy2="random"


    N = 10000
    a=np.zeros(N)
    b=np.zeros(N)
    winsStrat1=0
    winsStrat2=0

    Game=tictactoe()
    for i in range(1,N):
        computer=Game.startgame(Strategy1,Strategy2,NodeList,Show=False,Winner=False) # first position gives strategy of X, second position gives strategy of O
        if computer:
            if computer==Strategy1:
                winsStrat1+=1
            else:
                winsStrat2+=1
        a[i]=winsStrat1
        b[i]=winsStrat2

    WinArr.append(max(a)/N)
    DrawOrWinArr.append(1-max(b)/N)


""" 
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
        
    plt.plot(range(N), a, label=Strategy1+ " wins")
    plt.plot(range(N), b, label=Strategy2+ " wins")
    plt.ylabel('Number of wins')
    plt.xlabel('Number of games played')
    plt.title(Strategy1 + ' strategy vs ' + Strategy2 + ' strategy')
    plt.legend()
    plt.show()
 """
    

from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False

#%%

plt.figure(dpi=2000)
plt.plot(Xarr,WinArr,"-x",label='Win Percentage')
plt.plot(Xarr,DrawOrWinArr,"-x",label='Draw or Win Percentage')

plt.xlabel("Number of CFR Iterations")
plt.ylabel("Percent of Total Games Played")
plt.title(Strategy1 + ' strategy vs ' + Strategy2 + ' strategy',fontsize=20)
plt.legend()
plt.show()




# %%
print(a1["Turn: " + "X" + " Arrangement: " + "XOXO-----"].strategy)
print(a10["Turn: " + "X" + " Arrangement: " + "XOXO-----"].strategy)
# %%

plt.figure(dpi=2000)

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

x=a100["Turn: " + "X" + " Arrangement: " + "---------"].strategy

ax = sns.heatmap(x,vmin=0, linewidth=0.5,cmap="seismic",annot=True)
#ax.color_palette("coolwarm", as_cmap=seismic)
plt.title("Utility of Starting Points in Tic Tac Toe",fontsize=20)
plt.show()
# %%



Strategy1="CFR"
Strategy2="random"


N = 10000
a=np.zeros(N)
RandomPerformance=np.zeros(N)
winsStrat1=0
winsStrat2=0

Game=tictactoe()
for i in range(1,N):
    computer=Game.startgame(Strategy1,Strategy2,KnownArrangements,Show=False,Winner=False) # first position gives strategy of X, second position gives strategy of O
    if computer:
        if computer==Strategy1:
            winsStrat1+=1
        else:
            winsStrat2+=1
    a[i]=winsStrat1
    RandomPerformance[i]=winsStrat2

#%%


Strategy1="CFR"
Strategy2="smart1"


N = 10000
a=np.zeros(N)
Smart1=np.zeros(N)
winsStrat1=0
winsStrat2=0

Game=tictactoe()
for i in range(1,N):
    computer=Game.startgame(Strategy1,Strategy2,KnownArrangements,Show=False,Winner=False) # first position gives strategy of X, second position gives strategy of O
    if computer:
        if computer==Strategy1:
            winsStrat1+=1
        else:
            winsStrat2+=1
    a[i]=winsStrat1
    Smart1[i]=winsStrat2
#%%



Strategy1="CFR"
Strategy2="CFR"


N = 10000
a=np.zeros(N)
CFR=np.zeros(N)
winsStrat1=0
winsStrat2=0

Game=tictactoe()
for i in range(1,N):
    computer=Game.startgame(Strategy1,Strategy2,KnownArrangements,Show=False,Winner=False) # first position gives strategy of X, second position gives strategy of O
    if computer:
        if computer==Strategy1:
            winsStrat1+=1
        else:
            winsStrat2+=1
    a[i]=winsStrat1
    CFR[i]=winsStrat2

# %%
plt.figure(dpi=2000)
plt.plot(np.linspace(0,9999,10000),RandomPerformance,label="Smart Non-Learning Strategy")
plt.plot(np.linspace(0,9999,10000),Smart1,label="Random Strategy")
plt.plot(np.linspace(0,9999,10000),CFR, label="CFR Strategy")
plt.legend()
plt.xlabel("Number of Games")
plt.ylabel("Number of Wins Against CFR")
plt.title("All Strategies vs CFR Strategy", fontsize=20)
plt.show()
# %%


print(max(a)/N)
print(1-max(Smart1)/N)

# %%
