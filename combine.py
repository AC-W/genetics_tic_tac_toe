# -*- coding: utf-8 -*-
"""combine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tFXHJPNi4DvdVtVulYl1aK1B8np09h6o
"""

import numpy as np
from torch.nn import functional as F
from torch import nn
import torch
import copy

class agent():
  def __init__(self,netX):
    self.fitness = 0
    self.Xbrain = netX
    self.brain = None
    self.games_played = 0
    self.player = -1
    self.generation = 0
    self.parents = [-1,-1]
    self.is_parent = False
  def __str__(self):
    print(f'fitness: {self.fitness}')
    return ''
  def set_player(self,sym):
    self.player = sym
  def make_move(self,board):
    if self.player == -1:
      matrix = matrixX
      self.brain = self.Xbrain
    else:
      matrix = matrixO
      x_loc = 0
      y_loc = 0
      count = 0
      for x in range(3):
        for y in range(3):
            if board.board[x][y] != 0:
                count += 1
                x_loc = x
                y_loc = y
      if count == 1:
        model_path = f'models/modelO_1.{x_loc}_{y_loc}'
        state = torch.load(model_path,map_location=torch.device('cpu'))
        self.brain = ttt_netO()
        self.brain.load_state_dict(state)
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
      val = self.player * val
      if best_score == None or val > best_score:
        best_score = val
        best_move = move
    return best_move,best_score

class ttt_netX(nn.Module):
  def __init__(self):
    super(ttt_netX,self).__init__()
    self.layer1 = nn.Linear(3*3*3,10)
    self.layer2 = nn.Linear(10,1)
  def forward(self, x):
    x = x.view(-1,3*3*3)
    x = F.relu(self.layer1(x))
    x = self.layer2(x)
    return torch.tanh(x)

def matrixX(board):
  matrix = np.zeros((3,3,3))
  matrix[:,:,2] = board.turn
  for x in range(len(board.board)):
    for y in range(len(board.board[x])):
      if board.board[x][y] == 1:
        matrix[x,y,0] = 1
      elif board.board[x][y] == -1:
        matrix[x,y,1] = 1
  return torch.tensor(matrix).float()

class ttt_netO(nn.Module):
  def __init__(self):
    super(ttt_netO,self).__init__()
    self.layer1 = nn.Linear(3*3*2,10)
    self.layer2 = nn.Linear(10,1)
  def forward(self, x):
    x = x.view(-1,3*3*2)
    x = F.relu(self.layer1(x))
    x = self.layer2(x)
    return torch.sigmoid(x)

def matrixO(board):
  matrix = np.zeros((3,3,2))
  for x in range(len(board.board)):
    for y in range(len(board.board[x])):
      if board.board[x][y] == 1:
        matrix[x,y,0] = 1
      elif board.board[x][y] == -1:
        matrix[x,y,1] = 1
  return torch.tensor(matrix).float()

class ttt():
  def __init__(self,size=(3,3)):
    self.turn = -1
    self.win = None
    self.board = np.zeros(size)
    self.x = size[0]
    self.y = size[1]

  def reset(self,size=(3,3)):
    self.turn = -1
    self.win = None
    self.board = np.zeros(size)
    self.x = size[0]
    self.y = size[1]

  def getBoard(self):
    Rboard = np.empty([3,3], dtype = str)
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        sym = ""
        if self.board[x][y] == -1:
          sym = "X"
        elif self.board[x][y] == 1:
          sym = "O"
        Rboard[x][y] = sym
    return Rboard
    
  def check(self):
    empty = False
    for x in range(len(self.board)):
      scoreX = 0
      scoreY = 0
      for y in range(len(self.board[x])):
        if self.board[x][y] == 0:
          empty = True
        scoreX += self.turn*self.board[x][y]
        scoreY += self.turn*self.board[y][x]
      if scoreY == 3 or scoreX == 3:
        self.win = self.turn
        return
    score = 0
    score += self.turn*self.board[0][0]
    score += self.turn*self.board[1][1]
    score += self.turn*self.board[2][2]
    if score == 3:
       self.win = self.turn
       return
    score = 0
    score += self.turn*self.board[0][2]
    score += self.turn*self.board[1][1]
    score += self.turn*self.board[2][0]
    if score == 3:
       self.win = self.turn
       return
    if self.win == None and not empty:
      self.win = 0
      return
  def game_end(self):
    if self.win == None:
      return
    if self.win == 0:
      print("no win")
      return
    if self.win == 1:
      print("O wins")
      return
    if self.win == -1:
      print("X wins")
      return
    return

  def valid_moves(self):
    valid_moves = []
    if self.win != None:
      return valid_moves
    for x in range(len(self.board)):
      for y in range(len(self.board[x])):
        if self.board[x][y] == 0:
          valid_moves.append((x,y))
    return valid_moves

  def play(self,x,y):
    if self.win != None:
      self.check()
      return
    if x >= self.x or x < 0:
      print('Invalid move')
      return
    if y >= self.y or y < 0:
      print('Invalid move')
      return
    if self.board[x][y] != 0:
      print('Invalid move')
      return
    if self.turn == -1:
     self.board[x][y] = -1
     self.check()
     self.turn = 1
    elif self.turn == 1:
     self.board[x][y] = 1
     self.check()
     self.turn = -1

  def __str__(self):
    for x in range(len(self.board)):
      line = ''
      for y in range(len(self.board[x])):
        if self.board[x][y] == 0:
          sym = '.'
        elif self.board[x][y] == 1:
          sym = 'O'
        else:
          sym = 'X'
        line += f'{sym} '
      print(f'{line}')
    return ''

def play_game(player1=None,player2=None,human=False):
  board = ttt()
  if (not human):
    #'X' goes first
    #-1 = 'X' 1 = 'O'
    player1.set_player(-1)
    player2.set_player(1)
    while board.win == None:
      output = None
      score = None
      if (board.turn == player1.player):
        output,score = player1.make_move(board)
      else:
        output,score = player2.make_move(board)
      board.play(output[0],output[1])
    if board.win == -1:
      player1.fitness += 15
      player1.games_played += 1
      player2.games_played += 1

    elif board.win == 1:
      player2.fitness += 20
      player2.games_played += 1
      player1.games_played += 1

    else:
      player1.fitness += 5
      player2.fitness += 10
      player1.games_played += 1
      player2.games_played += 1
  else:
    player_turn = None
    while player_turn != "-1" and player_turn != "1":
      player_turn = input("-1 for X and 1 for O:")
      if player_turn != "-1" and player_turn != "1":
        print('invalid input')
    player_turn = int(player_turn)
    if player_turn == -1:
      player1.set_player(1)
    else:
      player1.set_player(-1)
    while board.win == None:
      output = None
      score = None
      if (board.turn == player1.player):
        output,score = player1.make_move(board)
      else:
        print(board)
        row = int(input("row:"))
        col = int(input("col:"))
        output = (row,col)
      board.play(output[0],output[1])
    board.game_end
    print(board)
  return

def play_game(player1=None,player2=None,human=False):
  board = ttt()
  if (not human):
    #'X' goes first
    #-1 = 'X' 1 = 'O'
    player1.set_player(-1)
    player2.set_player(1)
    while board.win == None:
      output = None
      score = None
      if (board.turn == player1.player):
        output,score = player1.make_move(board)
      else:
        output,score = player2.make_move(board)
      board.play(output[0],output[1])
    if board.win == -1:
      player1.fitness += 15
      player1.games_played += 1
      player2.games_played += 1

    elif board.win == 1:
      player2.fitness += 20
      player2.games_played += 1
      player1.games_played += 1

    else:
      player1.fitness += 5
      player2.fitness += 10
      player1.games_played += 1
      player2.games_played += 1
  else:
    player_turn = None
    while player_turn != "-1" and player_turn != "1":
      player_turn = input("-1 for X and 1 for O:")
      if player_turn != "-1" and player_turn != "1":
        print('invalid input')
    player_turn = int(player_turn)
    if player_turn == -1:
      player1.set_player(1)
    else:
      player1.set_player(-1)
    while board.win == None:
      output = None
      score = None
      if (board.turn == player1.player):
        output,score = player1.make_move(board)
      else:
        print(board)
        row = int(input("row:"))
        col = int(input("col:"))
        output = (row,col)
      board.play(output[0],output[1])
    board.game_end
    print(board)
  return