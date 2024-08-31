import random
import time
import math
from copy import deepcopy
from ConnectCode import ConnectCode
from meta import GameMeta, MCTSMeta

# MCTS Algorithm

class Node: # this is the 'node' class
    def __init__(self, move, parent): # initial state
        self.move = move # the move that lead to this state
        self.parent = parent # parent node
        self.N = 0 # number of times the node was visited (initially 0)
        self.Q = 0 # number of won simulations that resulted from this node
        self.children = {} # represents possible moves to be made next (children nodes)
        self.outcome = GameMeta.PLAYERS['none'] # the game outcome for this node
    def add_children(self, children: dict) -> None: # function to add all children
        for child in children:
            self.children[child.move] = child
    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0: # this prioritizes unexplored nodes
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * math.sqrt(math.log(self.parent.N) / self.N) # value based on UCT

class MCTS: # this is the main 'Monte Carlo Tree Search' class
    def __init__(self, state=ConnectCode()): # initialization function
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
    def select_node(self) -> tuple: # node selection function
        node = self.root # starts from the root node (which is the last move played)
        state = deepcopy(self.root_state) # takes the state of the board
        while len(node.children) != 0: # selects the node with the highest value (based on UCT)
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value() 
            max_nodes = [n for n in children if n.value() == max_value]
            node = random.choice(max_nodes)
            state.move(node.move)
            if node.N == 0: # forces exploration of an unexplored node
                return node, state
        if self.expand(node, state): # expand the children if possible and choose a randome children
            node = random.choice(list(node.children.values()))
            state.move(node.move)
        return node, state
    def expand(self, parent: Node, state: ConnectCode) -> bool: # node expansion function
        if state.game_over():
            return False
        children = [Node(move, parent) for move in state.get_legal_moves()]
        parent.add_children(children) # just adding the children
        return True
    def roll_out(self, state: ConnectCode) -> int: # roll-out or simulation function
        while not state.game_over(): # random moves until game is over
            state.move(random.choice(state.get_legal_moves()))
        return state.get_outcome()
    def back_propagate(self, node: Node, turn: int, outcome: int) -> None: # backpropagation function
        # For the current player, not the next player
        reward = 0 if outcome == turn else 1 # +1 reward if the game ends on the agents turn
        while node is not None: # updates the tree
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward
    def search(self, time_limit: int): # combination of all 4 phases (selection, expansion, roll-out/simulation, and backpropagation) function
        start_time = time.process_time()
        num_rollouts = 0
        while time.process_time() - start_time < time_limit: # repeats the 4 MCTS steps in the time allocated
            node, state = self.select_node() # selects the node and expands it
            outcome = self.roll_out(state) # gets the outcome of the random simulation
            self.back_propagate(node, state.to_play, outcome) # updates all the parents
            num_rollouts += 1 # 
        run_time = time.process_time() - start_time
        self.run_time = run_time # the run time of the MCTS (saved for statistics)
        self.num_rollouts = num_rollouts # the number of MCTS simulated games (saved for statistics)
    def best_move(self): # best move selection function
        if self.root_state.game_over():
            return -1
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes) # makes the move that takes us to the state with the highest 'N' (most visited state)
        return best_child.move
    def move(self, move): # the function that moves the state of the tree to the new based on the move made by the player
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return
        self.root_state.move(move)
        self.root = Node(None, None)
    def statistics(self) -> tuple: # statistics function
        return self.num_rollouts, self.run_time