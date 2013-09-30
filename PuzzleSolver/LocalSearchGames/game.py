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
        Generates a new game. Level determines how hard the game will be
        """

        self.max_steps = 10000
        if level == "easy":
            self.level = GameLevel.EASY
        elif level == "medium":
            self.level = GameLevel.MEDIUM
        elif level == "hard":
            self.level = GameLevel.HARD
            # not too much steps to keep good performances
            self.max_steps = 200
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