import numpy as np


class Rules:
    # Dimensionality
    dim = 2

    # Energy Requirement for movement
    @staticmethod
    def movement_cost(position, new_position, mass):
        energy_cost = np.linalg.norm(position-new_position)*mass*0.25
        return energy_cost

    @staticmethod
    def computation_cost(time):  # operations or time
        """Penalize excessive computation by agents"""
        computation_cost = time
        return computation_cost
