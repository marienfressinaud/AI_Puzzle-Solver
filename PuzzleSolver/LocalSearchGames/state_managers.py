# -*- coding: utf-8 -*-

class StateManager(object):
    """
    A StateManager manages states of a game.
    It must be an abstract class and being implemented.
    """

    def __init__(self):
        self.exists = False

    def build_new_game(self):
        """
        Generates a new game.
        Other methods must not do anything if self.exists is False
        """

        self.exists = True

class KQueensManager(StateManager):
    """
    State manager for a K-Queens game
    """

    def __init__(self):
        super(KQueensManager, self).__init__()

class ColorGraphManager(StateManager):
    """
    State manager for a Color Graph game
    """

    def __init__(self):
        super(ColorGraphManager, self).__init__()
