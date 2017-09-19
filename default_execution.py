import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from universe import *
from rules import *
from threading import Thread
from time import sleep
import tkinter as tk


class universe_window:
    def __init__(self,parent,universe,plot_frecuency):
        self.plot_frecuency = plot_frecuency
        #
        self.universe = universe
        uni_fig = plt.figure()
        self.ax = uni_fig.add_subplot(111)

        # Config window
        self.parent = parent
        self.parent.geometry("1024x800")
        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)
        main_frame = tk.Frame(self.parent)
        main_frame.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        tk.Grid.rowconfigure(main_frame, 0, weight=1)
        for i in range(0,3):tk.Grid.columnconfigure(main_frame,i,weight=1)

        # Frame for the window = matplotlib figure
        frame_window = tk.Frame(main_frame)
        frame_window.grid(row=0,column=0,columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.universe_canvas = FigureCanvasTkAgg(uni_fig, frame_window)
        self.universe_canvas.get_tk_widget().grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)

        # Frame for the info and the button of time
        frame_info_time = tk.Frame(main_frame)
        frame_info_time.grid(row=0,column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        # time_button = tk.Button(frame_info_time, text='Pass time', command=universe.pass_time)
        # time_button.grid(row=0,column=0,sticky=tk.N)
        self.label_t = tk.Label(frame_info_time,text='t = 0')
        self.label_t.grid(row=0,column=1,sticky=tk.W+tk.N)

        last_loop_thread = Thread(target=self.last_loop,name='Last Loop')
        last_loop_thread.start()

    def last_loop(self):
        while True:
            if universe.t % self.plot_frecuency == 0:
                self.update_window()
            else:
                self.update_universe()

    def update_window(self):
        self.ax.clear()
        self.ax.set_xlim([-2,2])
        self.ax.set_ylim([-2,2])
        agent_collection = universe.agent_charact
        food_collection = universe.food_charact
        self.ax.scatter(agent_collection[:,0],agent_collection[:,1],s=agent_collection[:,2]*10,
                        color='blue')
        for agent_charact in agent_collection:
            self.ax.annotate(agent_charact[-1],(agent_charact[0],agent_charact[1]))
        self.ax.scatter(food_collection[:, 0], food_collection[:, 1], s=food_collection[:, 2]*10,
                        color='red')
        self.universe_canvas.draw()
        self.update_universe()

    def update_universe(self):
        universe.pass_time()
        self.label_t.configure(text='t = ' + str(universe.t))


if __name__ == '__main__':
    plot_frecuency = 5

    num_agents = 50
    num_foods = 100
    num_dims = 2
    np.random.seed(2)
    rules = Rules
    agents = [Agent(np.random.rand(1),np.random.randn(num_dims),np.random.rand(1)*0.1)
              for i in range(0,num_agents)]
    foods = [Matter(np.random.rand(1),np.random.rand(num_foods)) for i in range(0,num_foods)]
    universe = Universe(num_dims, rules, agents, foods)

    root = tk.Tk()
    visualizer = universe_window(root, universe, plot_frecuency)
    root.mainloop()