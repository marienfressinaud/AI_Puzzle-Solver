# -*- coding: utf-8 -*-


def __build_list_choices(choices):
    msg = ""
    if len(choices) <= 3:
        for c in choices:
            msg += "%s or " % c.upper()
        msg = msg[:-4]
    else:
        for c in choices:
            msg += "\n* %s" % c

    return msg


def ask_choice(possible_choices=None):
    """
    Permits to get a choice between different choices as input
    """

    choice = None
    ok = False

    while not ok:
        choice = raw_input("> ").strip()

        if (possible_choices is None) or \
           (choice.lower() in possible_choices):
            ok = True
        else:
            message = "Invalid choice, choose between: %s" \
                % __build_list_choices(possible_choices)

            print message

    return choice


def ask_number(bound_min, bound_max):
    """
    Ask for a number between bound_min and bound_max
    """

    choice = None
    ok = False

    while not ok:
        choice_tmp = raw_input("> ").strip()

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


def ask_item(list_items):
    """
    Ask for the game we want to play
    """
    _str = "\n"

    for i in xrange(len(list_items)):
        _str += "(%d) %s\n" % (i + 1, list_items[i])

    print _str
    choice = ask_number(1, len(list_items))
    return list_items[choice - 1]


def ask_menu():
    """
    Print game menu
    """

    print """
=   (P)lay
=   (M)ode easy | medium | hard
=   (L)ocal Search Type SA | MC
=   (N)umber of loops
=   (T)ime limit
=   (V)erbosity on | off
=   (S)ee configuration
=   (Q)uit
    """

    return ask_choice((
        "p",
        "m easy", "m medium", "m hard",
        "l sa", "l mc",
        "n", "t",
        "v on", "v off",
        "s",
        "q"
    )).lower()


def ask_number_loops(_min, _max):
    """
    Show a message to ask a number of loops between _min and _max
    """

    print "Choose a number of loops between %d and %d" % (_min, _max)
    return ask_number(_min, _max)


def ask_time_limit(_min, _max):
    """
    Show a message to ask a time_limit
    """

    print "Choose a time limit between %d and %d (seconds)" % (_min, _max)
    return ask_number(_min, _max)


def show_configuration(env):
    """
    Print the current configuration
    """

    mode = env["mode"]
    nb_loops = env["nb_loops"]
    time_limit = env["time_limit"]
    verbosity = env["verbosity"]

    local_search_type = ""
    if env["local_search_type"] == "mc":
        local_search_type = "Min Conflicts"
    elif env["local_search_type"] == "sa":
        local_search_type = "Simulated Annealing"

    print """Local search type: %s
Mode: %s
Number of loops: %d
Time limit: %d seconds
Verbosity: %s""" \
    % (local_search_type, mode, nb_loops, time_limit, verbosity)


def show_not_exists_file(filename):
    print "Oops, %s doesn't exist in data directory" % filename


def show_invalid_file(filename):
    print "Oops, `%s` seems to be an invalid file" % filename


def show_outofsteps_game(game, nb_steps):
    print ("%s out of steps (%d)! " +
           "We have only found a non perfect result...") \
        % (game, nb_steps)


def show_outoftime_game(game, limit):
    print ("%s out of time (%d seconds)! " +
           "We have only found a non perfect result...") \
        % (game, limit)


def show_perfect_game(game, nb_steps, running_time):
    print "%s has been resolved in %d steps and %.2f seconds!" \
        % (game, nb_steps, running_time)
