# -*- coding: utf-8 -*-

from sys import exit

from LocalSearchGames.min_conflicts_game import MinConflictsGame
from LocalSearchGames.simulated_annealing_game import SimulatedAnnealingGame
from LocalSearchGames.state_manager import StateManager
from LocalSearchGames.game_levels import GameLevel
from LocalSearchGames.constraints import MustBeDifferentConstraint
from graph_output import draw_graph
from ui import show_not_exists_file, show_invalid_file


class ColorGraphManager(StateManager):
    """
    State manager for a Color Graph game
    """

    def __init__(self):
        super(ColorGraphManager, self).__init__()

    def __read_multiplicities(self, file):
        try:
            return (int(x) for x in file.readline().split())
        except ValueError:
            show_invalid_file(self.filename)
            exit(-1)

    def __read_node(self, file):
        node = [float(x) for x in file.readline().split()]
        if len(node) == 3:
            node[0] = int(node[0])
            return node
        else:
            show_invalid_file(self.filename)
            exit(-1)

    def __read_edge(self, file):
        edge = [int(x) for x in file.readline().split()]
        if len(edge) == 2:
            return edge
        else:
            show_invalid_file(self.filename)
            exit(-1)

    def __build_graph(self):
        """
        Read file with the given filename (into data/ directory) and generates
        graph following graph-color-format.txt file.
        We give random color value for each vertice (int between 1 and self.K)
        Vertices are stored in self.vars and edges in self.constraints
        """

        try:
            f = open("data/%s" % self.filename)
        except IOError:
            show_not_exists_file(self.filename)
            exit(-1)

        self.nb_v, self.nb_e = self.__read_multiplicities(f)

        self.vars = {}
        for i in xrange(self.nb_v):
            node = self.__read_node(f)
            self.vars[node[0]] = xrange(1, self.K + 1)

        self.constraints = []
        for i in xrange(self.nb_e):
            edge = self.__read_edge(f)
            self.constraints.append(
                MustBeDifferentConstraint([edge[0], edge[1]])
            )

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

    nb_print = 0

    def __str__(self):
        """
        Returns a representation of the current state into a file
        """

        filename = "data/graph_%d.dot" % ColorGraphManager.nb_print
        draw_graph(self, filename)

        ColorGraphManager.nb_print += 1

        return "Current state has been saved into %s" % filename


class GraphColorMC(MinConflictsGame):
    """
    Graph Color game based on min conflicts algorithm
    """

    def __init__(self):
        super(GraphColorMC, self).__init__()

        self.state_manager = ColorGraphManager()


class GraphColorSA(SimulatedAnnealingGame):
    """
    Graph color game based on simulated annealing algorithm
    """

    def __init__(self):
        super(GraphColorSA, self).__init__()

        self.state_manager = ColorGraphManager()
