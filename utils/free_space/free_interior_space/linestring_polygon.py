from shapely import Point, LineString, Polygon, MultiPolygon, unary_union
from shapely.geometry.base import BaseMultipartGeometry
from ..colliding_space import get_colliding_space


def compute_linestring_polygon_free_interior_space(
        geom: LineString, domain: Polygon, tol: float) -> Polygon | MultiPolygon:
    exterior_coll_space = get_colliding_space(geom, domain.exterior, tol)
    free_space = unary_union(
        [Polygon(ext_int_ring) for ext_int_ring in exterior_coll_space.interiors]
    )
    for int_ring in domain.interiors:
        interior_coll_space = get_colliding_space(geom, int_ring, tol)
        free_space -= Polygon(interior_coll_space.exterior)

    def is_valid_free_space(free_space_candidate: Polygon) -> bool:
        p = geom.representative_point()
        q = free_space_candidate.representative_point()
        return Point(p.x + q.x, p.y + q.y).within(domain)

    # final filtration
    if free_space.is_empty:
        return free_space
    if isinstance(free_space, BaseMultipartGeometry):
        return unary_union([geom for geom in free_space.geoms if is_valid_free_space(geom)])
    elif is_valid_free_space(free_space):
        return free_space
    else:
        return Polygon()