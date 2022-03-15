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

    def get_action(self):

        # GET RABDIN ACTION ACCORDING TO MIXED-STRATEGY DISTRIBUTION

        # Basically, we are using the alternative board coordinate system from
        # our get_avaiable_actions method. We create an array from 0 to 8
        # corresponding to these coordinates. We then use random.choice with
        # strategy as our probability distribution to randomly pick a move.

        # The research paper describes an alternative method for how you can
        # choose a random action according to a strategy, but I think my
        # implementation keeps it a lot simpler (the guy in the video also
        # thinks the research paper method is a bit iffy too).

        actions = np.arange(9)
        strategy = self.get_strategy()
        a = np.random.choice(actions, p=strategy)

        # Converting our coordinates back to our original coordinate system.

        coordinate = (a//3, a % 3)
        return coordinate


def get_available_actions(self):

    # So if you look at video, he doesn't have to worry about this since
    # for rock-paper-scissors the number of available actions at any stage
    # is always 3, but for us it will change so I added this function to check.

    available_actions = []
    # Just iterating over the board to find any available actions.
    for i in range(3):
        for j in range(3):
            # Checking if the space is empty.
            if self.board[i][j] == "-":
                # Adding the coordinate where the avaiable move is.

                # The 3*i + j converts the coordinate system of the board to be
                # 1D, i.e. from

                # 00, 01, 02
                # 10, 11, 12
                # 20, 21, 22

                # to

                # 0, 1, 2
                # 3, 4, 5
                # 6, 7, 8

                # This is to allow for indexing in the get_strategy function.

                available_actions.append(3*i + j)

    return available_actions
