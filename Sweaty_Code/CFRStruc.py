import numpy as np
from numpy import NaN

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










### CFR Function


#Node Dictionary:
Depth=0
AllNodes={}

## Inputs: Depth, Node-Child "Reach Probabilities", Our Grid

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
