# -*- coding: utf-8 -*-

from state_manager import StateManager
from game_levels import GameLevel
from constraints import queen_not_under_attack, Constraint


class KQueensManager(StateManager):
    """
    State manager for a K-Queens game
    """

    def __init__(self):
        super(KQueensManager, self).__init__()

        self.K = 0

    def build_new_game(self, level):
        if level == GameLevel.EASY:
            self.K = 4
        elif level == GameLevel.MEDIUM:
            self.K = 25
        else:
            self.K = 1000

        self.vars = {}
        for i in xrange(self.K):
            # Generation of the domain
            self.vars[i] = xrange(self.K)

        self.constraints = []
        for i in xrange(self.K):
            for j in xrange(i + 1, self.K):
                self.constraints.append(
                    Constraint(queen_not_under_attack, i, j))

    def __str__(self):
        """
        Returns a representation of the current state as a string
        """

        _str = ""

        _str = "-" * (4 * self.K) + "\n"
        for i in xrange(self.K):
            for j in xrange(self.K):
                if self.state[i] == j:
                    _str += " Q |"
                else:
                    _str += "   |"

            _str += "\n"
        _str += "-" * (4 * self.K)

        return _str
