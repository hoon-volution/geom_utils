from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import unary_union
from itertools import pairwise, product
from typing import TypeAlias
import numpy as np


Point2D: TypeAlias = tuple[float, float]
Segment: TypeAlias = tuple[Point2D, Point2D]


def compute_linestrings_minkowski_sum(ls1: LineString, ls2: LineString, tol: float) -> Polygon:
    edges1 = pairwise(ls1.coords)
    edges2 = pairwise(ls2.coords)

    def slight_buffer(geom: LineString | Polygon) -> Polygon:
        r = tol
        if geom.is_empty:
            return geom
        if isinstance(geom, LineString):
            d = r * geom.length
            return geom.buffer(d, join_style=2)
        elif isinstance(geom, Polygon):
            d = max(r, r * geom.area ** 0.5)

            while True:
                res = geom.buffer(d, join_style=2)
                if not res.is_empty:
                    return res
                d *= 1.001
        else:
            raise TypeError

    def get_direction(seg: Segment) -> Point2D:
        return np.array([-1, 1]) @ seg

    def are_parallel(seg1: Segment, seg2: Segment):
        direction1 = get_direction(seg1)
        direction2 = get_direction(seg2)
        det = np.linalg.det([direction1, direction2])
        return np.isclose(det, 0)

    def make_patch(seg1: Segment, seg2: Segment):
        p1, p2 = map(np.array, seg1)
        q1, q2 = map(np.array, seg2)
        if are_parallel(seg1, seg2):
            v = get_direction(seg1)
            sorting_key = lambda p: np.dot(p - p1, v)
            points = [
                p1 + q1, p1 + q2, p2 + q2, p2 + q1
            ]
            sorted_points = sorted(points, key=sorting_key)
            p_start, *_, p_end = sorted_points
            res = LineString([p_start, p_end])

        else:
            res = Polygon(
                [
                    p1 + q1, p1 + q2, p2 + q2, p2 + q1
                ]
            )

        res = slight_buffer(res)

        return res

    patches = [
        make_patch(seg1, seg2)
        for seg1, seg2 in product(edges1, edges2)
    ]

    patches_union = unary_union(patches)
    patches_union = patches_union.buffer(0)
    if isinstance(patches_union, MultiPolygon):
        patches_union = max(patches_union.geoms, key=lambda x: x.area)
    return patches_union
