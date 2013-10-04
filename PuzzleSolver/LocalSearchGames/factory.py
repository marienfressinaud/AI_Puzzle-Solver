# -*- coding: utf-8 -*-

from min_conflicts_games import KQueensMC, GraphColorMC, MagicSquareMC
from simulated_annealing_games import KQueensSA, GraphColorSA, MagicSquareSA


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

        assert(local_search_type == "mc" or local_search_type == "sa")
        assert(
            game_type == "k-queens" or
            game_type == "graph-coloring" or
            game_type == "magic-square"
        )

        games = {
            "mc": {
                "k-queens": KQueensMC,
                "graph-coloring": GraphColorMC,
                "magic-square": MagicSquareMC
            },
            "sa": {
                "k-queens": KQueensSA,
                "graph-coloring": GraphColorSA,
                "magic-square": MagicSquareSA
            }
        }

        return games[local_search_type][game_type]()

    build = classmethod(build)
