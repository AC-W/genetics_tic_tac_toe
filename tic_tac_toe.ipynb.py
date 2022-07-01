{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"name":"tic_tac_toe.ipynb","provenance":[],"authorship_tag":"ABX9TyNSQlg4bZrcAz184UIhBty1"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":1,"metadata":{"id":"vOtXXz9qD7m1","executionInfo":{"status":"ok","timestamp":1656717595342,"user_tz":420,"elapsed":152,"user":{"displayName":"Ryan Wei","userId":"17953581929929101304"}}},"outputs":[],"source":["import numpy as np\n","\n","class ttt():\n","  def __init__(self,size=(3,3)):\n","    self.turn = -1\n","    self.win = None\n","    self.board = np.zeros(size)\n","    self.x = size[0]\n","    self.y = size[1]\n","    \n","  def check(self):\n","    empty = False\n","    for x in range(len(self.board)):\n","      scoreX = 0\n","      scoreY = 0\n","      for y in range(len(self.board[x])):\n","        if self.board[x][y] == 0:\n","          empty = True\n","        scoreX += self.turn*self.board[x][y]\n","        scoreY += self.turn*self.board[y][x]\n","      if scoreY == 3 or scoreX == 3:\n","        self.win = self.turn\n","        return\n","    score = 0\n","    score += self.turn*self.board[0][0]\n","    score += self.turn*self.board[1][1]\n","    score += self.turn*self.board[2][2]\n","    if score == 3:\n","       self.win = self.turn\n","       return\n","    score = 0\n","    score += self.turn*self.board[0][2]\n","    score += self.turn*self.board[1][1]\n","    score += self.turn*self.board[2][0]\n","    if score == 3:\n","       self.win = self.turn\n","       return\n","    if self.win == None and not empty:\n","      self.win = 0\n","      return\n","  def game_end(self):\n","    if self.win == None:\n","      return\n","    if self.win == 0:\n","      print(\"no win\")\n","      return\n","    if self.win == 1:\n","      print(\"O wins\")\n","      return\n","    if self.win == -1:\n","      print(\"X wins\")\n","      return\n","    return\n","\n","  def play(self,x,y):\n","    if self.win != None:\n","      self.check()\n","      self.game_end()\n","      return\n","    if x >= self.x or x < 0:\n","      print('Invalid move')\n","      return\n","    if y >= self.y or y < 0:\n","      print('Invalid move')\n","      return\n","    if self.board[x][y] != 0:\n","      print('Invalid move')\n","      return\n","    if self.turn == -1:\n","     self.board[x][y] = -1\n","     self.check()\n","     self.game_end()\n","     self.turn = 1\n","    elif self.turn == 1:\n","     self.board[x][y] = 1\n","     self.check()\n","     self.game_end()\n","     self.turn = -1\n","\n","  def __str__(self):\n","    for x in range(len(self.board)):\n","      line = ''\n","      for y in range(len(self.board[x])):\n","        if self.board[x][y] == 0:\n","          sym = '.'\n","        elif self.board[x][y] == 1:\n","          sym = 'O'\n","        else:\n","          sym = 'X'\n","        line += f'{sym} '\n","      print(f'{line}')\n","    return ''"]}]}