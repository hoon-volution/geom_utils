from shapely.geometry import Point, LineString, Polygon, GeometryCollection
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry
from shapely.ops import unary_union
from shapely.affinity import scale, translate

from .linestring_linestring import compute_linestrings_minkowski_sum
from .linestring_polygon import compute_linestring_polygon_minkowski_sum
from .polygon_polygon import compute_polygons_minkowski_sum
from ..constant import DEFAULT_TOL


def minkowski_sum(geom1: BaseGeometry, geom2: BaseGeometry, tol: float = DEFAULT_TOL) -> BaseGeometry:

    """
    computes minkowski sum of two geometries.
    tol is used as a parameters in a slight buffer when making patches, to prevent topological error.

    """

    if geom1.is_empty or geom2.is_empty:
        return GeometryCollection()

    # handle multipart geometries
    if isinstance(geom1, BaseMultipartGeometry):
        return unary_union([minkowski_sum(subgeom, geom2, tol) for subgeom in geom1.geoms])

    if isinstance(geom2, BaseMultipartGeometry):
        return unary_union([minkowski_sum(geom1, subgeom, tol) for subgeom in geom2.geoms])


    # type guard
    if not isinstance(geom1, (Point, LineString, Polygon)):
        raise TypeError(f'invalid type of the first argument: {type(geom1)}')

    if not isinstance(geom2, (Point, LineString, Polygon)):
        raise TypeError(f'invalid type of the second argument: {type(geom2)}')

    # for implementational convenience
    if (type(geom1), type(geom2)) in {(LineString, Point), (Polygon, Point), (Polygon, LineString)}:
        return minkowski_sum(geom2, geom1)

    # 1. (Point, *)
    if isinstance(geom1, Point):
        return translate(geom2, geom1.x, geom1.y)

    # 2. (LineString, *)
    elif isinstance(geom1, LineString):
        # 2-1. (LineString, LineString)
        if isinstance(geom2, LineString):
            return compute_linestrings_minkowski_sum(geom1, geom2, tol)
        # 2-2. (LineString, Polygon)
        else:
            return compute_linestring_polygon_minkowski_sum(geom1, geom2, tol)

    # 3. (Polygon, Polygon)
    else:
        return compute_polygons_minkowski_sum(geom1, geom2, tol)


def minkowski_difference(geom1: BaseGeometry, geom2: BaseGeometry, tol: float = DEFAULT_TOL) -> BaseGeometry:
    geom2_negated = scale(geom2, -1, -1, origin=(0, 0))
    return minkowski_sum(geom1, geom2_negated, tol)
