# -*- coding: utf-8 -*-
"""X.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KXxwKakiZiJ_hASbDPEAwcAOUUMqy1iD
"""

import numpy as np

class ttt():
  def __init__(self,size=(3,3)):
    self.turn = -1
    self.win = None
    self.board = np.zeros(size)
    self.x = size[0]
    self.y = size[1]
    
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

from torch.nn import functional as F
from torch import nn, optim
import sys
import torch
from IPython.display import clear_output
from torchvision import transforms as tr
import random
import copy

class agent():
  def __init__(self,net):
    self.fitness = 0
    self.brain = net
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

def generate_agents(pop,net):
  agents = []
  while len(agents) < pop:
    new_net = net()
    agents.append(agent(new_net))
  return agents
    
def takefirst(elm):
  return elm[0]

def sort_agents(agents):
  leaderboard = []
  for agent in agents:
    leaderboard.append((agent.fitness,agent,agent.generation,agent.parents))
  leaderboard.sort(key=takefirst,reverse=True)
  return leaderboard

def reproduction(parent1,parent2,mutation_count=0,energy=0):
  net1 = parent1.brain
  net2 = parent2.brain
  new_net = ttt_net()

  shapes = []
  new_parm = []

  it1 = iter(net1.named_parameters())
  it2 = iter(net2.named_parameters())
  con = True
  while con:
    try:
      name, parm1 = next(it1)
      name, parm2 = next(it2)
    except:
      con = False
      continue
    shapes.append(parm1.shape)
    parm1 = (parm1.detach().numpy().flatten())
    parm2 = (parm2.detach().numpy().flatten())
    new_gen = np.zeros(parm2.shape,dtype="float32")
    for i in range(len(parm2)):
      if (random.uniform(0, 1)>=0.5):
        new_gen[i] = parm2[i]
      else:
        new_gen[i] = parm1[i]
      if (random.uniform(0, 1)<= energy):
        new_gen[i] = new_gen[i]+random.uniform(-.02 - energy/5, 0.02 + energy/5)
        mutation_count +=1
    new_parm.append(new_gen)

  i = 0
  new_state = new_net.state_dict()
  for name, parm in new_net.named_parameters():
    with torch.no_grad():
      new_state[name] = (torch.tensor((new_parm[i].reshape(shapes[i])),requires_grad=True))
      i += 1

  new_net.load_state_dict(new_state)
  # new_net = new_net.to(device)

  return agent(new_net),mutation_count

def crossOver(leaderboard,n_child,n_random,generation=0,energy=0):
  mutation_count=0
  newGen = []
  while len(newGen) <= n_child:
    weights = []
    for i in leaderboard:
      weights.append((i[1].fitness)**5)
    weights.sort(reverse=True)
    child = None
    parents = [i for i in range(len(leaderboard))]
    p1 = random.choices(parents,weights=weights,k=1)
    p1 = p1[0]
    parents.remove(p1)
    weights.pop(p1)
    P1 = leaderboard[p1][1]
    p2 = random.choices(parents,weights=weights,k=1)
    p2 = p2[0]
    P2 = leaderboard[p2][1]
    child,mutation_count = reproduction(P1,P2,mutation_count=mutation_count,energy=energy)
    child.parents = [p1,p2]
    child.generation = generation
    newGen.append(child)
  newGen += generate_agents(n_random,ttt_net)
  i = 0
  while len(newGen) != len(leaderboard):
    newGen.append(leaderboard[i][1])
    leaderboard[i][1].is_parent = True
    i += 1
  print(f'number of mutations: {mutation_count}')
  return newGen

class ttt_net(nn.Module):
  def __init__(self):
    super(ttt_net,self).__init__()
    self.layer1 = nn.Linear(3*3*3,10)
    self.layer2 = nn.Linear(10,1)
  def forward(self, x):
    x = x.view(-1,3*3*3)
    x = F.relu(self.layer1(x))
    x = self.layer2(x)
    return torch.tanh(x)

def matrix(board):
  matrix = np.zeros((3,3,3))
  matrix[:,:,2] = board.turn
  for x in range(len(board.board)):
    for y in range(len(board.board[x])):
      if board.board[x][y] == 1:
        matrix[x,y,0] = 1
      elif board.board[x][y] == -1:
        matrix[x,y,1] = 1
  return torch.tensor(matrix).float()

def agentsFirst(agents):
  min_loss = 10000
  for agent1 in agents:
    if agent1.is_parent:
      continue
    agent1.player = -1
    game = ttt()
    games = []
    games.append(game)
    last_set = []
    con = True
    wins = 0
    loss = 0
    tie = 0
    while con:
      last_set = games
      games = []
      for i in range(len(last_set)):
        move, _ = agent1.make_move(last_set[i])
        if (last_set[i].win == None):
          last_set[i].play(move[0],move[1])
        if last_set[i].win == -1:
          wins += 1
        elif last_set[i].win == 0:
          tie += 1
        else:
          for move in last_set[i].valid_moves():
            tempGame = copy.deepcopy(last_set[i])
            tempGame.play(move[0],move[1])
            if tempGame.win == 1:
              loss += 1
            elif tempGame.win == 0:
              tie += 1
            else:
              games.append(tempGame)
      if len(games) == 0:
        con = False
    total = (wins+tie+loss)
    fit = (1/(loss+1))*100 + (1/tie)/100
    if loss < min_loss:
      min_loss = loss
    if fit < 0:
      fit = 0
    agent1.fitness =  agent1.fitness + fit
  print('min loss: {}'.format(min_loss))

def checkOne(agent1):
  agent1.player = -1
  game = ttt()
  games = []
  games.append(game)
  last_set = []
  con = True
  wins = 0
  loss = 0
  tie = 0
  while con:
    last_set = games
    games = []
    for i in range(len(last_set)):
      move, _ = agent1.make_move(last_set[i])
      if (last_set[i].win == None):
        last_set[i].play(move[0],move[1])
      if last_set[i].win == -1:
        wins += 1
      elif last_set[i].win == 0:
        tie += 1
      else:
        for move in last_set[i].valid_moves():
          tempGame = copy.deepcopy(last_set[i])
          tempGame.play(move[0],move[1])
          if tempGame.win == 1:
            loss += 1
          elif tempGame.win == 0:
            tie += 1
          else:
            games.append(tempGame)
    if len(games) == 0:
      con = False
  print('O:wins:{} Losses:{} tie:{}'.format(wins,loss,tie))

state = torch.load('/content/drive/MyDrive/Models/tic_tac_toe_net_1.4',map_location=torch.device('cpu'))
new_net = ttt_net()
new_net.load_state_dict(state)
agent1 = agent(new_net)

import time
start = time.time()
checkOne(agent1)
end = time.time()
print('Time:{:0.2f}'.format(end-start))

import time

state = torch.load('/content/drive/MyDrive/Models/tic_tac_toe_net_1.4',map_location=torch.device('cpu'))
new_net = ttt_net()
new_net.load_state_dict(state)
agent1 = agent(new_net)

agents = generate_agents(99,ttt_net)
agents.append(agent1)
gen = 0
while gen <= 10000:
  print("\n")
  start = time.time()
  agentsFirst(agents)
  leaderboard = sort_agents(agents)
  end = time.time()
  print('Time:{:0.2f}'.format(end-start))
  print('Gen:{}'.format(gen))
  print(leaderboard)
  checkOne(leaderboard[0][1])
  gen += 1
  torch.save(leaderboard[0][1].brain.state_dict(),'/content/drive/MyDrive/Models/tic_tac_toe_net_1.4.X')
  agents = crossOver(leaderboard=leaderboard,n_child=60,n_random=20,generation=gen,energy = 0.05)