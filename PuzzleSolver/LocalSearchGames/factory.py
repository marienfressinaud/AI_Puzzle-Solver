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

        assert(local_search_type == "mc" or local_search_type == "sa")
        assert(
            game_type == "k-queens" or
            game_type == "graph-coloring" or
            game_type == "TODO"
        )

        games = {
            "mc": {
                "k-queens": KQueensMC,
                "graph-coloring": GraphColorMC,
                "TODO": None
            },
            "sa": {
                "k-queens": KQueensSA,
                "graph-coloring": GraphColorSA,
                "TODO": None
            }
        }

        return games[local_search_type][game_type]()

    build = classmethod(build)
