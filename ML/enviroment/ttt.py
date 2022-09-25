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
      print(board)
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