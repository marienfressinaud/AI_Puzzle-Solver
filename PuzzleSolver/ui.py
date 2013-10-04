# -*- coding: utf-8 -*-


def ask_choice(possible_choices=None):
    """
    Permits to get a choice between different choices as input
    """

    choice = None
    ok = False

    while not ok:
        choice = raw_input("> ")

        if (possible_choices is None) or \
           (choice.lower() in possible_choices):
            ok = True
        else:
            message = "Invalid choice, choose between "
            for c in possible_choices:
                message += c.upper() + " or "
            print message[:-4]

    return choice


def ask_number(bound_min, bound_max):
    """
    Ask for a number between bound_min and bound_max
    """

    choice = None
    ok = False

    while not ok:
        choice_tmp = raw_input("> ")

        try:
            choice = int(choice_tmp)
        except ValueError:
            # choice was not a integer
            choice = None

        if choice is not None and bound_max >= choice >= bound_min:
            ok = True
        else:
            print "Invalid choice, choose a number between %d and %d" \
                % (bound_min, bound_max)

    return choice


def show_menu():
    """
    Print game menu
    """

    print """
=   (P)lay
=   (L)evel easy | medium | hard
=   Local Search (T)ype SA | MC
=   (N)umber of loops
=   (S)ee configuration
=   (Q)uit
    """


def ask_game():
    """
    Ask for the game we want to play
    """

    print """
(1) K-Queens
(2) Graph Coloring
(3) Third game (not yet chosen)
"""
    games = ["k-queens", "graph-coloring", "TODO"]

    choice = ask_number(1, len(games))
    return games[choice - 1]


def ask_number_loops(_min, _max):
    """
    Show a message to ask a number of loops between _min and _max
    """

    print "Choose a number of loops between %d and %d" % (_min, _max)
    return ask_number(_min, _max)


def show_configuration(env):
    """
    Print the current configuration
    """

    level = env["level"]
    nb_loops = env["nb_loops"]
    local_search_type = ""
    if env["local_search_type"] == "mc":
        local_search_type = "Min Conflicts"
    elif env["local_search_type"] == "sa":
        local_search_type = "Simulated Annealing"
    else:
        assert(0)

    print """Local search type: %s
Level: %s
Number of loops: %d""" \
    % (local_search_type, level, nb_loops)


def show_non_perfect_game(nb_steps):
    print "Out of steps (%d)! We have only a non perfect result..." % nb_steps


def show_perfect_game(nb_steps):
    print "Game has been resolved in %d steps!" % nb_steps
