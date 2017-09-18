import pytest
import matplotlib.pyplot as plt
from universe import *


def test_creation():
    np.random.seed(1)
    universe = Universe(2,4,10)
    assert type(universe.agents) is list
    assert len(universe.agents) is 4
    assert len(universe.agents[1].position) is 2


def test_pass_time():
    np.random.seed(1)
    universe = Universe(2,4,10)  # 2 dimensions 4 agents
    fig = universe.plot_world()
    universe.pass_time()