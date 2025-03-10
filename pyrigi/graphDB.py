"""
This is a module for providing common types of graphs.
"""

import networkx as nx
from pyrigi.graph import Graph


def Cycle(n: int) -> Graph:
    """Return the cycle graph on n vertices."""
    return Graph(nx.cycle_graph(n))


def Complete(n: int) -> Graph:
    """Return the complete graph on n vertices."""
    return Graph(nx.complete_graph(n))


def Path(n: int) -> Graph:
    """Return the path graph with n vertices."""
    return Graph(nx.path_graph(n))


def CompleteBipartite(m: int, n: int) -> Graph:
    """Return the complete bipartite graph on m+n vertices."""
    return Graph(nx.complete_multipartite_graph(m, n))


def K33plusEdge() -> Graph:
    """Return the complete bipartite graph on 3+3 vertices with an extra edge."""
    G = CompleteBipartite(3, 3)
    G.add_edge(0, 1)
    return G


def Diamond() -> Graph:
    """Return the complete graph on 4 vertices minus an edge."""
    return Graph([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])


def ThreePrism() -> Graph:
    """Return the 3-prism graph."""
    return Graph(
        [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
    )


def ThreePrismPlusEdge() -> Graph:
    """Return the 3-prism graph with one extra edge."""
    return Graph(
        [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5), (0, 5)]
    )


def CubeWithDiagonal():
    """Return the graph given by the skeleton of the cube with a main diagonal."""
    return Graph(
        [(0, 1), (1, 2), (2, 3), (0, 3)]
        + [(4, 5), (5, 6), (6, 7), (4, 7)]
        + [(0, 4), (1, 5), (2, 6), (3, 7)]
        + [(0, 6)]
    )


def CompleteMinusOne(n: int) -> Graph:
    """Return the complete graph on n vertices minus one edge."""
    G = Complete(n)
    G.delete_edge((0, 1))
    return G


def Octahedral():
    """Return the graph given by the skeleton of an octahedron."""
    return Graph(
        [
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 4),
            (2, 5),
            (3, 4),
            (3, 5),
        ]
    )


def ThreePrismPlusTriangleOnSide():
    """Return the 3-prism graph where there is extra triangle on one of the connecting edges."""
    return Graph(
        [
            (0, 1),
            (1, 2),
            (0, 2),
            (3, 4),
            (4, 5),
            (3, 5),
            (0, 3),
            (1, 4),
            (2, 5),
            (0, 6),
            (3, 6),
        ]
    )


def DiamondWithZeroExtension():
    """
    Return the diamond graph with zero extension
    (the diamond with 2 extra connected edges from the opposite spikes).
    """
    return Graph(
        [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 4), (3, 4)],
    )


def SquareGrid2D(w: int, h: int):
    """
    Creates a square grid with width and height given.

    Parameters
    ----------
    w:
        width - no. of nodes in each column
    h:
        height - no. of nodes in each row
    ----------

    Example
    ----------
    For input w: 4, h: 2 you get this graph:

    0-1-2-3
    | | | |
    4-5-6-7
    ----------
    """
    G = Graph.from_vertices(range(w * h))
    for r in range(h):
        offset = r * w
        for c in range(offset, offset + w - 1):
            G.add_edge(c, c + 1)

        if r == 0:
            continue

        for c in range(offset, offset + w):
            G.add_edge(c - w, c)

    return G
