import numpy as np
from typing import TypeAlias, Iterable
from utils.vector_relation import VectorRelation
from utils.iteration import cyclic_pairwise


Pt: TypeAlias = tuple[float, float]


class NodeRotor:
    """
    Stores cyclic ordering on a node, with respect to angle.
    """

    def __init__(self, node: Pt, neighbors: Iterable[Pt], in_ccw: bool = True):
        self.node = node

        # remove redundant repetition or self-loop
        neighbors = set(neighbors) - {node}

        def _get_relative_angle(neighbor: Pt) -> float:
            # relative angle with respect to the self.node
            vector = np.array(neighbor) - np.array(self.node)
            x_vec = (1, 0)
            return VectorRelation(x_vec, vector).get_angle()

        # sort by angles
        sorted_neighbors = sorted(
            neighbors,
            key=_get_relative_angle,
            reverse=not in_ccw
            )

        self.cyclic_ordering = {
            p1: p2
            for p1, p2 in cyclic_pairwise(sorted_neighbors)
            }

    def next(self, neighbor: Pt) -> Pt:
        return self.cyclic_ordering[neighbor]
