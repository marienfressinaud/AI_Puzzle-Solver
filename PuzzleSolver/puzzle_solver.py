#!/bin/env python2
# -*- coding: utf-8 -*-

from time import time

from factory import Factory
import ui


MIN_LOOPS = 1
MAX_LOOPS = 2000

MIN_TIME_LIMIT = 5
MAX_TIME_LIMIT = 3600


def exec_game(game_type, env):
    """
    Function which runs a game according to the current configuration
    """

    local_search_type = env["local_search_type"]
    mode = env["mode"]
    time_limit = env["time_limit"]
    verbosity = env["verbosity"]

    game = Factory.build(game_type, local_search_type)
    game.max_time = time_limit
    game.verbose = (verbosity == "on")

    game.generate(mode)
    game.run()

    running_time = (time()-game.date_begin) * 1000
    evaluation = game.evaluate(game.state_manager.state)

    msg = ""
    if game.outofsteps():
        msg = "out of steps"
    elif game.outoftime():
        msg = "out of time"
    else:
        msg = "perfect game"

    ui.show_end_game(
        game_type, evaluation, game.number_steps, running_time, msg)


def run_games(game, env):
    """
    Executes a game for a certain number of loops
    """

    for i in xrange(env["nb_loops"]):
        exec_game(game, env)


def __set_env(env, var, val):
    """
    Sets a value to a variable of the environment
    """

    check_values = {
        "mode": ["easy", "medium", "hard"],
        "local_search_type": ["mc", "sa"],
        "nb_loops": xrange(MIN_LOOPS, MAX_LOOPS + 1),
        "time_limit": xrange(MIN_TIME_LIMIT, MAX_TIME_LIMIT + 1),
        "verbosity": ["on", "off"]
    }

    if var in check_values and val in check_values[var]:
        env[var] = val


def exec_choice(choice, env):
    """
    Executes a command
    """

    games = Factory.list_games()

    actions = {
        "p": lambda env, *args: run_games(ui.ask_item(games), env),
        "m": lambda env, *args: __set_env(env, "mode", args[0]),
        "l": lambda env, *args: __set_env(env, "local_search_type", args[0]),
        "n": lambda env, *args: __set_env(
            env, "nb_loops", ui.ask_number_loops(MIN_LOOPS, MAX_LOOPS)
        ),
        "t": lambda env, *args: __set_env(
            env, "time_limit", ui.ask_time_limit(
                MIN_TIME_LIMIT, MAX_TIME_LIMIT)
        ),
        "s": lambda env, *args: ui.show_configuration(env),
        "v": lambda env, *args: __set_env(env, "verbosity", args[0])
    }

    if choice[0] in actions:
        args = None
        if len(choice) > 1:
            args = choice[1]

        actions[choice[0]](env, args)


def main():
    """
    Program entry point. Here is the main loop which waits for an exit
    """

    choice = None
    env = {
        "mode": "easy",
        "local_search_type": "mc",
        "nb_loops": 20,
        "time_limit": 3600,
        "verbosity": "off"
    }

    while choice != "q":
        choice = ui.ask_menu()

        exec_choice(choice.split(), env)


if __name__ == "__main__":
    main()
