import tkinter as tk
import multiprocessing as mulp
from threading import Thread
import time

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from universe import UniverseWorker, Universe
from agent import Matter, Agent, random_foods, random_agents


class UniverseWindow:
    def __init__(self, parent, universe, plot_frecuency=5, field_value=2):
        self.plot_frecuency = plot_frecuency
        self.bool_window = True
        self.field_value = field_value
        self.new_agents = []
        self.new_foods = []
        # Window Configuration
        self.config_window(parent)
        #
        self.universe = universe
        self.universe_worker = UniverseWorker(universe, process_count)
        self.universe_worker.create_workers()
        self.universe_worker.start_workers()

        # Updater
        last_loop_thread = Thread(target=self.last_loop, name='Last Loop')
        last_loop_thread.start()

    def config_window(self, parent):
        # Config window
        self.parent = parent
        self.parent.geometry("1024x800")
        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)
        main_frame = tk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Grid.rowconfigure(main_frame, 0, weight=1)
        for i in range(0, 3):
            tk.Grid.columnconfigure(main_frame, i, weight=1)

        # Frame for the window = matplotlib figure
        uni_fig = plt.figure()
        self.ax = uni_fig.add_subplot(111)
        frame_window = tk.Frame(main_frame)
        frame_window.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.universe_canvas = FigureCanvasTkAgg(uni_fig, frame_window)
        self.universe_canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Frame for the info and the buttons
        frame_info_time = tk.Frame(main_frame)
        frame_info_time.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.label_t = tk.Label(frame_info_time, text='t = 0')
        self.label_t.grid(row=0, column=1, sticky=tk.W + tk.N)
        # ON/OFF Plot
        plot_button = tk.Button(frame_info_time, text='ON/OFF Plot', command=self.set_visualization)
        plot_button.grid(row=1, column=0, sticky=tk.N)
        # Plot Limits
        field_button = tk.Button(frame_info_time, text='Change Plot Lim', command=self.set_field)
        field_button.grid(row=2, column=0, sticky=tk.N + tk.W)
        self.field_entry_var = tk.StringVar()
        self.field_entry_var.set(str(self.field_value))
        self.field_entry = tk.Entry(frame_info_time, textvariable=self.field_entry_var)
        self.field_entry.grid(row=2, column=1, sticky=tk.N + tk.W)
        # Introduce new food
        food_button = tk.Button(frame_info_time, text='Add Foods', command=self.add_new_foods)
        food_button.grid(row=3, column=0, sticky=tk.N + tk.W)
        self.food_entry_var = tk.StringVar()
        self.food_entry_var.set(str(0))
        self.food_entry = tk.Entry(frame_info_time, textvariable=self.food_entry_var)
        self.food_entry.grid(row=3, column=1, sticky=tk.N + tk.W)
        # Introduce new agents
        agents_button = tk.Button(frame_info_time, text='Add Agents', command=self.add_new_agents)
        agents_button.grid(row=4, column=0, sticky=tk.N + tk.W)
        self.agents_entry_var = tk.StringVar()
        self.agents_entry_var.set(str(0))
        self.agents_entry = tk.Entry(frame_info_time, textvariable=self.agents_entry_var)
        self.agents_entry.grid(row=4, column=1, sticky=tk.N + tk.W)

    def last_loop(self):
        while True:
            if self.universe.t % self.plot_frecuency == 0:
                self.update_window()
            else:
                self.update_universe()

    def add_new_foods(self):
        try:
            entry = int(self.food_entry_var.get())
            self.new_foods = self.new_foods + random_foods(entry, self.field_value)
            self.food_entry_var.set('0')
        except ValueError:
            pass

    def add_new_agents(self):
        try:
            entry = int(self.agents_entry_var.get())
            self.new_agents = self.new_agents + random_agents(entry, self.field_value)
            self.agents_entry_var.set('0')
        except ValueError:
            pass

    def set_field(self):
        try:
            entry = int(self.field_entry_var.get())
            self.field_value = entry
        except ValueError:
            pass
        self.field_entry_var.set(str(self.field_value))

    def set_visualization(self):
        self.bool_window = not self.bool_window

    def update_window(self):
        if self.bool_window:
            self.ax.clear()
            self.ax.set_xlim([-self.field_value, self.field_value])
            self.ax.set_ylim([-self.field_value, self.field_value])
            agent_collection = unpack_matter_position_size(self.universe.agents)
            food_collection = unpack_matter_position_size(self.universe.foods)
            self.ax.scatter(agent_collection[:, 0], agent_collection[:, 1], s=agent_collection[:, 2]*10,
                            color='blue')
            for agent_charact in agent_collection:
                self.ax.annotate(agent_charact[-1], (agent_charact[0], agent_charact[1]))
            self.ax.scatter(food_collection[:, 0], food_collection[:, 1], s=food_collection[:, 2]*10,
                            color='red')
            self.universe_canvas.draw()
        self.update_universe()

    def update_universe(self):
        if len(self.new_agents)> 0 or len(self.new_foods) > 0:
            while self.universe_worker.computing == 1:
                time.sleep(0.1)
            self.universe.update_state([],self.new_agents,self.new_foods)
        self.universe_worker.run()
        self.label_t.configure(text='t = ' + str(self.universe.t))


def unpack_matter_position_size(matters):
    position_size = []
    if len(matters) > 0:
        if type(matters[0]) is Matter:
            for element in matters:
                position_size = position_size + [element.position, np.array(element.energy).reshape(1,1),
                                                 np.array(element.id).reshape(1,1)]
        if type(matters[0]) is Agent:
            for element in matters:
                position_size = position_size + [element.position, np.array(element.hp).reshape(1,1),
                                                 np.array(element.id).reshape(1,1)]
        position_size = np.concatenate(position_size,axis=1).reshape(len(matters),matters[0].position.size+2)
    return position_size


if __name__ == '__main__':
    plt_frecuency = 100
    fld_value = 5
    process_count = 7
    #
    num_agents = 14
    num_foods = 200
    num_dims = 2
    np.random.seed(2)

    agents = random_agents(num_agents,fld_value)
    foods = random_foods(num_foods,fld_value)
    univer = Universe(agents, foods)

    root = tk.Tk()
    visualizer = UniverseWindow(root, univer, plt_frecuency, fld_value*3)
    root.mainloop()
