# -*- coding: utf-8 -*-

from random import randint

from state_manager import StateManager
from game_levels import GameLevel


class MagicSquareManager(StateManager):
    """
    State manager for a Magic Square game
    """

    def __init__(self):
        super(MagicSquareManager, self).__init__()

        self.N = 0
        self.sum = 0

    def __generate_numbers(self):
        self.vars = {}
        for i in xrange(self.N * self.N):
            self.vars[i] = randint(1, self.sum - 1)

        self.constraints = self.vars.keys()

    def build_new_game(self, level):
        if level == GameLevel.EASY:
            self.N = 4
        elif level == GameLevel.MEDIUM:
            self.N = 10
        else:
            self.N = 15  # TODO: change levels

        self.sum = (self.N * (self.N ** 2 + 1)) / 2

        self.__generate_numbers()

    def count_constraint_violated(self, var_id, max_count=None):
        count = 0

        var_i = var_id % self.N
        var_j = var_id / self.N
        val = self.vars[var_id]

        # check number is different
        count += self.vars.values().count(val)

        # check sum of diagonals
        if var_i == var_j:
            num = 0
            for i in [(j*self.N + j) for j in xrange(self.N)]:
                num += self.vars[i]

            if num != self.sum:
                count += 1

        if var_i == self.N-1 - var_j:
            num = 0
            for i in [((self.N-1) * (self.N-j)) for j in xrange(self.N)]:
                num += self.vars[i]

            if num != self.sum:
                count += 1

        # check sum of row and column
        num = 0
        for i in [(var_j*self.N + j) for j in xrange(self.N)]:
            num += self.vars[i]

        if num != self.sum:
            count += 1

        num = 0
        for i in [(var_i + self.N*j) for j in xrange(self.N)]:
            num += self.vars[i]

        if num != self.sum:
            count += 1

        return count

    def list_next_states(self, var):
        first_num = self.vars[var["id"]]
        list_states = []

        max_count = var["constraints"]
        for num in xrange(1, self.sum - 1):
            self.vars[var["id"]] = num
            nb_constraints = self.count_constraint_violated(
                var["id"], max_count)

            list_states.append({
                "id": var["id"],
                "val": num,
                "constraints": nb_constraints
            })

            max_count = min(max_count, nb_constraints)

        self.vars[var["id"]] = first_num
        return list_states

    def upstate(self, state):
        self.vars[state["id"]] = state["val"]

    def __str__(self):
        """
        Returns a representation of the current state as a string
        """

        _str = "SUM = %d\n" % self.sum
        _str += "-" * (8 * self.N) + "\n"
        for i in xrange(self.N):
            for j in xrange(self.N):
                _str += " %5d |" % self.vars[i*self.N + j]

            _str += "\n"
        _str += "-" * (8 * self.N)

        return _str
