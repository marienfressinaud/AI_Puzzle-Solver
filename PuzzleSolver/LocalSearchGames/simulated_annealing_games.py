# -*- coding: utf-8 -*-

from game import Game
from state_managers import KQueensManager, ColorGraphManager

class SimulatedAnnealingGame(Game):
    """
    A SimulatedAnnealingGame must implement simulated annealing algorithm.
    A basic algorithm consists to evaluate neighboring states based on a certain
    "temperature" which determine how we should explore or exploite the game
    """

    def __init__(self):
        super(SimulatedAnnealingGame, self).__init__()

class KQueensSA(SimulatedAnnealingGame):
    """
    K-Queens game based on simulated annealing algorithm
    """

    def __init__(self):
        super(KQueensSA, self).__init__()

        self.state_manager = KQueensManager()

class GraphColorSA(SimulatedAnnealingGame):
    """
    Graph color game based on simulated annealing algorithm
    """

    def __init__(self):
        super(GraphColorSA, self).__init__()

        self.state_manager = ColorGraphManager()
