import numpy as np
import multiprocessing as mulp
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
        # Generate internal state
        self.gen_object_dict()

    def initialize_world_state(self):
        self.object_dict = {}
        self.agent_charact = np.ones((len(self.agents), self.num_dim + 2)) * np.nan
        self.food_charact = np.ones((len(self.foods), self.num_dim + 2)) * np.nan

    def gen_object_dict(self):
        self.initialize_world_state()
        id = 0
        for element in self.agents:
            self.object_dict[id] = element
            id += 1
        for element in self.foods:
            self.object_dict[id] = element
            id += 1
        self.gen_status_list()

    def gen_status_list(self):
        ind_agent = 0
        ind_food = 0
        list_of_death = []
        list_of_unexistance = []
        for entry in self.object_dict:
            if type(self.object_dict[entry]) is Agent:
                if self.object_dict[entry].hp>0:
                    self.agent_charact[ind_agent, 0] = self.object_dict[entry].position[0]
                    self.agent_charact[ind_agent, 1] = self.object_dict[entry].position[1]
                    self.agent_charact[ind_agent, 2] = self.object_dict[entry].hp
                    self.agent_charact[ind_agent, 3] = entry
                    ind_agent += 1
                else: # This element is dead, no longer exists
                    list_of_death.append(entry)

            elif type(self.object_dict[entry]) is Matter:
                if self.object_dict[entry].energy > 0:
                    self.food_charact[ind_food, 0] = self.object_dict[entry].position[0]
                    self.food_charact[ind_food, 1] = self.object_dict[entry].position[1]
                    self.food_charact[ind_food, 2] = self.object_dict[entry].energy
                    self.food_charact[ind_food, 3] = entry
                    ind_food += 1
                else: # This element is dead, no longer exists
                    list_of_unexistance.append(entry)
        for entry in list_of_death:
            agent_dead = self.object_dict.pop(entry)
            self.agents.remove(agent_dead)
            new_food = Matter(agent_dead.energy,agent_dead.position)
            self.foods.append(new_food)
        for entry in list_of_unexistance:
            food_disapear = self.object_dict.pop(entry)
            self.foods.remove(food_disapear)
        if len(list_of_death)>0 or len(list_of_unexistance)>0:
            self.gen_object_dict()

    def add_new_things(self, new_things):
        for element in new_things:
            if type(element) is Agent:
                self.agents.append(element)
            elif type(element) is Matter:
                self.foods.append(element)
        self.gen_object_dict()

    def retrieve_info(self, position, radius):
        info_array = np.concatenate((self.agent_charact,self.food_charact),axis=0)
        norms = np.linalg.norm(info_array[:,0:len(position)]-position,axis=1,keepdims=True)
        indexes_logic = np.logical_or(radius < norms, norms == 0) # Multi-dim Spherical check
        indexes_logic = indexes_logic.reshape((indexes_logic.size,))
        info_array = info_array[np.logical_not(indexes_logic),:]
        return info_array

    def retrieve_obj_byid(self,id):
        obj = self.object_dict[id]
        return obj

    def pass_time(self):
        for agent in self.agents:
            agent.live(self)
        self.t = self.t + 1
        self.gen_status_list()




