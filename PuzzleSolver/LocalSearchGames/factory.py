# -*- coding: utf-8 -*-

from min_conflicts_games import KQueensMC, GraphColorMC
from simulated_annealing_games import KQueensSA, GraphColorSA

class Factory():
    """
    Permits to build a game dynamically,
    corresponding to a certain local search type
    """

    def build(cls, game_type, local_search_type):
        """
        Unique class method. Create a game corresponding
        to game_type and local_search_type
        """

        game = None

        if game_type == "k-queens" and local_search_type == "sa":
            game = KQueensSA()
        elif game_type == "k-queens" and local_search_type == "mc":
            game = KQueensMC()
        elif game_type == "graph-coloring" and local_search_type == "sa":
            game = GraphColorSA()
        elif game_type == "graph-coloring" and local_search_type == "mc":
            game = GraphColorMC()
        elif game_type == "TODO" and local_search_type == "sa":
            pass # not chosen yet
        elif game_type == "TODO" and local_search_type == "mc":
            pass # not chosen yet

        assert(game is not None)

        return game

    build = classmethod(build)
