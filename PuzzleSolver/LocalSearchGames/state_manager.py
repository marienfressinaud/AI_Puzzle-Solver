# -*- coding: utf-8 -*-

from random import choice


class StateManager(object):
    """
    A StateManager manages states of a game.
    It must be an abstract class and being implemented.
    """

    def __init__(self):
        self.vars = {}
        self.constraints = []
        self.state = {}

    def generate_game(self):
        """
        Generates a new state by choosing a random value for each vars
        """

        for v in self.vars:
            self.state[v] = choice(self.vars[v])

    def build_new_game(self, level):
        """
        Generates a new game.
        Must be implemented by child classes
        """

        pass

    def get_random_variable(self):
        """
        Returns a random variable
        """

        return choice(self.state.keys())

    def get_random_conflict_variable(self):
        """
        Returns a random variable which involves in at least one conflict
        """

        var = None
        while var is None or \
                self.count_constraint_violated(self.state, var) <= 0:
            var = self.get_random_variable()

        return var

    def is_optimal(self):
        """
        Return True if all variables are constraint violation free
        """

        return self.count_constraint_violated(self.state) <= 0

    def generate_random_states(self, n):
        """
        Generates n random states
        """

        list_states = []

        for i in xrange(n):
            var = self.get_random_variable()
            domain = self.vars[var]
            val = choice(domain)
            while val == self.state[var]:
                val = choice(domain)

            new_state = self.state.copy()
            new_state[var] = val
            list_states.append(new_state)

        return list_states

    def list_next_states(self, var_id):
        """
        Generates different states for a given variable
        """

        for val in self.vars[var_id]:
            # We get all values of the domain
            # if val is different than the current one, we create a new state
            if val != self.state[var_id]:
                new_state = self.state.copy()
                new_state[var_id] = val
                yield new_state

    def count_constraint_violated(self, state, var_id=None, max_count=None):
        """
        Counts number of constraint violations for a given variable
        """

        count = 0
        for c in self.constraints:
            c_is_ok = c.check(state, var_id)
            count += (1*c.coeff_count) * (not c_is_ok)

            if max_count is not None and count - 1 > max_count:
                break

        return count

    def upstate(self, new_state):
        """
        Updates current state with state parameter
        """

        self.state = new_state

    def __str__(self):
        return str(self.state)
