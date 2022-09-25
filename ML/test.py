import enviroment.ttt as en
import torch
import training.objects.net as nt
import training.objects.agent as at
import training.procedures.gen as gn

state = torch.load('ttt_modelX')

# game = en.ttt()
# game.play(0,2)
# mat1 = at.matrix(game)

# game = en.ttt()
# game.play(1,1)
# mat2 = at.matrix(game)

new_net = nt.ttt_net()
new_net.load_state_dict(state)

agent1 = at.agent(new_net)

state = torch.load('ttt_modelO')
new_net = nt.ttt_net()
new_net.load_state_dict(state)
# print(new_net(mat1))
# print(new_net(mat2))

agent2 = at.agent(new_net)

en.play_game(player1=agent1,player2=agent2,human=False)
gn.checkOne(agent2)