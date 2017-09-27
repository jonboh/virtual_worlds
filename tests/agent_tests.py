from agent import *
from rules import *


def test_move():
    original_life = 4
    actions = 2

    position = [1, 2]
    direction = [1, 1]
    range_ = 2
    new_position = [position[0]+np.sqrt(2), position[1]+np.sqrt(2)]

    agent_ = Agent(original_life, np.array(position), actions)
    agent_.move(np.array(direction), range_)

    assert np.all(agent_.position == np.array(new_position))
    assert agent_.hp < original_life


def test_move_death():
    original_life = 1
    actions = 100

    position = [1, 2]
    direction = [1, 1]
    range_ = 100

    agent_ = Agent(original_life, np.array(position), actions)
    agent_.move(np.array(direction), range_)
    assert agent_.hp == 0


def test_eat_bigfood():  # food.hp is greater than agent action points
    food_energy = 10
    agent_hp = 10
    ac_points = 1
    food = Matter(food_energy, np.array([1, 2]))
    agent_ = Agent(agent_hp, np.array([1, 2]), ac_points)
    agent_.eat(food)
    assert agent_.hp == agent_hp + agent_.actions_eat
    assert food.energy == food_energy - agent_.actions_eat


def test_eat_smallfood():  # food.hp is less than agent action points
    food_energy = 3
    agent_hp = 10
    ac_points = 5
    food = Matter(food_energy, np.array([1, 2]))
    agent_ = Agent(agent_hp, np.array([1, 2]), ac_points)
    agent_.eat(food)
    assert agent_.hp == agent_hp + food_energy
    assert food.energy == 0
