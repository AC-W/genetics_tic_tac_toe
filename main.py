from torch.nn import functional as F
from torch import nn, optim
import sys
from IPython.display import clear_output
from tic_tac_toe import *
import torch

print(sys.path)


def matrix(board):
  matrix = np.zeros((3,3,2))
  matrix[:,:,1] = board.turn
  for x in range(len(board.board)):
    for y in range(len(board.board[x])):
      matrix[x,y,0] = board.board[x][y]
  return matrix


class ttt_net(nn.Module):
  def __init__(self):
    super(ttt_net,self).__init__()
    self.layer1 = nn.Linear(2*9*3,10)
    self.layer2 = nn.Linear(10,1)
  def forward(self, x):
    x = x.view(-1,2*9*3)
    x = F.relu(self.layer1(x))
    x = self.layer2(x)
    return torch.tanh(x)

board = ttt()
mat = matrix(board)
print(mat)
board.play(1,1)
mat = matrix(board)
print(mat)

board = ttt()
while board.win == None:
  dic = {-1:"X",1:"O"}
  print(f'{dic[board.turn]}\'s turn:')
  x = int(input("row:"))
  y = int(input("col:"))
  clear_output()
  board.play(x,y)
  print(board)