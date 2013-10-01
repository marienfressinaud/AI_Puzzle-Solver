# -*- coding: utf-8 -*-

from math import exp
from random import random, choice

from game import Game
from state_managers import KQueensManager, ColorGraphManager
from graph_output import draw_graph

class SimulatedAnnealingGame(Game):
    """
    A SimulatedAnnealingGame must implement simulated annealing algorithm.
    A basic algorithm consists to evaluate neighboring states based on a certain
    "temperature" which determine how we should explore or exploite the game
    """

    T_MAX = 10.0 # TODO I choose this value randomly, but it seems good
    N_GENERATION = 10
    EVAL_MAX = 500.0

    def __init__(self):
        super(SimulatedAnnealingGame, self).__init__()

        self.t = SimulatedAnnealingGame.T_MAX

    def evaluate(self, state=None):
        """
        Evaluates a state (objective function)
        Min value is 0 and max value is SimulatedAnnealingGame.EVAL_MAX
        """

        if state is not None:
            state_begin = self.state_manager.inv_state(state)
            self.state_manager.upstate(state)

        _eval = SimulatedAnnealingGame.EVAL_MAX

        for v in self.state_manager.vars:
            _eval -= self.state_manager.count_constraint_violated(v)

        if state is not None:
            assert(state_begin is not None)
            self.state_manager.upstate(state_begin)

        return max(0, _eval)

    def lower_temperature(self):
        """
        A simple function to decrease self.t value
        """

        self.t = max(0.00001, self.t * 0.5)

    def run(self):
        """
        Runs simulated annealing algorithm
        """

        eval_state = self.evaluate()
        self.number_steps = 0

        # while not F(P) ≥ F_target
        while not self.is_terminated():
            self.number_steps += 1

            neighbors = self.state_manager.generate_random_states(
                SimulatedAnnealingGame.N_GENERATION)
            state_max = None
            eval_state_max = 0.0
            for new_state in neighbors:
                _eval = self.evaluate(new_state)

                if _eval > eval_state_max:
                    state_max = new_state
                    eval_state_max = _eval

            q = (eval_state_max - eval_state) / eval_state
            try:
                p = min(1, exp(-q / self.t))
            except OverflowError:
                # TODO not really good but it works ;)
                p = 1

            x = random()

            if x > p:
                self.state_manager.upstate(state_max)
            else:
                self.state_manager.upstate(choice(neighbors))

            self.lower_temperature()

class KQueensSA(SimulatedAnnealingGame):
    """
    K-Queens game based on simulated annealing algorithm
    """

    def __init__(self):
        super(KQueensSA, self).__init__()

        self.state_manager = KQueensManager()

    def run(self):
        print self.state_manager

        super(KQueensSA, self).run()

        print self.state_manager

class GraphColorSA(SimulatedAnnealingGame):
    """
    Graph color game based on simulated annealing algorithm
    """

    def __init__(self):
        super(GraphColorSA, self).__init__()

        self.state_manager = ColorGraphManager()

    def run(self):
        draw_graph(self.state_manager, "graph_start.dot")

        super(GraphColorSA, self).run()

        draw_graph(self.state_manager, "graph_end.dot")
