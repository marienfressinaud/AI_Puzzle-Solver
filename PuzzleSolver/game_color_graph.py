# -*- coding: utf-8 -*-

from LocalSearchGames.min_conflicts_game import MinConflictsGame
from LocalSearchGames.simulated_annealing_game import SimulatedAnnealingGame
from LocalSearchGames.state_manager import StateManager
from LocalSearchGames.game_levels import GameLevel
from LocalSearchGames.constraints import MustBeDifferentConstraint
from graph_output import draw_graph


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

        self.vars = {}
        for i in xrange(self.nb_v):
            v = [float(x) for x in f.readline().split()]
            self.vars[int(v[0])] = xrange(1, self.K + 1)
            #self.coords[int(v[0])] = {"x": v[1], "y": v[2]}

        self.constraints = []
        for i in xrange(self.nb_e):
            e = [int(x) for x in f.readline().split()]
            self.constraints.append(
                MustBeDifferentConstraint([e[0], e[1]]))

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


class GraphColorMC(MinConflictsGame):
    """
    Graph Color game based on min conflicts algorithm
    """

    def __init__(self):
        super(GraphColorMC, self).__init__()

        self.state_manager = ColorGraphManager()

    def run(self):
        draw_graph(self.state_manager, "graph_start.dot")

        super(GraphColorMC, self).run()

        draw_graph(self.state_manager, "graph_end.dot")


class GraphColorSA(SimulatedAnnealingGame):
    """
    Graph color game based on simulated annealing algorithm
    """

    def __init__(self):
        super(GraphColorSA, self).__init__()

        self.state_manager = ColorGraphManager()

    def run(self):
        draw_graph(self.state_manager, "graph_start.dot")

        super(GraphColorSA, self).run()

        draw_graph(self.state_manager, "graph_end.dot")