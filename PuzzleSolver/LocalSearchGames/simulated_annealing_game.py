# -*- coding: utf-8 -*-

from time import time
from math import exp
from random import random, choice

from game import Game


class SimulatedAnnealingGame(Game):
    """
    A SimulatedAnnealingGame must implement simulated annealing algorithm.
    Basic algorithm consists to evaluate neighboring states based on a certain
    "temperature" which determine how we should explore or exploite the game
    """

    T_MAX = 10.0  # TODO I choose this value randomly, but it seems good
    N_GENERATION = 10
    EVAL_MAX = 500.0

    def __init__(self):
        super(SimulatedAnnealingGame, self).__init__()

        self.t = SimulatedAnnealingGame.T_MAX

    def evaluate(self, state):
        """
        Evaluates a state (objective function)
        Min value is 1 and max value is SimulatedAnnealingGame.EVAL_MAX
        """

        _eval = (SimulatedAnnealingGame.EVAL_MAX -
                self.state_manager.count_constraint_violated(state))

        return max(1, _eval)

    def __get_best_state(self, neighbors):
        state_max = None
        eval_state_max = 0.0

        for new_state in neighbors:
            _eval = self.evaluate(new_state)

            if _eval > eval_state_max:
                state_max = new_state
                eval_state_max = _eval

        return (state_max, eval_state_max)

    def lower_temperature(self):
        """
        A simple function to decrease self.t value
        """

        self.t = max(0.00001, self.t * 0.5)

    def run(self):
        """
        Runs simulated annealing algorithm
        """

        self.show_state_manager()
        self.date_begin = time()

        eval_state = self.evaluate(self.state_manager.state)
        self.number_steps = 0

        # while not F(P) ≥ F_target
        while not self.is_terminated():
            self.number_steps += 1

            neighbors = self.state_manager.generate_random_states(
                SimulatedAnnealingGame.N_GENERATION)
            (state_max, eval_state_max) = self.__get_best_state(neighbors)

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

        self.show_state_manager()
