from ConnectCode import ConnectCode
from mcts import MCTS

# This is for Human (p1) versus Agent (p2) 

def play():
    state = ConnectCode() # initial new gameboard
    mcts = MCTS(state) # initializes the agent
    while not state.game_over(): # runs a whole game
        print("Current state:")
        state.print()
        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))
        state.move(user_move) # changes the state of the gameboard
        mcts.move(user_move) # updates the MCTS tree based on the last move
        state.print()
        if state.game_over():
            print("Player one won!")
            break
        print("Thinking...")
        mcts.search(5) # the time(seconds) allocated to the agent to make its move
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move() # selects the best move
        print("MCTS chose move: ", move)
        state.move(move) # changes the state of the gameboard
        mcts.move(move) # updates the MCTS tree based on the last move
        if state.game_over():
            print("Player two won!")
            break
if __name__ == "__main__":
    play()