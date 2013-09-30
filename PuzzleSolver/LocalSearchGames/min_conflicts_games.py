# -*- coding: utf-8 -*-

from game import Game

class MinConflictsGame(Game):
    """
    A MinConflictsGame must implement min conflicts algorithm.
    A basic algorithm is:
        Repeat until optimal solution found or maximum number of steps:
        1. Randomly choose any variable, V, that is involved in
           at least one conflict (i.e., violated constraint)
        2. Assign V the new value a, where a is the value that produces the
           fewest number of conflicts.
    """

    def __init__(self):
        super(MinConflictsGame, self).__init__()

class KQueensMC(MinConflictsGame):
    """
    K-Queens game based on min conflicts algorithm
    """

    def __init__(self):
        super(KQueensMC, self).__init__()

class GraphColorMC(MinConflictsGame):
    """
    Graph Color game based on min conflicts algorithm
    """

    def __init__(self):
        super(GraphColorMC, self).__init__()
