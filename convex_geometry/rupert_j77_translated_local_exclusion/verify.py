#!/usr/bin/env python3
"""Exact translated local-exclusion certificate for the Johnson solid J77.

Python 3.11+, standard library only. The geometric implication is proved in
PROOF.md; this script checks all finite hypotheses using Q(sqrt(5)).
No floating-point hull or solver output is trusted.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import isqrt

from model import VERTICES, cupola_construction
from q5 import Q, add, cross, dot, scale, sub

AUTHOR = 'six-rupert-2'
DIRECTION = (Q(), Q(-1), Q(7, 1)/2)
SPHERE_RADIUS_SQUARED = Q(11, 4)/4
SUPPORT_CYCLE = (15, 48, 32, 54, 24, 51, 30, 44, 11,
                 8, 41, 29, 16, 19, 31, 45, 12)
# Probe 2*j uses one quarter of the outgoing normalized support normal;
# probe 2*j+1 uses three quarters. The remaining part is incoming.
BASES = (
    (0, 1, (5, 12, 25, 26)),
    (0, -1, (7, 10, 21, 30)),
    (1, 1, (2, 13, 18, 19, 27)),
    (1, -1, (4, 15, 24, 32, 33)),
    (2, 1, (1, 7, 9, 19, 23)),
    (2, -1, (8, 10, 16, 28, 32)),
)
C = F(61, 10)                 # maximum sum of coefficients
M = F(9, 8)                   # R times maximum probe norm
GAP = F(1, 80)                # minimum unique supporting-vertex gap
DELTA = F(1, 200)              # Euclidean unit-normal distance
THETA = F(3, 20)               # relative 3D rotation angle, radians


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(x):
    x = Q(x)
    return [str(x.a), str(x.b)]


def check_model():
    V = set(VERTICES)
    original, core, cap, gyrated, axis = cupola_construction()
    require(len(VERTICES) == len(V) == 55, 'invalid 55-vertex model')
    require((len(original), len(core), len(cap), len(gyrated)) == (60, 50, 5, 5),
            'invalid independent cupola construction')
    require(core | gyrated == V and not core & gyrated,
            'fixture differs from the independent J77 construction')
    require(all(tuple(-x for x in v) in core for v in core),
            'the 50-vertex core is not centrally symmetric')
    require(sum(tuple(-x for x in v) in V for v in V) == 50,
            'unexpected antipodal structure')
    spanning = tuple(VERTICES[i] for i in (8, 29, 23))
    require(all(v in core for v in spanning) and dot(spanning[0], cross(spanning[1], spanning[2])) != 0,
            'the symmetric core does not certify origin in the interior')
    require(all(dot(v, v) == SPHERE_RADIUS_SQUARED for v in V),
            'invalid common circumradius')
    require(dot(DIRECTION, DIRECTION) > 0, 'invalid base direction')
    # A 72-degree rotation about the cupola axis, exact over Q(sqrt(5)).
    cosine, sine_over_axis_norm = Q(-1, 1)/4, Q(1)/2
    require(cosine*cosine+sine_over_axis_norm*sine_over_axis_norm*dot(axis, axis) == 1,
            'invalid Rodrigues coefficients')

    def rotate(v):
        return add(add(scale(cosine, v),
                       scale((1-cosine)*dot(axis, v)/dot(axis, axis), axis)),
                   scale(sine_over_axis_norm, cross(axis, v)))

    e = tuple(tuple(Q(int(i == j)) for i in range(3)) for j in range(3))
    columns = tuple(rotate(v) for v in e)
    require(all(dot(columns[i], columns[j]) == int(i == j)
                for i in range(3) for j in range(3)), 'symmetry is not orthogonal')
    require(dot(columns[0], cross(columns[1], columns[2])) == 1,
            'symmetry is not proper')
    require({rotate(v) for v in V} == V, 'fivefold map does not preserve J77')
    current = DIRECTION
    orbit = []
    for _ in range(5):
        orbit.append(current)
        current = rotate(current)
    require(current == DIRECTION, 'symmetry orbit does not close')
    require(len(set(orbit)) == 5, 'fivefold orbit is degenerate')
    require(not any(tuple(-x for x in d) in orbit for d in orbit),
            'unoriented orbit has fewer than five directions')
    return orbit


def make_probes(cycle=SUPPORT_CYCLE):
    require(len(cycle) == 17 and len(set(cycle)) == 17,
            'expected 17 distinct support vertices')
    require(all(isinstance(i, int) and 0 <= i < len(VERTICES) for i in cycle),
            'invalid support-vertex index')
    edge_normals = []
    for i, j in zip(cycle, cycle[1:]+cycle[:1]):
        normal = cross(sub(VERTICES[j], VERTICES[i]), DIRECTION)
        offset = dot(normal, VERTICES[i])
        require(offset > 0, 'invalid support-normal orientation')
        normal = tuple(x/offset for x in normal)
        require(dot(normal, DIRECTION) == 0, 'support normal not in target plane')
        require(dot(normal, VERTICES[i]) == dot(normal, VERTICES[j]) == 1,
                'support line misses its endpoints')
        require(all(dot(normal, v) <= 1 for v in VERTICES),
                'a vertex crosses a supporting line')
        edge_normals.append(normal)
    probes = []
    for j, vertex in enumerate(cycle):
        incoming = edge_normals[(j-1) % len(cycle)]
        outgoing = edge_normals[j]
        for t in (F(1, 4), F(3, 4)):
            normal = tuple((1-t)*x+t*y for x, y in zip(incoming, outgoing))
            probes.append((vertex, normal))
    return probes


def exact_solve(columns, target):
    """Solve the complete six-coordinate identity, with at most five columns."""
    require(0 < len(columns) <= 5 and len(target) == 6,
            'invalid positive-combination dimensions')
    n = len(columns)
    matrix = [[columns[j][i] for j in range(n)]+[Q(target[i])] for i in range(6)]
    row = 0
    for j in range(n):
        pivot = next((k for k in range(row, 6) if matrix[k][j] != 0), None)
        require(pivot is not None, 'dependent certificate columns')
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        divisor = matrix[row][j]
        matrix[row] = [x/divisor for x in matrix[row]]
        for k in range(6):
            if k != row:
                multiplier = matrix[k][j]
                matrix[k] = [x-multiplier*y for x, y in zip(matrix[k], matrix[row])]
        row += 1
    require(all(matrix[k][-1] == 0 for k in range(row, 6)),
            'inconsistent exact positive-combination identity')
    weights = [matrix[k][-1] for k in range(n)]
    # Verify every original coordinate independently of row-reduction state.
    require(all(sum((w*col[k] for w, col in zip(weights, columns)), Q()) == target[k]
                for k in range(6)), 'reconstructed identity failed')
    return weights


def independent_sign_audit(values):
    """Rational enclosures of sqrt(5), independently of Q.sign's case rule."""
    denominator = 10**200
    floor_root = isqrt(5*denominator*denominator)
    low, high = F(floor_root, denominator), F(floor_root+1, denominator)
    extra = [Q(), Q(1), Q(-1), Q(0, 1), Q(0, -1), Q(9, -4), Q(9, 4)]
    pell = Q(1)
    for _ in range(60):
        pell = pell*Q(9, -4)
    extra += [pell, -pell]
    for x in values+extra:
        if x == 0:
            expected = 0
        else:
            endpoints = (x.a+x.b*low, x.a+x.b*high)
            require(min(endpoints) > 0 or max(endpoints) < 0,
                    'independent rational sign enclosure is inconclusive')
            expected = 1 if min(endpoints) > 0 else -1
        require(x.sign() == expected, 'ordered-field sign audit failed')


def check(probe_input=None, bases=BASES):
    orbit = check_model()
    probes = make_probes() if probe_input is None else probe_input
    require(len(probes) == 34, 'expected 34 support probes')
    gradients, gap_values, norm_values, audit = [], [], [], []
    for vertex, normal in probes:
        require(isinstance(vertex, int) and 0 <= vertex < len(VERTICES),
                'invalid probe vertex')
        require(len(normal) == 3 and dot(normal, DIRECTION) == 0,
                'probe does not lie in the target plane')
        v = VERTICES[vertex]
        require(dot(normal, v) == 1, 'probe support offset is not one')
        gaps = [dot(normal, sub(v, w)) for i, w in enumerate(VERTICES) if i != vertex]
        require(all(g > GAP for g in gaps), 'unique supporting-vertex gap too small')
        norm_squared = SPHERE_RADIUS_SQUARED*dot(normal, normal)
        require(norm_squared < M*M, 'R times probe norm is too large')
        gap_values.extend(gaps)
        norm_values.append(norm_squared)
        audit.extend(g-Q(GAP) for g in gaps)
        audit.append(Q(M*M)-norm_squared)
        gradients.append(cross(v, normal)+normal)
    expected_targets = {(axis, sign) for axis in range(3) for sign in (1, -1)}
    require(len(bases) == 6 and {(a, s) for a, s, _ in bases} == expected_targets,
            'all six signed rotation targets are required')
    certificates = []
    certificate_hash_data = []
    for axis, sign, ids in bases:
        require(len(set(ids)) == len(ids) and all(0 <= i < len(probes) for i in ids),
                'invalid probe basis')
        target = [0]*6
        target[axis] = sign
        weights = exact_solve([gradients[i] for i in ids], target)
        require(all(w > 0 for w in weights), 'nonpositive reconstructed coefficient')
        total = sum(weights, Q())
        require(total < C, 'coefficient sum exceeds its uniform bound')
        audit.extend(weights)
        audit.append(Q(C)-total)
        certificates.append({'axis': axis, 'sign': sign, 'probe_indices': list(ids),
                             'sum_a_plus_b_sqrt5': encode(total)})
        certificate_hash_data.append([axis, sign, list(ids), [encode(w) for w in weights]])
    require(2*M*DELTA < GAP, 'transported support gap is not positive')
    error = C*M*(DELTA+THETA/2)
    require(error > 0 and 3*error*error < 1, 'rotation torque bound does not dominate error')
    # Positive support offsets also persist in the nearby receiver plane.
    require(M*DELTA < 1, 'nearby support offset need not remain positive')
    independent_sign_audit(audit)
    digest = hashlib.sha256(json.dumps(certificate_hash_data, separators=(',', ':')).encode()).hexdigest()
    return {
        'agent': AUTHOR, 'role': 'researcher',
        'claim_status': 'analytic_local_exclusion_with_exact_translated_support_certificate',
        'closed_containment_conclusion': 'lambda=1, Q=identity, translation=0',
        'global_rupert_status_resolved': False,
        'arbitrary_planar_translations_covered': True,
        'passage_scales_covered': 'lambda >= 1',
        'target_unit_normal_distance_maximum': str(DELTA),
        'relative_3d_rotation_angle_maximum_radians': str(THETA),
        'base_normal_unnormalized_a_plus_b_sqrt5': [encode(x) for x in DIRECTION],
        'five_unoriented_symmetry_orbit_directions': [[encode(x) for x in d] for d in orbit],
        'vertex_count': len(VERTICES), 'antipodally_paired_vertex_count': 50,
        'origin_in_interior_certified_by_three_core_pairs': [8, 29, 23],
        'support_probe_count': len(probes), 'unique_support_gap_comparisons': len(gap_values),
        'minimum_unique_support_gap_a_plus_b_sqrt5': encode(min(gap_values)),
        'unique_support_gap_strict_lower_bound': str(GAP),
        'maximum_R_squared_times_probe_norm_squared_a_plus_b_sqrt5': encode(max(norm_values)),
        'R_times_probe_norm_strict_upper_bound': str(M),
        'coefficient_sum_strict_upper_bound': str(C),
        'positive_combinations': certificates,
        'transported_unique_support_gap_strict_lower_bound': str(GAP-2*M*DELTA),
        'torque_error_strict_upper_bound': str(error),
        'three_times_squared_error_upper_bound': str(3*error*error),
        'exact_positive_combination_sha256': digest,
        'independent_rational_sign_audit_count': len(audit)+9,
    }


def self_test():
    probes = make_probes()
    bad = list(probes)
    vertex, normal = bad[0]
    bad[0] = (vertex, tuple(-x for x in normal))
    invalid_cases = [lambda: check(probe_input=bad),
                     lambda: check(probe_input=probes[:-1]),
                     lambda: check(bases=BASES[:-1]),
                     lambda: check(bases=((0, 1, (0,)),)+BASES[1:])]
    for invalid in invalid_cases:
        try:
            invalid()
        except ValueError:
            pass
        else:
            raise ValueError('invalid certificate accepted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    print(json.dumps(check(), indent=2, sort_keys=True))
