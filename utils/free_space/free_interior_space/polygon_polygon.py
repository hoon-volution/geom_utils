from shapely import Point, Polygon, MultiPolygon, unary_union
from shapely.geometry.base import BaseMultipartGeometry
from ..colliding_space import get_colliding_space


def compute_polygons_free_interior_space(geom: Polygon, domain: Polygon, tol: float) -> Polygon | MultiPolygon:

    if geom.area > domain.area:
        return Polygon()

    # collding space of exteriors
    ext_ext_colliding_space = get_colliding_space(geom.exterior, domain.exterior, tol)

    # take interior of colliding space
    free_space_candidates = [Polygon(ring) for ring in ext_ext_colliding_space.interiors]
    free_space = unary_union(free_space_candidates).buffer(0)

    # iterate over interior rings of the domain to find additional forbidden spaces
    for domain_interior_ring in domain.interiors:
        ext_int_colliding_space = get_colliding_space(
            geom.exterior, domain_interior_ring, tol
        )
        forbidden_space = Polygon(ext_int_colliding_space.exterior)

        # iterate over interior rings of polygon_ref
        for ref_interior_ring in geom.interiors:
            if Polygon(ref_interior_ring).area < Polygon(domain_interior_ring).area:
                continue
            # allowed: domain_interior_ring is contained in ref_interior_ring
            int_int_colliding_space = get_colliding_space(
                ref_interior_ring, domain_interior_ring, tol
            )
            int_int_free_space = unary_union(
                [Polygon(ring) for ring in int_int_colliding_space.interiors]
            ).buffer(0)

            # exclude int-int free space from the forbidden space
            forbidden_space = (forbidden_space - int_int_free_space).buffer(0)

        # exclude forbidden space from free space
        free_space = (free_space - forbidden_space).buffer(0)

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