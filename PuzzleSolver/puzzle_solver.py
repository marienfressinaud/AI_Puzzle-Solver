#!/bin/env python2
# -*- coding: utf-8 -*-

from LocalSearchGames.factory import Factory
import ui

def run_game(game_type, local_search_type, level):
    """
    Function which runs a game according to the current configuration
    """

    game = Factory.build(game_type, local_search_type)

    game.generate(level)
    game.run()

def main():
    """
    Program entry point. Here is the main loop which waits for an exit
    """

    MIN_LOOPS = 1
    MAX_LOOPS = 2000

    choice = None
    level = "easy"
    local_search_type = "mc"
    nb_loops = 5

    while choice != 'q':
        ui.show_menu()

        try:
            choice = ui.ask_choice((
                'p',
                'l easy', 'l medium', 'l hard',
                't sa', 't mc',
                'n', 's',
                'q'
            )).lower()
        except EOFError:
            choice = 'q'

        if choice == 'p':
            game = ui.ask_game()

            for i in xrange(nb_loops):
                run_game(game, local_search_type, level)
        elif choice[0] == 'l':
            level = choice[2:]
        elif choice[0] == 't':
            local_search_type = choice[2:]
        elif choice == 'n':
            nb_loops = ui.ask_number_loops(MIN_LOOPS, MAX_LOOPS)
        elif choice == 's':
            ui.show_configuration(local_search_type, level, nb_loops)

if __name__ == "__main__":
    main()
