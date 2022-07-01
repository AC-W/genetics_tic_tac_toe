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

  def play(self,x,y):
    if self.win != None:
      self.check()
      self.game_end()
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
     self.game_end()
     self.turn = 1
    elif self.turn == 1:
     self.board[x][y] = 1
     self.check()
     self.game_end()
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