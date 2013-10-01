# -*- coding: utf-8 -*-

from random import choice

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

    def get_random_variable(self):
        """
        Returns a random variable
        """

        v = choice(self.vars.keys())
        nb_constraints = self.count_constraint_violated(v)
        return {
            "id": v,
            "val": self.vars[v],
            "constraints": nb_constraints
        }

    def get_random_conflict_variable(self):
        """
        Returns a random variable which involves in at least one conflict

        TODO (K-Queens case) may not be efficient when K is really big
             and no so many constraint violated variables
        """

        var = None
        while var is None or var["constraints"] <= 0:
            var = self.get_random_variable()

        return var

    def is_optimal(self):
        """
        Return True if all variables are constraint violation free
        """

        for v in self.vars:
            if self.count_constraint_violated(v) > 0:
                return False

        return True

    def generate_random_states(self, n):
        """
        Generates n random states
        """

        list_states = []

        for i in xrange(n):
            var = self.get_random_variable()
            states = self.list_next_states(var)
            list_states.append(choice(states))

        return list_states

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

    def inv_state(self, state):
        """
        Returns the state which cancel the given state
        constraints equals 0
        """

        return {
            "id": state["id"],
            "val": self.vars[state["id"]],
            "constraints": 0
        }
