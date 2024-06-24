from __future__ import annotations

from itertools import pairwise
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from utils.geometric_graph.graph import GeometricGraph


Pt: TypeAlias = tuple[float, float]
Cycle: TypeAlias = list[Pt]


class CycleDecomposer:
    def __init__(self, graph: GeometricGraph, ccw_on_outer: bool = True):
        self.graph = graph
        self.ccw_on_outer = ccw_on_outer

    def decompose(self) -> list[Cycle]:
        edges = set(self.graph.edges())

        # add inverted edges as well
        edges |= {(v, u) for u, v in edges}

        # no self-loop allowed
        edges -= {(u, u) for u in self.graph.nodes()}

        # make rotors for each node
        nodes_to_rotors = {
            node: self.graph.get_rotor(node, in_ccw=self.ccw_on_outer)
            for node in self.graph.nodes()
            }

        def find_cycle(edge_init: tuple[Pt, Pt]) -> Cycle:
            """
            start traversing from init_edge until it returns back
            """

            edge_now = edge_init
            cycle_ = [*edge_now]
            while True:
                p1, p2 = edge_now
                rotor = nodes_to_rotors[p2]
                p_next = rotor.next(p1)
                edge_next = p2, p_next

                # Returned to initial edge. Terminate and return the cycle
                if edge_next == edge_init:
                    return cycle_
                # Continue until reach to initial edge
                else:
                    cycle_.append(p_next)
                    edge_now = edge_next

        cycles = []
        while edges:
            edge = edges.pop()
            cycle = find_cycle(edge)
            edges -= set(pairwise(cycle))
            cycles.append(cycle)
        return cycles
