# -*- coding: utf-8 -*-

from random import randint

from state_manager import StateManager
from game_levels import GameLevel


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
        We give random color value for each vertice (int between 1 and self.K)
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
                break

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
