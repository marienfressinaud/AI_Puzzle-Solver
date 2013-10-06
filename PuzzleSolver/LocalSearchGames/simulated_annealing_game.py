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
    EVAL_MAX = 1000.0

    def __init__(self):
        super(SimulatedAnnealingGame, self).__init__()

        self.t = SimulatedAnnealingGame.T_MAX

    def evaluate(self, state):
        """
        Evaluates a state (objective function)
        Min value is 1 and max value is EVAL_MAX
        """

        # The idea is to subtract the number of violated constraints (NVC) to a
        # fix value (EVAL_MAX). But since the NVC can be greater than EVAL_MAX
        # we must keep 0 <= NVC <= EVAL_MAX with a rule of three.
        # There is still a problem: the number of total constraints is not
        # perfect because a constraint can modify the count with a coeff (see
        # Magic Square game with SumEqualsConstraint).
        # So here we increase this number by a coeff of 1000. It works fine
        # for this exercise but this solution is far from perfect.
        total_constraints = len(self.state_manager.constraints) * 1000
        nb_constraints = self.state_manager.count_constraint_violated(state)
        _max = SimulatedAnnealingGame.EVAL_MAX

        _eval = _max - (nb_constraints * _max) / total_constraints

        return max(1, _eval)

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
