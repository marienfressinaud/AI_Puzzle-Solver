# -*- coding: utf-8 -*-

from random import randint

from state_manager import StateManager
from game_levels import GameLevel


class KQueensManager(StateManager):
    """
    State manager for a K-Queens game
    """

    def __init__(self):
        super(KQueensManager, self).__init__()

        self.K = 0

    def __place_all_queens(self):
        """
        Places queens on a board.
        Queens are stored in a dictionnary where key is the position (tuple)
        If a position is not in self.queens, there is no queen here
        """

        self.vars = {}
        for i in xrange(self.K):
            j = randint(0, self.K - 1)
            self.vars[(i, j)] = (i, j)

        # Here, we can consider constraints is the same as vars (it works well)
        # But be careful, vars is a dictionary and constraints a list
        self.constraints = self.vars.values()

    def build_new_game(self, level):
        super(KQueensManager, self).build_new_game(level)

        if level == GameLevel.EASY:
            self.K = 8
        elif level == GameLevel.MEDIUM:
            self.K = 25
        else:
            self.K = 1000

        self.__place_all_queens()

    def count_constraint_violated(self, queen_i, max_count=None):
        # we begin at -1 because queen_i is in conflict with itself
        count = -1

        for queen_j in self.vars:
            list_col = (
                queen_i[1],
                queen_i[1] + abs(queen_i[0] - queen_j[0]),
                queen_i[1] - abs(queen_i[0] - queen_j[0])
            )

            if queen_j[1] in list_col:
                count += 1

            if max_count is not None and count - 1 > max_count:
                break

        return count

    def list_next_states(self, var):
        i = var["id"][0]
        list_states = []

        # max_count permits to increase drastically performance
        # we consider only better positions (less constraint violations)
        # than the current one
        max_count = var["constraints"]
        for j in xrange(self.K):
            v = (i, j)

            nb_constraints = self.count_constraint_violated(v, max_count)
            # We have to adjust nb_constraint to avoid selected_var effect
            adjust = 1
            if j == var["id"][1]:
                adjust = 0
            nb_constraints -= adjust

            list_states.append({
                "id": var["id"],
                "val": v,
                "constraints": nb_constraints
            })

            max_count = min(max_count, nb_constraints)

        return list_states

    def upstate(self, state):
        prev_pos = state["id"]
        next_pos = state["val"]

        assert(prev_pos in self.vars)
        self.vars.pop(prev_pos, None)
        self.vars[next_pos] = next_pos

        self.constraints = self.vars.values()

    def inv_state(self, state):
        return {
            "id": state["val"],
            "val": self.vars[state["id"]],
            "constraints": 0
        }

    def __str__(self):
        """
        Returns a representation of the current state as a string
        """

        _str = ""

        _str = "-" * (4 * self.K) + "\n"
        for i in xrange(self.K):
            for j in xrange(self.K):
                if (i, j) in self.vars:
                    _str += " Q |"
                else:
                    _str += "   |"

            _str += "\n"
        _str += "-" * (4 * self.K)

        return _str
