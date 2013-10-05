# -*- coding: utf-8 -*-

from game_color_graph import GraphColorMC, GraphColorSA
from game_kqueens import KQueensMC, KQueensSA
from game_magic_square import MagicSquareMC, MagicSquareSA


class Factory():
    """
    Permits to build a game dynamically,
    corresponding to a certain local search type
    """

    __LIST_GAMES = {
        "mc": {
            "K-Queens": KQueensMC,
            "Graph Coloring": GraphColorMC,
            "Magic Square": MagicSquareMC
        },
        "sa": {
            "K-Queens": KQueensSA,
            "Graph Coloring": GraphColorSA,
            "Magic Square": MagicSquareSA
        }
    }

    def list_games(cls):
        list_mc = Factory.__LIST_GAMES["mc"]
        list_sa = Factory.__LIST_GAMES["sa"]

        return list(set(list_mc.keys()) & set(list_sa.keys()))

    def build(cls, game_type, local_search_type):
        """
        Unique class method. Create a game corresponding
        to game_type and local_search_type
        """

        assert(local_search_type in Factory.__LIST_GAMES)

        games = Factory.__LIST_GAMES[local_search_type]

        assert(game_type in games)

        return games[game_type]()

    build = classmethod(build)
    list_games = classmethod(list_games)
