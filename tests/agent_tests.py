import pytest
from agent import *
from universe import *
from rules import *


def test_move():
    original_life = 4
    actions = 2

    position = [1,2]
    direction = [1,1]
    range = 2
    new_position = [position[0]+np.sqrt(2),position[1]+np.sqrt(2)]

    agent = Agent(original_life,np.array(position),actions)
    agent.move(np.array(direction),range)

    assert np.all(agent.position == np.array(new_position))
    assert agent.hp < original_life


def test_move_death():
    original_life = 1
    actions = 100

    position = [1,2]
    direction = [1,1]
    range = 100

    agent = Agent(original_life,np.array(position),actions)
    agent.move(np.array(direction),range)
    assert agent.hp ==0


def test_eat_bigfood(): # food.hp is greater than agent action points
    food_energy = 10
    agent_hp = 10
    ac_points = 1
    food = Matter(food_energy,np.array([1,2]))
    agent = Agent(agent_hp,np.array([1,2]),ac_points)
    agent.eat(food)
    assert agent.hp == agent_hp + agent.actions_eat
    assert food.energy == food_energy - agent.actions_eat


def test_eat_smallfood(): # food.hp is less than agent action points
    food_energy = 3
    agent_hp = 10
    ac_points = 5
    food = Matter(food_energy, np.array([1, 2]))
    agent = Agent(agent_hp, np.array([1, 2]), ac_points)
    agent.eat(food)
    assert agent.hp == agent_hp + food_energy
    assert food.energy == 0
