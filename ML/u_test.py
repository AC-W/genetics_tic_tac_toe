import unittest
import enviroment.ttt as en
import torch
import training.objects.net as nt
import training.objects.agent as ag

class TestAll(unittest.TestCase):

    def test_enviroment(self):
        game = en.ttt()
        game.play(1,1)
        game.play(0,0)
        game.play(2,1)
        game.play(1,0)
        game.play(0,1)
        self.assertEqual(game.win,-1)
        result = ag.matrix(game)
        res = torch.tensor([[1,-1,0,1],[1,-1,0,1],[0,-1,0,1]]).float()
        self.assertTrue(torch.min(torch.eq(result,res)))

    def test_net(self):
        result = nt.ttt_net()
        self.assertIsNotNone(result)

    def test_agent(self):
        result = ag.agent(nt.ttt_net)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()