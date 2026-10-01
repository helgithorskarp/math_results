"""Definition-level exact planar hulls and physical distance signatures."""
from q5 import Q, add, cross, dot, scale, sub


def projection(p, d):
    return sub(p, scale(dot(p, d)/dot(d, d), d))


def hull_indices(vertices, d):
    basis = [(Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))]
    u = next(cross(d, e) for e in basis if dot(cross(d, e), cross(d, e)) != 0)
    v = cross(d, u)
    points = {}
    for i, p in enumerate(vertices):
        points.setdefault((dot(u, p), dot(v, p)), i)
    points = sorted(points.items())

    def turn(a, b, c):
        return ((b[0][0]-a[0][0])*(c[0][1]-a[0][1])
                -(b[0][1]-a[0][1])*(c[0][0]-a[0][0]))

    def half(items):
        result = []
        for p in items:
            while len(result) > 1 and turn(result[-2], result[-1], p) <= 0:
                result.pop()
            result.append(p)
        return result

    return tuple(i for _, i in half(points)[:-1]+half(points[::-1])[:-1])


def squared_distance(a, b, d):
    p = sub(a, b)
    return dot(p, p)-dot(p, d)*dot(p, d)/dot(d, d)


def congruences(vertices, a, b):
    """All cyclic/reversed boundary bijections preserving physical distance."""
    ha, hb = hull_indices(vertices, a), hull_indices(vertices, b)
    if len(ha) != len(hb):
        return ha, hb, []
    size = len(ha)
    da = [[squared_distance(vertices[i], vertices[j], a) for j in ha] for i in ha]
    db = [[squared_distance(vertices[i], vertices[j], b) for j in hb] for i in hb]
    result = []
    for direction in (-1, 1):
        for shift in range(size):
            perm = [(shift+direction*i) % size for i in range(size)]
            if all(da[i][j] == db[perm[i]][perm[j]] for i in range(size) for j in range(size)):
                result.append({'direction': direction, 'shift': shift,
                               'vertex_pairs': list(zip(ha, [hb[p] for p in perm]))})
    return ha, hb, result


def proper_lift(vertices, a_unit, b_unit, match):
    """Lift a planar boundary congruence to its unique proper spatial motion."""
    pairs = match['vertex_pairs']
    source = [projection(vertices[i], a_unit) for i, _ in pairs[:3]]
    target = [projection(vertices[j], b_unit) for _, j in pairs[:3]]
    p, r = sub(source[1], source[0]), sub(source[2], source[0])
    q, s = sub(target[1], target[0]), sub(target[2], target[0])
    pp, pr, rr = dot(p, p), dot(p, r), dot(r, r)
    det = pp*rr-pr*pr
    if det <= 0:
        raise RuntimeError('Independent plane basis required')

    def motion(x):
        alpha = (rr*dot(x, p)-pr*dot(x, r))/det
        beta = (pp*dot(x, r)-pr*dot(x, p))/det
        return add(add(scale(alpha, q), scale(beta, s)),
                   scale(match['direction']*dot(x, a_unit), b_unit))

    basis = [(Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))]
    columns = tuple(motion(e) for e in basis)
    translation = sub(target[0], motion(source[0]))
    return columns, translation
