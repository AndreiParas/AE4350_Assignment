from ConnectCode import ConnectCode
from mcts import MCTS
import pandas as pd

# This is for Agent (p1) versus Agent (p2) 

def play():
    aux = 0 # to arrange the excel output
    wins_p1 = 0 # count for number of wins made by Agent 1
    wins_p2 = 0 # count for number of wins made by Agent 1
    for x in range(1): # change to how many games you want to be played
        state = ConnectCode() # initial new gameboard
        mcts = MCTS(state) # initializes the agents
        moves_1 = []
        sims_1 = []
        times_1 = []
        moves_2 = []
        sims_2 = []
        times_2 = []
        while not state.game_over(): # runs a whole game
            print("Current state:")
            state.print()
            print("Thinking...")
            mcts.search(1) # the time(seconds) allocated to agent 1 to make its move
            num_rollouts, run_time = mcts.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = mcts.best_move() # selects the best move
            print("MCTS(1) chose move: ", move)
            moves_1.append(move)
            sims_1.append(num_rollouts)
            times_1.append(run_time)
            state.move(move)
            mcts.move(move)
            state.print()
            if state.game_over():
                print("MCTS(1) won!")
                wins_p1 = wins_p1 + 1
                break
            print("Thinking...")
            mcts.search(1) # the time(seconds) allocated to agent 2 to make its move
            num_rollouts, run_time = mcts.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = mcts.best_move() # selects the best move
            print("MCTS(2) chose move: ", move)
            moves_2.append(move)
            sims_2.append(num_rollouts)
            times_2.append(run_time)
            state.move(move)
            mcts.move(move)
            if state.game_over():
                print("MCTS(2) won!")
                wins_p2 = wins_p2 + 1
                break
        # Output to excel
        df_moves_1 = pd.DataFrame(moves_1)
        df_moves_2 = pd.DataFrame(moves_2)
        df_sims_1 = pd.DataFrame(sims_1)
        df_sims_2 = pd.DataFrame(sims_2)
        df_times_1 = pd.DataFrame(times_1)
        df_times_2 = pd.DataFrame(times_2)
        with pd.ExcelWriter('output.xlsx', if_sheet_exists= 'overlay', mode='a') as writer:
            df_moves_1.to_excel(writer, index=False, header=False, startcol=aux)
            df_sims_1.to_excel(writer, index=False, header=False, startcol=aux+1)
            df_times_1.to_excel(writer, index=False, header=False, startcol=aux+2)
            df_moves_2.to_excel(writer, index=False, header=False, startcol=aux+3)
            df_sims_2.to_excel(writer, index=False, header=False, startcol=aux+4)
            df_times_2.to_excel(writer, index=False, header=False, startcol=aux+5)
        aux = aux + 7
        print('Player 1 has won', wins_p1, 'times')
        print('Player 2 has won', wins_p2, 'times')
        print('Games done:', x+1)
if __name__ == "__main__":
    play()