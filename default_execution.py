import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from universe import *
from threading import Thread
from time import sleep
import tkinter as tk


class universe_window:
    def __init__(self,parent,universe):
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
            if universe.t % 50 == 0:
                self.update_window()
            else:
                self.update_universe()

    def update_window(self):
        self.ax.clear()
        self.ax.set_xlim([0,1])
        self.ax.set_ylim([0,1])
        agent_collection, food_collection = universe.gen_collections()
        self.ax.scatter(agent_collection[:,0],agent_collection[:,1],s=agent_collection[:,2]*10,
                        color='blue')
        self.ax.scatter(food_collection[:, 0], food_collection[:, 1], s=food_collection[:, 2]*10,
                        color='red')
        self.universe_canvas.draw()
        self.update_universe()

    def update_universe(self):
        universe.pass_time()
        self.label_t.configure(text='t = ' + str(universe.t))



if __name__ == '__main__':
    num_agents = 7
    num_foods = 25
    num_dims = 2

    np.random.seed(1)
    universe = Universe(num_dims, num_agents, num_foods)

    root = tk.Tk()
    visualizer = universe_window(root, universe)
    root.mainloop()