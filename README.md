# Group 3 Project

## Rianna: 
Created a tic tac toe board and add a piece using a random move (board.py).

## Ana: 
Completed the code for the game based on Rianna's work, added 3 strategy's (random, medium and smart) and created plots that show the efficiency of each strategy (in gameXO.py). Added another more efficient code with similar strategies, which is based on arrays (instead of strings) in the file plot_games.py.

## Dan:

Created the CFR function using pseudo code from Lanctot's paper: "An introduction to counterfactual regret" Cross matched this code with other attempts online in order to confirm validity of the algoritm. After creating CFR algorithm I connected it to the two other code sets. I started by connecting it to Hashir's Node Class. Having to rearrange the information storage to classes so it matched with Ana & Rianna's TTT board (a 3x3 Array) as well as adding a CFR strategy into the board. I then linked the TTT class to the CFR algorithm before debugging.
Finally after the algoirthm was fully functional I then performed some analysis using Ana's strategies. Plotting:
1) An analysis of win rate & win/draw rate with different number of iterations
2) A heatmap of starting move strategies
3) An analysis of win rate & win/draw rate of different strategies against CFR.
    -> Was unable to use smart 2 as it sometimes spits out a move that's already been made.

## Hashir:
Created a class used in the final code to obtain a strategy based on regret matching and then choosing an action based on the obtained strategy (since the strategy is a probability distribution).
