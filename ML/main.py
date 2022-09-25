import enviroment.ttt as en
import training.procedures.gen as gn
import training.objects.net as nt
import training.objects.agent as at
import time
import torch

game = en.ttt()
agents = gn.generate_agents(20,nt.ttt_net)
state = torch.load('ttt_modelO')
new_net = nt.ttt_net()
new_net.load_state_dict(state)
agent1 = at.agent(new_net)
agents.append(agent1)
gen = 0

while True:
  print("\n")
  start = time.time()
  gn.fitness(agents,train="O")
  leaderboard = gn.sort_agents(agents)
  end = time.time()
  print('Time:{:0.2f}'.format(end-start))
  print('Gen:{}'.format(gen))
  print(leaderboard)
  gn.checkOne(leaderboard[0][1])
  gen += 1
  torch.save(leaderboard[0][1].brain.state_dict(),'ttt_modelO')
  agents = gn.crossOver(leaderboard=leaderboard,n_child=10,n_random=2,n_asex=1,generation=gen,energy = 0.2)
