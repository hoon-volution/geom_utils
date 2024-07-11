from functools import lru_cache

from shapely import Point, LineString, Polygon, GeometryCollection, unary_union, intersection_all
from shapely.affinity import translate
from shapely.geometry.base import BaseGeometry, BaseMultipartGeometry

from .linestring_linestring import compute_linestrings_free_interior_space
from .linestring_polygon import compute_linestring_polygon_free_interior_space
from .polygon_polygon import compute_polygons_free_interior_space
from ..constant import DEFAULT_TOL

@lru_cache
def get_free_interior_space(geom: BaseGeometry, domain: BaseGeometry, tol: float = DEFAULT_TOL) -> BaseGeometry:
    """
    returns the region {(x, y): geom + (x, y) is contained in domain}
    """

    if isinstance(geom, BaseMultipartGeometry):
        return intersection_all(
            [get_free_interior_space(subgeom, domain)
             for subgeom in geom.geoms]
            )

    if isinstance(domain, BaseMultipartGeometry):
        return unary_union(
            [get_free_interior_space(geom, subdomain)
             for subdomain in domain.geoms]

            )
    # type guard
    if not isinstance(geom, (Point, LineString, Polygon)):
        raise TypeError(f"geom argument must be a shapely geometry but we've got: {type(geom)}")

    if not isinstance(domain, (Point, LineString, Polygon)):
        raise TypeError(f"domain argument must be a shapely geometry but we've got: {type(domain)}")

    # invalid geometry types: hierarchy reversed
    if (type(geom), type(domain)) in {(LineString, Point), (Polygon, Point), (Polygon, LineString)}:
        return GeometryCollection()

    # 1. (Point, *)
    if isinstance(geom, Point):
        return translate(domain, -geom.x, -geom.y)

    # 2. (LineString, *)
    elif isinstance(geom, LineString):
        # 2-1. (LineString, LineString)
        if isinstance(domain, LineString):
            return compute_linestrings_free_interior_space(geom, domain, tol)

        # 2-2. (LineString, Polygon)
        else:
            return compute_linestring_polygon_free_interior_space(geom, domain, tol)

    # 3. (Polygon, Polygon)
    else:
        return compute_polygons_free_interior_space(geom, domain, tol)