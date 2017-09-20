import numpy as np


class Matter:
    def __init__(self,life,position):
        self.energy = life
        self.mass = self.energy
        self.position = position


class Agent(Matter):
    def __init__(self, life, position, actions):
        super().__init__(life, position)
        self.hp = life
        self.actions = actions
        self.eat_actions = actions * 10
        self.perception_reach = self.actions * 50 # Might change in the future
        self.reach = self.actions * 0.05

    def percept_world(self, world):
        world_positions = world.retrieve_info(self.position, self.perception_reach)
        return world_positions # it returns a list with info of all objects in perception_reach

    def closest_logic(self,world): # This logic is a substitute for future NN implementations
        info_world = self.percept_world(world)
        if info_world.size == 0: # Nothing around, wonder randomly
            movement_path = np.random.randn(world.num_dim)
            movement_range = self.actions
            funct_list = [self.move]
            arg_list = [(movement_path, movement_range, world.physics.movement_cost)]
        else: # There's at least an object in perception_reach
            distances = np.linalg.norm(info_world[:, 0:world.num_dim] - self.position,axis=1,keepdims=True)
            min_distance_index = np.argmin(distances, axis=0)
            # EAT OR MOVE
            if distances[min_distance_index] < self.reach: # If it is reachable, eat it
                object_food = world.retrieve_obj_byid(info_world[min_distance_index,-1][0])
                funct_list = [self.eat]
                arg_list = [(object_food,)]
            else:
                closest_obj_position = info_world[min_distance_index,0:world.num_dim][0]
                movement_path = closest_obj_position - self.position
                movement_range = np.min([self.actions,np.linalg.norm(movement_path,keepdims=True)])
                funct_list = [self.move]
                arg_list = [(movement_path, movement_range, world.physics.movement_cost)]
        return funct_list, arg_list

    def plan(self,world):
        funct_list, arg_list = self.closest_logic(world)
        return funct_list, arg_list

    def live(self,world):
        actions_list, args_list = self.plan(world)
        [funct(*args) for funct,args in zip(actions_list,args_list)]

    # Agent Actions
    def move(self, direction, range, movement_rule):
        if np.linalg.norm(direction) == 0:
            new_position = self.position
        else:
            new_position = self.position + np.finfo('float64').eps + direction/4 / np.linalg.norm(direction) * range
        cost = movement_rule(self.position, new_position, self.mass)
        self.hp = np.max([self.hp - cost,0])
        self.position = new_position

    def eat(self, food):
        if type(food) is Agent:
            self.hp = np.max([self.hp - self.eat_actions, 0])
            food.hp = np.max([food.hp - self.eat_actions, 0])
        else:
            self.hp = np.min([self.hp+self.eat_actions,self.hp + food.energy])
            self.energy = np.min([self.energy+self.eat_actions,self.energy + food.energy])
            food.energy = np.max([food.energy - self.eat_actions,0])