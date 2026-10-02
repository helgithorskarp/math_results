"""Check identities with sparse polynomials, signs with Bernstein products,
and seams with union-find and undirected boundary walks.

No producer or poly.py import. Same researcher, not independent review.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def keys(d, names):
    need(isinstance(d, dict) and set(d) == set(names.split()), 'field schema')


def plus(p, q):
    result = p.copy()
    for k, v in q.items():
        result[k] = result.get(k, F(0)) + v
    return {k: v for k, v in result.items() if v}


def minus(p):
    return {k: -v for k, v in p.items()}


def times(p, q):
    result = {}
    for i, a in p.items():
        for j, b in q.items():
            result[i + j] = result.get(i + j, F(0)) + a * b
    return {k: v for k, v in result.items() if v}


UNIT, C, H = {0: F(1)}, {1: F(1)}, {0: F(1), 1: F(2)}


def decode(values):
    need(isinstance(values, list) and all(isinstance(x, str) for x in values), 'rational coefficients')
    numbers = [F(x) for x in values]
    need(not numbers or numbers[-1] != 0, 'trailing polynomial zero')
    return {i: value for i, value in enumerate(numbers) if value}


def rational(value):
    keys(value, 'numerator denominator')
    n, d = decode(value['numerator']), decode(value['denominator'])
    need(bool(d), 'zero function denominator')
    return n, d


def constant(p):
    return p, UNIT


def radd(a, b):
    return plus(times(a[0], b[1]), times(b[0], a[1])), times(a[1], b[1])


def rneg(a):
    return minus(a[0]), a[1]


def rmul(a, b):
    return times(a[0], b[0]), times(a[1], b[1])


def equal(a, b):
    return not plus(times(a[0], b[1]), minus(times(b[0], a[1])))


def bernstein_product(a, b):
    m, n = len(a) - 1, len(b) - 1
    answer = [F(0)] * (m + n + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            answer[i + j] += x * y * F(comb(m, i) * comb(n, j), comb(m + n, i + j))
    return answer


def enclosure(p, lo, hi):
    """Build powers of c in Bernstein form, then elevate and add them."""
    degree = max(p, default=0)
    powers, now = [], [F(1)]
    for i in range(degree + 1):
        powers.append(bernstein_product(now, [F(1)] * (degree - i + 1)))
        now = bernstein_product(now, [lo, hi])
    return [sum(p.get(i, F(0)) * powers[i][j] for i in range(degree + 1))
            for j in range(degree + 1)]


def signs(p, lo, hi, sign):
    values = enclosure(p, lo, hi)
    need(all(sign * value > 0 for value in values), 'strict interval sign')
    return values


def star_cases(rows, lo, hi):
    need(isinstance(rows, list) and len(rows) == 3, 'three star cases')
    need({row['t'] for row in rows} == {1, 2, 3}, 'complete t domain')
    # Direct multiple-angle identities, not the producer's cotangent recurrence.
    expected_b = {1: (UNIT, UNIT),
                  2: (plus(H, minus(UNIT)), times({0: F(2)}, H)),
                  3: (plus(H, {0: F(-3)}), plus(times({0: F(3)}, H), minus(UNIT)))}
    for row in rows:
        keys(row, 't B_over_A S_over_A P Delta solver_divisor_over_A '
                  'solver_divisor_numerator_Bernstein solver_divisor_denominator_Bernstein '
                  'Delta_numerator_Bernstein Delta_denominator_Bernstein')
        t = row['t']
        need(type(t) is int and t in (1, 2, 3), 'star index')
        b, s, p, delta, divisor = [rational(row[name]) for name in
                                  ('B_over_A', 'S_over_A', 'P', 'Delta', 'solver_divisor_over_A')]
        need(equal(b, expected_b[t]), 'multiple-angle cotangent identity')
        need(equal(divisor, radd(constant(UNIT), rmul(constant(C), b))), 'star solver divisor')
        need(equal(radd(p, rmul(constant(H), s)), constant(UNIT)), 'A endpoint equation')
        rhs_b = rmul(constant(times(C, H)), rmul(s, b))
        need(equal(radd(p, rneg(constant(times(C, C)))), rhs_b), 'B endpoint equation')
        expected_delta = radd(rmul(constant(H), rmul(s, s)), rneg(rmul(constant({0: F(4)}), p)))
        need(equal(delta, expected_delta), 'squared-difference discriminant identity')
        for value in (b, s, p, delta, divisor):
            signs(value[1], lo, hi, 1)
        bindings = [('solver_divisor_numerator_Bernstein', divisor[0], 1),
                    ('solver_divisor_denominator_Bernstein', divisor[1], 1),
                    ('Delta_numerator_Bernstein', delta[0], -1),
                    ('Delta_denominator_Bernstein', delta[1], 1)]
        for field, polynomial, sign in bindings:
            expected = signs(polynomial, lo, hi, sign)
            need([F(x) for x in row[field]] == expected, 'full Bernstein coefficient binding')


def vertex(s):
    need(isinstance(s, str), 'vertex identifier')
    bits = s.split(':')
    need(len(bits) == 2 and all(x.isdigit() for x in bits), 'vertex encoding')
    result = tuple(map(int, bits))
    need(s == str(result[0]) + ':' + str(result[1]), 'canonical vertex encoding')
    return result


def audit_ring(row):
    keys(row, 'sides ports classes boundary_arcs boundary_cycles seams mixed_corners_per_boundary')
    q, k = row['sides'], row['ports']
    need(len(q) == len(k) == 3 and all(type(x) is int for x in q + k), 'typed three-face ports')
    need(all(size in (4, 5) and 2 <= port <= size - 2 for size, port in zip(q, k)), 'port domain')
    points = {(i, j) for i in range(3) for j in range(q[i])}
    parent = {v: v for v in points}

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    def join(a, b):
        a, b = root(a), root(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for i in range(3):
        join((i, k[i]), ((i + 1) % 3, 1))
        join((i, k[i] + 1), ((i + 1) % 3, 0))
    expected_classes = {}
    for point in points:
        expected_classes.setdefault(root(point), set()).add(point)
    supplied_classes = [frozenset(vertex(v) for v in group) for group in row['classes']]
    need(len(supplied_classes) == len(set(supplied_classes)), 'distinct quotient classes')
    need(set(supplied_classes) == {frozenset(group) for group in expected_classes.values()}, 'all quotient classes')
    need(all(len(group) in (1, 2) for group in expected_classes.values()), 'no triple points')
    directed = []
    adjacency = {v: set() for v in expected_classes}
    for i in range(3):
        for j in range(q[i]):
            if j in (0, k[i]):
                continue
            a, b = root((i, j)), root((i, (j + 1) % q[i]))
            need(a != b, 'no boundary loop')
            directed.append((a, b))
            adjacency[a].add(b)
            adjacency[b].add(a)
    actual_arcs = [tuple(vertex(v) for v in arc) for arc in row['boundary_arcs']]
    need(len(actual_arcs) == len(directed) and set(actual_arcs) == set(directed), 'every physical boundary arc')
    need(all(len(neighbors) == 2 for neighbors in adjacency.values()), 'boundary degree two')
    unseen, discovered = set(adjacency), []
    while unseen:
        start, previous = min(unseen), None
        current, cycle = start, []
        while current not in cycle:
            need(current in unseen, 'walk cannot merge with another component')
            unseen.remove(current)
            cycle.append(current)
            nxt = min(adjacency[current] - ({previous} if previous is not None else set()))
            previous, current = current, nxt
        need(current == start, 'closed boundary walk')
        discovered.append(set(cycle))
    cycles = [[vertex(v) for v in cycle] for cycle in row['boundary_cycles']]
    need(len(cycles) == 2, 'exactly two boundaries')
    need({frozenset(cycle) for cycle in cycles} == {frozenset(cycle) for cycle in discovered}, 'full boundary components')
    membership = {}
    for index, cycle in enumerate(cycles):
        need(len(cycle) == len(set(cycle)) >= 3, 'simple cycle')
        need(all(cycle[(i + 1) % len(cycle)] in adjacency[v] for i, v in enumerate(cycle)), 'cyclic edge order')
        for v in cycle:
            need(v not in membership, 'disjoint boundary cycles')
            membership[v] = index
    need(set(membership) == set(expected_classes), 'all vertices on boundary')
    need(row['mixed_corners_per_boundary'] == [3, 3], 'mixed-corner field')
    need(all(sum(len(expected_classes[v]) == 2 for v in cycle) == 3 for cycle in cycles), 'actual mixed-corner count')
    need(len(row['seams']) == 3 and {item['face'] for item in row['seams']} == {0, 1, 2}, 'complete seam domain')
    for item in row['seams']:
        keys(item, 'face endpoints')
        i = item['face']
        need(type(i) is int, 'seam face index')
        endpoints = [vertex(v) for v in item['endpoints']]
        need(len(endpoints) == 2 and set(endpoints) == {root((i, k[i])), root((i, k[i] + 1))}, 'exact seam endpoints')
        need(membership[endpoints[0]] != membership[endpoints[1]], 'seam crosses boundary components')
    return tuple(q), tuple(k)


def calibration(data, rows):
    keys(data, 'c labels Gram contact_pairs faces')
    need(data['c'] == '1/7' and data['labels'] == ['U0', 'U1', 'U2', 'V0', 'V1', 'V2'], 'prism calibration domain')
    gram, labels = data['Gram'], data['labels']
    need(len(gram) == 6 and all(len(row) == 6 for row in gram), 'full prism Gram matrix')
    contacts, noncontacts = set(), 0
    for a in range(6):
        for b in range(6):
            expected = F(1) if a == b else (F(1, 7) if a // 3 == b // 3 or a % 3 == b % 3 else F(-5, 7))
            need(F(gram[a][b]) == expected, 'every prism Gram entry')
            if a < b:
                need(expected <= F(1, 7), 'prism packing inequality')
                if expected == F(1, 7):
                    contacts.add(frozenset((labels[a], labels[b])))
                else:
                    noncontacts += 1
    supplied = [frozenset(pair) for pair in data['contact_pairs']]
    need(len(supplied) == len(contacts) == 9 and set(supplied) == contacts and noncontacts == 6, 'complete prism contacts')
    need(all(sum(label in edge for edge in contacts) == 3 for label in labels), 'prism degrees')
    need({frozenset(face) for face in data['faces']} == {
        frozenset(('U0', 'U1', 'U2')), frozenset(('V0', 'V1', 'V2')),
        frozenset(('U0', 'U1', 'V0', 'V1')), frozenset(('U1', 'U2', 'V1', 'V2')),
        frozenset(('U2', 'U0', 'V2', 'V0'))}, 'all prism face vertex sets')
    arcs = []
    for face in data['faces']:
        need(len(face) == len(set(face)), 'simple prism face')
        for i, label in enumerate(face):
            edge = (label, face[(i + 1) % len(face)])
            need(frozenset(edge) in contacts, 'prism facial edge')
            arcs.append(edge)
    need(len(arcs) == 18 and set(arcs) == {(a, b) for edge in contacts for a in edge for b in edge if a != b}, 'oriented prism face complex')
    first = next(row for row in rows if row['t'] == 1)
    numerator, denominator = rational(first['Delta'])
    evaluate = lambda p: sum(value * F(1, 7) ** i for i, value in p.items())
    need(evaluate(numerator) == 0 and evaluate(denominator) > 0, 'outside-band zero discriminant calibration')


def verify(data):
    keys(data, 'format actual_agent role algebraic_closed_band physical_upper_endpoint_excluded '
               'application_closed_band A_squared star_cases rings prism_calibration adjacent_angle_factorization')
    need(data['format'] == 1 and data['actual_agent'] == 'six-tammes-1' and data['role'] == 'researcher', 'artifact identity')
    need(data['algebraic_closed_band'] == ['9/20', '1'] and data['physical_upper_endpoint_excluded'] is True,
         'closed algebraic band and open physical upper endpoint')
    need(data['application_closed_band'] == ['1/2', '3/5'] and decode(data['A_squared']) == H, 'application/A domain')
    lo, hi = map(F, data['algebraic_closed_band'])
    star_cases(data['star_cases'], lo, hi)
    # Base-three enumeration of the three possible typed ports on each face.
    expected_domain = set()
    for number in range(27):
        digits = [number // 3 ** i % 3 for i in range(3)]
        expected_domain.add((tuple(4 if digit == 0 else 5 for digit in digits),
                             tuple(3 if digit == 2 else 2 for digit in digits)))
    need(len(data['rings']) == 27, 'full 27-row annulus catalog')
    found = [audit_ring(row) for row in data['rings']]
    need(len(set(found)) == 27 and set(found) == expected_domain, 'every labeled port case exactly once')
    calibration(data['prism_calibration'], data['star_cases'])
    factor = data['adjacent_angle_factorization']
    keys(factor, 'left right_factors')
    left = plus(times({0: F(4)}, times(C, times(C, C))),
                minus(times(times(plus(UNIT, minus(C)), plus(UNIT, minus(C))), H)))
    right = UNIT
    need(len(factor['right_factors']) == 3, 'three factor occurrences')
    for p in factor['right_factors']:
        right = times(right, decode(p))
    need(decode(factor['left']) == left == right, 'adjacent-angle exact factorization')
    need([decode(p) for p in factor['right_factors']] == [{0: F(-1), 1: F(2)}, plus(UNIT, C), plus(UNIT, C)], 'factor endpoint signs')
    return {'star_cases': 3, 'all_star_equations_and_discriminants_bound': True,
            'strict_negative_discriminants': 3, 'annulus_port_cases': 27,
            'seams_joining_distinct_boundaries': 81, 'prism_Gram_entries': 36,
            'prism_contacts': 9, 'prism_strict_noncontacts': 6,
            'independent_adjacent_angle_factorization': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    answer = verify(json.loads(raw))
    answer['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(answer, sort_keys=True))


if __name__ == '__main__':
    main()
