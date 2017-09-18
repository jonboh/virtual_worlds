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

    def percept_world(self, world):
        world_percepted = world
        return world_percepted

    def plan(self,world):
        pass

    def live(self,world):
        percepted_world = self.percept_world(world)
        self.plan(percepted_world)

        movement_behaviour = np.random.randn(world.num_dim) * self.actions
        self.move(self.position+movement_behaviour, world.physics.movement_cost)

    def move(self, new_position, movement_rule):
        cost = movement_rule(self.position, new_position, self.mass)
        self.hp = max([self.hp - cost,0])
        self.position = new_position

    def eat(self, food):

        self.hp = self.hp + food.hp
        food.hp = food.hp - self.actions