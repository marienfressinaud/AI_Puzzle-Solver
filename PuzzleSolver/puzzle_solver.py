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


def exec_choice(choice, env):
    """
    Executes a command
    """

    if choice[0] == "p":
        game = ui.ask_game()
        run_games(game, env)
    elif choice[0] == "l":
        env["level"] = choice[1]
    elif choice[0] == "t":
        env["local_search_type"] = choice[1]
    elif choice[0] == "n":
        env["nb_loops"] = ui.ask_number_loops(MIN_LOOPS, MAX_LOOPS)
    else:
        ui.show_configuration(env)


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
