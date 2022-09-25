import training.objects.agent as ag
import training.objects.net as nt
import enviroment.ttt as en
import torch
import random
import numpy as np
import copy

def generate_agents(pop,net):
  agents = []
  while len(agents) < pop:
    new_net = net()
    agents.append(ag.agent(new_net))
  return agents

def reproduction(parent1,parent2,mutation_count=0,energy=0):
  net1 = parent1.brain
  net2 = parent2.brain
  new_net = nt.ttt_net()

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
      if (random.uniform(0, 1)<= energy/30):
        new_gen[i] = new_gen[i]+random.uniform(-energy/10,energy/10)
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
  return ag.agent(new_net),mutation_count

def a_reproduction(parent1,mutation_count=0,energy=0):
  net1 = parent1.brain
  new_net = nt.ttt_net()

  shapes = []
  new_parm = []

  it1 = iter(net1.named_parameters())
  con = True
  while con:
    try:
      name, parm1 = next(it1)
    except:
      con = False
      continue
    shapes.append(parm1.shape)
    parm1 = (parm1.detach().numpy().flatten())
    new_gen = np.zeros(parm1.shape,dtype="float32")
    for i in range(len(parm1)):
      new_gen[i] = parm1[i]
      if (random.uniform(0, 1)<= energy/10):
        new_gen[i] = new_gen[i]+random.uniform(-energy/3,energy/3)
        mutation_count +=1
    new_parm.append(new_gen)

  i = 0
  new_state = new_net.state_dict()
  for name, parm in new_net.named_parameters():
    with torch.no_grad():
      new_state[name] = (torch.tensor((new_parm[i].reshape(shapes[i])),requires_grad=True))
      i += 1
  new_net.load_state_dict(new_state)
  return ag.agent(new_net),mutation_count

def crossOver(leaderboard,n_child,n_random,n_asex,generation=0,energy=0):
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
    child.generation = "R"
    newGen.append(child)

  a_mutation_count=0
  weights = []
  for i in leaderboard:
    weights.append((i[1].fitness)**5)
  weights.sort(reverse=True)
  parents = [i for i in range(len(leaderboard))]
  while len(newGen)-n_child < n_asex:
    child = None
    p1 = random.choices(parents,weights=weights,k=1)
    p1 = p1[0]
    P1 = leaderboard[0][1]
    child,a_mutation_count = a_reproduction(P1,mutation_count=a_mutation_count,energy=energy)
    child.parents = [p1]
    child.generation = "A"
    newGen.append(child)

  newGen += generate_agents(n_random,nt.ttt_net)
  i = 0
  while len(newGen) != len(leaderboard):
    newGen.append(leaderboard[i][1])
    leaderboard[i][1].is_parent = True
    i += 1
  print(f'number of mutations: {mutation_count}')
  print(f'number of a_mutations: {a_mutation_count}')
  return newGen

def fitness(agents,train="both"):
  min_loss = 10000
  for agent1 in agents:
    if agent1.is_parent:
      continue
    wins = 0
    loss = 0
    tie = 0

    if train == "X" or train == "both":
      # X: 
      agent1.player = -1
      game = en.ttt()
      games = []
      games.append(game)
      last_set = []
      con = True
      
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
      # X:
    if train == "O" or train == "both":
    # O:
      agent1.player = 1
      game = en.ttt()
      games = []
      last_set = []
      last_set.append(game)
      con = True
      while con:
        games = []
        for i in range(len(last_set)):
          for move in last_set[i].valid_moves():
            temp = copy.deepcopy(last_set[i])
            temp.play(move[0],move[1])
            if temp.win == None:
              move, _ = agent1.make_move(temp)
              temp.play(move[0],move[1])
            if temp.win == -1:
              loss += 1
            elif temp.win == 1:
              wins += 1
            elif temp.win == 0:
              tie += 1
            else:
              games.append(temp)
        last_set = games
        if len(games) == 0:
          con = False
    # O end
    total = (wins+tie+loss)
    fit = 1/(loss+1) + 1/(tie+1)/10000
    if loss < min_loss:
      min_loss = loss
    if fit < 0:
      fit = 0
    agent1.fitness =  agent1.fitness + fit
  print('min loss: {}'.format(min_loss))

def takefirst(elm):
  return elm[0]

def sort_agents(agents):
  leaderboard = []
  for agent in agents:
    agent.is_parent = True
    leaderboard.append((agent.fitness,agent,agent.generation,agent.parents))
  leaderboard.sort(key=takefirst,reverse=True)
  return leaderboard

def checkOne(agent1):
# check for AI playing as X
  agent1.player = -1
  game = en.ttt()
  games = []
  games.append(game)
  last_set = []
  con = True
  wins = 0
  loss = 0
  tie = 0

# search all possible games
  while con:
    last_set = games
    games = []
    for i in range(len(last_set)):
      move, val = agent1.make_move(last_set[i])
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
  print('X:wins:{} Losses:{} tie:{}'.format(wins,loss,tie))

# check for AI playing as O
  agent1.player = 1
  game = en.ttt()
  games = []
  last_set = []
  last_set.append(game)
  con = True
  wins = 0
  loss = 0
  tie = 0
  while con:
    games = []
    for i in range(len(last_set)):
      for move in last_set[i].valid_moves():
        temp = copy.deepcopy(last_set[i])
        temp.play(move[0],move[1])
        if temp.win == None:
          move, val = agent1.make_move(temp)
          temp.play(move[0],move[1])
        if temp.win == -1:
          # print(f'loss: {val}')
          loss += 1
        elif temp.win == 1:
          # print(f'win: {val}')
          wins += 1
        elif temp.win == 0:
          tie += 1
        else:
          games.append(temp)
    last_set = games
    if len(games) == 0:
      con = False
  print('O:wins:{} Losses:{} tie:{}'.format(wins,loss,tie))