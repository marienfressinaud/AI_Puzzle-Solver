# -*- coding: utf-8 -*-

from random import randint

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

    def get_conflict_variable(self):
        """
        Choose a random variable which involved in at least one conflict
        """

        return self.state_manager.get_random_conflict_variable()

    def get_fewest_conflict_state(self, var_id):
        """
        Choose a new state we can assign to selected_var in order to produce
        less conflicts
        """

        best_states = [self.state_manager.state]
        best_constraint = self.state_manager.count_constraint_violated(
            self.state_manager.state, var_id)

        for state in self.state_manager.list_next_states(var_id):
            assert(len(best_states) >= 1)

            cur_constraint = self.state_manager.count_constraint_violated(
                state, var_id)

            if cur_constraint < best_constraint or \
                    (best_states[0] == self.state_manager.state and
                        cur_constraint == best_constraint):
                # if constraint value is less than previous constraint values
                # we regenerate list of best states. Same if we never change
                # best_states (when best_states[0] == self.state_manager.state)
                best_states = [state]
                best_constraint = cur_constraint
            elif cur_constraint == best_constraint:
                # We extend best_states if we have multiple best states
                # We will selected them randomly after
                best_states.append(state)

        return best_states[randint(0, len(best_states) - 1)]

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
