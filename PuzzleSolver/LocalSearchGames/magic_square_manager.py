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
        # _list_tmp = [6,7,2,1,5,9,8,3,4]
        for i in xrange(self.N * self.N):
            self.vars[i] = randint(1, self.N * self.N)
            # self.vars[i] = _list_tmp[i]

        self.constraints = self.vars.keys()

    def build_new_game(self, level):
        if level == GameLevel.EASY:
            self.N = 3
        elif level == GameLevel.MEDIUM:
            self.N = 12
        else:
            self.N = 20  # TODO: change levels

        self.sum = (self.N * (self.N**2 + 1)) / 2

        self.__generate_numbers()

    def count_constraint_violated(self, var_id, max_count=None):
        count = 0

        var_i = var_id % self.N
        var_j = var_id / self.N

        # check number is different
        # TODO with this counstraint, algo is really bad
        # count += self.vars.values().count(self.vars[var_id]) - 1

        # check sum of row and column
        list_list_index = [
            [(var_j*self.N + i) for i in xrange(self.N)],
            [(var_i + self.N*i) for i in xrange(self.N)]
        ]
        # check sum of diagonals
        if var_i == var_j:
            list_list_index.append(
                [(i*self.N + i) for i in xrange(self.N)])
        if var_i == self.N-1 - var_j:
            list_list_index.append(
                [((self.N-1) * (self.N-i)) for i in xrange(self.N)])

        for list_index in list_list_index:
            list_nb = [self.vars[i] for i in list_index]
            diff = abs(self.sum - sum(list_nb))
            count += 1 * diff

            if max_count is not None and count - 1 > max_count:
                break

        return count

    def list_next_states(self, var):
        first_num = self.vars[var["id"]]
        list_states = []

        max_count = var["constraints"]
        for num in xrange(1, self.N * self.N):
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
        _str += "-" * (6 * self.N) + "\n"
        for i in xrange(self.N):
            for j in xrange(self.N):
                _str += " %3d |" % self.vars[i*self.N + j]

            _str += "\n"
        _str += "-" * (6 * self.N)

        return _str
