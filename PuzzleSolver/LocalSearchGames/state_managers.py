# -*- coding: utf-8 -*-

from random import randint, choice

from game_levels import GameLevel

class StateManager(object):
    """
    A StateManager manages states of a game.
    It must be an abstract class and being implemented.
    """

    def __init__(self):
        self.exists = False
        self.vars = {}
        self.constraints = []

    def build_new_game(self, level):
        """
        Generates a new game.
        Other methods must not do anything if not self.exists
        """

        self.exists = True

    def get_random_conflict_variable(self):
        """
        Returns a random variable which involves in at least one conflict

        TODO (K-Queens case) may not be efficient when K is really big
             and no so many constraint violated variables
        """

        var = None
        nb_constraints = 0
        while nb_constraints <= 0:
            v = choice(self.vars.keys())
            nb_constraints = self.count_constraint_violated(v)
            var = {
                "id": v,
                "val": self.vars[v],
                "constraints": nb_constraints
            }

        return var

    def is_optimal(self):
        """
        Return True if all variables are constraint violation free
        """

        for v in self.vars:
            if self.count_constraint_violated(v) > 0:
                return False

        return True

    def list_next_states(self, var):
        """
        Generates different states for a given variable
        Must be implemented by child classes
        """

        pass

    def count_constraint_violated(self, var, max_count=None):
        """
        Counts number of constraint violations for a given variable
        Must be implemented by child classes
        """

        pass

    def upstate(self, state):
        """
        Updates current state with state parameter
        Returns the previous state (constraints attribute is not updated)
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
        count = 0

        for queen_j in self.vars:
            if queen_i == queen_j:
                # don't compare a queen with itself (herself?)
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

    def __build_graph(self):
        """
        Read file with the given filename (into data/ directory) and generates
        graph following graph-color-format.txt file.
        We give a random color value for each vertice (int between 1 and self.K)
        Vertices are stored in self.vars and edges in self.constraints
        """

        # TODO: check file format and errors
        f = open("data/%s" % self.filename)

        self.nb_v, self.nb_e = (int(x) for x in f.readline().split())

        for i in xrange(self.nb_v):
            v = [float(x) for x in f.readline().split()]
            self.vars[int(v[0])] = randint(1, self.K)
            #self.coords[int(v[0])] = {"x": v[1], "y": v[2]}

        for i in xrange(self.nb_e):
            e = [int(x) for x in f.readline().split()]
            self.constraints.append(e)

        f.close()

    def build_new_game(self, level):
        super(ColorGraphManager, self).build_new_game(level)

        self.K = 4

        if level == GameLevel.EASY:
            self.filename = "graph-color-2.txt"
        elif level == GameLevel.MEDIUM:
            self.filename = "graph-color-1.txt"
        else:
            self.filename = "graph-color-3.txt"

        self.__build_graph()

    def count_constraint_violated(self, cur_var_id, max_count=None):
        count = 0

        for c in self.constraints:
            if (c[0] == cur_var_id or c[1] == cur_var_id) and \
                    (self.vars[c[1]] == self.vars[c[0]]):
                count += 1

            if max_count is not None and count - 1 > max_count:
                return count

        return count

    def list_next_states(self, var):
        first_color = self.vars[var["id"]]
        list_states = []

        max_count = var["constraints"]
        for color in xrange(1, self.K + 1):
            self.vars[var["id"]] = color
            nb_constraints = self.count_constraint_violated(
                var["id"], max_count)

            list_states.append({
                "id": var["id"],
                "val": color,
                "constraints": nb_constraints
            })

            max_count = min(max_count, nb_constraints)

        self.vars[var["id"]] = first_color
        return list_states

    def upstate(self, state):
        self.vars[state["id"]] = state["val"]
