"""Produce the complete exact G22 facial-injectivity certificate.

Actual author: six-tammes-1, researcher. Standard library; exact rationals.
The geometric necessity of the predicates is proved in PROOF.md.
"""
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from itertools import combinations, permutations
from math import comb, gcd
from pathlib import Path
import argparse
import hashlib
import json

LEFT = (1, 2, 4, 8, 10, 12, 13)
RIGHT = (0, 5, 6, 7, 9, 11)
TRIANGLES = ((2, 10, 1), (2, 1, 4), (2, 4, 8), (2, 8, 13),
             (1, 10, 12), (0, 5, 11), (0, 11, 6), (5, 0, 7), (11, 5, 9))
PENTAGON = (12, 10, 9, 5, 7)
FACES = TRIANGLES + (PENTAGON,)
LOW, HIGH = F(28, 39), F(1186, 1593)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def poly(coefficients):
    result = list(map(F, coefficients))
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def plus(a, b):
    return poly((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))


def times(a, b):
    result = [F(0)] * max(0, len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return poly(result)


def scale(a, scalar):
    return poly(x * scalar for x in a)


def minus(a, b):
    return plus(a, scale(b, -1))


def square(a):
    return times(a, a)


ONE, R, D = poly([1]), poly([0, 1]), poly([2, -1])


def reflected(a, b, opposite):
    return tuple(minus(times(R, plus(x, y)), z) for x, y, z in zip(a, b, opposite))


def dot_numerator(a, b):
    euclidean = reduce(plus, (times(x, y) for x, y in zip(a, b)), ())
    return plus(times(poly([2, -2]), euclidean),
                times(R, times(reduce(plus, a, ()), reduce(plus, b, ()))))


def basis(index):
    return tuple(ONE if index == j else () for j in range(3))


def bernstein(coefficients):
    degree = len(coefficients) - 1
    powers = [F(0)] * (degree + 1)
    for j, value in enumerate(coefficients):
        for i in range(j + 1):
            powers[i] += value * comb(j, i) * LOW ** (j - i) * (HIGH - LOW) ** i
    return [sum(powers[j] * F(comb(i, j), comb(degree, j)) for j in range(i + 1))
            for i in range(degree + 1)]


def quotient(dividend, divisor):
    work = list(dividend)
    result = [F(0)] * max(0, len(work) - len(divisor) + 1)
    while work and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        ratio = work[-1] / divisor[-1]
        result[shift] += ratio
        for i, value in enumerate(divisor):
            work[i + shift] -= ratio * value
        while work and not work[-1]:
            work.pop()
    return poly(result), poly(work)


def gram_data():
    left = {1: basis(0), 2: basis(1), 4: basis(2)}
    for new, a, b, old in ((10, 1, 2, 4), (8, 2, 4, 1), (13, 2, 8, 4), (12, 1, 10, 2)):
        left[new] = reflected(left[a], left[b], left[old])
    right = {0: basis(0), 5: basis(1), 11: basis(2)}
    for new, a, b, old in ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0)):
        right[new] = reflected(right[a], right[b], right[old])
    rows, lookup, contact = [], {}, {}
    for side, points in (('left', left), ('right', right)):
        for vertex, vector in points.items():
            require(dot_numerator(vector, vector) == D, 'unit norm identity')
        contact[side] = set()
        for a, b in combinations(sorted(points), 2):
            numerator = dot_numerator(points[a], points[b])
            lookup[side, a, b] = numerator
            row = {'side': side, 'pair': [a, b], 'numerator': list(map(str, numerator)),
                   'contact': numerator == R}
            if numerator == R:
                contact[side].add(frozenset((a, b)))
            else:
                gap = minus(R, numerator)
                coefficients = bernstein(gap)
                require(min(coefficients) > 0, 'strict intrinsic noncontact gap')
                row['gap_bernstein'] = list(map(str, coefficients))
            rows.append(row)
    require(len(rows) == 36, 'complete pair table')
    require(sum(not row['contact'] for row in rows) == 16, 'noncontact table')
    return rows, lookup, contact


def all_maps():
    def extend(index, image, used):
        if index == len(RIGHT):
            yield dict(zip(RIGHT, image))
            return
        for value in (RIGHT[index], *LEFT):
            if value not in used:
                yield from extend(index + 1, image + [value], used | {value})
    yield from extend(0, [], set())


def ring_possible(neighbors, forced):
    """A partial cyclic permutation is either one cycle or disjoint paths."""
    incoming = set(forced.values())
    if len(incoming) != len(forced):
        return False
    starts = set(neighbors) - incoming
    if not starts:
        origin = min(neighbors)
        visited, current = set(), origin
        while current not in visited:
            visited.add(current)
            current = forced[current]
        return current == origin and visited == set(neighbors)
    visited = set()
    for start in starts:
        current = start
        while current not in visited:
            visited.add(current)
            if current not in forced:
                break
            current = forced[current]
    return visited == set(neighbors)


def classify(mapping, contact):
    renamed = lambda x: mapping.get(x, x)
    faces = [tuple(map(renamed, face)) for face in FACES]
    if any(len(set(face)) != len(face) for face in faces):
        return 'nonsimple_face'
    if len({frozenset(face) for face in faces[:9]}) != 9:
        return 'repeated_triangle'
    edges = {frozenset((face[i - 1], face[i])) for face in faces for i in range(len(face))}
    names = sorted(set().union(*edges))
    neighbors = {x: set().union(*(e for e in edges if x in e)) - {x} for x in names}
    if any(len(n) > 5 for n in neighbors.values()):
        return 'degree_above_five'
    if any(n >= 5 for n in Counter(x for face in faces[:9] for x in face).values()):
        return 'five_triangle_faces'
    corners = {x: {} for x in names}
    for face in faces:
        for i, x in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % len(face)]
            if before in corners[x]:
                return 'corner_overlap_or_conflict'
            corners[x][before] = after
    for x in names:
        if not ring_possible(neighbors[x], corners[x]):
            return 'no_local_cyclic_order'
        if len(corners[x]) == len(neighbors[x]):
            if x not in faces[-1]:
                return 'sealed_triangle_star'
            if len(neighbors[x]) < 4:
                return 'sealed_nonconvex_pentagon'
    inverse = {mapping[r]: r for r in RIGHT if mapping[r] != r}
    for a, b in sorted(tuple(sorted(edge)) for edge in edges):
        edge = frozenset((a, b))
        if a in LEFT and b in LEFT and edge not in contact['left']:
            return 'left_noncontact_required'
        u, v = inverse.get(a, a), inverse.get(b, b)
        if u in RIGHT and v in RIGHT and frozenset((u, v)) not in contact['right']:
            return 'right_noncontact_required'
    return 'retained'


def enumerate_aliases(contact):
    counts, survivors, decisions = Counter(), [], []
    for mapping in all_maps():
        kind = classify(mapping, contact)
        counts[kind] += 1
        key = tuple(mapping[r] for r in RIGHT)
        decisions.append((key, kind == 'retained'))
        if kind == 'retained':
            survivors.append({str(r): mapping[r] for r in RIGHT if mapping[r] != r})
    expected_count = sum(comb(6, k) * reduce(lambda a, b: a * b, range(8 - k, 8), 1)
                         for k in range(7))
    require(len(decisions) == expected_count == 37633, 'partial injection coverage')
    require(len({key for key, _ in decisions}) == expected_count, 'unique maps')
    survivors.sort(key=lambda row: tuple(row.get(str(r), r) for r in RIGHT))
    decision_bytes = canonical(sorted(decisions))
    return {'raw_maps': len(decisions), 'rejection_counts': dict(sorted(counts.items())),
            'complete_local_survivors': survivors,
            'all_map_decision_sha256': hashlib.sha256(decision_bytes).hexdigest(),
            'global_embedding_enumeration_used': False}


def closure_cases(lookup):
    k = lookup['right', 6, 7]
    require(k == lookup['right', 6, 9] == lookup['right', 7, 9], 'outer triangle Gram identity')
    require(k == poly([0, -3, 2, 2]), 'credited outer Gram formula')
    result = []
    for vertex in (4, 8, 13):
        A = lookup['left', *sorted((vertex, 10))]
        B = lookup['left', *sorted((vertex, 12))]
        P, Q = minus(square(D), square(A)), minus(square(D), square(B))
        U = minus(times(R, D), times(A, B))
        radius = minus(square(D), square(k))
        V = minus(times(k, D), square(k))
        W, Z = minus(times(R, D), times(B, k)), minus(times(R, D), times(A, k))
        delta, sine = minus(times(P, Q), square(U)), minus(square(radius), square(V))
        E = minus(plus(minus(times(radius, plus(times(P, square(W)), times(Q, square(Z)))),
                                   scale(times(times(U, V), times(W, Z)), 2)),
                             scale(times(square(U), square(V)), 2)),
                  plus(times(square(U), square(radius)), times(times(P, Q), square(V))))
        original = minus(square(E), scale(times(times(delta, sine), square(minus(times(W, Z), times(U, V)))), 4))
        require(original and len(original) <= 61, 'nonzero closure and degree bound')
        remaining, factors = original, []
        for root in (F(0), F(1), F(2), F(-1)):
            factor, multiplicity = poly([-root, 1]), 0
            while remaining:
                candidate, remainder = quotient(remaining, factor)
                if remainder:
                    break
                remaining, multiplicity = candidate, multiplicity + 1
            if multiplicity:
                require(not LOW <= root <= HIGH, 'removed factor nonzero on closed band')
                factors.append({'root': str(root), 'multiplicity': multiplicity})
        require(all(x.denominator == 1 for x in remaining), 'integer reduced coefficients')
        content = reduce(gcd, (abs(x.numerator) for x in remaining), 0)
        require(content > 0, 'positive polynomial content')
        reduced = scale(remaining, F(1, content))
        coefficients = bernstein(reduced)
        require(max(coefficients) < 0, 'whole-interval strict root exclusion')
        result.append({'alias': [6, vertex], 'closure_degree': len(original) - 1,
                       'linear_factors': factors, 'content': content,
                       'reduced_coefficients': list(map(str, reduced)),
                       'reduced_bernstein': list(map(str, coefficients))})
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def generate():
    rows, lookup, contact = gram_data()
    aliases = enumerate_aliases(contact)
    cases = closure_cases(lookup)
    for row in aliases['complete_local_survivors']:
        require(not row or row.get('6') in (4, 8, 13), 'every nonempty survivor covered by Gram obstruction')
    return {'schema': 'G22-facial-injectivity-v1',
            'actual_author': 'six-tammes-1', 'role': 'researcher',
            'closed_c_interval': ['14/25', '593/1000'], 'closed_r_interval': [str(LOW), str(HIGH)],
            'triangular_faces': TRIANGLES, 'pentagonal_face': PENTAGON,
            'intrinsic_pair_table': rows, 'aliases': aliases, 'closure_cases': cases,
            'only_original_alias_survivor_after_Gram': {},
            'geometric_necessity_proved_in': 'PROOF.md'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='write fresh compact certificate here')
    args = parser.parse_args()
    certificate = generate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(certificate, sort_keys=True, indent=2) + '\n')
    else:
        expected = Path(__file__).with_name('CERTIFICATE.json')
        require(canonical(json.loads(expected.read_text())) == canonical(certificate), 'fresh certificate differs')
    print(json.dumps({'status': 'CHECKED_EXACT_AUTHOR_FACIAL_INJECTIVITY',
                      'raw_maps': certificate['aliases']['raw_maps'],
                      'local_survivors': certificate['aliases']['complete_local_survivors'],
                      'excluded_single_aliases': [row['alias'] for row in certificate['closure_cases']],
                      'certificate_sha256': hashlib.sha256(canonical(certificate)).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
