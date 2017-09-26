import multiprocessing as mulp

from rules import *


class AgentWorker(mulp.Process):
    def __init__(self, pipe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipe = pipe
        self.stop_trigger = 0

    def run(self):
        while not self.stop_trigger:
            # Receive world_state. This is also the starting signal
            try:
                info = self.pipe.recv()
            except EOFError:
                continue
            actions = []  # this will be a list of tuples
            for state_list in info:
                world_state = state_list[0]
                agent_state = state_list[1]
                actions.append(plan(world_state, agent_state))
            self.pipe.send(actions)
        # Go back to the start and wait for a new world_state


def closest_logic(world_state, agent_state):  # This logic is a substitute for future NN implementations
    # Unpack the dictionaries
    agents = [world_state['agents'][i] for i in range(0,len(world_state['agents']))]
    agents_positions = [agents[i]['position'] for i in range(0,len(agents))]
    agents_positions = np.array(agents_positions).reshape(len(agents_positions), Rules.dim)
    foods = [world_state['foods'][i] for i in range(0, len(world_state['foods']))]
    foods_positions = [foods[i]['position'] for i in range(0,len(foods))]
    foods_positions = np.array(foods_positions).reshape(len(foods_positions), Rules.dim)
    agents_foods = agents + foods
    agents_foods_positions = np.concatenate([agents_positions, foods_positions],axis=0)

    # Logic
    if len(world_state['agents']) == 0 and len(world_state['foods']) == 0:  # Nothing around, wonder randomly
        movement_path = np.random.randn(Rules.dim)
        movement_range = agent_state['actions']
        fun_code = [1]
        arg_list = [(movement_path, movement_range)]
    else:  # There's at least an object in reach_perception
        distances = np.linalg.norm(agents_foods_positions - agent_state['position'], axis=1, keepdims=True)
        min_distance_index = np.argmin(distances, axis=0)
        # EAT OR MOVE
        if distances[min_distance_index] < agent_state['reach']:  # If it is reachable, eat it
            object_food_id = agents_foods[int(min_distance_index)]['id']
            fun_code = [2]
            arg_list = [(object_food_id,)]
        else:
            closest_obj_position = agents_foods_positions[min_distance_index]
            movement_path = closest_obj_position - agent_state['position']
            movement_range = np.min([agent_state['actions'], np.linalg.norm(movement_path, keepdims=True)])
            fun_code = [1]
            arg_list = [(movement_path, movement_range)]
    return fun_code, arg_list


def plan(world_state, agent_state):
    funct_list, arg_list = closest_logic(world_state, agent_state)
    return tuple([agent_state['id'], funct_list, arg_list])


class Matter:
    id = 0

    def __init__(self, life, position):
        self.id = Matter.id
        Matter.id = Matter.id + 1
        self.energy = life
        self.mass = self.energy
        self.position = position.reshape(1, len(position))


class Agent(Matter):
    def __init__(self, life, position, actions):
        super().__init__(life, position)
        # Attributes
        self.hp = life
        self.actions = actions
        self.actions_eat = actions * 10
        self.reach = self.actions * 0.05
        self.reach_perception = self.actions * 50  # Might change in the future

    def percept_world(self, world):
        world_positions = world.retrieve_info(self.position, self.reach_perception)
        return world_positions  # it returns a list with info of all objects in reach_perception

    # Agent Actions
    def move(self, direction, range_):
        if np.linalg.norm(direction) == 0:
            new_position = self.position
        else:
            new_position = self.position + np.finfo('float64').eps + direction / np.linalg.norm(direction) * range_
        cost = Rules.movement_cost(self.position, new_position, self.mass)
        self.hp = np.max([self.hp - cost, 0])
        self.position = new_position

    def eat(self, food):
        if type(food) is Agent:
            self.hp = np.max([self.hp - self.actions_eat, 0])
            food.hp = np.max([food.hp - self.actions_eat, 0])
        else:
            self.hp = np.min([self.hp+self.actions_eat, self.hp + food.energy])
            self.energy = np.min([self.energy+self.actions_eat, self.energy + food.energy])
            food.energy = np.max([food.energy - self.actions_eat, 0])
