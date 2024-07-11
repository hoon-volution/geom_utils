from functools import lru_cache
from .minkowski import minkowski_difference
from .constant import DEFAULT_TOL
from shapely import LineString, Polygon


@lru_cache
def get_colliding_space(
        linestring_ref: LineString,
        linestring_domain: LineString,
        tol: float = DEFAULT_TOL
        ) -> Polygon:
    """
    returns the region {(x, y): linestring_ref + (x, y) intersects linestring_domain}
    """
    return minkowski_difference(linestring_domain, linestring_ref, tol)
