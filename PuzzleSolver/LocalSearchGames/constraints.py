# -*- coding: utf-8 -*-


class Constraint(object):
    """
    A Constraint check if all vars into list_vars validate a specific function
    Basic Constraint use a user-defined function
    """

    def __init__(self, list_vars, function=None):
        self.list_vars = list_vars
        self.coeff_count = 1
        self.function = function

    def check(self, state):
        if self.function is not None:
            return self.function(state, self.list_vars)

        return True


class MustBeDifferentConstraint(Constraint):
    """
    Each vars in list_vars must be different
    """

    def __init__(self, list_vars):
        super(MustBeDifferentConstraint, self).__init__(list_vars)

    def check(self, state):
        var_exist = []
        for var in self.list_vars:
            if state[var] in var_exist:
                return False
            else:
                var_exist.append(state[var])

        return True


class SumEqualsConstraint(Constraint):
    """
    Sum of all list_vars must be equal to _sum
    coeff_count is set to the difference between _sum and effective sum
    """

    def __init__(self, _sum, list_vars):
        super(SumEqualsConstraint, self).__init__(list_vars)
        self.sum = _sum

    def check(self, state):
        list_nb = [state[var] for var in self.list_vars]
        diff = abs(self.sum - sum(list_nb))
        self.coeff_count = diff

        return diff == 0
