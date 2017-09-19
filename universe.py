import numpy as np
import matplotlib.pyplot as plt
import matplotlib.artist as art
import matplotlib.collections as col
from agent import *


class Universe:
    def __init__(self, num_dims, rules, agents, foods):
        self.t = 0
        self.num_dim = num_dims
        self.physics = rules
        self.agents = agents
        self.foods = foods
        self.gen_status_list()

    def retrieve_info(self, position, radius):
        info_array = np.concatenate((self.agent_positions_hp,self.food_positions_hp),axis=0)
        indexes_logic = radius < np.sqrt(
            np.sum((info_array[:,0:len(position)]-position)**2
                   ,axis=1,keepdims=True)) # Multi-dim Spherical check
        info_array = np.delete(info_array,np.where(indexes_logic),axis=0)
        return info_array

    def pass_time(self):
        for agent in self.agents:
            agent.live(self)
        self.t = self.t + 1
        self.gen_status_list()


    def gen_status_list(self):
        self.agent_positions_hp = np.ones((len(self.agents),3))*np.nan
        self.food_positions_hp = np.ones((len(self.foods),3))*np.nan
        for i in range(0,len(self.agents)):
            self.agent_positions_hp[i,0] = self.agents[i].position[0]
            self.agent_positions_hp[i,1] = self.agents[i].position[1]
            self.agent_positions_hp[i,2] = self.agents[i].hp
        for i in range(0,len(self.foods)):
            self.food_positions_hp[i,0] = self.foods[i].position[0]
            self.food_positions_hp[i,1] = self.foods[i].position[1]
            self.food_positions_hp[i,2] = self.foods[i].hp


