# -*- coding: utf-8 -*-

from random import randint

from game_levels import GameLevel

class StateManager(object):
    """
    A StateManager manages states of a game.
    It must be an abstract class and being implemented.
    """

    def __init__(self):
        self.exists = False
        self.vars = {}

    def build_new_game(self, level):
        """
        Generates a new game.
        Other methods must not do anything if not self.exists
        """

        self.exists = True

    def count_constraint_violated(self, var, max_count=None):
        """
        Counts number of constraint violations for a given variable
        Must be implemented by child classes
        """

        pass

    def get_random_conflict_variable(self):
        """
        Returns a random variable which involves in at least one conflict

        TODO (K-Queens case) may not be efficient when K is really big
             and no so many constraint violated variables
        """

        var = None
        nb_constraints = 0
        while nb_constraints <= 0:
            i = randint(0, self.K)
            for v in self.vars:
                if v[0] == i:
                    nb_constraints = self.count_constraint_violated(v)
                    var = {
                        "id": v,
                        "val": nb_constraints
                    }
                    break

        return var

    def list_constraints_variables(self, selected_var):
        """
        Returns a generator of possible future "position" for selected_var
        and indicates number of constraint violations
        """

        pass

    def is_optimal(self):
        """
        Return True if all variables are constraint violation free
        """

        for v in self.vars:
            if self.count_constraint_violated(v) > 0:
                return False

        return True

    def upstate(self, prev_var, next_var):
        """
        Update current state by giving prev_var value to next_var
        Must be implemented by child classes
        """

        pass

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

        if not self.exists:
            return

        self.vars = {}
        for i in xrange(self.K):
            j = randint(0, self.K - 1)
            self.vars[(i, j)] = (i, j)

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
        count = 0

        for queen_j in self.vars:
            if queen_i == queen_j:
                continue

            list_col = (
                queen_i[1],
                queen_i[1] + abs(queen_i[0] - queen_j[0]),
                queen_i[1] - abs(queen_i[0] - queen_j[0])
            )

            if queen_j[1] in list_col:
                count += 1

            if max_count is not None and count - 1 > max_count:
                return count

        return count

    def list_constraints_variables(self, selected_var):
        i = selected_var["id"][0]
        list_vars = []

        # max_count permits to increase drastically performance
        # we consider only better positions (less constraint violations)
        # than the current one
        max_count = selected_var["val"]
        for j in xrange(self.K):
            v = (i, j)

            nb_constraints = self.count_constraint_violated(v, max_count)
            # We have to adjust nb_constraint to avoid selected_var effect
            adjust = 1
            if j == selected_var["id"][1]:
                adjust = 0
            nb_constraints -= adjust

            list_vars.append({
                "id": v,
                "val": nb_constraints
            })

            max_count = min(max_count, nb_constraints)

        return list_vars

    def upstate(self, prev_var, next_var):
        prev_pos = prev_var["id"]
        next_pos = next_var["id"]

        if prev_pos in self.vars:
            self.vars.pop(prev_pos, None)

        self.vars[next_pos] = next_pos

    def __str__(self):
        """
        Returns a representation of the current state as a string
        """

        _str = ""

        if self.exists:
            _str = "-" * (3 * self.K) + "\n"
            for i in xrange(self.K):
                for j in xrange(self.K):
                    if (i, j) in self.vars:
                        _str += "| Q "
                    else:
                        _str += "|   "

                _str += "\n"
            _str += "-" * (3 * self.K)

        return _str

class ColorGraphManager(StateManager):
    """
    State manager for a Color Graph game
    """

    def __init__(self):
        super(ColorGraphManager, self).__init__()
