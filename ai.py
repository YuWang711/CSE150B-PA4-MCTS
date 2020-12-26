from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

class Node:
    # NOTE: modifying this block is not recommended
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0 #number of wins at the node
        self.num_visits = 0 #number of visits of the node
        self.parent = parent #parent node of the current node
        self.children = [] #store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(actions) #store actions that have not been tried

        simulator = Game(*state)
        self.is_terminal = simulator.game_over

# NOTE: deterministic_test() requires BUDGET = 1000
#   You can try higher or lower values to see how the AI's strength changes
BUDGET = 1000

class AI:
    # NOTE: modifying this block is not recommended
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state) #using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):
        #TODO: Main MCTS loop

        iters = 0
        action_win_rates = {} #store the table of actions and their ucb values

        # TODO: Delete this block ->
        # self.simulator.reset(*self.root.state)
        # for action in self.simulator.get_actions():
        #     action_win_rates[action] = 0
        # return random.choice(self.simulator.get_actions()), action_win_rates
        # <- Delete this block

        # TODO: Implement the MCTS Loop
        while(iters < BUDGET):
            if ((iters + 1) % 100 == 0):
                # NOTE: if your terminal driver doesn't support carriage returns you can use: 
                # print("{}/{}".format(iters + 1, BUDGET))
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")
            
            # TODO: select a node, rollout, and backpropagate
            self.simulator.reset(*self.root.state)
            new_node = self.select(self.root)
            winner = self.rollout(new_node)
            self.backpropagate(new_node,winner)
            iters += 1
        print()
        # for child in self.root.children:
        #     print(child[1].num_wins)
        # Note: Return the best action, and the table of actions and their win values 
        #   For that we simply need to use best_child and set c=0 as return values
        # for child in self.root.children:
        #     print(child[1].num_wins, "/", child[1].num_visits)

        _, action, action_win_rates = self.best_child(self.root, 0)
        return action, action_win_rates

    def select(self, node):
        # TODO: select a child node
        while not node.is_terminal:
            if len(node.untried_actions) > 0: 
                return self.expand(node)
            else:
                node,_,_ = self.best_child(node)
        # HINT: you can use 'is_terminal' field in class Node to check if node is terminal node
        # NOTE: deterministic_test() requires using c=1 for best_child()
        return node

    def expand(self, node):
        # TODO: add a new child node from an untried action and return this new node

        child_node = None #choose a child node to grow the search tree

        # NOTE: deterministic_test() requires popping an action like this
        action = node.untried_actions.pop(0)

        # NOTE: Make sure to add the new node to the node.children
        # NOTE: You may find the following methods useful:
        #   self.simulator.state()
        #   self.simulator.get_actions()
        self.simulator.reset(*node.state)
        self.simulator.place(action[0],action[1])
        child_node = Node(self.simulator.state(), self.simulator.get_actions(), parent=node)
        node.children.append((action, child_node))
        return child_node

    def best_child(self, node, c=1): 
        # TODO: determine the best child and action by applying the UCB formula

        best_child_node = None # to store the child node with best UCB
        best_action = None # to store the action that leads to the best child
        action_ucb_table = {} # to store the UCB values of each child node (for testing)

        # NOTE: deterministic_test() requires iterating in this order
        # NOTE: deterministic_test() requires, in the case of a tie, choosing the FIRST action with 
        # the maximum upper confidence bound
        best_ucb = 0
        N_s = node.num_visits
        for child in node.children:

            N_s_prime = child[1].num_visits
            Q_s_prime = child[1].num_wins
            action_ucb_table[child[0]] = (Q_s_prime/N_s_prime) +  (c * (sqrt( ( 2*log(N_s) )/N_s_prime)))
            if best_ucb < action_ucb_table[child[0]]:
                best_child_node = child[1]
                best_action = child[0]
                best_ucb = action_ucb_table[child[0]]

        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):
        
        while (node is not None):
            # TODO: backpropagate the information about winner
            # IMPORTANT: each node should store the number of wins for the player of its **parent** node
            node.num_visits += 1
            if node.parent != None:
                node.num_wins += result[node.parent.state[0]]
            node = node.parent


    def rollout(self, node):
        # TODO: rollout (called DefaultPolicy in the slides)

        # HINT: you may find the following methods useful:
        #   self.simulator.reset(*node.state)
        #   self.simulator.game_over
        #   self.simulator.rand_move()
        #   self.simulator.place(r, c)
        # NOTE: deterministic_test() requires that you select a random move using self.simulator.rand_move()
        self.simulator.reset(*node.state)
        while self.simulator.game_over == False:
            r, c = self.simulator.rand_move()
            self.simulator.place(r,c)



        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        return reward
    