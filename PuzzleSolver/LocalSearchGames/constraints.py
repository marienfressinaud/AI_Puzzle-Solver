# -*- coding: utf-8 -*-


class Constraint(object):

    def __init__(self, list_vars, function):
        self.list_vars = list_vars
        self.function = function
        self.coeff_count = 1

    def check(self, state, var_involved=None):
        if var_involved is None or var_involved in self.list_vars:
            return self.function(state, self.list_vars)
        return True


class MustBeDifferentConstraint(Constraint):

    def __init__(self, list_vars):
        self.list_vars = list_vars
        self.coeff_count = 1

    def check(self, state, var_involved=None):
        if var_involved is None or var_involved in self.list_vars:
            var_exist = []
            for var in self.list_vars:
                if state[var] in var_exist:
                    return False
                else:
                    var_exist.append(state[var])
        return True


class SumEqualsConstraint(Constraint):

    def __init__(self, _sum, list_vars):
        self.sum = _sum
        self.list_vars = list_vars
        self.coeff_count = 1

    def check(self, state, var_involved=None):
        if var_involved is None or var_involved in self.list_vars:
            list_nb = [state[var] for var in self.list_vars]
            diff = abs(self.sum - sum(list_nb))
            self.coeff_count = diff

            return diff == 0
        return True
