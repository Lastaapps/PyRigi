from typing import Set, Tuple
from pyrigi.data_type import Edge
from pyrigi.graph import Graph
import pyrigi.graphDB as graphs
from pyrigi.exception import LoopError

import pytest
from sympy import Matrix


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(2),
        graphs.Complete(3),
        graphs.Complete(4),
        graphs.CompleteBipartite(3, 3),
        graphs.CompleteBipartite(3, 4),
        graphs.CompleteBipartite(4, 4),
        graphs.Diamond(),
        graphs.K33plusEdge(),
        graphs.ThreePrism(),
        graphs.ThreePrismPlusEdge(),
    ],
)
def test_rigid_in_d2(graph):
    assert graph.is_rigid(dim=2, combinatorial=True)
    assert graph.is_rigid(dim=2, combinatorial=False)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.CompleteBipartite(1, 3),
        graphs.CompleteBipartite(2, 3),
        graphs.Cycle(4),
        graphs.Cycle(5),
        graphs.Path(3),
        graphs.Path(4),
    ],
)
def test_not_rigid_in_d2(graph):
    assert not graph.is_rigid(dim=2, combinatorial=True)
    assert not graph.is_rigid(dim=2, combinatorial=False)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.CompleteBipartite(1, 3),
        graphs.CompleteBipartite(2, 3),
        graphs.CompleteBipartite(3, 3),
        graphs.Complete(2),
        graphs.Complete(3),
        graphs.Cycle(4),
        graphs.Cycle(5),
        graphs.Diamond(),
        graphs.Path(3),
        graphs.Path(4),
        graphs.ThreePrism(),
    ],
)
def test_2_3_sparse(graph):
    assert graph.is_sparse(2, 3)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(4),
        graphs.CompleteBipartite(3, 4),
        graphs.CompleteBipartite(4, 4),
        graphs.K33plusEdge(),
        graphs.ThreePrismPlusEdge(),
    ],
)
def test_not_2_3_sparse(graph):
    assert not graph.is_sparse(2, 3)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(2),
        graphs.Complete(3),
        graphs.CompleteBipartite(3, 3),
        graphs.Diamond(),
        graphs.ThreePrism(),
    ],
)
def test_2_3_tight(graph):
    assert graph.is_tight(2, 3)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(4),
        graphs.CompleteBipartite(1, 3),
        graphs.CompleteBipartite(2, 3),
        graphs.CompleteBipartite(3, 4),
        graphs.CompleteBipartite(4, 4),
        graphs.Cycle(4),
        graphs.Cycle(5),
        graphs.K33plusEdge(),
        graphs.Path(3),
        graphs.Path(4),
        graphs.ThreePrismPlusEdge(),
    ],
)
def test_not_2_3_tight(graph):
    assert not graph.is_tight(2, 3)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(2),
        graphs.Complete(3),
        graphs.CompleteBipartite(3, 3),
        graphs.Diamond(),
        graphs.ThreePrism(),
    ],
)
def test_min_rigid_in_d2(graph):
    assert graph.is_min_rigid(dim=2, combinatorial=True)
    assert graph.is_min_rigid(dim=2, combinatorial=False)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(4),
        graphs.CompleteBipartite(1, 3),
        graphs.CompleteBipartite(2, 3),
        graphs.CompleteBipartite(3, 4),
        graphs.CompleteBipartite(4, 4),
        graphs.Cycle(4),
        graphs.Cycle(5),
        graphs.K33plusEdge(),
        graphs.Path(3),
        graphs.Path(4),
        graphs.ThreePrismPlusEdge(),
    ],
)
def test_not_min_rigid_in_d2(graph):
    assert not graph.is_min_rigid(dim=2, combinatorial=True)
    assert not graph.is_min_rigid(dim=2, combinatorial=False)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.Complete(2),
        graphs.Complete(3),
        graphs.Complete(4),
        graphs.CompleteBipartite(3, 4),
        graphs.CompleteBipartite(4, 4),
        graphs.K33plusEdge(),
        graphs.ThreePrismPlusEdge(),
    ],
)
def test_globally_rigid_in_d2(graph):
    assert graph.is_globally_rigid(dim=2)


@pytest.mark.parametrize(
    "graph",
    [
        graphs.CompleteBipartite(1, 3),
        graphs.CompleteBipartite(2, 3),
        graphs.CompleteBipartite(3, 3),
        graphs.Cycle(4),
        graphs.Cycle(5),
        graphs.Diamond(),
        graphs.Path(3),
        graphs.Path(4),
        graphs.ThreePrism(),
    ],
)
def test_not_globally_in_d2(graph):
    assert not graph.is_globally_rigid(dim=2)


@pytest.mark.slow
def test_min_max_rigid_subgraphs():
    G = Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, "a", "b"])
    G.add_edges_from(
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 0),
            (0, 3),
            (1, 4),
            (2, 5),
            (0, "a"),
            (0, "b"),
            ("a", "b"),
        ]
    )
    max_subgraphs = G.max_rigid_subgraphs()
    assert (
        len(max_subgraphs) == 2
        and len(max_subgraphs[0].vertex_list()) in [3, 6]
        and len(max_subgraphs[1].vertex_list()) in [3, 6]
        and len(max_subgraphs[0].edges) in [3, 9]
        and len(max_subgraphs[1].edges) in [3, 9]
    )
    min_subgraphs = G.min_rigid_subgraphs()
    print(min_subgraphs[0])
    print(min_subgraphs[1])
    assert (
        len(min_subgraphs) == 2
        and len(min_subgraphs[0].vertex_list()) in [3, 6]
        and len(min_subgraphs[1].vertex_list()) in [3, 6]
        and len(min_subgraphs[0].edges) in [3, 9]
        and len(min_subgraphs[1].edges) in [3, 9]
    )


@pytest.mark.parametrize(
    ("graph", "result"),
    [
        (graphs.Path(3), True),
        (graphs.Cycle(3), False),
        (graphs.Cycle(4), True),
        (graphs.Cycle(5), True),
        (graphs.Complete(5), False),
        (graphs.CompleteBipartite(3, 4), True),
        (graphs.Diamond(), False),
        (graphs.ThreePrism(), True),
        (graphs.ThreePrismPlusEdge(), False),
        (graphs.SmallestMinimallyRigitGraph(), True),
    ],
    ids=[
        "path",
        "cycle3",
        "cycle4",
        "cycle5",
        "complete5",
        "bipartite5",
        "diamond",
        "prism",
        "prismPlus",
        "minimallyRigid",
    ],
)
def test_sinlge_and_has_NAC_coloring(graph: Graph, result: bool):
    assert (graph.single_NAC_coloring() is not None) == result
    assert graph.has_NAC_coloring() == result


@pytest.mark.parametrize(
    ("graph", "result"),
    [
        (
            graphs.Path(3),
            set(),
        ),
        (
            graphs.Cycle(3),
            set([(0, 1, 2)]),
        ),
        (
            graphs.Cycle(4),
            set([(0, 1, 2, 3)]),
        ),
        (
            graphs.Cycle(5),
            set([(0, 1, 2, 3, 4)]),
        ),
        (
            graphs.Diamond(),
            set([(0, 1, 2), (0, 2, 3)]),
        ),
        (
            graphs.ThreePrism(),
            set([(0, 1, 2), (3, 4, 5)]),
        ),
        (
            graphs.ThreePrismPlusEdge(),
            set([(0, 1, 2), (3, 4, 5), (0, 2, 5), (0, 3, 5)]),
        ),
        (
            graphs.SmallestMinimallyRigitGraph(),
            set([(0, 1, 2), (0, 2, 3), (0, 1, 4, 3), (1, 2, 3, 4)]),
        ),
    ],
    ids=[
        "path",
        "cycle3",
        "cycle4",
        "cycle5",
        "diamond",
        "prism",
        "prismPlus",
        "minimallyRigid",
    ],
)
def test__find_cycles(graph, result: Set[Tuple]):
    res = Graph._find_cycles(graph, all=True)
    print(f"{res=}")
    assert res == result


@pytest.mark.parametrize(
    ("graph", "colorings_no"),
    [
        (graphs.Path(3), 2),
        (Graph.from_vertices_and_edges([0, 1, 2, 3], [(0, 1), (1, 2)]), 2),
        (graphs.Cycle(3), 0),
        (graphs.Cycle(4), 6),
        (graphs.Cycle(5), 20),
        (graphs.Complete(5), 0),
        (graphs.CompleteBipartite(1, 3), 6),
        (
            Graph.from_vertices_and_edges(
                [0, 1, 2, 3], [(0, 1), (0, 2), (0, 3), (2, 3)]
            ),
            2,
        ),
        (graphs.CompleteBipartite(1, 4), 14),
        (
            Graph.from_vertices_and_edges(
                [0, 1, 2, 3, 4], [(0, 1), (0, 2), (0, 3), (0, 4), (3, 4)]
            ),
            6,
        ),
        (graphs.CompleteBipartite(2, 3), 14),
        (graphs.CompleteBipartite(2, 4), 30),
        (graphs.CompleteBipartite(3, 3), 30),
        (graphs.CompleteBipartite(3, 4), 62),
        (graphs.Diamond(), 0),
        (graphs.ThreePrism(), 2),
        (graphs.ThreePrismPlusEdge(), 0),
        (graphs.SmallestMinimallyRigitGraph(), 2),
    ],
    ids=[
        "path",
        "path_and_single_vertex",
        "cycle3",
        "cycle4",
        "cycle5",
        "complete5",
        "bipartite1x3",
        "bipartite1x3-improved",
        "bipartite1x4",
        "bipartite1x4-improved",
        "bipartite2x3",
        "bipartite2x4",
        "bipartite3x3",
        "bipartite3x4",
        "diamond",
        "prism",
        "prismPlus",
        "minimallyRigid",
    ],
)
def test_NAC_colorings(graph, colorings_no: int):
    print(f"{graph=}")
    algorithm = ["naive", "cycles", "subgraphs"][2]
    coloringList = list(graph.NAC_colorings(algorithm=algorithm))
    print(f"{coloringList=}")

    for coloring in sorted([str(x) for x in coloringList]):
        print(coloring)

    assert len(coloringList) == colorings_no

    for coloring in coloringList:
        assert graph.is_NAC_coloring(coloring)


@pytest.mark.parametrize(
    ("graph", "coloring", "result"),
    [
        (
            graphs.SmallestMinimallyRigitGraph(),
            (set([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]), set([(1, 4), (3, 4)])),
            True,
        ),
        (
            graphs.SmallestMinimallyRigitGraph(),
            (set([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 4), (3, 4)]), set([])),
            False,
        ),
        (
            graphs.SmallestMinimallyRigitGraph(),
            (set([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 4)]), set([(3, 4)])),
            False,
        ),
        (
            graphs.SmallestMinimallyRigitGraph(),
            (set([(0, 1), (1, 2), (3, 0), (0, 2)]), set([(2, 3), (1, 4), (3, 4)])),
            False,
        ),
        (
            graphs.ThreePrism(),
            (
                set([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),
                set([(0, 3), (1, 4), (2, 5)]),
            ),
            True,
        ),
        # TODO more tests
    ],
)
def test_is_NAC_coloring(graph, coloring: Tuple[Set[Edge], Set[Edge]], result: bool):
    assert graph.is_NAC_coloring(coloring) == result


def test_str():
    G = Graph([[2, 1], [2, 3]])
    assert str(G) == "Graph with vertices [1, 2, 3] and edges [[1, 2], [2, 3]]"
    G = Graph([(chr(i + 67), i + 1) for i in range(3)] + [(i, i + 1) for i in range(3)])
    assert str(G) == (
        "Graph with vertices ['C', 1, 'D', 2, 'E', 3, 0] "
        "and edges [('C', 1), (1, 0), (1, 2), ('D', 2), (2, 3), ('E', 3)]"
    )
    G = Graph.from_vertices(["C", 1, "D", 2, "E", 3, 0])
    assert str(G) == "Graph with vertices ['C', 1, 'D', 2, 'E', 3, 0] and edges []"


def test_vertex_edge_lists():
    G = Graph([[2, 1], [2, 3]])
    assert G.vertex_list() == [1, 2, 3]
    assert G.edge_list() == [[1, 2], [2, 3]]
    G = Graph([(chr(i + 67), i + 1) for i in range(3)] + [(i, i + 1) for i in range(3)])
    assert set(G.vertex_list()) == set(["C", 1, "D", 2, "E", 3, 0])
    assert set(G.edge_list()) == set(
        [("C", 1), (1, 0), (1, 2), ("D", 2), (2, 3), ("E", 3)]
    )
    G = Graph.from_vertices(["C", 1, "D", 2, "E", 3, 0])
    assert set(G.vertex_list()) == set(["C", 2, "E", 1, "D", 3, 0])
    assert G.edge_list() == []


def test_adjacency_matrix():
    G = Graph()
    assert G.adjacency_matrix() == Matrix([])
    G = Graph([[2, 1], [2, 3]])
    assert G.adjacency_matrix() == Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert G.adjacency_matrix(vertex_order=[2, 3, 1]) == Matrix(
        [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
    )
    assert graphs.Complete(4).adjacency_matrix() == Matrix.ones(4) - Matrix.diag(
        [1, 1, 1, 1]
    )
    G = Graph.from_vertices(["C", 1, "D"])
    assert G.adjacency_matrix() == Matrix.zeros(3)
    G = Graph.from_vertices_and_edges(["C", 1, "D"], [[1, "D"], ["C", "D"]])
    assert G.adjacency_matrix(vertex_order=["C", 1, "D"]) == Matrix(
        [[0, 0, 1], [0, 0, 1], [1, 1, 0]]
    )
    M = Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert G.from_adjacency_matrix(M).adjacency_matrix() == M


@pytest.mark.parametrize(
    "graph, gint",
    [
        [graphs.Complete(2), 1],
        [graphs.Complete(3), 7],
        [graphs.Complete(4), 63],
        [graphs.CompleteBipartite(3, 4), 507840],
        [graphs.CompleteBipartite(4, 4), 31965120],
        [graphs.ThreePrism(), 29327],
    ],
)
def test_integer_representation(graph, gint):
    assert graph.to_int() == gint
    assert Graph.from_int(gint).is_isomorphic(graph)
    assert Graph.from_int(gint).to_int() == gint
    assert Graph.from_int(graph.to_int()).is_isomorphic(graph)


def test_integer_representation_fail():
    with pytest.raises(ValueError):
        Graph([]).to_int()
    with pytest.raises(ValueError):
        M = Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
        G = Graph.from_adjacency_matrix(M)
        G.to_int()
    with pytest.raises(ValueError):
        Graph.from_int(0)
    with pytest.raises(TypeError):
        Graph.from_int(1 / 2)
    with pytest.raises(TypeError):
        Graph.from_int(1.2)
    with pytest.raises(ValueError):
        Graph.from_int(-1)


@pytest.mark.parametrize(
    "method, params",
    [
        ["is_rigid", []],
        ["is_min_rigid", []],
        ["is_redundantly_rigid", []],
        ["is_vertex_redundantly_rigid", []],
        ["is_k_vertex_redundantly_rigid", [2]],
        ["is_k_redundantly_rigid", [2]],
        ["is_globally_rigid", []],
        ["is_Rd_dependent", []],
        ["is_Rd_independent", []],
        ["is_Rd_circuit", []],
        ["is_Rd_closed", []],
        ["max_rigid_subgraphs", []],
        ["min_rigid_subgraphs", []],
    ],
)
def test_loops(method, params):
    with pytest.raises(LoopError):
        G = Graph([[1, 2], [1, 1], [2, 3], [1, 3]])
        func = getattr(G, method)
        func(*params)
