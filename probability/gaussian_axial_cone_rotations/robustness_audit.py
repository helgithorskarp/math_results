#!/usr/bin/env python3
"""Exact constants and identities for ROBUSTNESS.md, standard library only.

Default writes deterministic JSON. --check compares EXPECTED_ROBUSTNESS.json.
The continuum theorem is the written proof, not a sampled perturbation test.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from verify import Poly, determinant, dist2, dot, neg, norm2, require, sub


ORIGINAL_EXPECTED_SHA256 = (
    "50ce427908f4f6e355ea7ed58996954bc2b5ebc72c2ac547417659be6b8196c4"
)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def diagonal_lower_bound(a):
    """Gershgorin bound for the symmetric matrix, with exact entries."""
    require(a == transpose(a), "nonsymmetric Gram matrix")
    return min(a[i][i] - sum(abs(a[i][j]) for j in range(len(a)) if j != i)
               for i in range(len(a)))


def symbolic_audit():
    # Poly is used as a free polynomial ring: never call its trig reduction.
    # Each identity assigns its own local names to the same indeterminates.
    t = Poly.var(0)
    u = [Poly.var(i) for i in (1, 2, 3)]
    v = [Poly.var(i) for i in (4, 5, 6)]
    w = [(1-t)*a+t*b for a, b in zip(u, v)]
    segment = (F(1, 2)*norm2(w).diff(0)
               - dot(v, sub(v, u)) + (1-t)*norm2(sub(v, u)))
    firm = norm2(sub([2*x for x in v], u)) - norm2(u) - 4*(norm2(v)-dot(v, u))
    parallelogram = (norm2(sub(u, [t*x for x in v]))
                     + norm2([a+t*b for a, b in zip(u, v)])
                     - 2*norm2(u) - 2*t*t*norm2(v))
    a, b, c, ea, eb, ec = [Poly.var(i) for i in range(6)]
    polarization = F(1, 2)*((a+ea)+(b+eb)-(c+ec)-(a+b-c)-(ea+eb-ec))
    error_square = 2*b*b + 2*(a-b)*(a-b) - a*a - (a-2*b)*(a-2*b)
    lam, eta, r = [Poly.var(i) for i in range(3)]
    output_plus = ((lam+eta)*(lam+eta-r)
                   - (lam*lam-r*lam+eta*eta+(2*lam-r)*eta))
    output_minus = ((lam-eta)*(lam-eta-r)
                    - (lam*lam-r*lam+eta*eta-(2*lam-r)*eta))
    identities = {
        'segment_derivative': segment,
        'firm_nonexpansive_identity': firm,
        'paired_parallelogram': parallelogram,
        'polarization_error': polarization,
        'scalar_error_square': error_square,
        'output_extreme_plus': output_plus,
        'output_extreme_minus': output_minus,
    }
    for name, p in identities.items():
        require(not p.terms, 'polynomial identity failed: '+name)
    require(bool((segment+t).terms), 'nonzero polynomial mutation was accepted')
    return {'free_ring_identities': sorted(identities),
            'trigonometric_reduction_used': False,
            'nonzero_identity_control_rejected': True}


def reconstruct():
    directions = [(F(x, 5), F(y, 5)) for x, y in
                  [(5, 0), (4, 3), (3, 4), (0, 5), (-3, 4), (-4, 3),
                   (-5, 0), (-4, -3), (-3, -4), (0, -5), (3, -4), (4, -3)]]
    require(all(norm2(d) == 1 for d in directions), 'nonunit reference ray')
    p, q = F(3, 4), F(4, 5)
    A = [(p*x, p*y, F(1)) for x, y in directions]
    B = [(q*x, q*y, F(1)) for x, y in directions]
    origin = (F(0),)*3
    return p, q, A, B, [origin]+A+[neg(b) for b in B], [origin]+A+B


def validate_reserve(epsilon, eta, lam, r):
    require(0 <= epsilon < 1 and eta >= 0 and lam > 0,
            'invalid deformation parameters')
    require(0 < r <= 1-epsilon and 0 <= lam-eta <= lam+eta <= r,
            'insufficient straight-segment reserve')
    first = r*(r-1+epsilon)
    last = max((lam+s*eta)*(lam+s*eta-r) for s in (-1, 1))
    require(first <= 0 and last <= 0, 'positive endpoint derivative')
    return first, last


def rejected(call, label):
    try:
        call()
    except ValueError:
        return label
    raise ValueError('invalid control was accepted: '+label)


def interval_gram_audit(anchored, lam, E):
    """Second enclosure: all corners of the six independent squared edges.

    Every actual Gram is a convex combination of these corner Grams. Exact
    Sylvester tests therefore suffice without the operator-norm error bound.
    """
    edges = list(combinations(range(4), 2))
    intervals = [(lam*lam*dist2(anchored[i], anchored[j])-E,
                  dist2(anchored[i], anchored[j])+E) for i, j in edges]
    require(all(0 < lo < hi for lo, hi in intervals), 'bad squared-edge box')
    records = []
    for choices in product((0, 1), repeat=6):
        values = {edge: interval[choice]
                  for edge, interval, choice in zip(edges, intervals, choices)}
        gram = [[values[(0, i)] if i == j else
                 (values[(0, i)]+values[(0, j)]-values[tuple(sorted((i, j)))])/2
                 for j in (1, 2, 3)] for i in (1, 2, 3)]
        minors = [determinant([row[:n] for row in gram[:n]]) for n in (1, 2, 3)]
        require(all(x > 0 for x in minors), 'a squared-edge corner Gram is not positive definite')
        records.append([list(choices), [str(x) for x in minors]])
    data = json.dumps(records, separators=(',', ':')).encode()
    return {'corners_checked': len(records),
            'minimum_leading_principal_minors':
                [min(F(row[1][i]) for row in records) for i in range(3)],
            'corner_record_sha256': sha256(data).hexdigest()}


def audit():
    original = Path(__file__).with_name('EXPECTED.json').read_bytes()
    require(sha256(original).hexdigest() == ORIGINAL_EXPECTED_SHA256,
            'the original axial certificate changed')
    p, q, A, B, X, Y = reconstruct()
    lam, delta, r = F(19, 20), F(1, 2000), F(49, 50)
    alpha, E = 2*delta, F(1, 250)
    epsilon, eta = 2*delta/F(1, 5), 2*delta/F(1, 20)
    first, last = validate_reserve(epsilon, eta, lam, r)
    require((first, last) == (F(-147, 10000), F(-97, 10000)),
            'wrong uniform segment margins')
    pair_records = []
    for i, j in combinations(range(25), 2):
        x2, y2 = dist2(X[i], X[j]), dist2(Y[i], Y[j])
        loss = x2-lam*lam*y2
        require(loss > 0, 'the damped reference is not a strict contraction')
        pair_records.append([i, j, str(x2), str(y2), str(loss)])
    source_min2 = min(F(row[2]) for row in pair_records)
    target_min2 = min(F(row[3]) for row in pair_records)
    require((source_min2, target_min2) == (F(9, 200), F(1, 400)),
            'incorrect reference separation')
    require(source_min2 > F(1, 5)**2 and target_min2 == F(1, 20)**2,
            'conservative separation bound failed')
    require(F(1, 5) > 2*delta and lam*F(1, 20) > 2*delta,
            'the perturbed endpoints could collide')

    chosen = (0, 4, 8)
    selected = []
    for name, slope, cloud in [('A', p, A), ('B', q, B)]:
        M = [list(cloud[i]) for i in chosen]
        gram = matmul(transpose(M), M)
        expected = [[43*slope*slope/25, F(0), -slope/5],
                    [F(0), 32*slope*slope/25, F(0)],
                    [-slope/5, F(0), F(3)]]
        require(gram == expected, 'wrong selected coordinate Gram matrix')
        lower = diagonal_lower_bound(gram)
        require(lower == 32*slope*slope/25 and lower >= F(18, 25),
                'Gram coercivity failed')
        require(lower > F(4, 5)**2, 'singular-value lower bound failed')
        det = determinant(M)
        require(det == 64*slope*slope/25 and det > 0, 'wrong orientation')
        radii2 = [norm2(a) for a in cloud]
        require(set(radii2) == {1+slope*slope}, 'cloud radius mismatch')
        anchored = [(F(0),)*3]+[tuple(row) for row in M]
        edges2 = [dist2(a, b) for a, b in combinations(anchored, 2)]
        internal2 = [dist2(a, b) for a, b in combinations(M, 2)]
        require(max(edges2) <= F(8, 5)**2, 'selected edge length too large')
        require(max(internal2) <= 2*(1+slope*slope), 'Gram error premise failed')
        moment = [[sum(a[i]*a[j] for a in cloud)/12 for j in range(3)]
                  for i in range(3)]
        require(moment == [[slope*slope/2, 0, 0], [0, slope*slope/2, 0], [0, 0, 1]],
                'directional second moment mismatch')
        selected.append({'cloud': name, 'matrix': M, 'coordinate_gram': gram,
                         'gram_lower_bound': lower, 'determinant': det,
                         'maximum_selected_squared_edge': max(edges2),
                         'maximum_internal_squared_edge': max(internal2),
                         'second_moment': moment,
                         'squared_edge_box': interval_gram_audit(anchored, lam, E)})

    squared_edge_error = 2*F(8, 5)*alpha+alpha*alpha
    require(squared_edge_error == F(3201, 1000000) < E, 'squared-edge error budget')
    entry_error = (1-lam*lam)*F(41, 25)+F(3, 2)*E
    gram_floor = F(18, 25)-3*entry_error
    require(gram_floor == F(2223, 10000) > 0, 'orientation barrier not certified')
    source_orientation_margin = F(4, 5)-3*alpha
    target_orientation_margin = lam*F(4, 5)-3*alpha
    paired_rank_margin = lam*F(4, 5)-6*alpha
    require(min(source_orientation_margin, target_orientation_margin, paired_rank_margin) > 0,
            'endpoint orientation or paired-rank perturbation bound failed')
    ma, mb = selected[0]['matrix'], selected[1]['matrix']
    paired_rows = [a+[lam*x for x in a] for a in ma]
    paired_rows += [[-x for x in b]+[lam*x for x in b] for b in mb]
    det6 = determinant(paired_rows)
    require(det6 == 8*lam**3*determinant(ma)*determinant(mb) > 0,
            'paired reference determinant identity failed')
    DA = (1-lam*lam)*(1+p*p)+2*E
    DB = (1-lam*lam)*(1+q*q)+2*E
    scalar_rhs = (2*DA+8*alpha*alpha)/(p*p/2)+(2*DB+8*alpha*alpha)/(q*q/2)
    scalar_lhs = 2*(1+lam*lam)
    scalar_gap = scalar_lhs-scalar_rhs
    require((scalar_lhs, scalar_rhs, scalar_gap) ==
            (F(761, 200), F(821119, 375000), F(151439, 93750)),
            'scalar certificate arithmetic failed')
    require(scalar_gap > 0, 'scalar contradiction not certified')

    controls = [
        rejected(lambda: validate_reserve(F(1, 10), F(0), F(1, 2), F(1)),
                 'source reserve violation'),
        rejected(lambda: validate_reserve(F(0), F(1, 5), F(1, 10), F(9, 10)),
                 'negative output extreme'),
        rejected(lambda: validate_reserve(F(0), F(1, 5), F(9, 10), F(19, 20)),
                 'output reserve violation'),
    ]
    # T=-Id/2 is nonexpansive but its straight segment is not contracting.
    bad_u, bad_v = F(1), F(-1, 2)
    require(abs(bad_v) < abs(bad_u) and bad_v*(bad_v-bad_u) == F(3, 4) > 0,
            'nonexpansive/firm distinction was missed')
    controls.append('nonexpansiveness alone fails the segment test')
    require(validate_reserve(F(0), F(0), F(1), F(1)) == (0, 0),
            'identity boundary control failed')
    controls.append('identity boundary accepted')
    # Large damping permits the Gram lower estimate to fail: do not advertise
    # its positivity without the checked hypotheses.
    bad_floor = F(18, 25)-3*((1-F(1, 5)**2)*F(41, 25)+F(3, 2)*E)
    require(bad_floor < 0, 'weakened orientation estimate unexpectedly positive')
    controls.append('large-damping orientation bound fails as expected')
    record_bytes = json.dumps(pair_records, separators=(',', ':')).encode()
    return {
        'status': 'AXIAL_UNIFORM_ROBUSTNESS_AUDITS_PASS',
        'arithmetic': 'integers and fractions.Fraction; free polynomial identities',
        'original_expected_sha256': ORIGINAL_EXPECTED_SHA256,
        'symbolic': symbolic_audit(),
        'parameters': {'lambda': lam, 'endpoint_radius': delta, 'difference_error': alpha,
                       'epsilon': epsilon, 'eta': eta, 'r': r, 'squared_edge_allowance': E},
        'reference': {'sites': 25, 'pairs_checked': len(pair_records),
                      'source_minimum_squared_separation': source_min2,
                      'target_minimum_squared_separation': target_min2,
                      'minimum_damped_squared_loss': min(F(row[4]) for row in pair_records),
                      'pair_record_sha256': sha256(record_bytes).hexdigest(),
                      'selected_direction_indices': chosen, 'selected_clouds': selected},
        'positive_motion': {'first_endpoint_test_upper': first, 'last_endpoint_test_upper': last,
                            'endpoint_lipschitz_upper': (lam+eta)/(1-epsilon)},
        'orientation': {'squared_edge_error_upper': squared_edge_error,
                        'gram_entry_error_upper': entry_error,
                        'uniform_gram_eigenvalue_lower': gram_floor,
                        'source_endpoint_singular_margin': source_orientation_margin,
                        'target_endpoint_singular_margin': target_orientation_margin,
                        'relative_orientation_sign_initial': -1,
                        'relative_orientation_sign_final': 1},
        'paired_rank': {'rank': 6, 'reference_minor': det6,
                        'smallest_singular_lower_after_perturbation': paired_rank_margin},
        'scalar_defect': {'anchor_pairs_used': 24, 'D_A': DA, 'D_B': DB,
                          'necessary_lhs': scalar_lhs, 'necessary_rhs': scalar_rhs,
                          'contradiction_gap': scalar_gap},
        'controls': controls,
        'scope': 'All endpoint perturbations in the stated Euclidean balls; no perturbation grid',
    }


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = (json.dumps(encode(audit()), indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        expected = Path(__file__).with_name('EXPECTED_ROBUSTNESS.json').read_bytes()
        require(result == expected, 'EXPECTED_ROBUSTNESS.json does not match the exact audit')
        print('AXIAL_UNIFORM_ROBUSTNESS_AUDITS_PASS', sha256(result).hexdigest())
    else:
        print(result.decode(), end='')


if __name__ == '__main__':
    main()
