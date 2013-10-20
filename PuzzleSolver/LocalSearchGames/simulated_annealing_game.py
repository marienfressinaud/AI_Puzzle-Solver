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

    T_MAX = 10.0
    N_GENERATION = 15

    def __init__(self):
        super(SimulatedAnnealingGame, self).__init__()

        self.t = SimulatedAnnealingGame.T_MAX

    def __get_best_state(self, neighbors):
        """
        Get the neighbor state with the higher evaluation
        Returns a tuple with the state and its evalutation
        """

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

        # t should not be 0 since we divide q with this value later
        self.t = max(0.00001, self.t * 0.75)

    def run(self):
        """
        Runs simulated annealing algorithm
        """

        self.show_state_manager()
        self.date_begin = time()

        # We evaluate the current state
        eval_state = self.evaluate(self.state_manager.state)

        self.number_steps = 0
        while not self.is_terminated():
            self.number_steps += 1

            # We generate N neighbors and calculate the better one
            neighbors = self.state_manager.generate_random_states(
                SimulatedAnnealingGame.N_GENERATION)
            (state_max, eval_state_max) = self.__get_best_state(neighbors)

            # Calculation of p
            # As the temperature will decrease, p will do the same
            q = (eval_state_max - eval_state) / eval_state
            try:
                p = min(1, exp(-q / self.t))
            except OverflowError:
                # Easy way to correct OverflowError
                # In this case, we choose a random neighbors
                p = 1

            # If x (for x in [0,1]) is greater than p, we keep the better
            # neighbors (exploiting), else we get a random neighbor (exploring)
            x = random()
            if x > p:
                self.state_manager.upstate(state_max)
            else:
                self.state_manager.upstate(choice(neighbors))

            # And we decrease the temperature
            self.lower_temperature()

        self.show_state_manager()
