# -*- coding: utf-8 -*-

from time import time

from state_manager import StateManager
from game_levels import GameLevel


class Game(object):
    """
    A Game is a general abstraction for local search based games
    Known children are MinConflictsGame and SimulatedAnnealingGame
    These children should be also abstract
    """

    def __init__(self):
        self.state_manager = StateManager()
        self.level = None
        self.max_steps = 0
        self.number_steps = 0
        self.max_time = 120
        self.date_begin = 0
        self.verbose = False

    def generate(self, level):
        """
        Generates a new game. Level determines how hard the game will be
        """

        levels = {
            "easy": GameLevel.EASY,
            "medium": GameLevel.MEDIUM,
            "hard": GameLevel.HARD
        }

        assert(level in levels)

        self.level = levels[level]
        self.max_steps = 10000
        self.state_manager.build_new_game(self.level)
        self.state_manager.indexing_constraints()
        self.state_manager.generate_game()

    def run(self):
        """
        Runs the current game.
        It's just an execution of algorithms in the case of MinConflictsGame
        and SimulatedAnnealingGame classes
        """

        pass

    def is_terminated(self):
        """
        Returns True if the current state is an optimal one, False else
        """

        return self.state_manager.is_optimal() or \
            self.outofsteps() or self.outoftime()

    def outofsteps(self):
        return self.number_steps >= self.max_steps

    def outoftime(self):
        return self.date_begin > 0 and \
            time() > (self.date_begin + self.max_time)

    def show_state_manager(self):
        if self.verbose:
            print self.state_manager
