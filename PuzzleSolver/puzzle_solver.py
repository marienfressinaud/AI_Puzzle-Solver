#!/bin/env python2
# -*- coding: utf-8 -*-

from LocalSearchGames.factory import Factory
import ui


MIN_LOOPS = 1
MAX_LOOPS = 2000


def exec_game(game_type, local_search_type, level):
    """
    Function which runs a game according to the current configuration
    """

    game = Factory.build(game_type, local_search_type)

    game.generate(level)
    game.run()

    if game.number_steps >= game.max_steps:
        ui.show_non_perfect_game(game.number_steps)
    else:
        ui.show_perfect_game(game.number_steps)


def run_games(game, env):
    """
    Executes a game for a certain number of loops
    """

    for i in xrange(env["nb_loops"]):
        exec_game(game, env["local_search_type"], env["level"])


def __set_env(env, var, val):
    """
    Sets a value to a variable of the environment
    """

    check_values = {
        "level": ["easy", "medium", "hard"],
        "local_search_type": ["mc", "sa"],
        "nb_loops": xrange(MIN_LOOPS, MAX_LOOPS)
    }

    if var in check_values and val in check_values[var]:
        env[var] = val


def exec_choice(choice, env):
    """
    Executes a command
    """

    actions = {
        "p": lambda env, *args: run_games(ui.ask_game(), env),
        "l": lambda env, *args: __set_env(env, "level", args[0]),
        "t": lambda env, *args: __set_env(env, "local_search_type", args[0]),
        "n": lambda env, *args: __set_env(
            env, "nb_loops", ui.ask_number_loops(MIN_LOOPS, MAX_LOOPS)
        ),
        "s": lambda env, *args: ui.show_configuration(env)
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
        "local_search_type": "sa",
        "nb_loops": 5
    }

    while choice != "q":
        ui.show_menu()

        choice = ui.ask_choice((
            "p",
            "l easy", "l medium", "l hard",
            "t sa", "t mc",
            "n", "s",
            "q"
        )).lower()

        exec_choice(choice.split(), env)


if __name__ == "__main__":
    main()
