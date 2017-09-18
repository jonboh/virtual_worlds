import pytest
from universe import *

def test_move():
    original_life = 2
    position = [1,2]
    new_position = [1,1]

    agent = Agent(original_life,np.array(position))

    agent.move(np.array(new_position),Rules.movement_cost)

    assert np.all(agent.position == np.array(new_position))
    assert agent.hp < original_life

def test_eat():
    pass