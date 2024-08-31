from copy import deepcopy
import numpy as np
from meta import GameMeta

# This is the Code for the Connect-4 Game

class ConnectCode:
    def __init__(self): # game initialization - first turn
        self.gameboard = [[0] * GameMeta.COLS for _ in range(GameMeta.ROWS)] # gameboard: '0' if no piece, '1' if player one's piece, '2' if players 2 piece
        self.to_play = GameMeta.PLAYERS['one'] # who's playing (first player is player one)
        self.Height = [GameMeta.ROWS - 1] * GameMeta.COLS # height of gameboard
        self.last_played = [] # the last move played - to check for win
    def get_board(self):
        return deepcopy(self.gameboard)
    def move(self, col):
        self.gameboard[self.Height[col]][col] = self.to_play
        self.last_played = [self.Height[col], col]
        self.Height[col] -= 1
        self.to_play = GameMeta.PLAYERS['two'] if self.to_play == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']
    def get_legal_moves(self): # check for illegal move
        return [col for col in range(GameMeta.COLS) if self.gameboard[0][col] == 0]
    def check_win(self): # check who won
        if len(self.last_played) > 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.gameboard[self.last_played[0]][self.last_played[1]]
        return 0
    def check_win_from(self, row, col): # check if there is a win based on the last move played
        player = self.gameboard[row][col]
        consecutive = 1
        # Check for horizontal win
        tmprow = row
        while tmprow + 1 < GameMeta.ROWS and self.gameboard[tmprow + 1][col] == player:
            consecutive += 1
            tmprow += 1
        tmprow = row
        while tmprow - 1 >= 0 and self.gameboard[tmprow - 1][col] == player:
            consecutive += 1
            tmprow -= 1
        if consecutive >= 4:
            return True
        # Check for vertical win
        consecutive = 1
        tmpcol = col
        while tmpcol + 1 < GameMeta.COLS and self.gameboard[row][tmpcol + 1] == player:
            consecutive += 1
            tmpcol += 1
        tmpcol = col
        while tmpcol - 1 >= 0 and self.gameboard[row][tmpcol - 1] == player:
            consecutive += 1
            tmpcol -= 1
        if consecutive >= 4:
            return True
        # Check for diagonal win
        consecutive = 1
        tmprow = row
        tmpcol = col
        while tmprow + 1 < GameMeta.ROWS and tmpcol + 1 < GameMeta.COLS and self.gameboard[tmprow + 1][tmpcol + 1] == player:
            consecutive += 1
            tmprow += 1
            tmpcol += 1
        tmprow = row
        tmpcol = col
        while tmprow - 1 >= 0 and tmpcol - 1 >= 0 and self.gameboard[tmprow - 1][tmpcol - 1] == player:
            consecutive += 1
            tmprow -= 1
            tmpcol -= 1
        if consecutive >= 4:
            return True
        # Check for anti-diagonal win
        consecutive = 1
        tmprow = row
        tmpcol = col
        while tmprow + 1 < GameMeta.ROWS and tmpcol - 1 >= 0 and self.gameboard[tmprow + 1][tmpcol - 1] == player:
            consecutive += 1
            tmprow += 1
            tmpcol -= 1
        tmprow = row
        tmpcol = col
        while tmprow - 1 >= 0 and tmpcol + 1 < GameMeta.COLS and self.gameboard[tmprow - 1][tmpcol + 1] == player:
            consecutive += 1
            tmprow -= 1
            tmpcol += 1
        if consecutive >= 4:
            return True
        return False
    def game_over(self): # check if the game is done
        return self.check_win() or len(self.get_legal_moves()) == 0
    def get_outcome(self): # get the outcome
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameMeta.OUTCOMES['draw']
        return GameMeta.OUTCOMES['one'] if self.check_win() == GameMeta.PLAYERS['one'] else GameMeta.OUTCOMES['two']
    def print(self): # printing the board
        print('=====================================')
        for row in range(GameMeta.ROWS):
            for col in range(GameMeta.COLS):
                print('|| {} '.format('X' if self.gameboard[row][col] == 1 else 'O' if self.gameboard[row][col] == 2 else ' '), end='')
            print('||')
        print('=====================================')