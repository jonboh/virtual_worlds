import multiprocessing as mulp
import time

from rules import *
import agent


class UniverseWorker(mulp.Process):
    def __init__(self, universe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Universe Worker'
        self.stop_trigger = 0
        self.universe = universe
        self.workers = []
        self.pipes = []

    def create_workers(self, amount_workers):
        for i in range(0, amount_workers):
            parent_pipe, child_pipe = mulp.Pipe()
            self.pipes.append(parent_pipe)
            worker = agent.AgentWorker(pipe=child_pipe, name='AgentWorker_'+str(i))
            self.workers.append(worker)

    def start_workers(self):
        for worker in self.workers:
            worker.start()

    def stop_workers(self):
        for worker in self.workers:
            worker.stop_trigger = 1


    def assign_agents_pipes(self):
        pipe_agents = [list() for _ in self.pipes]
        ind = 0
        for i in range(0, len(self.universe.agents)):
            pipe_agents[ind].append(self.universe.agents[i])
            ind+=1
            if ind>=len(self.workers):
                ind = 0
        return pipe_agents

    def run(self):
        self.start_workers()
        while not self.stop_trigger:

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
        self.stop_workers()


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

    def update_state(self, action_package):
        self.t = self.t + 1
        if self.t % 100 == 0:
            print(self.t)
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
