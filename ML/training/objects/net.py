from torch.nn import functional as F
from torch import nn
import torch

# class ttt_net(nn.Module):
#   def __init__(self):
#     super(ttt_net,self).__init__()
#     self.layer1 = nn.Linear(3*3*3,100)
#     self.layer2 = nn.Linear(100,50)
#     self.layer3 = nn.Linear(50,10)
#     self.layer4 = nn.Linear(10,1)
#   def forward(self, x):
#     x = x.view(-1,3*3*3)
#     x = F.relu(self.layer1(x))
#     x = F.relu(self.layer2(x))
#     x = F.relu(self.layer3(x))
#     x = self.layer4(x)
#     return torch.tanh(x)

class ttt_net(nn.Module):
  def __init__(self):
    super(ttt_net,self).__init__()
    self.layer1 = nn.Linear(3*4,100)
    self.layer2 = nn.Linear(100,50)
    self.layer3 = nn.Linear(50,10)
    self.layer4 = nn.Linear(10,1)
  def forward(self, x):
    x = x.view(-1,3*4)
    x = F.relu(self.layer1(x))
    x = F.relu(self.layer2(x))
    x = F.relu(self.layer3(x))
    x = self.layer4(x)
    return torch.tanh(x)