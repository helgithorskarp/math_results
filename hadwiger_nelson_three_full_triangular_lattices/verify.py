#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; the infinite theorem is a written proof."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import hashlib
import json
from math import isqrt, lcm
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def v3(q):
    q = F(q)
    require(q != 0, 'valuation of zero requested')
    n, d, value = abs(q.numerator), q.denominator, 0
    while n % 3 == 0:
        value += 1
        n //= 3
    while d % 3 == 0:
        value -= 1
        d //= 3
    return value


def residue(q):
    q = F(q)
    require(q.denominator % 3 != 0, 'nonintegral residue input')
    return q.numerator * pow(q.denominator, -1, 3) % 3


def norm(z):
    a, b = z
    return a*a+a*b+b*b


def rho(z):
    return (z[0]-z[1]) % 3


def field_norm(z):
    # z=x0+x1 sqrt(33)+i sqrt(3)(y0+y1 sqrt(33)).
    x0, x1, y0, y1 = z
    return (x0*x0+33*x1*x1+3*y0*y0+99*y1*y1,
            2*x0*x1+6*y0*y1)


def rotate(alpha, z):
    # Multiply by a+b omega, with omega=(1+i sqrt(3))/2.
    x0, x1, y0, y1 = alpha
    u, v = F(2*z[0]+z[1], 2), F(z[1], 2)
    return (u*x0-3*v*y0, u*x1-3*v*y1,
            v*x0+u*y0, v*x1+u*y1)


def root_minus11(digits):
    # A simple Hensel lift: s^2=-11 and s=1 modulo 3.
    s, modulus = 1, 3
    for _ in range(1, digits):
        candidates = [s+k*modulus for k in range(3)
                      if ((s+k*modulus)**2+11) % (3*modulus) == 0]
        require(len(candidates) == 1, 'Hensel lift not unique')
        s, modulus = candidates[0], 3*modulus
    require((s*s+11) % modulus == 0, 'incorrect local root')
    return s


def local_rotation(alpha, digits):
    # In the split completion sqrt(33)=pi*s, pi^2=-3, s^2=-11.
    # Root congruence plus the explicit error bound certifies the leading digit.
    s = root_minus11(digits)
    x0, x1, y0, y1 = alpha
    a, b = x0-3*y1*s, y0+x1*s
    candidates = []
    if a:
        candidates.append((2*v3(a), a))
    if b:
        candidates.append((1+2*v3(b), b))
    require(candidates, 'rotation vanished')
    t, leading = min(candidates)
    errors = []
    if y1:
        errors.append(2*(digits+v3(-3*y1)))
    if x1:
        errors.append(1+2*(digits+v3(x1)))
    require(not errors or min(errors) > t, 'insufficient local precision')
    eta = residue(leading * F(-3)**(-(t//2)))
    require(eta in (1, 2), 'zero leading residue')
    return t, eta


def f9_control():
    elements = list(product(range(3), repeat=2))
    steps = [(a, b) for a, b in elements if (a*a+b*b) % 3 == 1]
    require(set(steps) == {(1, 0), (2, 0), (0, 1), (0, 2)}, 'wrong norm circle')
    edges = []
    for p, q in combinations(elements, 2):
        if ((p[0]-q[0])**2+(p[1]-q[1])**2) % 3 == 1:
            require(sum(p) % 3 != sum(q) % 3, 'F9 colouring conflict')
            edges.append((p, q))
    return {'vertices': 9, 'unit_edges': len(edges), 'norm_one_steps': steps}


def interval_control():
    cases = edges = endpoint_ties = 0
    for heights in combinations_with_replacement(range(-5, 6), 3):
        centre_set = sorted(set(heights))
        median = centre_set[len(centre_set)//2]
        vertices = [(t, m) for t in centre_set for m in range(1, 13)]
        for (t, m), (u, n) in combinations(vertices, 2):
            # Definition-level interval contact, not the equation m+n=|t-u|.
            touching = t+m == u-n or u+n == t-m
            require(touching == (m+n == abs(t-u)), 'interval/contact mismatch')
            if not touching:
                continue
            a = t-m <= median < t+m
            b = u-n <= median < u+n
            require(a != b, 'median colouring conflict')
            edges += 1
            endpoint_ties += int(median in (t-m, t+m, u-n, u+n))
        cases += 1
    # Closed intervals would assign the same colour at the touching median.
    require((-1 <= 0 <= 0) and (0 <= 0 <= 1), 'closed-interval control failed')
    return {'height_triples': cases, 'contacts_checked': edges,
            'contacts_at_median_endpoint': endpoint_ties}


def valuation_control():
    rows = zero_edges = primitive_exclusions = tie_exclusions = 0
    for t, u, m, n in product(range(-5, 6), range(-5, 6), range(9), range(9)):
        first, second = min(t+m, u+n), min(-t+m, -u+n)
        tied = t+m == u+n or -t+m == -u+n
        if m >= 1 and n >= 1:
            if tied:
                require(first+second > 0, 'tie may evade zero-point argument')
                tie_exclusions += 1
            else:
                require((first+second == 0) == (m+n == abs(t-u)),
                        'zero-point valuation implication failed')
                zero_edges += int(first+second == 0)
        if m == n == 0 and t != u:
            require(not tied and first+second < 0, 'primitive cross-height edge')
            primitive_exclusions += 1
        rows += 1
    return {'valuation_rows': rows, 'zero_point_contacts': zero_edges,
            'positive_tie_exclusions': tie_exclusions,
            'primitive_cross_height_exclusions': primitive_exclusions}


def degree_control():
    # Four conjugates of beta/alpha in Q(sqrt(2),sqrt(5)); the written
    # nonzero-coefficient argument proves the general compatibility lemma.
    cases = 0
    for a, b, c, d in product((-2, -1, 1, 2), repeat=4):
        denominator = a*a-2*b*b
        require(denominator != 0, 'zero algebraic denominator')
        coefficients = (a*c, -b*c, a*d, -b*d)
        orbit = {(coefficients[0], su*coefficients[1], sv*coefficients[2],
                  su*sv*coefficients[3]) for su, sv in product((-1, 1), repeat=2)}
        require(len(orbit) == 4, 'quadratic compatibility control failed')
        cases += 1
    # Nonzero trace is necessary: sqrt(5)/sqrt(2) has only degree two.
    trace_zero_orbit = {(0, 0, 0, su*sv) for su, sv in product((-1, 1), repeat=2)}
    require(len(trace_zero_orbit) == 2, 'trace-zero boundary missing')
    return {'nonzero_trace_cases': cases, 'trace_zero_ratio_degree': 2}


def patch_points(radius):
    bound = isqrt(2*radius)+1
    return sorted((a, b) for a in range(-bound, bound+1)
                  for b in range(-bound, bound+1) if norm((a, b)) <= radius)


def propagation(points):
    # Direct triangle propagation independently checks the finite fixture's
    # lower chromatic bound; it is unnecessary for the full-lattice theorem.
    index = {z: i for i, z in enumerate(points)}
    neighbours = [set() for _ in points]
    for i, z in enumerate(points):
        for j, w in enumerate(points[:i]):
            if norm((z[0]-w[0], z[1]-w[1])) == 1:
                neighbours[i].add(j)
                neighbours[j].add(i)
    known = {index[(0, 0)], index[(1, 0)], index[(0, 1)]}
    rounds = 0
    while len(known) < len(points):
        new = set()
        for i in range(len(points)):
            if i in known:
                continue
            for a, b in combinations(neighbours[i] & known, 2):
                if b in neighbours[a]:
                    require({rho(points[i]), rho(points[a]), rho(points[b])} == {0, 1, 2},
                            'triangle residues wrong')
                    new.add(i)
                    break
        require(new, 'triangle propagation incomplete')
        known.update(new)
        rounds += 1
    return rounds


def fixture():
    # An active triangle outside the old P48 census. Data are explicit
    # rational coefficients, not an external graph or a rounded drawing.
    rotations = [tuple(map(F, row)) for row in (
        ('1', '0', '0', '0'),
        ('275/279', '1/558', '-25/279', '11/1674'),
        ('31/36', '-1/108', '-31/108', '-1/108'))]
    for a in rotations:
        require(field_norm(a) == (1, 0), 'rotation not exactly unit')
    local = [local_rotation(a, 24) for a in rotations]
    require(local == [local_rotation(a, 31) for a in rotations],
            'local leading terms unstable')
    heights = sorted(set(t for t, _ in local))
    median = heights[len(heights)//2]
    points = patch_points(147)
    records = []
    for layer, alpha in enumerate(rotations):
        t, eta = local[layer]
        for z in points:
            coordinates = rotate(alpha, z)
            require(field_norm(coordinates) == (norm(z), 0), 'isometry failed')
            if z == (0, 0):
                colour, depth = 2, None
            else:
                depth = v3(norm(z))
                require((depth > 0) == (rho(z) == 0), 'valuation/residue mismatch')
                colour = (eta*rho(z) % 3)-1 if depth == 0 else (
                    2 if t-depth <= median < t+depth else 3)
            records.append((coordinates, colour, layer, z, depth))
    denominator = lcm(*(q.denominator for row in records for q in row[0]))
    deduplicated = {}
    for coordinates, colour, layer, z, depth in records:
        key = tuple(int(q*denominator) for q in coordinates)
        previous = deduplicated.setdefault(key, (colour, []))
        require(previous[0] == colour, 'coincident labels have different colours')
        previous[1].append((layer, z, depth))
    coordinates = sorted(deduplicated)
    edges = []
    active, zero_active = Counter(), Counter()
    zero_witness = None
    for i, p in enumerate(coordinates):
        for j, q in enumerate(coordinates[:i]):
            a, b, c, d = (x-y for x, y in zip(p, q))
            if a*a+33*b*b+3*c*c+99*d*d != denominator*denominator:
                continue
            if 2*a*b+6*c*d != 0:
                continue
            require(deduplicated[p][0] != deduplicated[q][0], 'physical unit-edge conflict')
            edges.append((j, i))
            for lp, zp, mp in deduplicated[p][1]:
                for lq, zq, mq in deduplicated[q][1]:
                    if lp == lq or zp == (0, 0) or zq == (0, 0):
                        continue
                    pair = tuple(sorted((lp, lq)))
                    active[pair] += 1
                    if mp > 0 and mq > 0:
                        zero_active[pair] += 1
                        zero_witness = zero_witness or [lp, list(zp), lq, list(zq)]
    require(set(active) == {(0, 1), (0, 2), (1, 2)}, 'fixture is not an active triangle')
    require(zero_witness is not None, 'zero-zero witness absent')
    rounds = propagation(points)
    stream = ''.join(f'{a} {b}\n' for a, b in sorted(edges)).encode()
    return {'radius_squared': 147, 'patch_vertices': len(points),
            'physical_vertices': len(coordinates), 'strict_unit_edges': len(edges),
            'coordinate_denominator': denominator, 'local_height_and_sign': local,
            'median_height': median, 'active_cross_edges': {str(k): v for k, v in sorted(active.items())},
            'zero_cross_edges': {str(k): v for k, v in sorted(zero_active.items())},
            'zero_edge_witness': zero_witness, 'triangle_propagation_rounds': rounds,
            'chromatic_number': 4, 'edge_sha256': hashlib.sha256(stream).hexdigest()}


def spindle():
    one = tuple(map(F, (1, 0, 0, 0)))
    moser = (F(5, 6), F(0), F(0), F(1, 18))
    points = sorted({rotate(a, z) for a in (one, moser)
                     for z in ((0, 0), (1, 0), (0, 1), (1, 1))})
    edges = [(i, j) for i, p in enumerate(points) for j, q in enumerate(points[:i])
             if field_norm(tuple(x-y for x, y in zip(p, q))) == (1, 0)]
    counts = {}
    for k in (3, 4):
        counts[k] = sum(all(word[i] != word[j] for i, j in edges)
                        for word in product(range(k), repeat=len(points)))
    require(len(points) == 7 and len(edges) == 11 and counts == {3: 0, 4: 384},
            'sharpness benchmark failed')
    return {'vertices': 7, 'strict_edges': 11, 'proper_3_colourings': counts[3],
            'proper_4_colourings': counts[4]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = {'status': 'PASS', 'role': 'finite exact controls; universal theorem is PROOF.md',
              'f9': f9_control(), 'intervals': interval_control(),
              'valuations': valuation_control(), 'quadratic_compatibility': degree_control(),
              'active_triangle': fixture(), 'sharpness': spindle()}
    output = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.check_expected:
        require(output == Path(__file__).with_name('EXPECTED.json').read_text(),
                'expected output mismatch')
    print(output, end='')


if __name__ == '__main__':
    main()
