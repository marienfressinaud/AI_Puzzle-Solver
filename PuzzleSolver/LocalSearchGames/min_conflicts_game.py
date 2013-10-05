# -*- coding: utf-8 -*-

from time import time
from random import choice

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

    def get_fewest_conflict_state(self, var_id):
        """
        Choose a new state where our selected var produce less conflicts
        If there are several possible states, we choose one randomly
        """

        best_states = [self.state_manager.state]
        best_constraint = self.state_manager.count_constraint_violated(
            self.state_manager.state, var_id)

        next_states = self.state_manager.list_next_states(var_id)
        for state in next_states:
            cur_constraint = self.state_manager.count_constraint_violated(
                state, var_id, best_constraint) - 1

            if cur_constraint < best_constraint or \
                    (best_states[0] == self.state_manager.state and
                        cur_constraint == best_constraint):
                # if constraint value is less than previous constraint values
                # we regenerate list of best states. Same if we have never
                # changed best_states and current constraint == best constraint
                best_states = [state]
                best_constraint = cur_constraint
            elif cur_constraint == best_constraint:
                # We extend best_states if we have multiple best states
                # We will selected them randomly after
                best_states.append(state)

        return choice(best_states)

    def run(self):
        """
        Runs min conflicts algorithm
        """

        self.show_state_manager()
        self.date_begin = time()

        self.number_steps = 0
        while not self.is_terminated():
            self.number_steps += 1

            # we get a random *conflicted* variable and we modify its value
            # in order to minimize the number of conflicts
            conflict_var = self.state_manager.get_random_conflict_variable()
            state = self.get_fewest_conflict_state(conflict_var)

            self.state_manager.upstate(state)

        self.show_state_manager()
