import multiprocessing as mulp

from rules import *
import agent


class UniverseWorker(mulp.Process):
    def __init__(self, universe, amount_workers, *args, **kwargs):
        super().__init__(*args, **kwargs, name='Universe Worker')
        self.universe = universe
        self.computing = 0
        self.amount_workers = amount_workers
        self.workers = []
        self.pipes = []

    def create_workers(self):
        for i in range(0, self.amount_workers):
            parent_pipe, child_pipe = mulp.Pipe()
            self.pipes.append(parent_pipe)
            worker = agent.AgentWorker(pipe=child_pipe, name='AgentWorker_'+str(i))
            self.workers.append(worker)

    def start_workers(self):
        for worker in self.workers:
            worker.start()

    def stop_workers(self):
        for worker in self.workers:
            worker.terminate()  # dirty job...

    def assign_agents_pipes(self):
        pipe_agents = [list() for _ in self.pipes]
        ind = 0
        for i in range(0, len(self.universe.agents)):
            pipe_agents[ind].append(self.universe.agents[i])
            ind += 1
            if ind >= len(self.workers):
                ind = 0
        return pipe_agents

    def run(self):
        self.computing = 1
        # Assign agents to pipes
        pipe_agents = self.assign_agents_pipes()
        # Send info to workers
        for pipe, agents in zip(self.pipes, pipe_agents):
            info = []
            for agent_ in agents:
                info.append(tuple([agent_.percept_world(self.universe), agent_.__dict__]))
            pipe.send(info)

        # Receive info from workers
        action_package = []
        for pipe in self.pipes:
            action_package = action_package + pipe.recv()  # concatenate

        # Compute new world state with actions from the agents
        self.universe.update_state(action_package)
        self.computing = 0


class Universe:
    def __init__(self, agents, foods):
        self.t = 0
        self.agents = agents
        self.foods = foods

    def retrieve_info(self, position, radius):
        info_dict = dict.fromkeys(self.__dict__.keys())
        for entry in info_dict:
            if type(self.__dict__[entry]) is list:
                info_dict.update({entry: []})

        for entry in self.__dict__:
            if type(self.__dict__[entry]) is list:
                for element in self.__dict__[entry]:
                    if hasattr(element, 'position'):
                        norm = np.linalg.norm(element.position - position, axis=1, keepdims=True)
                        if 0 < norm < radius:
                            info_dict[entry].append(element.__dict__)
            elif isinstance(self.__dict__[entry], (int, float, complex)):
                info_dict[entry] = self.__dict__[entry]

        return info_dict  # it returns a dict with all info objects in radius

    def retrieve_byid(self, id_):
        for agent_ in self.agents:
            if agent_.id == id_:
                return agent_
        for food_ in self.foods:
            if food_.id == id_:
                return food_

    def update_state(self, action_package, new_agents=None, new_foods=None):
        self.t = self.t + 1
        new_agents = [] if new_agents is None else new_agents
        new_foods = [] if new_foods is None else new_foods
        self.agents = self.agents + new_agents
        self.foods = self.foods + new_foods
        # fun_codes -> List of all action to be done in this "turn":
        # 0-> Nothing
        # 1-> Move
        # 2-> Eat
        for actions in action_package:
            agent_id = actions[0]
            fun_code = actions[1]
            arguments = actions[2]
            agent_ = self.retrieve_byid(agent_id)
            for action, arg in zip(fun_code, arguments):
                if action == 0:
                    pass
                elif action == 1:  # move
                    agent_.move(*arg)
                elif action == 2:  # eat
                    food = self.retrieve_byid(arg[0])
                    agent_.eat(food)
