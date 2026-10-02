"""Separate B-anchored sparse-polynomial audit. Imports no producer module."""
from fractions import Fraction as Q
from pathlib import Path
import json

AT = ((0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11))
BT = ((1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12))
LA = (0, 5, 6, 7, 9, 11)
LB = (1, 2, 4, 8, 10, 12)
ALL = tuple(sorted(LA + LB))
# Oriented boundary cycles are literal input, independent of incidence counting.
AC = (0, 6, 11, 9, 5, 7)
BC = (1, 4, 8, 2, 10, 12)
LOW, HIGH = Q(28, 39), Q(1186, 1593)
VARIABLE = {1: Q(1)}
DENOMINATOR = {0: Q(2), 1: Q(-1)}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def norm(p):
    return {i: Q(v) for i, v in p.items() if v}


def plus(*polys):
    answer = {}
    for p in polys:
        for degree, value in p.items():
            answer[degree] = answer.get(degree, Q(0)) + value
    return norm(answer)


def times(p, q):
    answer = {}
    for i, x in p.items():
        for j, y in q.items():
            answer[i + j] = answer.get(i + j, Q(0)) + x * y
    return norm(answer)


def scale(p, scalar):
    return norm({i: scalar * v for i, v in p.items()})


def division(dividend, divisor):
    need(bool(divisor), 'nonzero polynomial divisor')
    remainder, quotient = dict(dividend), {}
    degree = max(divisor)
    while remainder and max(remainder) >= degree:
        shift = max(remainder) - degree
        factor = remainder[max(remainder)] / divisor[degree]
        quotient[shift] = quotient.get(shift, Q(0)) + factor
        remainder = plus(remainder, scale({i + shift: v for i, v in divisor.items()}, -factor))
    return norm(quotient), remainder


def witness(f, g):
    """Row elimination; verify Bezout identity, not merely common divisibility."""
    need(bool(f or g), 'both prescribed gaps identically zero')
    first, second = [f, {0: Q(1)}, {}], [g, {}, {0: Q(1)}]
    while second[0]:
        quotient, remainder = division(first[0], second[0])
        next_row = [plus(a, scale(times(quotient, b), -1))
                    for a, b in zip(first, second)]
        need(next_row[0] == remainder, 'row elimination remainder')
        first, second = second, next_row
    leading = first[0][max(first[0])]
    h, u, v = [scale(p, 1 / leading) for p in first]
    need(plus(times(u, f), times(v, g)) == h, 'exact Bezout identity')
    need(not division(f, h)[1] and not division(g, h)[1], 'root-free polynomial is common gcd')
    return h, u, v


def bern(p, lo=LOW, hi=HIGH):
    """Bernstein multiplication and degree elevation; no affine power expansion."""
    need(bool(p) and lo < hi, 'nonzero polynomial and nonempty interval')
    degree = max(p)
    answer = [Q(0)] * (degree + 1)
    monomial = [Q(1)]
    for j in range(degree + 1):
        if j in p:
            elevated = monomial[:]
            for n in range(j, degree):
                elevated = [((n + 1 - i) * (elevated[i] if i <= n else 0)
                             + i * (elevated[i - 1] if i else 0)) / (n + 1)
                            for i in range(n + 2)]
            answer = [x + p[j] * y for x, y in zip(answer, elevated)]
        n = j
        monomial = [((n + 1 - i) * lo * (monomial[i] if i <= n else 0)
                     + i * hi * (monomial[i - 1] if i else 0)) / (n + 1)
                    for i in range(n + 2)]
    return answer


def certify_nonzero(p, lo=LOW, hi=HIGH):
    values = bern(p, lo, hi)
    need(all(x > 0 for x in values) or all(x < 0 for x in values), 'strict single-sign Bernstein')
    return values


def cycle_edges(cycle):
    return {frozenset((cycle[i], cycle[(i + 1) % len(cycle)])) for i in range(len(cycle))}


def pairs(triangle):
    a, b, c = triangle
    return (frozenset((a, b)), frozenset((a, c)), frozenset((b, c)))


def verify_patch(triangles, cycle):
    counts = {}
    for t in triangles:
        for e in pairs(t):
            counts[e] = counts.get(e, 0) + 1
    need(set(counts.values()) <= {1, 2}, 'patch edge incidence')
    need({e for e, n in counts.items() if n == 1} == cycle_edges(cycle), 'literal patch boundary cycle')
    # Root and add along an edge with a fresh vertex: the patch is an abstract disk.
    reached, support = {0}, set(triangles[0])
    while len(reached) < 4:
        added = False
        for i, t in enumerate(triangles):
            if i in reached:
                continue
            ancestors = [j for j in reached if len(set(t) & set(triangles[j])) == 2]
            if len(ancestors) != 1:
                continue
            need(len(set(t) & support) == 2, 'fresh patch vertex')
            reached.add(i)
            support.update(t)
            added = True
        need(added, 'four-face patch tree')
    need(support == set(cycle), 'six distinct patch vertices')


def flip(x, y, z):
    return tuple(plus(times(VARIABLE, plus(a, b)), scale(c, -1))
                 for a, b, c in zip(x, y, z))


def inner_num(x, y):
    diagonal = plus(*(times(a, b) for a, b in zip(x, y)))
    sx, sy = plus(*x), plus(*y)
    # H numerator is (2-2r)Id+rJ; a different contraction than the producer.
    return plus(times({0: Q(2), 1: Q(-2)}, diagonal), times(VARIABLE, times(sx, sy)))


def backward(placement):
    a, aa, b, bb = placement
    need(frozenset((a, aa)) in cycle_edges(AC), 'A boundary edge')
    need(frozenset((b, bb)) in cycle_edges(BC), 'B boundary edge')
    one, zero = {0: Q(1)}, {}
    p = {1: (one, zero, zero), 2: (zero, one, zero), 4: (zero, zero, one)}
    p[8] = flip(p[2], p[4], p[1])
    p[10] = flip(p[1], p[2], p[4])
    p[12] = flip(p[1], p[10], p[2])
    inside_b = next(t for t in BT if {b, bb} <= set(t))
    old_b = next(v for v in inside_b if v not in (b, bb))
    p[a] = flip(p[b], p[bb], p[old_b])
    p[aa] = flip(p[a], p[b], p[bb])
    root = next(i for i, t in enumerate(AT) if {a, aa} <= set(t))
    other = next(v for v in AT[root] if v not in (a, aa))
    p[other] = flip(p[a], p[aa], p[b])
    processed = {root}
    while len(processed) < 4:
        candidates = [(i, j) for i in range(4) if i not in processed
                      for j in processed if len(set(AT[i]) & set(AT[j])) == 2]
        need(bool(candidates), 'backward A propagation')
        i, j = candidates[-1]
        shared = set(AT[i]) & set(AT[j])
        x, y = sorted(shared)
        old = next(v for v in AT[j] if v not in shared)
        new = next(v for v in AT[i] if v not in shared)
        need(new not in p, 'fresh backward A label')
        p[new] = flip(p[x], p[y], p[old])
        processed.add(i)
    triangles = AT + BT + ((a, aa, b), (a, b, bb))
    edges = set(e for t in triangles for e in pairs(t))
    need(set(p) == set(ALL) and len(edges) == 21, 'complete reverse twelve-point patch')
    for v in p.values():
        need(inner_num(v, v) == DENOMINATOR, 'reverse unit identity')
    for e in edges:
        x, y = sorted(e)
        need(inner_num(p[x], p[y]) == VARIABLE, 'reverse contact identity')
    gram = [[inner_num(p[x], p[y]) for y in ALL] for x in ALL]
    f = plus(inner_num(p[7], p[12]), scale(VARIABLE, -1))
    g = plus(inner_num(p[9], p[10]), scale(VARIABLE, -1))
    return gram, f, g


def parse(p):
    need(isinstance(p, list) and all(isinstance(x, str) for x in p), 'encoded rational polynomial')
    values = [Q(x) for x in p]
    need(not values or values[-1] != 0, 'canonical polynomial degree')
    return {i: x for i, x in enumerate(values) if x}


def dense(p):
    return [p.get(i, Q(0)) for i in range(max(p) + 1)] if p else []


def audit(record, forward=None):
    keys = {'format', 'cosine_closed_band', 'r_closed_band', 'A_triangles', 'B_triangles',
            'cross_contacts', 'row_fields', 'rows', 'root_free_polynomials',
            'maximum_contact_gap_degree', 'maximum_Bezout_witness_degree'}
    need(set(record) == keys and record['format'] == 'ten-triangle-bridge-v1', 'exact certificate schema')
    need(record['cosine_closed_band'] == ['14/25', '593/1000'], 'closed cosine scope')
    need(record['r_closed_band'] == [str(LOW), str(HIGH)], 'closed transformed scope')
    need(record['A_triangles'] == [list(t) for t in AT] and record['B_triangles'] == [list(t) for t in BT],
         'literal two clusters')
    need(record['cross_contacts'] == [[7, 12], [9, 10]], 'both prescribed cross contacts')
    need(record['row_fields'] == ['a', 'a_prime', 'b', 'b_prime', 'root_free_polynomial_index'], 'row schema')
    verify_patch(AT, AC)
    verify_patch(BT, BC)
    expected = {(a, aa, b, bb) for ae in cycle_edges(AC) for be in cycle_edges(BC)
                for a in ae for aa in ae if aa != a for b in be for bb in be if bb != b}
    need(len(expected) == 144, 'literal144 expected cases')
    polys = []
    for item in record['root_free_polynomials']:
        need(set(item) == {'polynomial', 'Bernstein'}, 'root-free item schema')
        h = parse(item['polynomial'])
        need(bool(h) and h[max(h)] == 1, 'nonzero monic root-free polynomial')
        computed = certify_nonzero(h)
        need(item['Bernstein'] == [str(x) for x in computed], 'all Bernstein coefficients')
        need(all(x > 0 for x in computed) or all(x < 0 for x in computed), 'strict single-sign Bernstein')
        polys.append(h)
    need(len(polys) == len({tuple(dense(p)) for p in polys}) == 23, 'distinct root-free basis')
    # Completeness is checked before arithmetic, including adversarial missing rows.
    need(isinstance(record['rows'], list) and len(record['rows']) == 144, 'all144 encoded rows')
    listed = []
    for row in record['rows']:
        need(isinstance(row, list) and len(row) == 5 and all(type(x) is int for x in row), 'integer literal case')
        need(tuple(row[:4]) in expected and 0 <= row[4] < len(polys), 'valid literal placement/index')
        listed.append(tuple(row[:4]))
    need(len(set(listed)) == 144 and set(listed) == expected, 'full unique encoded placement coverage')
    seen, used = set(), set()
    gap_degree = witness_degree = full_gram = 0
    histogram = {}
    for row in record['rows']:
        need(isinstance(row, list) and len(row) == 5 and all(type(x) is int for x in row), 'integer literal case')
        placement, index = tuple(row[:4]), row[4]
        need(placement in expected and placement not in seen, 'unique complete boundary case')
        need(0 <= index < len(polys), 'root-free index')
        seen.add(placement)
        used.add(index)
        gram, f, g = backward(placement)
        h, u, v = witness(f, g)
        need(h == polys[index], 'case-specific Bezout/root-free binding')
        gap_degree = max(gap_degree, max(f, default=-1), max(g, default=-1))
        witness_degree = max(witness_degree, max(u, default=-1), max(v, default=-1))
        histogram[str(max(h))] = histogram.get(str(max(h)), 0) + 1
        if forward is not None:
            _, _, producer_gram, producer_f, producer_g = forward(placement)
            need([[dense(p) for p in r] for r in gram] == producer_gram, 'all144 full Gram polynomials')
            need(dense(f) == producer_f and dense(g) == producer_g, 'both cross-gap polynomials')
            full_gram += 144
    need(seen == expected and used == set(range(23)), 'full case and polynomial coverage')
    need(type(record['maximum_contact_gap_degree']) is int and record['maximum_contact_gap_degree'] == gap_degree,
         'contact-gap degree binding')
    need(type(record['maximum_Bezout_witness_degree']) is int and record['maximum_Bezout_witness_degree'] == witness_degree,
         'Bezout witness degree binding')
    return {'status': 'complete', 'placements': len(seen), 'root_free_polynomials': len(polys),
            'Bezout_identities': len(seen), 'reverse_norm_identities': len(seen) * 12,
            'reverse_patch_contact_identities': len(seen) * 21, 'root_free_degree_histogram': histogram,
            'full_Gram_polynomial_comparisons': full_gram,
            'maximum_contact_gap_degree': gap_degree, 'maximum_Bezout_witness_degree': witness_degree}


def main():
    record = json.loads((Path(__file__).parent / 'CERTIFICATE.json').read_text())
    # Cross comparison only: no producer function implements any audit arithmetic.
    from check import construct
    print(json.dumps(audit(record, construct), sort_keys=True))


if __name__ == '__main__':
    main()
