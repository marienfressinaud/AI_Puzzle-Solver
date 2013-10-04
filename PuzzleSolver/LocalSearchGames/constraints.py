# -*- coding: utf-8 -*-

def queen_not_under_attack(state, var1, var2):
    queen_i = (var1, state[var1])
    queen_j = (var2, state[var2])

    return queen_j[1] not in (
        queen_i[1],
        queen_i[1] + abs(queen_i[0] - queen_j[0]),
        queen_i[1] - abs(queen_i[0] - queen_j[0])
    )


class Constraint(object):

    def __init__(self, function, var1, var2):
        self.function = function
        self.var1 = var1
        self.var2 = var2
        self.coeff_count = 1

    def check(self, state):
        return self.function(state, self.var1, self.var2)


class MustBeDifferentConstraint(Constraint):

    def __init__(self, list_vars):
        self.list_vars = list_vars
        self.coeff_count = 1

    def check(self, state):
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

    def check(self, state):
        list_nb = [state[var] for var in self.list_vars]
        diff = abs(self.sum - sum(list_nb))
        self.coeff_count = diff

        return diff == 0
