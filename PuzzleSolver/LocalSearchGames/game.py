# -*- coding: utf-8 -*-

class Game(object):
    """
    A Game is a general abstraction for local search based games
    Known children are MinConflictsGame and SimulatedAnnealingGame
    These children should be also abstract
    """

    def __init__(self):
        self.state_manager = None
        self.level = None

    def generate(self, level):
        """
        Generate a new game. Level determines how hard the game will be
        """

        pass

    def run(self):
        """
        Run the current game.
        It's just an execution of algorithms in the case of MinConflictsGame
        and SimulatedAnnealingGame classes
        """

        pass
