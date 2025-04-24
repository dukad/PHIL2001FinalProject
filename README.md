# Final Project for PHIL2001 Spring 2025 by Kaden Du

## Overview

This project was made to simulate networked behavior of those participating in games when they are given the option to both choose their strategy and which parter they play the game with. Both the strategy and partner are chosen with the "probe-and-adjust" rule. The rule goes as follows: at a small probability, each player will try something new, i.e. change their partner or their strategy. If it is better than the result they got previously, then they will continue to do that.

## Run instructions (tested on Windows)

1. Use 'cd' to navigate to the project directory
2. Enter the virtual environement using <pre> .\\.venv\Scripts\activate </pre>
3. Run program using  <pre> python main.py</pre>
4. Open <href> http://127.0.0.1:8050 </href> in a browser

## TLDR Recommendations for easy, good results
* Use player count less than 200
* Use connections less than 10
* 

## Control Parameters
* Number of Players 
    * Number of nodes/players to be generated in the network, updates when 'Generate' is clicked.
* Starting Number of Connections 
    * Number of other players each player originally plays against. This will be changed as players probe and adjust. Updates on 'Generate'.
* Number of Strategies
    * From 1 to 5, updates the payoff matrix and percentages automatically.
* Payoff Matrix (S1 S2 ...)
    * Traditional Payoff Matrix for a symmetrical game. The payoff is given to 'P1' or the player whose strategy is on the left hand side.
* Strategy Percentages
    * The percent of each strategy to include on 'Generate'.
* Run for (generations)
    * When 'Run' is clicked, this many genrations will occur before stopping
* Probe and Adjust Rate
    * Chance (out of 1) that any given player will probe and adjust
* Strategy/Connection Ratio
    * When a player does probe and adjust, what is the chance (out of 1) that the player changes their strategy. 1 means they will only change strategy, and 0 means that they will only change connections.

## A Note on complex simulations

If the number of players and connections are too high, then the run for (generations) may not work properly. This is because the latency on each generation is too high, and the scheduling and rendering cannot keep up. To fix this, simply increase the INTERVAL variable on line 1 of main.py. This will slow down all other simulations, my apologies for not providing a more robust solution to this.

## How it works

On each generation, each player will randomly decide (based on input percent) what type of action it will take. It will either porbe and adjust strategy, connections, or play as normal. When playing as normal, the player will maintain memory of its past payoffs against each of its connections, and it will use these when it does get the chance to probe and adjust. When probing strategy, the player will simply play a round as normal, but using a randomly generated new strategy. If it got more total payoff points than the previous round, then it will keep its strategy. When probing for connections, a player will look into its memory to find its connection which has been givin the worst payoffs, and disconnect from them. The player will connect randomly to a new player. If the new player treats them better (higher payoff), this connection will maintain, and if not, then the player will revert to the original connection. One note about this implementation is that since players are dependant on having  a connection to remove, if a player loses all connections and is isolated, it makes it very difficult for them to re-enter the group, since another player must randomly choose them and gain a good payoff from the experience.
