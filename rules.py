import numpy as np

class Rules:
    @staticmethod
    def movement_cost(position, new_position, mass):
        energy_cost = np.linalg.norm(position-new_position)*mass*0.1
        return energy_cost