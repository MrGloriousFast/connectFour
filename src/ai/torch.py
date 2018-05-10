from ai.bot_base import BotBase
import torch as pytorch

class Torch(BotBase):

    def __init__(self):
        super().__init__()

        self.dtype = pytorch.float
        self.device = pytorch.device("cpu")
        # dtype = torch.device("cuda:0") # Uncomment this to run on GPU

        # N is batch size; D_in is input dimension;
        # H is hidden dimension; D_out is output dimension.
        N, D_in, H, D_out = 64, 1000, 100, 10


    def choose_action(self, gamefield, action_list):




        return 0