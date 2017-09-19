import pytest
from unittest import mock
import matplotlib.pyplot as plt
import numpy as np
from universe import *
from rules import *


def default_universe_creation():
    np.random.seed(1)
    num_agents = 7
    num_foods = 25
    num_dims = 2
    np.random.seed(2)
    rules = Rules
    agents = [Agent(np.random.rand(1), np.random.rand(num_dims), np.random.rand(1) * 0.01)
              for i in range(0, num_agents)]
    foods = [Matter(np.random.rand(1), np.random.rand(num_foods)) for i in range(0, num_foods)]
    universe = Universe(num_dims, rules, agents, foods)
    return universe


def test_retrieve_info():
    position = [5,6]
    reach = 2
    agents_positions_hp = np.array([[1,2,1],
                                 [5,5,1],
                                 [5,6,1]])
    food_positions_hp = np.array([[1,1,1]])
    universe = default_universe_creation()
    universe.agent_positions_hp = agents_positions_hp
    universe.food_positions_hp = food_positions_hp
    info_array = universe.retrieve_info(np.array([position]),reach)

    assert np.all(info_array==np.array([[5,5,1],[5,6,1]]))
