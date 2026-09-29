"""Exact J77 symmetry chamber and supporting-face-plane partition."""
import hashlib
import json
from model import C1, C5, FACES, VERTICES
from q5 import Q, add, cross, dot, scale, sub


def encode(x):
    return [str(x.a), str(x.b)]


def rotation(v, axis, cosine, sine_over_norm):
    return add(add(scale(cosine, v), scale((1-cosine)*dot(axis, v)/dot(axis, axis), axis)),
               scale(sine_over_norm, cross(axis, v)))


def chamber():
    axis = (Q(), C5, Q(1))
    radial0 = (Q(), Q(1), -C5)
    radial1 = rotation(radial0, axis, C1, Q(-1, 1)/4)
    H = add(axis, add(radial0, radial1))
    if not all(dot(H, v) > 0 for v in (axis, radial0, radial1)):
        raise ValueError("The projective slice is not positive on chamber rays")
    triangle = tuple(scale(1/dot(H, v), v) for v in (axis, radial0, radial1))
    if not all(dot(H, v) == 1 and v[1] > 0 for v in triangle):
        raise ValueError('Invalid bounded projective chamber')
    V = set(VERTICES)
    if {(-v[0], v[1], v[2]) for v in V} != V:
        raise ValueError('Base mirror is not a J77 symmetry')
    if {rotation(v, axis, Q(-1, 1)/4, Q(1)/2) for v in V} != V:
        raise ValueError('Fivefold rotation is not a J77 symmetry')
    if dot(axis, radial0) != 0 or dot(axis, radial1) != 0:
        raise ValueError('Invalid equatorial chamber rays')
    if dot(radial0, radial1) != C1*dot(radial0, radial0):
        raise ValueError('Chamber wedge is not exactly 36 degrees')
    return H, triangle


def face_planes():
    planes = set()
    for face in FACES:
        a, b, c = (VERTICES[i] for i in face[:3])
        n = cross(sub(b, a), sub(c, a))
        offset = dot(n, a)
        if offset < 0:
            n = scale(-1, n)
            offset = -offset
        if not offset > 0 or not all(dot(n, VERTICES[i]) == offset for i in face):
            raise ValueError('Invalid standard face')
        if not all(dot(n, v) <= offset for v in VERTICES):
            raise ValueError('A listed face is not supporting')
        first = next(x for x in n if x != 0)
        planes.add(tuple(x/first for x in n))
    return tuple(sorted(planes))


def area(poly, H):
    # Twice Euclidean signed area multiplied by ||H||; a common positive scale.
    return sum((dot(H, cross(a, b)) for a, b in zip(poly, poly[1:]+poly[:1])), Q())


def clip(poly, normal):
    out = []
    for a, b in zip(poly, poly[1:]+poly[:1]):
        da, db = dot(normal, a), dot(normal, b)
        if da >= 0:
            out.append(a)
        if da*db < 0:
            out.append(add(a, scale(da/(da-db), sub(b, a))))
    deduplicated = []
    for p in out:
        if not deduplicated or p != deduplicated[-1]:
            deduplicated.append(p)
    if len(deduplicated) > 1 and deduplicated[0] == deduplicated[-1]:
        deduplicated.pop()
    return tuple(deduplicated)


def partition():
    H, triangle = chamber()
    initial_area = area(triangle, H)
    if initial_area <= 0:
        raise ValueError('Initial projective triangle orientation failed')
    polygons = [triangle]
    planes = face_planes()
    for plane in planes:
        next_polygons = []
        for poly in polygons:
            children = [clip(poly, plane), clip(poly, scale(-1, plane))]
            children = [p for p in children if len(p) >= 3 and area(p, H) > 0]
            # If the entire polygon lies in a cutting plane, both clips would
            # retain it; positive two-dimensional area excludes that case.
            if sum((area(p, H) for p in children), Q()) != area(poly, H):
                raise ValueError('Exact half-plane split does not preserve area')
            next_polygons.extend(children)
        polygons = next_polygons
    if sum((area(p, H) for p in polygons), Q()) != initial_area:
        raise ValueError('Final exact coverage area failed')
    triangles = [tuple((p[0], p[i], p[i+1])) for p in polygons for i in range(1, len(p)-1)]
    # Remove zero-area fan pieces caused by collinear boundary vertices.
    triangles = [t for t in triangles if area(t, H) > 0]
    if sum((area(t, H) for t in triangles), Q()) != initial_area:
        raise ValueError('Fan triangulation area failed')
    vertices = sorted({v for p in polygons for v in p})
    cells = [[[encode(x) for x in v] for v in p] for p in polygons]
    digest = hashlib.sha256(json.dumps(cells, separators=(',', ':')).encode()).hexdigest()
    return {'status': 'exact_projective_chamber_partition',
            'agent': 'six-rupert-2', 'role': 'researcher',
            'H': [encode(x) for x in H],
            'initial_triangle': [[encode(x) for x in v] for v in triangle],
            'face_count_checked': len(FACES), 'distinct_unoriented_face_planes': len(planes),
            'polygon_count': len(polygons), 'polygon_sizes': [len(p) for p in polygons],
            'positive_area_fan_triangle_count': len(triangles),
            'distinct_partition_vertex_count': len(vertices),
            'cells_sha256': digest, 'polygons': cells,
            'triangles': [[[encode(x) for x in v] for v in t] for t in triangles]}
