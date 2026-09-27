#!/usr/bin/env python3
"""Exact all-threshold certificate for the parameter cell in CELL.json.

CPython >=3.11, standard library only. See PROOF.md for all analytic bridges.
The imported scalar enclosures and quadrature bound are pinned dependencies.
This is an author checker, not an independent review or formal proof.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import factorial
from pathlib import Path
import argparse
import json
import sys
import time

HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE.parent / 'gaussian_prior_localization'
PINS = {
    'direct_hinge.py': '94e9ee5f643a6d98bf18983eda3a13f5b8513f2f6e06753ad133ad046d2e5bb9',
    'DIRECT_HINGE.md': 'b6abfa8a14481aa834869403f80c424c7d9f62b75a62e5db6890d1278c4867ea',
    'CUBATURE_FRONTIER.md': '0dbcaf36263ee8ce2976d75d1073db4f878db908fd5c53161e55485c5da53632',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


for name, expected_hash in PINS.items():
    need(sha256((DEPENDENCY / name).read_bytes()).hexdigest() == expected_hash,
         'dependency hash mismatch: ' + name)
sys.path.insert(0, str(DEPENDENCY))
from direct_hinge import (density_histograms, exp_neg, gaussian_constant,
                          quadrature_error)


def window_max(source, target, left, right):
    """Maximum of the upper adverse polygon on the WHOLE closed window."""
    need(0 <= left < right, 'invalid threshold window')
    need(sum(source.values()) == sum(target.values()), 'unequal site totals')
    need(all(isinstance(v, int) and v >= 0 and isinstance(n, int) and n > 0
             for hist in (source, target) for v, n in hist.items()),
         'invalid histogram')
    value = sum(n * max(v-left, 0) for v, n in source.items())
    value -= sum(n * max(v-left, 0) for v, n in target.items())
    best, arg = value, left
    slope = -sum(n for v, n in source.items() if v > left)
    slope += sum(n for v, n in target.items() if v > left)
    previous = left
    knots = sorted({v for v in source.keys() | target.keys()
                    if left < v <= right} | {right})
    for knot in knots:
        value += slope * (knot-previous)
        if value > best:
            best, arg = value, knot
        slope += source.get(knot, 0)-target.get(knot, 0)
        previous = knot
    return best, arg, len(knots)


def orbit_histograms(h, M, bits):
    """Source upper and point-target lower density values, with multiplicity."""
    need(h > 0 and isinstance(M, int) and M >= 0 and bits >= 16,
         'invalid lattice parameters')
    Q = 1 << bits
    A = [exp_neg((h*j)**2/2, bits) for j in range(M+1)]
    B = []
    for j in range(M+1):
        a = exp_neg((h*j-1)**2/2, bits)
        b = exp_neg((h*j+1)**2/2, bits)
        B.append((a[0]+b[0], a[1]+b[1]))
    source, target = Counter(), Counter()
    count = orbits = 0
    stream = sha256()
    for i, j, k in combinations_with_replacement(range(M+1), 3):
        mult = (1 << sum(v > 0 for v in (i, j, k))) * 6
        divisor = 1
        for n in Counter((i, j, k)).values():
            divisor *= factorial(n)
        need(mult % divisor == 0, 'nonintegral orbit multiplicity')
        mult //= divisor
        ai, aj, ak = A[i][1], A[j][1], A[k][1]
        numerator = 12*ai*aj*ak + 11*(B[i][1]*aj*ak
                       + ai*B[j][1]*ak + ai*aj*B[k][1])
        denominator = 78*Q*Q
        fu = (numerator+denominator-1)//denominator
        gl = A[i][0]*A[j][0]*A[k][0]//(Q*Q)
        source[fu] += mult
        target[gl] += mult
        count += mult
        orbits += 1
        stream.update(f'{i},{j},{k},{mult},{fu},{gl}\n'.encode())
    need(count == (2*M+1)**3, 'incomplete lattice coverage')
    return source, target, orbits, stream.hexdigest()


def determinant(rows):
    a = [list(map(F, row)) for row in rows]
    n = len(a)
    need(all(len(row) == n for row in a), 'nonsquare determinant')
    answer = F(1)
    for i in range(n):
        p = next((j for j in range(i, n) if a[j][i]), None)
        if p is None:
            return F(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            answer = -answer
        pivot = a[i][i]
        answer *= pivot
        for j in range(i+1, n):
            factor = a[j][i]/pivot
            for k in range(i, n):
                a[j][k] -= factor*a[i][k]
    return answer


def controls(centers):
    # A general, unquotiented implementation checks every histogram entry.
    groups = Counter({tuple(map(F, x)): 12 if i == 0 else 11
                      for i, x in enumerate(centers)})
    zero = Counter({(F(0),)*3: 1})
    lattice_cases = 0
    for h, M in [(F(1, 2), 2), (F(1, 3), 3), (F(1, 4), 4)]:
        source, target, _, _ = orbit_histograms(h, M, 32)
        _, direct_source, *_ = density_histograms(groups, 78, h, M, 32)
        direct_target, *_ = density_histograms(zero, 1, h, M, 32)
        need(source == direct_source and target == direct_target,
             'orbit histograms disagree with unquotiented density sums')
        lattice_cases += (2*M+1)**3
    # Definition-level maxima, including negative maxima and boundary knots.
    sweep_cases = 0
    values = list(product(range(4), repeat=2))
    for xs in values:
        for ys in values:
            source, target = Counter(xs), Counter(ys)
            for left, right in [(0, 3), (1, 2), (1, 3)]:
                best, arg, _ = window_max(source, target, left, right)
                knots = {left, right} | {v for v in xs+ys if left <= v <= right}
                direct = {u: sum(max(x-u, 0) for x in xs)
                          - sum(max(y-u, 0) for y in ys) for u in knots}
                need(best == max(direct.values()) and direct[arg] == best,
                     'window sweep disagrees with definition')
                sweep_cases += 1
    return {'unquotiented_lattice_sites': lattice_cases,
            'definition_level_window_sweeps': sweep_cases}


def calculate():
    data = (HERE/'CELL.json').read_bytes()
    cell = json.loads(data)
    centers = [[0, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 1, 0],
               [0, -1, 0], [0, 0, 1], [0, 0, -1]]
    need(cell['source_centers'] == centers, 'wrong reference source')
    weights = list(map(F, cell['weights']))
    need(weights == [F(2, 13)]+[F(11, 78)]*6, 'wrong cell weights')
    need(F(cell['variance']) == 1 and cell['frontier_level'] == 1
         and cell['coordinate_denominator'] == 256
         and cell['weight_denominator'] == 156, 'wrong frontier normalization')
    need(F(cell['source_coordinate_radius']) == F(1, 256)
         and F(cell['target_coordinate_radius']) == F(1, 16), 'wrong cell radii')
    need(cell['frontier_anchoring'] == 'subtract each endpoint label 0 separately'
         and cell['anchored_subcell_dimension'] == 36, 'wrong frontier gauge')
    a, b = map(F, cell['middle_window'])
    need((a, b) == (F(1, 256), F(11, 16)), 'wrong window')
    need(F(cell['claimed_adverse_middle_upper']) == -F(1, 200), 'wrong margin')
    eps, target_radius, rho = F(1, 128), F(7, 64), F(25, 8)
    need(3*F(1, 256)**2 < eps**2
         and 3*F(1, 16)**2 < target_radius**2, 'invalid Euclidean bounds')
    loss_floor = (1-2*eps)**2-F(3, 64)
    need(loss_floor > F(1, 256) and 1+2*eps < 3 and 2*target_radius < 3,
         'anchored frontier cell not strict or outside its radius')
    example = [tuple(F(v, 256) for v in row)
               for row in cell['rank_six_target_integer_numerators']]
    need(len(example) == 7 and all(len(row) == 3 for row in example),
         'malformed example')
    need(all(abs(v) <= F(1, 16) for row in example for v in row),
         'example outside cell')
    paired_rows = [[F(centers[i][j]-centers[0][j]) for j in range(3)]
                   + [example[i][j]-example[0][j] for j in range(3)]
                   for i in range(1, 7)]
    det = determinant(paired_rows)
    need(det != 0, 'example not paired rank six')
    losses = [sum(F(centers[i][k]-centers[j][k])**2 for k in range(3))
              - sum((example[i][k]-example[j][k])**2 for k in range(3))
              for i in range(7) for j in range(i)]
    need(min(losses) >= loss_floor and len(set(example)) == 7,
         'invalid injective strict example')
    checked = controls(centers)
    bits, h, M = 48, F(1, 16), 112
    Q = 1 << bits
    source, target, orbits, digest = orbit_histograms(h, M, bits)
    upper, arg, knots = window_max(source, target, int(a*Q), int(b*Q))
    cl, cu = gaussian_constant(bits)
    # A negative sum needs the LOWER positive C for an UPPER product bound.
    discrete = (cl if upper < 0 else cu)*h**3*F(upper, Q)
    quad, tail = quadrature_error(h, M*h-1, bits+10)
    reference_upper = discrete+quad+tail
    perturbation = eps/2+F(3, 256)/4
    cell_upper = reference_upper+perturbation
    need(cell_upper < -F(1, 200), 'middle cell margin not established')
    slope = F(4, 7)-eps-target_radius
    exponent = rho*slope-F(1, 2)-eps-eps**2/2+target_radius**2/2
    need(slope > 0 and exponent > 0, 'outer comparison has wrong slope')
    outer_exp_upper = F(exp_neg(exponent, bits)[1], Q)
    need(outer_exp_upper < F(11, 26), 'outer density domination unproved')
    source_inside = F(exp_neg((rho+eps)**2/2+F(11, 26)+eps, bits)[0], Q)
    target_inside = F(exp_neg((rho+target_radius)**2/2, bits)[0], Q)
    need(min(source_inside, target_inside) > a, 'low endpoint has a gap')
    need(F(exp_neg(F(1, 2), bits)[1], Q) < F(61, 100), 'peak scalar bound')
    peak = F(2, 13)+F(11, 13)*F(61, 100)+eps
    need(peak < b, 'upper endpoint has a gap')
    return {
        'status': 'GAP_FREE_FRONTIER_CELL_PASS',
        'cell_sha256': sha256(data).hexdigest(), 'dependency_sha256': PINS,
        'variance': 1, 'window': [str(a), str(b)], 'step': str(h),
        'bits': bits, 'half_grid': M, 'full_lattice_sites': (2*M+1)**3,
        'orbit_representatives': orbits, 'window_knots': knots,
        'discrete_adverse_upper': str(discrete), 'argmax_over_C': str(F(arg, Q)),
        'quadrature_error': str(quad), 'tail_error': str(tail),
        'reference_adverse_upper': str(reference_upper),
        'cell_perturbation_loss': str(perturbation),
        'cell_adverse_upper': str(cell_upper), 'claimed_upper': '-1/200',
        'outer_slope_lower': str(slope), 'outer_exponent': str(exponent),
        'outer_exp_upper': str(outer_exp_upper),
        'source_inside_lower': str(source_inside), 'target_inside_lower': str(target_inside),
        'source_peak_upper': str(peak), 'uniform_pair_loss_lower': str(loss_floor),
        'anchored_source_radius_upper': str(1+2*eps),
        'anchored_target_radius_upper': str(2*target_radius),
        'anchored_independent_coordinates': 36,
        'example_paired_determinant': str(det), 'example_minimum_loss': str(min(losses)),
        'orbit_stream_sha256': digest, 'controls': checked,
        'scope': 'All thresholds and every point of the stated continuous cell at variance one. Independent review pending; unrestricted majorisation remains open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'EXPECTED.json')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    record = calculate()
    encoded = (json.dumps(record, indent=2, sort_keys=True)+'\n').encode()
    if args.write_expected:
        args.expected.write_bytes(encoded)
    else:
        need(json.loads(args.expected.read_text()) == record, 'expected certificate mismatch')
    print(record['status'])
    print('record_sha256', sha256(encoded).hexdigest())
    print('cell_adverse_upper', record['cell_adverse_upper'])
    print('full_lattice_sites', record['full_lattice_sites'])
    print('seconds', round(time.monotonic()-start, 3))


if __name__ == '__main__':
    main()
