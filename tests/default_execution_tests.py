from agent import Matter, Agent, random_foods, random_agents
from universe import Universe
import default_execution as de


def test_unpack_matter_position_size():
    agents = random_agents(5)
    foods = random_foods(5)
    de.unpack_matter_position_size(agents)
    de.unpack_matter_position_size(foods)
