#!/usr/bin/env python3
"""Exact arithmetic and tiny necessary H cover; no embedding enumeration.

Python >=3.11, standard library. See PROOF.md for the geometric trust boundary.
All failed obligations raise exceptions, including under python -O.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


# Small sparse commutative polynomial ring in r,s,K,a,b,t over Q.
# Used only to audit the displayed Gram and projection identities.
NV = 6


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, dict):
            self.terms = {e: F(c) for e, c in terms.items() if c}
        else:
            self.terms = {(0,) * NV: F(terms)} if terms else {}

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = dict(self.terms)
        for e, c in other.terms.items():
            out[e] = out.get(e, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -(other if isinstance(other, Poly) else Poly(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = {}
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                g = tuple(x + y for x, y in zip(e, f))
                out[g] = out.get(g, F(0)) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        need(type(exponent) is int and exponent >= 0, 'polynomial exponent')
        out = Poly(1)
        for _ in range(exponent):
            out = out * self
        return out


def variable(i):
    e = tuple(int(j == i) for j in range(NV))
    return Poly({e: 1})


def reduce_square(poly, index, replacement):
    """Exact substitution X_index^2=replacement, independent of X_index."""
    need(all(e[index] == 0 for e in replacement.terms), 'cyclic replacement')
    out = Poly()
    for e, c in poly.terms.items():
        exponent = e[index] // 2
        f = tuple(x % 2 if i == index else x for i, x in enumerate(e))
        out = out + Poly({f: c}) * replacement ** exponent
    return out


def determinant(matrix):
    n = len(matrix)
    need(all(len(row) == n for row in matrix), 'square determinant')
    out = Poly()
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j] for i, j in combinations(range(n), 2))
        term = Poly((-1) ** inversions)
        for i, j in enumerate(order):
            term = term * matrix[i][j]
        out = out + term
    return out


def identities():
    r, s, K, a, b, t = [variable(i) for i in range(NV)]
    checks = []

    def check(poly, name, index=None, replacement=None):
        if index is not None:
            poly = reduce_square(poly, index, replacement)
        need(not poly.terms, name)
        checks.append(name)

    # p,q are free formal variables in these two decomposition identities.
    p, q = a, b
    g = [[1, r, p, s], [r, 1, s, q], [p, s, 1, r], [s, q, r, 1]]
    dp = (1 + p) * (1 + q) - (r + s) ** 2
    dm = (1 - p) * (1 - q) - (r - s) ** 2
    check(determinant(g) - dp * dm, 'opposite-exchange Gram determinant')
    g = [[1, r, p, s], [r, 1, s, p], [p, s, 1, t], [s, p, t, 1]]
    dp = (1 + r) * (1 + t) - (p + s) ** 2
    dm = (1 - r) * (1 - t) - (p - s) ** 2
    check(determinant(g) - dp * dm, 'adjacent-exchange Gram determinant')

    relation = (1 - r ** 2) * (1 - s ** 2)
    p, q = r * s + K * b, r * s + K * a
    dp = (1 + p) * (1 + q) - (r + s) ** 2
    dm = (1 - p) * (1 - q) - (r - s) ** 2
    check(dp - K * (K * (1 + a * b) + (1 + r * s) * (a + b)),
          'mixed opposite-plus determinant', 2, relation)
    check(dm - K * (K * (1 + a * b) - (1 - r * s) * (a + b)),
          'mixed opposite-minus determinant', 2, relation)
    projected = s * (p + q) - r * (p * q + s ** 2)
    base = r * s ** 2 + s * K * (a + b) - r * (1 - s ** 2) * a * b
    check(projected - (1 - r ** 2) * base,
          'two-plane projection numerator', 2, relation)
    check(1 + 2 * r * s * p - r ** 2 - s ** 2 - p ** 2
          - relation * (1 - b ** 2), 'first perpendicular norm', 2, relation)
    check(1 + 2 * r * s * q - r ** 2 - s ** 2 - q ** 2
          - relation * (1 - a ** 2), 'second perpendicular norm', 2, relation)

    # Reuse formal variables r,b as k,B; reduce B^2=(1+k)/2.
    k, B = r, b
    aa, bb = (1 - 2 * k) * B, -B
    U, V = (1 + k + 2 * k ** 2) * F(1, 2), (1 + k - 2 * k ** 2) * F(1, 2)
    check(1 + aa * bb - U, 'U half-angle identity', 4, (1 + k) * F(1, 2))
    check((1 - aa ** 2) * (1 - bb ** 2) - V ** 2,
          'positive sine-product square', 4, (1 + k) * F(1, 2))
    check(aa + bb + 2 * k * B, 'sum of direction cosines')
    return checks


def arithmetic():
    margins = {
        'alpha_lower_squared': F(529 - 512),
        'B_lower_squared': F(2, 3) - F(9, 16),
        'B_upper_squared': F(25, 36) - F(11, 16),
        'diagonal_upper_vs_one_sixteenth': F(1, 16) - F(1, 25),
        'phi_cos_vs_triangle_upper': F(3, 16) - F(3, 32),
        'AA_positive_opposite_cos': -F(1, 48) + F(8, 9) * F(3, 16),
        'AA_minus_block': F(5, 9) - F(19, 48),
        'AS_ratio_squared': F(448 ** 2 - 135 ** 2 * 11),
        'no_opposite_common_neighbor': F(1) - F(8, 9),
        'AA_adjacent_plus': F(40, 81) - F(1, 16),
        'AA_adjacent_minus': F(40, 81) - F(1, 3),
        'AS_adjacent_plus': F(35, 72) - F(25, 243) - F(5, 128) - F(1, 16),
        'AS_adjacent_minus': F(35, 64) - F(53, 192) - F(15, 64),
        'SS_adjacent_minus_block': F(15, 16) ** 2 - F(11, 12) ** 2,
        'third_corner_above_x_in_pi_units': 11 * F(3, 8) - 4,
        'third_plus_large_excess_in_pi_units': 9 * F(3, 8) + F(2, 3) - 4,
    }
    need(all(v > 0 for v in margins.values()), 'nonpositive arithmetic margin')
    need(4 * F(1, 2) ** 2 / (1 + F(1, 2)) - 1 == -F(1, 3),
         'diagonal lower endpoint')
    need((3 * F(3, 5) ** 2 - 1) / 2 == F(1, 25), 'diagonal upper endpoint')
    need((-F(1, 3) - F(1, 9)) / F(8, 9) == -F(1, 2), 'triangle angle lower')
    need((F(1, 16) + F(1, 48)) / F(8, 9) == F(3, 32), 'triangle angle upper')
    need(F(1, 9) - F(8, 9) * F(3, 4) == -F(5, 9), 'SS opposite cosine')
    need(F(35, 64) - F(53, 192) - F(15, 64) == F(7, 192), 'AS lower margin')
    lo, hi = F(1, 3), F(3, 8)
    U = lambda k: (1 + k + 2 * k ** 2) / 2
    V = lambda k: (1 + k - 2 * k ** 2) / 2
    need(U(lo) == F(7, 9) and U(hi) == F(53, 64), 'U endpoint bounds')
    need(1 - U(lo) == F(2, 9), 'J upper bound')
    need(V(hi) == F(35, 64) and V(lo) == F(5, 9), 'V endpoint bounds')
    need(F(1, 2) + 2 * lo > 0 and F(1, 2) - 2 * lo < 0,
         'U increasing and V decreasing throughout the interval')
    return {key: str(v) for key, v in sorted(margins.items())}


def normalized_edges(edges):
    return frozenset(tuple(sorted(e)) for e in edges)


def legal(labels, edges, stage='final'):
    n = len(labels)
    pairs = set(combinations(range(n), 2))
    need(set(edges) <= pairs, 'invalid auxiliary edge')
    degree = [sum(i in e for e in edges) for i in range(n)]
    if any((d != 2 if c == '5/1' else d > (2 if c == '4/1' else 3))
           for c, d in zip(labels, degree)):
        return False
    triangles = [v for v in combinations(range(n), 3)
                 if all(e in edges for e in combinations(v, 2))]
    if stage == 'old_triangle':
        return not any(any(labels[i] == '5/1' for i in v) for v in triangles)
    if triangles:
        return False
    if stage == 'triangle_free':
        return True
    need(stage == 'final', 'unknown cover stage')
    if n == 4 and len(edges) == 4 and all(d == 2 for d in degree):
        return labels.count('5/1') < 2
    return True


def code(labels, edges):
    groups = [[i for i, c in enumerate(labels) if c == color]
              for color in sorted(set(labels))]
    codes = []
    for within in product(*(tuple(permutations(g)) for g in groups)):
        order = tuple(i for g in within for i in g)
        codes.append(''.join('1' if tuple(sorted((order[i], order[j]))) in edges else '0'
                             for i, j in combinations(range(len(labels)), 2)))
    return min(codes)


def signature(labels, edges):
    """Independent colored component descriptor for paths and four-cycles."""
    n = len(labels)
    adj = [{j for j in range(n) if tuple(sorted((i, j))) in edges and i != j}
           for i in range(n)]
    unseen = set(range(n))
    result = []
    while unseen:
        first = min(unseen)
        component, stack = set(), [first]
        while stack:
            v = stack.pop()
            if v not in component:
                component.add(v)
                stack.extend(adj[v] - component)
        unseen -= component
        need(all(len(adj[v]) <= 2 for v in component), 'non-path/cycle component')
        leaves = [v for v in component if len(adj[v]) < 2]
        cycle = not leaves
        need(not cycle or len(component) == 4, 'unexpected cycle')
        start = min(component) if cycle else min(leaves)
        order, prev, v = [], None, start
        while v not in order:
            order.append(v)
            choices = sorted(adj[v] - ({prev} if prev is not None else set()))
            if not choices:
                break
            prev, v = v, choices[0]
        need(set(order) == component, 'incomplete component walk')
        colors = tuple(labels[i] for i in order)
        if cycle:
            options = [q[i:] + q[:i] for q in (colors, colors[::-1]) for i in range(4)]
            result.append(('cycle', min(options)))
        else:
            result.append(('path', min(colors, colors[::-1])))
    return tuple(sorted(result))


def partitions(vertices):
    """Generate set partitions without graph-edge masks."""
    if not vertices:
        yield ()
        return
    first, rest = vertices[0], vertices[1:]
    for p in partitions(rest):
        yield ((first,),) + p
        for i in range(len(p)):
            yield p[:i] + ((first,) + p[i],) + p[i + 1:]


def component_cover(labels):
    """Independent generation by allowed colored path/cycle components."""
    records = set()
    for blocks in partitions(tuple(range(len(labels)))):
        choices = []
        for block in blocks:
            possibilities = []
            for order in permutations(block):
                # A 5/1 vertex must be internal in a path; every internal
                # vertex has degree two, other colors allow degrees <=two.
                if all(labels[v] != '5/1' or (0 < i < len(order) - 1)
                       for i, v in enumerate(order)):
                    possibilities.append(normalized_edges(zip(order, order[1:])))
                if len(block) == 4 and sum(labels[i] == '5/1' for i in block) < 2:
                    possibilities.append(normalized_edges(zip(order, order[1:] + order[:1])))
            choices.append(possibilities)
        for components in product(*choices):
            edges = frozenset().union(*components)
            records.add(signature(labels, edges))
    return records


def cover():
    rows, profiles = [], []
    stage_counts = {'old_triangle': 0, 'triangle_free': 0, 'final': 0}
    for d41, d42, d51 in product(range(5), range(3), range(5)):
        if d41 + 2 * d42 + d51 != 4:
            continue
        labels = ['4/1'] * d41 + ['4/2'] * d42 + ['5/1'] * d51
        pairs = tuple(combinations(range(len(labels)), 2))
        types = {stage: set() for stage in stage_counts}
        descriptors = set()
        for mask in range(1 << len(pairs)):
            edges = frozenset(e for i, e in enumerate(pairs) if (mask >> i) & 1)
            for stage in stage_counts:
                if legal(labels, edges, stage):
                    types[stage].add(code(labels, edges))
                    if stage == 'final':
                        descriptors.add(signature(labels, edges))
        need(descriptors == component_cover(labels), 'independent colored cover mismatch')
        need(len(descriptors) == len(types['final']), 'canonical code/signature mismatch')
        for stage in stage_counts:
            stage_counts[stage] += len(types[stage])
        raw = []
        for n3 in range(7):
            n4, n5 = 13 - 2 * n3, n3 + 2
            if d41 + d42 <= n4 and d51 <= n5:
                record = {'n3': n3, 'n4': n4, 'n5': n5,
                          'd41': d41, 'd42': d42, 'd51': d51}
                raw.append(record)
                if types['final']:
                    profiles.append({**record, 'H_codes': sorted(types['final'])})
        rows.append({'d41': d41, 'd42': d42, 'd51': d51,
                     'vertex_colors': labels, 'initial_degree_profiles': len(raw),
                     'allowed_H_codes': sorted(types['final']),
                     'surviving_degree_profiles': len(raw) if types['final'] else 0})
    need(len(rows) == 9, 'initial deficit distribution count')
    need(sum(x['initial_degree_profiles'] for x in rows) == 53, 'initial profile count')
    need(len(profiles) == 35, 'remaining profile count')
    need(sum(bool(x['allowed_H_codes']) for x in rows) == 6, 'remaining distributions')
    need(stage_counts == {'old_triangle': 24, 'triangle_free': 22, 'final': 18},
         'colored graph counts')
    forbidden = [(x['d41'], x['d42'], x['d51']) for x in rows if not x['allowed_H_codes']]
    need(forbidden == [(0, 0, 4), (0, 1, 2), (1, 0, 3)], 'forbidden distributions')
    return {'initial_degree_profiles': 53, 'remaining_degree_profiles': 35,
            'remaining_colored_H_types': 18, 'remaining_deficit_distributions': 6,
            'stage_type_counts': stage_counts, 'distributions': rows, 'profiles': profiles}


def selftest():
    controls = 0

    def check(condition, name):
        nonlocal controls
        need(condition, name)
        controls += 1

    triangle = normalized_edges(((0, 1), (1, 2), (0, 2)))
    cycle = normalized_edges(((0, 1), (1, 2), (2, 3), (3, 0)))
    path = normalized_edges(((0, 1), (1, 2), (2, 3)))
    check(not legal(['4/1'] * 4, triangle), 'pure-four triangle rejected')
    check(not legal(['4/1', '4/1', '4/2'], triangle), 'mixed-four triangle rejected')
    check(not legal(['4/2', '5/1', '5/1'], triangle), 'five triangle rejected')
    for labels in (['5/1'] * 4, ['5/1'] * 3 + ['4/1'],
                   ['5/1', '5/1', '4/1', '4/1'], ['5/1', '4/1', '5/1', '4/1']):
        check(not legal(labels, cycle), 'multiple-five cycle rejected')
    check(legal(['5/1', '4/1', '4/1', '4/1'], cycle), 'single-five cycle retained')
    check(legal(['4/1', '5/1', '5/1', '4/1'], path), 'two-five internal path retained')
    check(not legal(['5/1', '4/1', '5/1', '4/1'], path), 'five leaf rejected')
    check(legal(['4/2', '4/2'], frozenset()), 'empty two-vertex cover retained')
    check(code(['4/1'] * 4, path) == code(['4/1'] * 4,
          normalized_edges(((0, 2), (2, 1), (1, 3)))), 'relabeling invariant')
    check(signature(['5/1', '4/1', '5/1', '4/1'], cycle)
          != signature(['5/1', '5/1', '4/1', '4/1'], cycle), 'cycle color positions distinguished')
    bad = Poly(1)
    check(bool(reduce_square(bad, 2, Poly(1)).terms), 'nonzero identity remains nonzero')
    check(arithmetic()['AS_adjacent_minus'] == '7/192', 'critical sign retained')
    check(len(identities()) == 10, 'all polynomial obligations checked')
    check(len(cover()['profiles']) == 35, 'full independent cover controls')
    return controls


def main():
    need(sys.argv[1:] in ([], ['--selftest']), 'usage: check.py [--selftest]')
    result = {'agent': 'six-tammes-1', 'role': 'researcher',
              'scope': 'exact arithmetic and necessary auxiliary cover; spherical hand proof separate',
              'polynomial_identities': identities(), 'strict_margins': arithmetic(),
              'cover': cover()}
    if sys.argv[1:]:
        print(json.dumps({'status': 'PASS', 'controls': selftest(),
                          'degree_profiles': 35, 'colored_H_types': 18}, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
