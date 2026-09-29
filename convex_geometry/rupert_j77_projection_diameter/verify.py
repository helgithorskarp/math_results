"""Exact certificate checker for J77 projection diameter; Python 3.11+, stdlib.

The proof of the finite direction reduction is in PROOF.md.  This checker
uses no floating point for any mathematical assertion.  Run without -O.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from model import VERTICES, FACES, cupola_construction
from q5 import Q, add, cross, dot, scale, sub

if not __debug__:
    raise RuntimeError('Verification requires Python without -O or -OO')

R2 = Q(11, 4)/4
B = Q(65, 10)/596
L2 = R2-B
D = (Q(), Q(-1), Q(7, 1)/2)


def interval_sign(q):
    """Independent sign audit using integer-square-root rational enclosures."""
    if q.a == 0 and q.b == 0:
        return 0
    for bits in (16, 32, 64, 128, 256, 512, 1024, 2048):
        den = 1 << bits
        lo = Fraction(math.isqrt(5*den*den), den)
        hi = lo+Fraction(1, den)
        endpoints = sorted((q.a+q.b*lo, q.a+q.b*hi))
        if endpoints[0] > 0:
            return 1
        if endpoints[1] < 0:
            return -1
    raise RuntimeError('Sign audit enclosure unresolved')


def field_audit():
    s = Q(0, 1)
    assert s*s == 5
    assert (1+s)*(1-s) == -4
    assert (1+s)/(1+s) == 1
    values = [Q(), Q(2), Q(-2), Q(-2, 1), Q(2, -1), Q(0, -1)]
    p = Q(1)
    for _ in range(60):
        p = p*Q(9, -4)  # Very small positive Pell conjugates; cancellation audit.
        values.extend((p, -p))
    for q in values:
        assert q.sign() == interval_sign(q)
    return len(values)


def validate_model():
    v = VERTICES
    assert len(v) == 55 and len(set(v)) == 55
    assert all(dot(p, p) == R2 for p in v)
    original, core, cap, rotated_cap, axis = cupola_construction()
    assert (len(original), len(core), len(cap), len(rotated_cap)) == (60, 50, 5, 5)
    assert core | rotated_cap == set(v)
    assert core.isdisjoint(rotated_cap)
    assert {scale(-1, p) for p in core} == core

    edges = {}
    face_counts = {}
    cosine_turn = {3: Q(-1)/2, 4: Q(), 5: Q(-1, 1)/4, 10: Q(1, 1)/4}
    for face in FACES:
        assert len(face) == len(set(face))
        face_counts[len(face)] = face_counts.get(len(face), 0)+1
        n = cross(sub(v[face[1]], v[face[0]]), sub(v[face[2]], v[face[0]]))
        assert dot(n, n) > 0
        assert all(dot(n, sub(v[i], v[face[0]])) == 0 for i in face)
        side = [dot(n, sub(p, v[face[0]])).sign()
                for i, p in enumerate(v) if i not in face]
        assert all(s == side[0] for s in side) and side[0] != 0
        e = [sub(v[face[(j+1) % len(face)]], v[i]) for j, i in enumerate(face)]
        for j, x in enumerate(e):
            nxt = e[(j+1) % len(e)]
            assert dot(x, x) == 1
            assert dot(x, nxt) == cosine_turn[len(face)]
            assert dot(cross(x, nxt), n) > 0
            key = tuple(sorted((face[j], face[(j+1) % len(face)])))
            edges[key] = edges.get(key, 0)+1
    assert len(edges) == 105 and all(count == 2 for count in edges.values())
    assert face_counts == {10: 1, 5: 11, 4: 25, 3: 15}
    assert len(v)-len(edges)+len(FACES) == 2
    return core, axis, face_counts


def direction_candidates(a):
    """All one-, two-, and three-active candidates from the coverage lemma."""
    yield from a
    for x, y in itertools.combinations(a, 2):
        for s in (-1, 1):
            yield add(x, scale(s, y))
    for x, y, z in itertools.combinations(a, 3):
        for s, t in itertools.product((-1, 1), repeat=2):
            yield cross(sub(x, scale(s, y)), sub(x, scale(t, z)))


def reduction_controls():
    """Hand-solvable cases that require the one-, two- and three-active branches."""
    basis = [(Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))]
    for size in (1, 2, 3):
        points = basis[:size]
        values = []
        for d in direction_candidates(points):
            norm = dot(d, d)
            if norm:
                values.append(min(dot(p, d)*dot(p, d)/norm for p in points))
        assert max(values) == Q(1)/size
    return 3


def verify():
    sign_audits = field_audit()
    controls = reduction_controls()
    core, axis, face_counts = validate_model()
    pairs = []
    a = []
    for i, p in enumerate(VERTICES):
        if p not in core:
            continue
        j = VERTICES.index(scale(-1, p))
        if i < j:
            pairs.append((i, j))
            a.append(p)
    assert len(a) == 25
    assert min(dot(p, D)*dot(p, D)/dot(D, D) for p in a) == B

    tested = zero = 0
    digest = hashlib.sha256()
    for d in direction_candidates(a):
        norm = dot(d, d)
        if norm == 0:
            zero += 1
            continue
        for j, p in enumerate(a):
            z = dot(p, d)
            if z*z <= B*norm:
                break
        else:
            raise AssertionError(('uncovered candidate direction', d))
        digest.update(f'{tested}:{j}\n'.encode())
        tested += 1
    assert (tested, zero) == (9825, 0)

    diameter_pairs = 0
    equality_pairs = []
    for i, j in itertools.combinations(range(len(VERTICES)), 2):
        z = sub(VERTICES[i], VERTICES[j])
        distance2 = dot(z, z)-dot(z, D)*dot(z, D)/dot(D, D)
        assert distance2 <= 4*L2
        if distance2 == 4*L2:
            equality_pairs.append((i, j))
        diameter_pairs += 1
    assert diameter_pairs == 1485 and equality_pairs

    # Analytic axial-receiver exclusion ingredients: five same-height vectors.
    k = Q(-1, 1)/4
    t2 = Q(5, -2)/20
    r2 = Q(25, 11)/10
    assert k*k/dot(axis, axis) == t2 and t2+r2 == R2
    assert all(dot(p, axis)*dot(p, axis) >= k*k for p in VERTICES)
    ring = [p for p in core if dot(p, axis) == k]
    assert len(ring) == 5
    assert tuple(sum((p[j] for p in ring), Q()) for j in range(3)) == scale(5*k/dot(axis, axis), axis)
    # Exact 72-degree rotation: cos(72) = k, sin(72)/|axis| = 1/2.
    assert k*k+dot(axis, axis)/4 == 1
    p = ring[0]
    orbit = []
    for _ in range(5):
        orbit.append(p)
        p = add(add(scale(k, p), scale((1-k)*dot(axis, p)/dot(axis, axis), axis)),
                scale(Q(1)/2, cross(axis, p)))
    assert p == ring[0] and set(orbit) == set(ring)
    cosine36 = Q(1, 1)/4
    cone_ratio2 = t2/(r2*cosine36*cosine36)
    assert cone_ratio2 == Q(123, -55)/2 and 0 < cone_ratio2 < 1

    scale2 = R2/L2
    assert scale2 == Q(2797, -75)/2552
    decimal_lo = Fraction(1015031019664, 10**12)
    decimal_hi = Fraction(1015031019665, 10**12)
    assert Q(decimal_lo*decimal_lo) < scale2 < Q(decimal_hi*decimal_hi)
    result = {
        'status': 'exact verification passed',
        'field_sign_audits': sign_audits,
        'reduction_controls': controls,
        'vertices': 55,
        'edges': 105,
        'faces_by_size': face_counts,
        'core_antipodal_pairs': pairs,
        'candidate_count': tested,
        'degenerate_count': zero,
        'first_blocker_sha256': digest.hexdigest(),
        'diameter_witness_pair_checks': diameter_pairs,
        'diameter_witness_equality_pairs': equality_pairs,
        'max_min_core_dot_squared': str(B),
        'minimum_core_projection_radius_squared': str(L2),
        'minimum_J77_projection_diameter_squared': str(4*L2),
        'passage_scale_upper_bound_squared': str(scale2),
        'certified_scale_upper_bound_enclosure': ['1.015031019664', '1.015031019665'],
        'axial_ring_count': len(ring),
        'axial_ring_regular_pentagon': True,
        'axial_height_squared': str(t2),
        'axial_projection_radius_squared': str(r2),
        'axial_cone_tan_half_angle_squared': str(cone_ratio2),
    }
    return result


if __name__ == '__main__':
    result = verify()
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    # JSON serialization normalizes tuples and integer dictionary keys.
    canonical = json.loads(json.dumps(result))
    assert canonical == expected, 'Result differs from the compact expected certificate'
    print(json.dumps(result, indent=2))
