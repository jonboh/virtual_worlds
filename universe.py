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


    def pass_time(self):
        for agent in self.agents:
            agent.live(self)
        self.t = self.t + 1


    def gen_collections(self):
        agent_positions_hp = np.ones((len(self.agents),3))*np.nan
        food_positions_hp = np.ones((len(self.foods),3))*np.nan
        for i in range(0,len(self.agents)):
            agent_positions_hp[i,0] = self.agents[i].position[0]
            agent_positions_hp[i,1] = self.agents[i].position[1]
            agent_positions_hp[i,2] = self.agents[i].hp
        for i in range(0,len(self.foods)):
            food_positions_hp[i,0] = self.foods[i].position[0]
            food_positions_hp[i,1] = self.foods[i].position[1]
            food_positions_hp[i,2] = self.foods[i].hp

        # agent_collection = plt.scatter(agent_positions_hp[:,0],agent_positions_hp[:,1],
        #                                s=agent_positions_hp[:,2],color='blue')
        # food_collection =  plt.scatter(food_positions_hp[:,0],food_positions_hp[:,1],
        #                                s=food_positions_hp[:,2], color='red')
        return agent_positions_hp, food_positions_hp


