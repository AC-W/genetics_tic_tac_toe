import torch
import numpy as np
import copy

# Binary encoding:
# def matrix(board):
#   matrix = np.zeros((3,3,3))
#   matrix[:,:,2] = board.turn
#   for x in range(len(board.board)):
#     for y in range(len(board.board[x])):
#       if board.board[x][y] == 1:
#         matrix[x,y,0] = 1
#       elif board.board[x][y] == -1:
#         matrix[x,y,1] = 1
#   return torch.tensor(matrix).float()

# regular board encoding
def matrix(board):
  matrix = np.zeros((3,4))
  matrix[:,3] = board.turn
  for x in range(len(board.board)):
    for y in range(len(board.board[x])):
        matrix[x,y] = board.board[x][y]
  return torch.tensor(matrix).float()

class agent():
  def __init__(self,net):
    self.fitness = 0
    self.brain = net
    self.games_played = 0
    self.player = -1
    self.generation = 0
    self.parents = [-1,-1]
    self.is_parent = False

  def __repr__(self):
    return(f'agent generation:{self.generation}')

  def __str__(self):
    print(f'fitness: {self.fitness}')
    return ''
  def set_player(self,sym):
    self.player = sym

  def make_move(self,board):
    valid_moves = board.valid_moves()
    best_move = None
    best_score = None
    for move in valid_moves:
      temp_board = copy.deepcopy(board)
      temp_board.play(move[0],move[1])
      mat = matrix(temp_board)
      with torch.no_grad():
        out = self.brain(mat)
      
      val = float(out[0])
    #   print(val)
    #   print(move)
      val = self.player * val
      if best_score == None or val > best_score:
        best_score = val
        best_move = move
    return best_move,best_score

    
