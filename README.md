# Assignment 4: Gomoku with Monte Carlo Tree Search

Your task is to implement MCTS for playing Gomoku. The base game engine is from [here](https://github.com/HackerSir/PygameTutorials/tree/master/Lesson04/Gomoku). 

Again, DO NOT publicly fork this repositiory. 

## Due date
Dec-6 11:59pm. Submissions by Nov-29 11:59 pm will receive 3 extra points, assuming that it is close to being fully correct in the first place (12 points or more normal points). A detailed pseudocode document will be released on Nov-30 which should make the implementation much easier, so submissions after that will not receive extra credits. 

As usual, only submit the `ai.py` file on Gradescope. 

## The Game
Gomoku is a popular game played on the Go board, following much simpler rules. 

- There are two players, one placing black pieces and the other white pieces, at the grid intersections of the board. 
- The two players take turns to place one piece each time. Pieces are never moved or removed from the board. 
- The players' goal is to have five pieces of their own color to form an unbroken line horizontally (`examples/ex1.png`), vertically (`examples/ex2.png`), or diagonally (`examples/ex3.png`). Of course, these are unlikely realistic games between reasonable players. A real game is more like `examples/ex4.png` (black is still very lame at the end).  
- The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

Here's a youtube video of a competitive Gomoku game (in case you're interested, or want to procrastinate): https://www.youtube.com/watch?v=siYgHaEwmZU&ab_channel=SandraJones

## Tasks
Implement MCTS in `ai.py`. Read the comments carefully.

Note that the starter code makes it clear that your MCTS should return more than just one action in the end, but also the table of winning rates for all actions for the root node (number of wins divided by total number of samples, i.e., the X-bar term in the best child formula). The tests compare these values that you compute with the correct ones for a few predefined states. 

In MCTS, the search exits when the "computation budget" is reached (Line 23 in `ai.py`). The current default value is 1000, which will be used for testing. You can increase or decrease it to see the different behaviors of AI. For instance, with a budget over 6000, a correctly implemented MCTS AI should be able to play a fairly interesting game against you (although it may still make some obvious mistakes when the number of next actions to consider gets larger). Check the MCTS-1000.mov and MCTS-6000.mov files in the repo for MCTS with 1000 and 6000 budgets respectively.

It is easy to see that good moves should be pretty close to the pieces already on the board. Thus, to accelerate search, we have limited the search to a small "active" area around existing pieces (this area uses black lines on the board, compared to grey lines in the inactive area). 

## Usage
To run the program, do:
```
python main.py
```

To run tests for the winning rate table in several predefined states, do:
```
python main.py -t 1
```

To run AI against random policy, do:
```
python main.py -t 2
```

The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

More details can be found in `Tests` section below.

## Tests
- `python main.py -t 1` runs tests for the winning rate table in several predefined states. Note that a budget of 1000 runs and parameter c=1 in the `best_child` function is used in the test cases. Note that the order in the table is important; make sure to follow the instructions in the `ai.py` starter code. 
- `python main.py -t 2` runs your AI against a random policy. Your AI should always win (you can try smaller budgets too). 

## Tips/FAQ
- Make sure to start early. This PA requires more work than previous assignments. 
- Check this [survey article](http://www.incompleteideas.net/609%20dropbox/other%20readings%20and%20resources/MCTS-survey.pdf) for more info on MCTS. 
- If you aren't already, check out `pdb` to help you debug!