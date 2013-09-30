# -*- coding: utf-8 -*-

from random import randint

from game import Game
from state_managers import KQueensManager, ColorGraphManager

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

    def get_fewest_conflict_variable(self, selected_var):
        """
        Choose where we can assign selected_var in order to produce
        less conflicts
        """

        best_vars = [selected_var]
        for var in self.state_manager.list_constraints_variables(selected_var):
            if var["id"] == selected_var["id"]:
                # don't compare selected_var with itself
                continue

            if var["val"] < best_vars[0]["val"] or \
                    (best_vars[0]["id"] == selected_var["id"] and \
                        var["val"] == best_vars[0]["val"]):
                # if constraint value is less than previous constraint values
                # we regenerate list of best vars. Same if we never change
                # best_vars (when best_vars[0] == selected_var)
                best_vars = [var]
            elif var["val"] == best_vars[0]["val"]:
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

            #print self.state_manager

            conflict_var = self.get_conflict_variable()
            new_var = self.get_fewest_conflict_variable(conflict_var)

            self.state_manager.upstate(conflict_var, new_var)

        #print self.state_manager

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
