# -*- coding: utf-8 -*-

from random import randint

from game import Game
from state_managers import KQueensManager, ColorGraphManager
from graph_output import draw_graph

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

    def is_terminated(self):
        return self.state_manager.is_optimal() or \
               self.number_steps >= self.max_steps

    def get_conflict_variable(self):
        """
        Choose a random variable which involved in at least one conflict
        """

        return self.state_manager.get_random_conflict_variable()

    def get_fewest_conflict_state(self, selected_var):
        """
        Choose a new state we can assign to selected_var in order to produce
        less conflicts
        """

        best_vars = [selected_var]
        for var in self.state_manager.list_next_states(selected_var):
            if var["val"] == selected_var["val"]:
                # don't compare the current value
                continue

            if var["constraints"] < best_vars[0]["constraints"] or \
                    (best_vars[0]["val"] == selected_var["val"] and \
                        var["constraints"] == best_vars[0]["constraints"]):
                # if constraint value is less than previous constraint values
                # we regenerate list of best vars. Same if we never change
                # best_vars (when best_vars[0] == selected_var)
                best_vars = [var]
            elif var["constraints"] == best_vars[0]["constraints"]:
                # We extend best_vars if we have multiple best variables
                # We will selected them randomly after
                best_vars.append(var)

        return best_vars[randint(0, len(best_vars) - 1)]

    def run(self):
        """
        Runs min conflicts algorithm
        """

        self.number_steps = 0
        while not self.is_terminated():
            self.number_steps += 1

            conflict_var = self.get_conflict_variable()
            state = self.get_fewest_conflict_state(conflict_var)

            self.state_manager.upstate(state)

class KQueensMC(MinConflictsGame):
    """
    K-Queens game based on min conflicts algorithm
    """

    def __init__(self):
        super(KQueensMC, self).__init__()

        self.state_manager = KQueensManager()

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
