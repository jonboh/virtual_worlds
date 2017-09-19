import numpy as np


class Matter:
    def __init__(self,life,position):
        self.hp = life
        self.mass = self.hp
        self.position = position

class Agent(Matter):
    def __init__(self, life, position, actions):
        super().__init__(life, position)
        self.actions = actions
        self.reach = self.actions * 3 # Might change in the future

    def percept_world(self, world):
        world_positions = world.retrieve_info(self.position, self.reach)
        return world_positions # it returns a list with info of all objects in reach

    def plan(self,world,info_world):

        movement_direction = np.random.randn(world.num_dim)

        funct_list = [self.move]
        arg_list = [(movement_direction,world.physics.movement_cost)]

        return funct_list, arg_list

    def live(self,world):

        actions_list, args_list = self.plan(world, self.percept_world(world))
        [funct(*args) for funct,args in zip(actions_list,args_list)]



    def move(self, direction, movement_rule):
        new_position = self.position + direction / np.linalg.norm(direction) * self.actions
        cost = movement_rule(self.position, new_position, self.mass)
        self.hp = np.max([self.hp - cost,0])
        self.position = new_position

    def eat(self, food):
        self.hp = np.min([self.hp+self.actions,self.hp + food.hp])
        food.hp = np.max([food.hp - self.actions,0])