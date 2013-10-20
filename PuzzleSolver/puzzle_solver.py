#!/bin/env python2
# -*- coding: utf-8 -*-

from time import time

from factory import Factory
import ui


MIN_LOOPS = 1
MAX_LOOPS = 2000

MIN_TIME_LIMIT = 5
MAX_TIME_LIMIT = 1800


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

    if game.outofsteps():
        ui.show_outofsteps_game(game_type, game.number_steps)
    elif game.outoftime():
        ui.show_outoftime_game(game_type, game.max_time)
    else:
        running_time = time() - game.date_begin
        ui.show_perfect_game(game_type, game.number_steps, running_time)


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
        "nb_loops": 5,
        "time_limit": 120,
        "verbosity": "off"
    }

    while choice != "q":
        choice = ui.ask_menu()

        exec_choice(choice.split(), env)


if __name__ == "__main__":
    main()
