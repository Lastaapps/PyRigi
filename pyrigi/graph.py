"""
Module for rigidity related graph properties.
"""
from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from random import randrange

import networkx as nx
from sympy import Matrix

from pyrigi.data_type import Vertex, Edge, GraphType, List, Any


class Graph(nx.Graph):
    '''
    Class representing a graph.
    '''

    def __str__(self) -> str:
        return 'Vertices: ' + str(self.vertices()) + ',\t'\
            + 'Edges: ' + str(self.edges)

    @classmethod
    def from_vertices_and_edges(
            cls,
            vertices: List[Vertex],
            edges: List[Edge]) -> GraphType:
        G = Graph()
        G.add_nodes_from(vertices)
        for edge in edges:
            if len(edge) != 2 or \
                    not edge[0] in G.nodes or \
                    not edge[1] in G.nodes:
                raise TypeError(
                    "Edge {edge} does not have the correct format or has adjacent vertices the graph does not contain")
            G.add_edge(*edge)
        return G

    @classmethod
    def from_vertices(cls, vertices: List[Vertex]) -> GraphType:
        return Graph.from_vertices_and_edges(vertices, [])

    @classmethod
    def complete_graph(cls, n: int) -> GraphType:
        if not isinstance(n, int) or n < 1:
            raise TypeError("n needs to be a positive integer")
        vertices = range(n)
        edges = combinations(vertices, 2)
        return Graph.from_vertices_and_edges(vertices, edges)

    @classmethod
    def complete_graph_on_vertices(cls, vertices: List[Vertices]) -> GraphType:
        edges = combinations(vertices, 2)
        return Graph.from_vertices_and_edges(vertices, edges)

    def vertices(self) -> List[Vertex]:
        return list(self.nodes)

    def delete_vertex(self, vertex: Vertex) -> None:
        self.remove_node(vertex)

    def delete_vertices(self, vertices: List[Vertex]) -> None:
        self.remove_nodes_from(vertices)

    def delete_edge(self, edge: Edge) -> None:
        self.remove_edge(*edge)

    def delete_edges(self, edges: List[Edge]) -> None:
        self.remove_edges_from(edges)

    def vertex_connectivity(self) -> int:
        return nx.node_connectivity(self)

    def is_sparse(self, K: int, L: int) -> bool:
        r"""
        Check whether the graph is :prf:ref:`(K, L)-sparse <def-kl-sparse-tight>`.
        """
        if not (isinstance(K, int) and isinstance(L, int)):
            raise TypeError("K and L need to be integers!")

        for j in range(K, len(self.vertices()) + 1):
            for vertex_set in combinations(self.vertices(), j):
                G = self.subgraph(vertex_set)
                if len(G.edges) > K * len(G.nodes) - L:
                    return False
        return True

    def is_tight(self, K: int, L: int) -> bool:
        r"""
        Check whether the graph is :prf:ref:`(K, L)-tight <def-kl-sparse-tight>`.
        """
        return self.is_sparse(K, L) and \
            len(self.edges) <= K * len(self.nodes) - L

    def zero_extension(self, vertices: List[Vertex], dim: int = 2) -> None:
        """
        Notes
        -----
        Modifies self only when explicitly required.
        """
        raise NotImplementedError()

    def one_extension(
            self,
            vertices: List[Vertex],
            edge: Edge,
            dim: int = 2) -> None:
        """
        Notes
        -----
        Modifies self only when explicitly required.
        """
        raise NotImplementedError()

    def k_extension(
            self,
            k: int,
            vertices: List[Vertex],
            edges: Edge,
            dim: int = 2) -> None:
        """
        Notes
        -----
        Modifies self only when explicitly required.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def all_k_extensions(self, k: int, dim: int = 2) -> None:
        """
        Return list of all possible k-extensions.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def extension_sequence(self, dim: int = 2) -> Any:
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def is_vertex_redundantly_rigid(self, dim: int = 2) -> bool:
        """
        Check whether the graph is :prf:ref:`vertex redundantly (generically) dim-rigid <def-minimally-redundantly-rigid-graph>`.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        return self.is_k_vertex_redundantly_rigid(1, dim)

    def is_k_vertex_redundantly_rigid(self, k: int, dim: int = 2) -> bool:
        """
        Check whether the graph is :prf:ref:`k-vertex redundantly (generically) dim-rigid <def-minimally-redundantly-rigid-graph>`.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        if not isinstance(k, int):
            raise TypeError(f"k needs to be a nonnegative integer, but is {k}!")
        for vertex_set in combinations(self.vertices(), k):
            G = deepcopy(self)
            G.delete_vertices(vertex_set)
            if not G.is_rigid(dim):
                return False
        return True

    def is_redundantly_rigid(self, dim: int = 2) -> bool:
        """
        Check whether the graph is :prf:ref:`redundantly (generically) dim-rigid <def-minimally-redundantly-rigid-graph>`.
        """
        return self.is_k_redundantly_rigid(1, dim)

    def is_k_redundantly_rigid(self, k: int, dim: int = 2) -> bool:
        """
        Check whether the graph is :prf:ref:`k-redundantly (generically) dim-rigid <def-minimally-redundantly-rigid-graph>`.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        if not isinstance(k, int):
            raise TypeError(f"k needs to be a nonnegative integer, but is {k}!")
        for edge_set in combinations(self.edges, k):
            G = deepcopy(self)
            G.delete_edges(edge_set)
            if not G.is_rigid(dim):
                return False
        return True

    def is_rigid(self, dim: int = 2, combinatorial: bool = True) -> bool:
        """
        Check whether the graph is :prf:ref:`(generically) dim-rigid <def-gen-rigid>`.

        Notes
        -----
         * dim=1: Connectivity
         * dim=2: Pebble-game/(2,3)-rigidity
         * dim>=1: Probabilistic Rigidity Matrix (maybe symbolic?)
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        if not isinstance(combinatorial, bool):
            raise TypeError(
                f"combinatorial determines the method of rigidity-computation. It needs to be a Boolean.")

        elif dim == 1:
            return self.is_connected()
        elif dim == 2 and combinatorial:
            deficiency = -(2 * len(self.vertices()) - 3) + len(self.edges)
            if deficiency < 0:
                return False
            else:
                for edge_subset in combinations(self.edges, deficiency):
                    H = self.edge_subgraph(
                        [edge for edge in self.edges if edge not in edge_subset])
                    if H.is_tight(2, 3):
                        return True
                return False
        elif not combinatorial:
            from pyrigi.framework import Framework
            N = 10 * len(self.vertices())**2 * dim
            realization = {
                vertex: [
                    randrange(
                        1,
                        N) for _ in range(
                        0,
                        dim)] for vertex in self.vertices()}
            F = Framework(self, realization, dim)
            return F.is_infinitesimally_rigid()
        else:
            raise ValueError(
                f"The Dimension for combinatorial computation must be either 1 or 2, but is {dim}")

    def is_minimally_rigid(
            self,
            dim: int = 2,
            combinatorial: bool = True) -> bool:
        """
        Check whether the graph is :prf:ref:`minimally (generically) dim-rigid <def-minimally-redundantly-rigid-graph>`.

        Notes
        -----
         * dim=1: Tree
         * dim=2: Pebble-game/(2,3)-tight
         * dim>=1: Probabilistic Rigidity Matrix (maybe symbolic?)
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        if not isinstance(combinatorial, bool):
            raise TypeError(
                f"combinatorial determines the method of rigidity-computation. It needs to be a Boolean.")

        elif dim == 1:
            return self.is_tree()
        elif dim == 2 and combinatorial:
            return self.is_tight(2, 3)
        elif not combinatorial:
            from pyrigi.framework import Framework
            N = 10 * len(self.vertices())**2 * dim
            realization = {
                vertex: [
                    randrange(
                        1,
                        N) for _ in range(
                        0,
                        dim)] for vertex in self.vertices()}
            F = Framework(self, realization, dim)
            return F.is_minimally_infinitesimally_rigid()
        else:
            raise ValueError(
                f"The dimension for combinatorial computation must be either 1 or 2, but is {dim}")

    def is_globally_rigid(self, dim: int = 2) -> bool:
        """
        Notes
        -----
         * dim=1: 2-connectivity
         * dim=2: redundantly rigid+3-connected
         * dim>=3: Randomized Rigidity Matrix => Stress (symbolic maybe?)
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")

        elif dim == 1:
            return self.vertex_connectivity() >= 2
        elif dim == 2:
            return self.is_redundantly_rigid() and self.vertex_connectivity() >= 3
        else:
            from pyrigi.framework import Framework
            # Random sampling from [1,N] for N depending quadratically on number
            # of vertices.
            raise NotImplementedError()

    def is_Rd_dependent(self, dim: int = 2) -> bool:
        """
        Notes
        -----
         * dim=1: Graphic Matroid
         * dim=2: not (2,3)-sparse
         * dim>=1: Compute the rank of the rigidity matrix and compare with edge count
        """
        raise NotImplementedError()

    def is_Rd_independent(self, dim: int = 2) -> bool:
        """
        Notes
        -----
         * dim=1: Graphic Matroid
         * dim=2: (2,3)-sparse
         * dim>=1: Compute the rank of the rigidity matrix and compare with edge count
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def is_Rd_circuit(self, dim: int = 2) -> bool:
        """
        Notes
        -----
         * dim=1: Graphic Matroid
         * dim=2: Remove any edge and it becomes sparse (sparsity for every subgraph except whole graph?)
         * dim>=1: Dependent + Remove every edge and compute the rigidity matrix' rank
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def is_Rd_closed(self, dim: int = 2) -> bool:
        """
        Notes
        -----
         * dim=1: Graphic Matroid
         * dim=2: ??
         * dim>=1: Adding any edge does not increase the rigidity matrix rank
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")
        raise NotImplementedError()

    def maximal_rigid_subgraphs(self, dim: int = 2) -> List[GraphType]:
        """
        List vertex-maximal rigid subgraphs.

        We consider a subgraph
        to be maximal, if it is maximal with respect to subgraph-inclusion.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")

        if len(self.vertices()) <= 2:
            return []
        if self.is_rigid():
            return [self]
        maximal_subgraphs = []
        for vertex_subset in combinations(
            self.vertices(), len(
                self.vertices()) - 1):
            G = self.subgraph(vertex_subset)
            maximal_subgraphs = [
                j for i in [
                    maximal_subgraphs,
                    G.maximal_rigid_subgraphs(dim)] for j in i]
        clean_list = []
        for i in range(0, len(maximal_subgraphs)):
            iso_bool = False
            for j in range(i + 1, len(maximal_subgraphs)):
                if maximal_subgraphs[i].is_isomorphic(maximal_subgraphs[j]):
                    iso_bool = True
                    break
            if not iso_bool:
                clean_list.append(maximal_subgraphs[i])
        return clean_list

    def minimal_rigid_subgraphs(self, dim: int = 2) -> List[GraphType]:
        """
        List vertex-minimal non-trivial rigid subgraphs.

        We consider a subgraph
        to be minimal, if it minimal with respect to subgraph-inclusion.
        """
        if not isinstance(dim, int) or dim < 1:
            raise TypeError(
                f"The dimension needs to be a positive integer, but is {dim}!")

        minimal_subgraphs = []
        if len(self.vertices()) <= 2:
            return []
        elif len(self.vertices()) == 3 and self.is_rigid():
            return [self]
        elif len(self.vertices()) == 3:
            return []
        for vertex_subset in combinations(
            self.vertices(), len(
                self.vertices()) - 1):
            G = self.subgraph(vertex_subset)
            subgraphs = G.minimal_rigid_subgraphs(dim)
            if len(subgraphs) == 0 and G.is_rigid():
                minimal_subgraphs.append(G)
            else:
                minimal_subgraphs = [
                    j for i in [
                        minimal_subgraphs,
                        G.minimal_rigid_subgraphs(dim)] for j in i]
        clean_list = []
        for i in range(0, len(minimal_subgraphs)):
            iso_bool = False
            for j in range(i + 1, len(minimal_subgraphs)):
                if minimal_subgraphs[i].is_isomorphic(minimal_subgraphs[j]):
                    iso_bool = True
                    break
            if not iso_bool:
                clean_list.append(minimal_subgraphs[i])
        return clean_list

    def is_isomorphic(self, graph: GraphType) -> bool:
        return nx.is_isomorphic(self, graph)

    def graph_to_int(self) -> int:
        r"""
        Return the integer representation of the graph.

        The graph integer representation is the integer
        whose binary expansion is given by the sequence
        obtained by concatenation of the rows
        of the upper triangle of the adjacency matrix,
        excluding the diagonal.

        TODO
        ----
        Implement taking canonical before computing the integer representation.
        Tests.
        Specify order of vertices.
        """
        M = nx.adjacency_matrix(self, weight=None).todense()
        upper_diag = [str(b)
                      for i, row in enumerate(M.tolist())
                      for b in row[i + 1:]]
        return int(''.join(upper_diag), 2)

    @classmethod
    def from_int(cls) -> GraphType:
        raise NotImplementedError()

    def adjacency_matrix(
            self,
            vertex_order: List[Vertex] = None) -> Matrix:
        """
        Return the adjacency matrix.
        """
        try:
            if vertex_order is None:
                vertex_order = sorted(self.vertices())
            else:
                if not set(
                        self.vertices()) == set(vertex_order) or not len(
                        self.vertices()) == len(vertex_order):
                    raise IndexError(
                        "The vertex_order needs to contain the same vertices as the graph!")
        except TypeError as error:
            vertex_order = self.vertices()
        return nx.adjacency_matrix(
            self, nodelist=vertex_order, weight=None).todense()