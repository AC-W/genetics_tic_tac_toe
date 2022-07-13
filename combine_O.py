import numpy as np
from torch.nn import functional as F
from torch import nn
import torch
import copy
import combine

# class agent():
#   def __init__(self,netX,netO):
#     self.fitness = 0
#     self.Obrain = netO
#     self.Xbrain = netX
#     self.brain = None
#     self.games_played = 0
#     self.player = -1
#     self.generation = 0
#     self.parents = [-1,-1]
#     self.is_parent = False
#     self.rotate = 0
#     self.flipX = False
#     self.flipY = False
#   def __str__(self):
#     print(f'fitness: {self.fitness}')
#     return ''
#   def set_player(self,sym):
#     self.player = sym
#   def make_move(self,board):
#     if self.player == -1:
#       matrix = combine.matrixX
#       self.brain = self.Xbrain
#     else:
#       matrix = combine.matrixO
#       x_loc = 0
#       y_loc = 0
#       count = 0
#       for x in range(3):
#         for y in range(3):
#             if board[x][y] != 0:
#                 count += 1
#                 x_loc = x
#                 y_loc = y

#       self.brain = self.Obrain[x_loc][y_loc]
#     valid_moves = board.valid_moves()
#     best_move = None
#     best_score = None
#     for move in valid_moves:
#       temp_board = copy.deepcopy(board)
#       temp_board.play(move[0],move[1])
#       mat = matrix(temp_board)
#       with torch.no_grad():
#         out = self.brain(mat)
#       val = float(out[0])
#       val = self.player * val
#       if best_score == None or val > best_score:
#         best_score = val
#         best_move = move
#     return best_move,best_score

state = torch.load('modelX',map_location=torch.device('cpu'))
netX = combine.ttt_netX()
netX.load_state_dict(state)

agent1 = combine.agent(netX)
games = []
agents = combine.generate_agents(100,combine.ttt_netX)
for agent_temp in agents:
    games.append(combine.oneVSone(player1=agent_temp,player2=agent1))

print(f'X player wins: {games.count(-1)}')
print(f'O player wins: {games.count(1)}')
print(f'ties: {games.count(0)}')