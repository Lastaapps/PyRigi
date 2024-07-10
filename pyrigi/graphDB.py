"""
This is a module for providing common types of graphs.
"""

import networkx as nx
from pyrigi.graph import Graph


def Cycle(n: int):
    """Return the cycle graph on n vertices."""
    return Graph(nx.cycle_graph(n))


def Complete(n: int):
    """Return the complete graph on n vertices."""
    return Graph(nx.complete_graph(n))


def Path(n: int):
    """Return the path graph with n vertices."""
    return Graph(nx.path_graph(n))


def CompleteBipartite(m: int, n: int):
    """Return the complete bipartite graph on m+n vertices."""
    return Graph(nx.complete_multipartite_graph(m, n))


def K33plusEdge():
    """Return the complete bipartite graph on 3+3 vertices with an extra edge."""
    G = CompleteBipartite(3, 3)
    G.add_edge(0, 1)
    return G


def Diamond():
    """Return the complete graph on 4 vertices minus an edge."""
    return Graph([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])


def ThreePrism():
    """Return the 3-prism graph."""
    return Graph(
        [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
    )


def ThreePrismPlusEdge():
    """Return the 3-prism graph with one extra edge."""
    return Graph(
        [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5), (0, 5)]
    )


def DiamondWithZeroExtension():
    """
    Return the diamond graph with zero extension
    (the diamond with 2 extra connected edges from the opposite spikes).
    """
    return Graph(
        [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 4), (3, 4)],
    )


def ThreeSquares():
    """
    3 squares in a row, used for cartesian NAC coloring testing

    0-1-2-3
    | | | |
    4-5-6-7
    """
    return Graph.from_vertices_and_edges(
        [0, 1, 2, 3, 4, 5, 6, 7],
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (4, 5),
            (5, 6),
            (6, 7),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ],
    )
