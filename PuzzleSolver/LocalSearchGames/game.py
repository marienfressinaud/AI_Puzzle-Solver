# -*- coding: utf-8 -*-

from state_managers import StateManager
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

    def generate(self, level):
        """
        Generate a new game. Level determines how hard the game will be
        """

        if level == "easy":
            self.level = GameLevel.EASY
            self.max_steps = 100
        elif level == "medium":
            self.level = GameLevel.MEDIUM
            self.max_steps = 1000
        elif level == "hard":
            self.level = GameLevel.HARD
            self.max_steps = 200 # not too much to keep good performances
        else:
            assert(0)

        self.state_manager.build_new_game(self.level)

    def run(self):
        """
        Run the current game.
        It's just an execution of algorithms in the case of MinConflictsGame
        and SimulatedAnnealingGame classes
        """

        pass

    def is_optimal(self):
        """
        Return True if the current state is an optimal one, False else
        Must be implemented
        """

        return False

    def upstate(self, prev_var, new_var):
        """
        Update current state by assign prev_var to new_var
        Must be implemented
        """

        pass