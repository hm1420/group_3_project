import numpy as np

# Begin by initialising a constant. I decided to create a constant NUM_ACTIONS
# like the Google doc since it should make the code easier to understand as
# it's read.

# DEFINITIONS

NUM_ACTIONS = 9

# Next we move on the get_strategy function. I more or less adapted the code
# in the video and also used the code in the Google doc to help, but regardless
# , both the video and Google doc very clearly adapted the pseudocode from
# the research paper.

# Unlike the rock-paper-scissors implementation in the video, the number of
# actions we have changes as the game goes on so I created a function to help
# determine these.


class Node:

    def __init__(self):
        self.regretSum = np.zeroes(NUM_ACTIONS)
        self.strategy = np.zeroes(NUM_ACTIONS)
        self.strategySum = np.zeroes(NUM_ACTIONS)

    def get_strategy(self):

        # GET CURRENT MIXED STRATEGY THROUGH REGRET-MATCHING

        # The code for this function is more or less identical to the one in
        # the Google doc but if you take a look at the page 5, section 2.4 in
        # the paper it is literally just adapting that code to Python.

        # Basically the paper, the Google doc and the guy in the video all
        # adopt the below code.

        available_actions = get_available_actions(self)
        normalisingSum = 0

        for a in available_actions:
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 \
                                                    else 0
            self.normalisingSum += self.strategy[a]

        for a in available_actions:
            if normalisingSum > 0:
                self.strategy /= normalisingSum
            else:
                self.strategy[a] = 1 / len(available_actions)
            self.strategySum[a] += self.strategy[a]

        return self.strategy

def CHECKWINNER(grid):
    return 0

# Check for Full Board Function: (poss fix if b)


def BOARDFULL(grid):
    if len(grid) == 9:
        return True
    else:
        return False

# Make Grid Layout printer!?


def GridArrangement(grid):
    print(grid)

### Node Structure

## Characteristics:

##Functions


# Yikes.

# Make check winner function!?




def GETPROB(Node, ReachProb, grid):
    ###WRITE THIS FUNC THEN IMPLEMENT NODE
    pass






#Node Dictionary:
Depth=0
AllNodes={}

## Inputs: Depth, Node-Child "Reach Probabilities", Our Grid




### CFR Function

def CounterFactualisedRegret(grid,Depth, Plyr1Prob, Plyr2Prob):

    # Depth: How many nodes deep are we? 0-9

    # Based off depth - Whose turn is it? X always starts.

    Remainder=Depth-2*Depth//2
    if Remainder==0:
        TurnNum=0
        TurnPiece="X"
        RelevantProb=Plyr1Prob
        Player1Coeff=1
        Player2Coeff=0
    else:
        TurnNum=1
        TurnPiece="O"
        RelevantProb=Plyr2Prob
        Player1Coeff=0
        Player2Coeff=1


    # Is the board full?

    if BOARDFULL(grid):
        return 0


    # Is there a winner on the board?

    if CHECKWINNER(grid):
        return 1


    # Define Node Name via Arrangement: Player : Board i.e. Turn: X Arrangement: -OX -XO ---
    
    NodeArrangement = "Turn:"

    NodeArrangement += TurnPiece
    
    NodeArrangement += " Arrangement: "

    CurrentArrangement = GridArrangement(grid)

    NodeArrangement += CurrentArrangement

    # Question: Does this Node exist already? (Different paths can lead to same state!) Start w Node as Empty

    Node= NaN
    Known= NaN
    
    if NodeArrangement in KnownArrangements is False:


    # Answer 1: No - Lets make it exist! Create Node. -> Add the Node to the map!

        Node=CREATENODE()
        KnownArrangements[NodeArrangement] = Node


    # Answer 2: Yes - State Node from Map of Nodes

    else:
        Known = True
        Node = KnownArrangements[NodeArrangement]

    # Which Node-Child "Reach Probabilities" is relevant?

    # GET-PROBABILITIES FUNC - Find Current Node prob.
#
    ChildProb = GETPROB(Node, RelevantProb)

    # What are the response moves?
#
    Responses = FindExmpties(grid)

    # State Values of Child Nodes to be 0 - There are as many children nodes as there are possible responses

    ChildVals=np.zeros(len(Responses))

    # State Node Value to be 0 (until proven otherwise! Via summation of children values*reachprob.)

    NodeVal=0

    # For Each Action:

    for i in Responses:

        # Make a new (temporary) grid for further exploration of path.

            DeeperGrid = GRIDCOPY(grid)

        # Place a point on the grid (apply action)

            DeeperGrid.add(TurnPiece,i)

        # Premptively increasing depth by one!

            Depth2 = Depth + 1

        # Recursion Time :) - Go another node deeper by recalling the same function. (this will continue until we find a winner down this node route and we can extract a value for this child val (reach probability adjusted summation of grandchildren.))
        # This will be negative version  of current "regret frame" - as moves which are good for X are bad for Y

            ChildVals[i] = -CounterFactualisedRegret(DeeperGrid,  Depth2, Plyr1Prob + Player1Coeff*ChildProb[i], Plyr2Prob +Player2Coeff*ChildProb[i])
            NodeVal = NodeValue + ChildVals[i] * ChildProb[i]

    # Find i th Child Regret (=Vi*RPi-Sum(Vj*RPj))

            Regret[i] = ChildVals[i]*ChildProb[i]-NodeVal

    # Redefine node's own value (regret) by resumming children: Sum(Vj*RPj)

    # Spit out
