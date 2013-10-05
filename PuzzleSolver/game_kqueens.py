# -*- coding: utf-8 -*-

from LocalSearchGames.min_conflicts_game import MinConflictsGame
from LocalSearchGames.simulated_annealing_game import SimulatedAnnealingGame
from LocalSearchGames.state_manager import StateManager
from LocalSearchGames.game_levels import GameLevel
from LocalSearchGames.constraints import Constraint


def queen_not_under_attack(state, var1, var2):
    queen_i = (var1, state[var1])
    queen_j = (var2, state[var2])

    return queen_j[1] not in (
        queen_i[1],
        queen_i[1] + abs(queen_i[0] - queen_j[0]),
        queen_i[1] - abs(queen_i[0] - queen_j[0])
    )


class KQueensManager(StateManager):
    """
    State manager for a K-Queens game
    """

    def __init__(self):
        super(KQueensManager, self).__init__()

        self.K = 0

    def __set_constraints(self):
        self.constraints = []
        for i in xrange(self.K):
            for j in xrange(self.K):
                if i != j:
                    self.constraints.append(
                        Constraint(queen_not_under_attack, i, j)
                    )

    def build_new_game(self, level):
        if level == GameLevel.EASY:
            self.K = 8
        elif level == GameLevel.MEDIUM:
            self.K = 25
        else:
            self.K = 1000

        self.vars = {}
        for i in xrange(self.K):
            # Generation of the domain
            self.vars[i] = xrange(self.K)

        self.__set_constraints()

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


class KQueensMC(MinConflictsGame):
    """
    K-Queens game based on min conflicts algorithm
    """

    def __init__(self):
        super(KQueensMC, self).__init__()

        self.state_manager = KQueensManager()


class KQueensSA(SimulatedAnnealingGame):
    """
    K-Queens game based on simulated annealing algorithm
    """

    def __init__(self):
        super(KQueensSA, self).__init__()

        self.state_manager = KQueensManager()
