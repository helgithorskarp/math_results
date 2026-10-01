"""Exact geometric computations for J74. Python 3.11+, standard library."""
import hashlib
import itertools
import json
import math
from fractions import Fraction
from functools import cmp_to_key
from pathlib import Path

from model import FACES, VERTICES, cupola_construction
from q5 import Q, add, cross, dot, scale, sub
from shadow import congruences, hull_indices, projection, proper_lift


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def absolute(x):
    return x if x.sign() >= 0 else -x


def canonical(d):
    for x in d:
        if x != 0:
            return scale(1/x, d)
    return None


def sign_enclosure(x):
    if x == 0:
        return 0
    for bits in (16, 32, 64, 128, 256, 512, 1024):
        den = 1 << bits
        lo = Fraction(math.isqrt(5*den*den), den)
        hi = lo+Fraction(1, den)
        a, b = sorted((x.a+x.b*lo, x.a+x.b*hi))
        if a > 0:
            return 1
        if b < 0:
            return -1
    raise RuntimeError('Sign enclosure unresolved')


def validate_model():
    v = VERTICES
    require(len(v) == len(set(v)) == 60, '60 distinct vertices')
    radius2 = Q(11, 4)/4
    require(all(dot(p, p) == radius2 for p in v), 'common radius')
    original, caps, gyrated, constructed, axes = cupola_construction()
    require(len(original) == 60, 'original RID vertex count')
    require([len(c) for c in caps] == [5, 5], 'two pentagonal caps')
    require(caps[0].isdisjoint(caps[1]), 'disjoint caps')
    require([len(c) for c in gyrated] == [5, 5], 'gyrated caps')
    require(constructed == set(v), 'independent cupola construction')
    require(len({frozenset(face) for face in FACES}) == 62, 'distinct complete facets')
    require(dot(sub(v[1], v[0]), cross(sub(v[2], v[0]), sub(v[8], v[0]))) != 0,
            'full-dimensional original hull')
    require(dot(axes[0], axes[1])/dot(axes[0], axes[0]) == -Q(0, 1)/5,
            'nonopposite meta cap axes')
    edges, counts, vectors, side_audits, boundary_gates = {}, {}, [], 0, 0
    turn_cos = {3: Q(-1)/2, 4: Q(), 5: Q(-1, 1)/4}
    for face in FACES:
        require(len(face) == len(set(face)), 'face has distinct vertices')
        counts[len(face)] = counts.get(len(face), 0)+1
        n = cross(sub(v[face[1]], v[face[0]]), sub(v[face[2]], v[face[0]]))
        require(dot(n, n) > 0, 'nondegenerate face')
        offsets = [dot(n, sub(p, v[face[0]])) for p in v]
        require(all(offsets[i] == 0 for i in face), 'coplanar face')
        signs = [offsets[i].sign() for i in range(60) if i not in face]
        require(len(set(signs)) == 1 and signs[0] != 0, 'complete actual supporting facet')
        for x in offsets:
            require(x.sign() == sign_enclosure(x), 'independent support sign enclosure')
            side_audits += 1
        e = [sub(v[face[(j+1) % len(face)]], v[i]) for j, i in enumerate(face)]
        for j, x in enumerate(e):
            require(dot(x, x) == 1, 'unit edge')
            require(dot(x, e[(j+1) % len(e)]) == turn_cos[len(face)], 'regular polygon turn')
            require(dot(cross(x, e[(j+1) % len(e)]), n) > 0, 'convex face ordering')
            for k in face:
                if k not in (face[j], face[(j+1) % len(face)]):
                    require(dot(cross(x, sub(v[k], v[face[j]])), n) > 0,
                            'entire actual face lies strictly inside each boundary edge')
                    boundary_gates += 1
            key = tuple(sorted((face[j], face[(j+1) % len(face)])))
            edges[key] = edges.get(key, 0)+1
        b = (Q(), Q(), Q())
        for i, j in zip(face, face[1:]+face[:1]):
            b = add(b, scale(Q(1)/2, cross(v[i], v[j])))
        # Choose outward orientation. Origin is strictly inside every facet.
        if dot(b, v[face[0]]) < 0:
            b = scale(-1, b)
        require(dot(b, v[face[0]]) > 0, 'origin strictly inside')
        vectors.append(b)
    require(counts == {3: 20, 4: 30, 5: 12}, 'face inventory')
    require(len(edges) == 120 and set(edges.values()) == {2}, 'closed actual facet complex')
    require(len(set(sum((list(f) for f in FACES), []))) == 60, 'all vertices used')
    require(tuple(sum((b[i] for b in vectors), Q()) for i in range(3)) == (Q(), Q(), Q()),
            'outward area-vector balance')
    return vectors, {'vertices': 60, 'edges': 120, 'facets': 62,
                     'face_inventory': counts, 'support_sign_audits': side_audits,
                     'face_boundary_gates': boundary_gates}


def brightness(vectors, d):
    return sum((absolute(dot(b, d)) for b in vectors), Q())/2


def area_candidates(vectors):
    result = {}
    parallel = 0
    for i, j in itertools.combinations(range(len(vectors)), 2):
        d = canonical(cross(vectors[i], vectors[j]))
        if d is None:
            parallel += 1
            continue
        result.setdefault(d, (i, j))
    return result, parallel


def oriented_ray(d):
    for x in d:
        if x != 0:
            return scale(1/absolute(x), d)
    raise RuntimeError('Zero tangent ray')


def adjacent_vertex_vectors(vectors, d):
    """All zonotope vertices in chambers incident to the arrangement axis d."""
    zeros = [b for b in vectors if dot(b, d) == 0]
    rays = set()
    for b in zeros:
        r = oriented_ray(cross(d, b))
        rays.add(r)
        rays.add(scale(-1, r))
    e = next(iter(sorted(rays, key=repr)))
    f = cross(d, e)

    def half(r):
        x, y = dot(r, e), dot(r, f)
        return 0 if y > 0 or (y == 0 and x > 0) else 1

    def compare(a, b):
        ha, hb = half(a), half(b)
        if ha != hb:
            return ha-hb
        return -dot(d, cross(a, b)).sign()

    rays = sorted(rays, key=cmp_to_key(compare))
    require(len(rays) >= 4, 'two independent zero generators')
    for a, b in zip(rays, rays[1:]+rays[:1]):
        require(dot(d, cross(a, b)) > 0, 'complete tangent-circle sectors shorter than pi')
        h = add(a, b)
        g = (Q(), Q(), Q())
        for v in vectors:
            sign = dot(v, d).sign()
            if sign == 0:
                sign = dot(v, h).sign()
                require(sign != 0, 'interior chamber direction')
            g = add(g, scale(Q(sign)/2, v))
        yield g


def maximum_area(vectors, candidates):
    vertices = set()
    chamber_entries = 0
    for d in candidates:
        for g in adjacent_vertex_vectors(vectors, d):
            vertices.add(g)
            vertices.add(scale(-1, g))
            chamber_entries += 1
    values = [(dot(g, g), g) for g in vertices]
    maximum = max(x for x, _ in values)
    maximizers = sorted([g for x, g in values if x == maximum], key=repr)
    # There are two facets per projective normal. Each polygon edge belongs
    # to two facets; the directed facet-edge incidence is 2*chamber_entries.
    require(len(vertices)-chamber_entries+2*len(candidates) == 2,
            'complete zonotope vertex/facet incidence Euler check')
    for g in maximizers:
        require(brightness(vectors, g) == maximum, 'maximum-area witness attains radius')
    require(all((maximum-x).sign() == sign_enclosure(maximum-x) for x, _ in values),
            'independent maximum-area comparisons')
    return maximum, maximizers, len(vertices), chamber_entries


def controls():
    s = Q(0, 1)
    require(s*s == 5 and (1+s)/(1+s) == 1, 'field identities')
    x = Q(1)
    for _ in range(40):
        x *= Q(9, -4)
        require(x.sign() == sign_enclosure(x) == 1, 'Pell cancellation control')
        require((-x).sign() == sign_enclosure(-x) == -1, 'negative Pell control')
    e = [(Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))]
    cube = e+[scale(-1, d) for d in e]
    candidates, parallel = area_candidates(cube)
    require(len(candidates) == 3 and parallel == 3, 'cube facet control')
    require({brightness(cube, d)*brightness(cube, d)/dot(d, d)
             for d in candidates} == {Q(1)}, 'cube minimum control')
    maximum, _, vertices, incidences = maximum_area(cube, candidates)
    require((maximum, vertices, incidences) == (Q(3), 8, 12), 'cube maximum control')
    # Splitting a generator leaves the zonotope unchanged. This checks
    # parallel-generator deduplication, including tangent-circle ordering.
    split = [scale(Q(1)/2, b) for b in cube for _ in range(2)]
    candidates2, _ = area_candidates(split)
    require(set(candidates2) == set(candidates), 'split-generator facet control')
    maximum2, _, vertices2, incidences2 = maximum_area(split, candidates2)
    require((maximum2, vertices2, incidences2) == (Q(3), 8, 12), 'split-generator maximum control')
    return {'pell_sign_controls': 80, 'zonotope_controls': 2}


def minimum_shadow_classification(minima):
    phi = Q(1, 1)/2
    axes = [(Q(1), Q(), Q()), (Q(), Q(1), Q())]+[
        (Q(1), t*phi, u*(1+phi)) for t in (-1, 1) for u in (-1, 1)]
    require(set(axes) == set(minima), 'stated six axes match complete area enumeration')
    norm = [Q(1), Q(1)]+[2*phi]*4
    units = [scale(1/r, a) for a, r in zip(axes, norm)]
    require(all(dot(u, u) == 1 for u in units), 'exact unit minimum axes')
    matches, signatures, area_checks = [], [], 0
    for i, a in enumerate(axes):
        h = hull_indices(VERTICES, a)
        require(len(h) == 12, 'twelve minimum-shadow corners')
        signed_vector = (Q(), Q(), Q())
        points = [projection(VERTICES[j], a) for j in h]
        for p, q in zip(points, points[1:]+points[:1]):
            signed_vector = add(signed_vector, cross(p, q))
        require(dot(signed_vector, units[i])/2 == Q(13, 7)/2,
                'independent polygon-area check at a minimum')
        area_checks += 1
        row = []
        for j, b in enumerate(axes):
            ha, hb, isometries = congruences(VERTICES, a, b)
            row.append(len(isometries))
            for match in isometries:
                columns, translation = proper_lift(VERTICES, units[i], units[j], match)
                require(all(dot(columns[r], columns[t]) == (1 if r == t else 0)
                            for r in range(3) for t in range(3)), 'orthogonal lift')
                require(dot(columns[0], cross(columns[1], columns[2])) == 1, 'proper lift')
                require(translation == (Q(), Q(), Q()), 'zero physical translation')

                def motion(p):
                    return tuple(sum((columns[k][r]*p[k] for k in range(3)), Q())
                                 for r in range(3))

                for source, target in match['vertex_pairs']:
                    require(motion(projection(VERTICES[source], a)) ==
                            projection(VERTICES[target], b), 'entire shadow congruence lift')
                matches.append({'source_axis': i, 'receiver_axis': j,
                                'direction': match['direction'], 'shift': match['shift'],
                                'proper_matrix_columns': [[str(x) for x in c] for c in columns]})
        signatures.append(row)
    require(signatures == [[2, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0],
                           [0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1],
                           [0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1]],
            'three distinct minimum-shadow congruence classes')
    require(len(matches) == 22, 'complete closed minimum-receiver motion list')
    return {'minimum_shadow_congruence_counts': signatures,
            'minimum_receiver_proper_motions': matches,
            'independent_minimum_polygon_area_checks': area_checks}


def common_shadow_cone():
    original, _, _, constructed, _ = cupola_construction()
    common = original & constructed
    changed = (original | constructed)-common
    axis = (Q(), Q(1), Q())
    hull = [VERTICES[i] for i in hull_indices(VERTICES, axis)]
    require(all(p in common for p in hull), 'common inscribed polygon')
    require(len(changed) == 20, 'ten deleted and ten added cap points')
    rho = Q(-1, 1)/8
    gates, ratios, zero_slacks = 0, [], 0
    for p, q in zip(hull, hull[1:]+hull[:1]):
        for w in sorted(set(hull) | changed, key=repr):
            if w == p or w == q:
                continue
            t = cross(sub(q, p), sub(w, p))
            transverse = absolute(t[0])+absolute(t[2])
            slack = t[1]-rho*transverse
            require(t[1] > 0 and slack >= 0, 'whole closed common-shadow square cone')
            require(slack.sign() == sign_enclosure(slack), 'independent cone sign')
            if w in hull:
                require(slack > 0, 'strict convexity of the entire inscribed polygon')
            if transverse != 0:
                ratios.append(t[1]/transverse)
            zero_slacks += int(slack == 0)
            gates += 1
    require(min(ratios) == rho, 'exact box margin for this inscribed polygon')
    require(gates == 360 and zero_slacks > 0, 'complete cone gate inventory')
    return {'common_shadow_cone_ratio': str(rho), 'common_shadow_cone_gates': gates,
            'common_shadow_cone_zero_slacks': zero_slacks}


def maximum_shadow_checks(maximizers, maximum):
    axes = sorted(set(canonical(g) for g in maximizers), key=repr)
    kappa = Q(13, 5)/22
    require(set(axes) == {(Q(1), Q(), -kappa), (Q(1), Q(), kappa)},
            'stated maximum-area axes')
    corners = []
    for d in axes:
        hull = hull_indices(VERTICES, d)
        p = [projection(VERTICES[i], d) for i in hull]
        b = (Q(), Q(), Q())
        for x, y in zip(p, p[1:]+p[:1]):
            b = add(b, scale(Q(1)/2, cross(x, y)))
        require(dot(b, b) == maximum, 'independent maximum polygon-area check')
        corners.append(len(hull))
    return {'independent_maximum_polygon_area_checks': len(axes),
            'maximum_shadow_corner_counts': corners}


def verify():
    result_controls = controls()
    vectors, result = validate_model()
    candidates, parallel = area_candidates(vectors)
    values = [(brightness(vectors, d)*brightness(vectors, d)/dot(d, d), d)
              for d in candidates]
    minimum = min(x[0] for x in values)
    minima = sorted([d for x, d in values if x == minimum], key=repr)
    require(all((x-minimum).sign() == sign_enclosure(x-minimum) for x, _ in values),
            'independent area comparison signs')
    maximum, maximizers, vertex_count, chamber_entries = maximum_area(vectors, candidates)
    require(minimum == Q(207, 91)/2, 'stated exact minimum')
    require(maximum == Q(113, 50), 'stated exact maximum')
    ratio = maximum/minimum
    lo, hi = Fraction(1023021211654, 10**12), Fraction(1023021211655, 10**12)
    require(Q(lo**4) < ratio < Q(hi**4), 'exact scale upper-bound decimal enclosure')
    result.update({'candidate_pairs': math.comb(62, 2), 'parallel_pairs': parallel,
                   'projective_area_candidates': len(candidates),
                   'minimum_area_squared': str(minimum),
                   'minimum_projective_axes': [[str(x) for x in d] for d in minima],
                   'maximum_area_squared': str(maximum),
                   'maximum_projective_axes': [[str(x) for x in d] for d in sorted(
                       set(canonical(g) for g in maximizers), key=repr)],
                   'brightness_zonotope_vertex_count': vertex_count,
                   'brightness_zonotope_edge_count': chamber_entries,
                   'brightness_zonotope_facet_count': 2*len(candidates),
                   'incident_chamber_entries': chamber_entries,
                   'passage_scale_upper_bound_fourth_power': str(maximum/minimum),
                   'scale_upper_bound_enclosure': ['1.023021211654', '1.023021211655'],
                   'candidate_spectrum_sha256': hashlib.sha256(
                       ''.join(repr(d)+':'+str(x)+'\n' for x, d in values).encode()).hexdigest()})
    result.update(result_controls)
    result.update(minimum_shadow_classification(minima))
    result.update(common_shadow_cone())
    result.update(maximum_shadow_checks(maximizers, maximum))
    return result


if __name__ == '__main__':
    result = verify()
    expected_path = Path(__file__).with_name('expected.json')
    expected = json.loads(expected_path.read_text())
    require(json.loads(json.dumps(result)) == expected, 'full compact expected certificate matches')
    summary = {key: value for key, value in result.items()
               if key not in ('minimum_receiver_proper_motions', 'minimum_projective_axes',
                              'maximum_projective_axes')}
    summary['status'] = 'exact verification passed'
    summary['proper_closed_minimum_receiver_fits'] = len(result['minimum_receiver_proper_motions'])
    print(json.dumps(summary, indent=2))
