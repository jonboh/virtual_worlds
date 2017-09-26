import pickle
import time

from agent import *
from rules import *
from universe import *


# UniverseWorker Class
def universe_worker_init():
    universe_worker = UniverseWorker(universe=universe_creation_random())
    return universe_worker


def test_universe_worker_init():
    UniverseWorker(universe=universe_creation_random())


def test_create_workers():
    universe_worker = UniverseWorker(universe=universe_creation_random())
    universe_worker.create_workers(1)


# def test_universe_worker_start_stop_trigger(): NOT WORKING
#     universe_worker = UniverseWorker(universe=universe_creation_random())
#     universe_worker.create_workers(3)
#     universe_worker.start()
#     universe_worker.stop_trigger = 1
#
#
# def test_universe_worker_start_stop_method(): NOT WORKING
#     universe_worker = UniverseWorker(universe=universe_creation_random())
#     universe_worker.create_workers(3)
#     universe_worker.start()
#     universe_worker.stop_workers()


def test_universe_worker_run():
    universe_worker = UniverseWorker(universe=universe_creation_random())
    universe_worker.create_workers(1)
    universe_worker.run()


# Universe Class
def universe_creation_random():
    np.random.seed(1)
    num_agents = 35
    num_foods = 200
    num_dims = 2
    np.random.seed(2)
    agents = [Agent(np.random.rand(1), np.random.rand(num_dims), np.random.rand(1) * 0.01)
              for _ in range(0, num_agents)]
    foods = [Matter(np.random.rand(1), np.random.rand(num_dims)) for _ in range(0, num_foods)]
    universe = Universe(agents, foods)
    return universe


def universe_creation_position3d():
    positions_ag = np.array([[1, 2, 1],
                             [5, 5, 1],
                             [5, 6, 1]])
    positions_fo = np.array([[1, 1, 1]])
    agents = [Agent(position=position, life=np.random.rand(1),
                    actions=np.random.rand(1))
              for position in positions_ag]
    foods = [Matter(position=position, life=np.random.rand(1))
             for position in positions_fo]
    universe = Universe(agents, foods)
    return universe


def universe_creation_position2d():
    positions_ag = np.array([[1, 2],
                             [5, 5],
                             [5, 6]])
    positions_fo = np.array([[1, 1]])
    agents = [Agent(position=position, life=np.random.rand(1),
                    actions=np.random.rand(1))
              for position in positions_ag]
    foods = [Matter(position=position, life=np.random.rand(1))
             for position in positions_fo]
    universe = Universe(agents, foods)
    return universe


def test_retrieve_info_is_pickleable():
    ref_point = [5, 4.5]
    reach_percept = 2
    universe = universe_creation_position2d()
    info_dict = universe.retrieve_info(np.array([ref_point]), reach_percept)

    pickle.dumps(info_dict)
