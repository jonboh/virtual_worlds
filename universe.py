import numpy as np
import matplotlib.pyplot as plt
import matplotlib.artist as art
import matplotlib.collections as col
from agent import *


class Universe:
    def __init__(self, num_dim, num_agents, num_food):
        self.t = 0
        self.num_dim = num_dim
        self.agents = [Agent(np.random.rand(1),np.random.rand(num_dim),np.random.rand(1)*0.01) for i in range(0,num_agents)]
        self.foods = [Matter(np.random.rand(1),np.random.rand(num_food)) for i in range(0,num_food)]
        self.physics = Rules


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


class Rules:
    @staticmethod
    def movement_cost(position, new_position, mass):
        energy_cost = np.linalg.norm(position-new_position)*mass*0.1
        return energy_cost


