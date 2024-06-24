import networkx as nx
from typing import TypeAlias
from utils.geometric_graph.node_rotor import NodeRotor
from utils.geometric_graph.cycle import CycleDecomposer


Pt: TypeAlias = tuple[float, float]
Cycle: TypeAlias = list[Pt]


class GeometricGraph(nx.Graph):
    """
    Assumes its nodes are 2D points in Euclidean Plane
    """
    def get_rotor(self, node: Pt, in_ccw: bool = True) -> NodeRotor:
        neighbors = nx.all_neighbors(self, node)
        return NodeRotor(node, neighbors, in_ccw)

    def get_cycle_decomposition(self, ccw_on_outer: bool = True) -> list[Cycle]:
        return CycleDecomposer(self, ccw_on_outer=ccw_on_outer).decompose()


class GeometricDiGraph(GeometricGraph, nx.DiGraph):
    ...
