#!/bin/env python2
# -*- coding: utf-8 -*-

from time import time

from factory import Factory
import ui


MIN_LOOPS = 1
MAX_LOOPS = 2000


def exec_game(game_type, local_search_type, level, verbosity):
    """
    Function which runs a game according to the current configuration
    """

    game = Factory.build(game_type, local_search_type)
    game.verbose = (verbosity == "on")

    game.generate(level)
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
        exec_game(
            game, env["local_search_type"], env["level"], env["verbosity"]
        )


def __set_env(env, var, val):
    """
    Sets a value to a variable of the environment
    """

    check_values = {
        "level": ["easy", "medium", "hard"],
        "local_search_type": ["mc", "sa"],
        "nb_loops": xrange(MIN_LOOPS, MAX_LOOPS),
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
        "l": lambda env, *args: __set_env(env, "level", args[0]),
        "t": lambda env, *args: __set_env(env, "local_search_type", args[0]),
        "n": lambda env, *args: __set_env(
            env, "nb_loops", ui.ask_number_loops(MIN_LOOPS, MAX_LOOPS)
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
        "level": "easy",
        "local_search_type": "mc",
        "nb_loops": 5,
        "verbosity": "off"
    }

    while choice != "q":
        choice = ui.ask_menu()

        exec_choice(choice.split(), env)


if __name__ == "__main__":
    main()
