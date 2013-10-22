# -*- coding: utf-8 -*-

from LocalSearchGames.min_conflicts_game import MinConflictsGame
from LocalSearchGames.simulated_annealing_game import SimulatedAnnealingGame
from LocalSearchGames.state_manager import StateManager
from LocalSearchGames.game_levels import GameLevel
from LocalSearchGames.constraints import SumEqualsConstraint
# from LocalSearchGames.constraints import MustBeDifferentConstraint


class MagicSquareManager(StateManager):
    """
    State manager for a Magic Square game
    """

    def __init__(self):
        super(MagicSquareManager, self).__init__()

        self.N = 0
        self.sum = 0

    def __set_constraints(self):
        self.constraints = []

        # All numbers must be differents
        # it works... once for ten
        # self.constraints.append(
        #     MustBeDifferentConstraint(xrange(self.N * self.N))
        # )

        # Diagonals constraints
        list_diag1 = [(i*self.N + i) for i in xrange(self.N)]
        list_diag2 = [((self.N-1) * (self.N-i)) for i in xrange(self.N)]
        self.constraints.append(
            SumEqualsConstraint(self.sum, list_diag1))
        self.constraints.append(
            SumEqualsConstraint(self.sum, list_diag2))

        # Rows and columns constraints
        for var_id in xrange(self.N):
            list_row = [(var_id*self.N + i) for i in xrange(self.N)]
            list_col = [(var_id + self.N*i) for i in xrange(self.N)]

            self.constraints.append(
                SumEqualsConstraint(self.sum, list_row))
            self.constraints.append(
                SumEqualsConstraint(self.sum, list_col))

    def build_new_game(self, level):
        if level == GameLevel.EASY:
            self.N = 3
        elif level == GameLevel.MEDIUM:
            self.N = 8
        else:
            self.N = 24

        self.sum = (self.N * (self.N**2 + 1)) / 2

        domain = xrange(1, self.N*self.N + 1)
        self.vars = {i: domain for i in xrange(self.N * self.N)}

        self.__set_constraints()

    def __str__(self):
        """
        Returns a representation of the current state as a string
        """

        _str = "SUM = %d\n" % self.sum
        _str += "-" * (6 * self.N) + "\n"
        for i in xrange(self.N):
            for j in xrange(self.N):
                _str += " %3d |" % self.state[i*self.N + j]

            _str += "\n"
        _str += "-" * (6 * self.N)

        return _str


class MagicSquareMC(MinConflictsGame):
    """
    Magic Square game based on min conflicts algorithm
    """

    def __init__(self):
        super(MagicSquareMC, self).__init__()

        self.state_manager = MagicSquareManager()


class MagicSquareSA(SimulatedAnnealingGame):
    """
    Magic Square game based on simulated annealing algorithm
    """

    def __init__(self):
        super(MagicSquareSA, self).__init__()

        self.state_manager = MagicSquareManager()
