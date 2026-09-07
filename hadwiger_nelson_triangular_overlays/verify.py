#!/usr/bin/env python3
"""Independent Cartesian audit. Standard library; imports no producer code."""
import argparse
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt, lcm
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fraction(value):
    require(isinstance(value, list) and len(value) == 2
            and all(type(x) is int for x in value), 'bad fraction encoding')
    n, d = value
    require(d > 0 and gcd(n, d) == 1, 'noncanonical fraction')
    return Fraction(n, d)


def coordinates():
    # Actual plane point is (X/2, sqrt(3)*Y/2). Scan Cartesian rows.
    result = []
    for y in range(-9, 10):
        for x in range(-16, 17):
            if (x-y) % 2 == 0 and x*x+3*y*y <= 268:
                result.append((x, y))
    return sorted(result, key=lambda z: ((z[0]-z[1])//2, z[1]))


def primitive_equation(values):
    divisor = gcd(*values)
    answer = tuple(x//divisor for x in values)
    if next(x for x in answer if x) < 0:
        answer = tuple(-x for x in answer)
    return answer


def expected_inventory(points):
    lines = set()
    coincidence_angles = set()
    for x, y in points:
        for a, b in points:
            if (x, y) == (0, 0) or (a, b) == (0, 0):
                continue
            if x*x+3*y*y == a*a+3*b*b:
                denominator = a*a+3*b*b
                coincidence_angles.add((Fraction(x*a+3*y*b, denominator),
                                        Fraction(y*a-x*b, denominator)))
            u = x*a+3*y*b
            v = 3*(y*a-x*b)
            k = (x*x+3*y*y+a*a+3*b*b-4)//2
            if 3*k*k <= 3*u*u+v*v:
                lines.add(primitive_equation((u, v, k)))
    irrational, rational = set(), set()
    for u, v, k in lines:
        d = 3*u*u+v*v-3*k*k
        h = isqrt(d)
        if h*h != d:
            irrational.add((u, v, k))
            continue
        # Rational parametrization of x^2+3*y^2=1, distinct from the
        # producer's orthogonal projection / line-intersection formula.
        parameters = set()
        if u+k:
            parameters.update(Fraction(v+sign*h, 3*(u+k)) for sign in (-1, 1))
        else:
            rational.add((Fraction(-1), Fraction(0)))  # t=infinity
            if v:
                parameters.add(Fraction(k-u, 2*v))
        for t in parameters:
            rational.add(((1-3*t*t)/(1+3*t*t), 2*t/(1+3*t*t)))
    require(coincidence_angles <= rational, 'omitted coincidence-only angle')
    return lines, irrational, rational, coincidence_angles


def three_colour_propagation(points, edges):
    adjacent = [set() for _ in points]
    for i, j in edges:
        adjacent[i].add(j)
        adjacent[j].add(i)
    colour = {points.index((0, 0)): 0,
              points.index((2, 0)): 1,
              points.index((1, 1)): 2}
    changed = True
    steps = []
    while changed:
        changed = False
        for i, j in edges:
            if i not in colour or j not in colour:
                continue
            require(colour[i] != colour[j], 'inconsistent forced colouring')
            for k in sorted(adjacent[i] & adjacent[j]):
                c = 3-colour[i]-colour[j]
                if k in colour:
                    require(colour[k] == c, 'inconsistent triangle')
                else:
                    colour[k] = c
                    steps.append([i, j, k])
                    changed = True
    require(len(colour) == len(points), 'patch is not triangle-connected')
    require(all(colour[i] == (-x) % 3 for i, (x, y) in enumerate(points)),
            'forced colouring differs from Cartesian residue')
    return len(steps)


def audit_irrational(row, points, residues, seed_edges):
    u, v, k = row['line']
    s = 3*u*u+v*v
    d = s-3*k*k
    require(d > 0 and isqrt(d)**2 != d and row['radicand'] == d,
            'bad irrational radicand')
    # alpha = (3uk + v sqrt(d))/s + i sqrt(3)*(vk-u sqrt(d))/s.
    # Its conjugate radical root is checked at the same time: for a
    # nonsquare positive d a norm is 1 iff both coefficients match.
    require((3*u*k)**2+3*(v*k)**2+d*(v*v+3*u*u) == s*s,
            'rotation has nonunit norm')
    require(3*u*k*v-3*v*k*u == 0, 'rotation radical norm term')
    moved = [(3*u*k*x-3*v*k*y, v*x+3*u*y,
              v*k*x+3*u*k*y, -u*x+v*y) for x, y in points]
    contacts = []
    coincidences = []
    for i, (x, y) in enumerate(points):
        bx, by = s*x, s*y
        for j, (x0, x1, y0, y1) in enumerate(moved):
            dx, dy = bx-x0, by-y0
            rational = dx*dx+3*dy*dy+d*(x1*x1+3*y1*y1)
            radical = dx*x1+3*dy*y1
            if radical == 0:
                if rational == 4*s*s:
                    contacts.append([i, j])
                if rational == 0:
                    coincidences.append([i, j])
    origin = points.index((0, 0))
    require(coincidences == [[origin, origin]], 'unexpected irrational coincidence')
    proper_contacts = [e for e in contacts if origin not in e]
    require(proper_contacts == row['cross_edges'], 'irrational contact mismatch')
    epsilon = row['epsilon']
    require(type(epsilon) is int and epsilon in (1, 2), 'bad epsilon')
    products = {residues[i]*residues[j] % 3 for i, j in proper_contacts
                if residues[i] and residues[j]}
    require(len(products) <= 1 and (not products or products == {epsilon}),
            'residue-product obstruction')
    zeros = [e for e in proper_contacts if not residues[e[0]] and not residues[e[1]]]
    require(row['zero_edge'] == (zeros[0] if zeros else None), 'bad lower witness')
    chi = 4 if zeros else 3
    require(row['chromatic_number'] == chi, 'bad chromatic classification')
    first = [0 if r == 0 else r+1 for r in residues]
    second = [((1 if chi == 4 else 0) if r == 0 else (-epsilon*r)%3+1)
              for r in residues]
    second[origin] = 0
    for colours in (first, second):
        require(all(colours[i] != colours[j] for i, j in seed_edges),
                'invalid within-layer colouring')
    require(all(first[i] != second[j] for i, j in contacts),
            'invalid cross-layer colouring')
    return (2*len(points)-1, 2*len(seed_edges)+len(proper_contacts), chi), len(contacts)


def audit_rational(row, points, residues, seed_edges):
    x, y = map(fraction, row['rotation'])
    require(x*x+3*y*y == 1, 'rational rotation norm')
    n = lcm(x.denominator, y.denominator)
    r, t = int(n*x), int(n*y)
    require(n % 3 != 0, 'rotation denominator divisible by three')
    epsilon = (r*pow(n, -1, 3)) % 3
    require(epsilon in (1, 2), 'rotation residue zero')
    base = [(n*a, n*b) for a, b in points]
    moved = [(r*a-3*t*b, t*a+r*b) for a, b in points]
    all_points = sorted(set(base+moved))
    index = {z: i for i, z in enumerate(all_points)}
    colours = {}
    for cloud, factor in ((base, 1), (moved, epsilon)):
        for z, residue in zip(cloud, residues):
            c = factor*residue % 3
            require(z not in colours or colours[z] == c, 'coincidence colour mismatch')
            colours[z] = c
    edges = set()
    for cloud in (base, moved):
        for i, j in seed_edges:
            edges.add(tuple(sorted((index[cloud[i]], index[cloud[j]]))))
    contacts, coincidences = [], []
    for i, (a, b) in enumerate(base):
        for j, (c, d) in enumerate(moved):
            norm = (a-c)**2+3*(b-d)**2
            if norm == 4*n*n:
                contacts.append([i, j])
                edges.add(tuple(sorted((index[a, b], index[c, d]))))
            if norm == 0:
                coincidences.append([i, j])
    origin = points.index((0, 0))
    require([e for e in contacts if origin not in e] == row['cross_edges'],
            'rational contact mismatch')
    require([e for e in coincidences if origin not in e] == row['coincidences'],
            'rational coincidence mismatch')
    require(all(i != j and colours[all_points[i]] != colours[all_points[j]]
                for i, j in edges), 'invalid rational colouring')
    return (len(all_points), len(edges), 3), len(contacts), len(coincidences)


def audit(table):
    require(table['format'] == 1 and table['norm_limit'] == 67, 'wrong family')
    points = coordinates()
    require(table['points'] == [[(x-y)//2, y] for x, y in points], 'point set mismatch')
    edges = [[i, j] for i, (x, y) in enumerate(points)
             for j, (a, b) in enumerate(points[:i]) if (x-a)**2+3*(y-b)**2 == 4]
    require(edges == table['seed_edges'], 'seed edge mismatch')
    origin = points.index((0, 0))
    universal = [[i, j] for i, (x, y) in enumerate(points)
                 for j, (a, b) in enumerate(points)
                 if (i == origin or j == origin) and x*x+3*y*y+a*a+3*b*b == 4]
    require(table['universal_cross_edges'] == universal, 'universal contacts mismatch')
    lines, irr, rat, coincidence_angles = expected_inventory(points)
    require(table['contact_lines'] == [list(t) for t in sorted(lines)], 'line census mismatch')
    require([row['line'] for row in table['irrational']] == [list(t) for t in sorted(irr)],
            'irrational inventory mismatch')
    given_rat = [tuple(map(fraction, row['rotation'])) for row in table['rational']]
    require(given_rat == sorted(rat), 'rational inventory mismatch')
    propagation = three_colour_propagation(points, edges)
    residues = [(-x) % 3 for x, y in points]
    census = Counter()
    contact_checks = 0
    for row in table['irrational']:
        key, count = audit_irrational(row, points, residues, edges)
        census[key] += 2
        contact_checks += 2*count
    coincidence_checks = 0
    for row in table['rational']:
        key, count, coinc = audit_rational(row, points, residues, edges)
        census[key] += 1
        contact_checks += count
        coincidence_checks += coinc
    return {'verified': True, 'patch_vertices': len(points), 'patch_edges': len(edges),
            'forced_triangle_steps': propagation, 'contact_lines': len(lines),
            'irrational_lines': len(irr), 'rational_rotations': len(rat),
            'nonzero_coincidence_rotations': len(coincidence_angles),
            'exceptional_rotations': 2*len(irr)+len(rat),
            'three_chromatic_exceptional_rotations': sum(v for k, v in census.items() if k[2] == 3),
            'four_chromatic_exceptional_rotations': sum(v for k, v in census.items() if k[2] == 4),
            'cartesian_cross_norm_evaluations': (len(irr)+len(rat))*len(points)**2,
            'unit_contacts_including_both_irrational_roots': contact_checks,
            'rational_coincidences_including_origins': coincidence_checks,
            'generic_graph': [2*len(points)-1, 2*len(edges), 3],
            'census': [list(k)+[v] for k, v in sorted(census.items())],
            'record_improvement': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    data = (args.work/'catalog.json').read_bytes()
    result = audit(json.loads(data))
    result['catalog_sha256'] = hashlib.sha256(data).hexdigest()
    (args.work/'verified.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
    print(json.dumps({'seconds': time.monotonic()-started}, sort_keys=True))


if __name__ == '__main__':
    main()
