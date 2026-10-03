"""Sparse B-anchored checker core; only main imports a producer comparator."""
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


def dense(p):
    return [p.get(i, Q(0)) for i in range(max(p) + 1)] if p else []


def parse(p):
    need(isinstance(p, list) and all(isinstance(x, str) for x in p), 'encoded rational polynomial')
    values = [Q(x) for x in p]
    need(not values or values[-1] != 0, 'canonical polynomial degree')
    return {i: x for i, x in enumerate(values) if x}


def core_points(which):
    one, zero = {0: Q(1)}, {}
    if which == 'A':
        p = {0: (one, zero, zero), 5: (zero, one, zero), 11: (zero, zero, one)}
        steps = [(6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0)]
    elif which == 'B':
        p = {1: (one, zero, zero), 2: (zero, one, zero), 4: (zero, zero, one)}
        steps = [(8, 2, 4, 1), (10, 1, 2, 4), (12, 1, 10, 2)]
    else:
        raise ValueError('core selector')
    for new, x, y, old in steps:
        p[new] = flip(p[x], p[y], p[old])
    return p


def core_data():
    records = []
    for name, triangles in [('A', AT), ('B', BT)]:
        p = core_points(name)
        contacts = {e for t in triangles for e in pairs(t)}
        found = set()
        for i in sorted(p):
            need(inner_num(p[i], p[i]) == DENOMINATOR, 'core norm')
            for j in sorted(p):
                if j <= i:
                    continue
                value = plus(inner_num(p[i], p[j]), scale(VARIABLE, -1))
                if frozenset((i, j)) in contacts:
                    need(not value, 'core contact')
                    found.add(frozenset((i, j)))
                else:
                    coefficients = bern(value)
                    need(all(x < 0 for x in coefficients), 'strict core noncontact')
                    records.append({'cluster': name, 'pair': [i, j], 'gap': [str(x) for x in dense(value)],
                                    'Bernstein': [str(x) for x in coefficients]})
        need(found == contacts and len(found) == 9, 'exact internal contact graph')
        cliques = {frozenset((i, j, k)) for i in p for j in p for k in p if i < j < k
                   and all(e in found for e in pairs((i, j, k)))}
        need(cliques == {frozenset(t) for t in triangles}, 'only four internal contact triples')
    return records


def enumerate_cases():
    """Short Cartesian cases + exhaustive3024 long candidates, no typed recipe."""
    ea, eb = cycle_edges(AC), cycle_edges(BC)
    short = {('S', a, aa, b, bb) for x in ea for y in eb
             for a in x for aa in x if aa != a for b in y for bb in y if bb != b}
    ca = {e for t in AT for e in pairs(t)}
    cb = {e for t in BT for e in pairs(t)}
    long = set()
    attempted = 0
    for x in ea:
        for y in eb:
            for t in set(LB) | {13}:
                u = set(x) | {t}
                for s in set(LA) | {13}:
                    w = set(y) | {s}
                    if len(u & w) != 1:
                        continue
                    z = next(iter(u & w))
                    for i in u - {z}:
                        for j in w - {z}:
                            v = {z, i, j}
                            attempted += 1
                            if any((e <= set(LA) and e not in ca) or (e <= set(LB) and e not in cb)
                                   for tri in (u, v, w) for e in pairs(tuple(sorted(tri)))):
                                continue
                            triangles = [set(t) for t in AT + BT] + [u, v, w]
                            if len({frozenset(t) for t in triangles}) != 11:
                                continue
                            adj = {(i, j) for i in range(11) for j in range(i + 1, 11)
                                   if len(triangles[i] & triangles[j]) == 2}
                            # Exactly the cluster edges and the path A-U-V-W-B.
                            internal = {(i, j) for i, j in adj if i < 4 and j < 4 or 4 <= i < 8 and 4 <= j < 8}
                            external = adj - internal
                            if len(internal) != 6 or len(external) != 4:
                                continue
                            if (8, 9) not in external or (9, 10) not in external:
                                continue
                            if sum(i < 4 and j == 8 for i, j in external) != 1:
                                continue
                            if sum(4 <= i < 8 and j == 10 for i, j in external) != 1:
                                continue
                            need(13 in v, 'fresh corner in middle face')
                            a = next(iter(v & set(LA)))
                            b = next(iter(v & set(LB)))
                            aa, bb = next(iter(x - {a})), next(iter(y - {b}))
                            kind = 'UVW' if 13 in u and 13 in w else 'UV' if 13 in u else 'VW'
                            case = (kind, a, aa, b, bb)
                            need(case not in long, 'no double encoding of a long path')
                            long.add(case)
    need(attempted == 3024 and len(short) == 144 and len(long) == 432, 'entire short/long enumeration')
    need(len(short | long) == 576, 'entire576 distinct cases')
    return short | long


def reverse_path(case):
    kind, a, aa, b, bb = case
    # Return W,V,U order; this construction is B to A, opposite the producer.
    if kind == 'S':
        return ((a, b, bb), (a, aa, b))
    if kind == 'UV':
        return ((a, b, bb), (a, b, 13), (a, aa, 13))
    if kind == 'VW':
        return ((b, bb, 13), (a, b, 13), (a, aa, b))
    need(kind == 'UVW', 'reverse path type')
    return ((b, bb, 13), (a, b, 13), (a, aa, 13))


def backward(case):
    kind, a, aa, b, bb = case
    need(frozenset((a, aa)) in cycle_edges(AC) and frozenset((b, bb)) in cycle_edges(BC),
         'reverse boundary case')
    p = core_points('B')
    old_face = next(t for t in BT if {b, bb} <= set(t))
    bridge = reverse_path(case)
    for triangle in bridge:
        shared = set(old_face) & set(triangle)
        need(len(shared) == 2, 'reverse bridge shared edge')
        i, j = sorted(shared)
        old = next(v for v in old_face if v not in shared)
        new = next(v for v in triangle if v not in shared)
        need(new not in p, 'reverse fresh bridge corner')
        p[new] = flip(p[i], p[j], p[old])
        old_face = triangle
    root = next(i for i, t in enumerate(AT) if {a, aa} <= set(t))
    outside = next(v for v in old_face if v not in (a, aa))
    new = next(v for v in AT[root] if v not in (a, aa))
    need(new not in p, 'reverse fresh A root')
    p[new] = flip(p[a], p[aa], p[outside])
    processed = {root}
    while len(processed) < 4:
        choices = [(i, j) for i in range(4) if i not in processed
                   for j in processed if len(set(AT[i]) & set(AT[j])) == 2]
        need(bool(choices), 'complete reverse cluster')
        i, j = choices[-1]
        common = set(AT[i]) & set(AT[j])
        x, y = sorted(common)
        old = next(v for v in AT[j] if v not in common)
        new = next(v for v in AT[i] if v not in common)
        need(new not in p, 'reverse fresh A corner')
        p[new] = flip(p[x], p[y], p[old])
        processed.add(i)
    wanted = set(ALL) | ({13} if kind != 'S' else set())
    triangles = AT + BT + bridge
    edges = {e for t in triangles for e in pairs(t)}
    need(set(p) == wanted and len(edges) == (21 if kind == 'S' else 23), 'reverse entire patch')
    for v in p.values():
        need(inner_num(v, v) == DENOMINATOR, 'reverse norm identity')
    for e in edges:
        i, j = sorted(e)
        need(inner_num(p[i], p[j]) == VARIABLE, 'reverse contact identity')
    gram = [[inner_num(p[i], p[j]) for j in sorted(wanted)] for i in sorted(wanted)]
    return gram, plus(inner_num(p[7], p[12]), scale(VARIABLE, -1)), \
        plus(inner_num(p[9], p[10]), scale(VARIABLE, -1))


def prepare(record):
    keys = {'format', 'cosine_closed_band', 'r_closed_band', 'A_triangles', 'B_triangles', 'cross_contacts',
            'fresh_corner_label', 'types', 'row_fields', 'rows', 'root_free_polynomials', 'core_noncontacts',
            'maximum_gap_degree', 'maximum_Bezout_witness_degree'}
    need(set(record) == keys and record['format'] == 'eleven-triangle-bridge-v1', 'exact certificate schema')
    need(record['cosine_closed_band'] == ['14/25', '593/1000'] and record['r_closed_band'] == [str(LOW), str(HIGH)],
         'closed parameter scope')
    need(record['A_triangles'] == [list(t) for t in AT] and record['B_triangles'] == [list(t) for t in BT], 'literal cores')
    need(record['cross_contacts'] == [[7, 12], [9, 10]], 'both prescribed cross contacts')
    need(type(record['fresh_corner_label']) is int and record['fresh_corner_label'] == 13, 'fresh corner label')
    need(record['types'] == ['S', 'UV', 'VW', 'UVW'], 'complete path types')
    need(record['row_fields'] == ['type', 'a', 'a_prime', 'b', 'b_prime', 'root_free_polynomial_index'], 'row interpretation')
    verify_patch(AT, AC)
    verify_patch(BT, BC)
    need(record['core_noncontacts'] == core_data(), 'all twelve strict core noncontacts')
    expected = enumerate_cases()
    polys = []
    for entry in record['root_free_polynomials']:
        need(set(entry) == {'polynomial', 'Bernstein'}, 'root-free schema')
        h = parse(entry['polynomial'])
        need(bool(h) and h[max(h)] == 1, 'nonzero monic polynomial')
        values = certify_nonzero(h)
        need(entry['Bernstein'] == [str(x) for x in values], 'all root-free Bernstein entries')
        polys.append(h)
    need(len(polys) == len({tuple(dense(p)) for p in polys}), 'unique root-free list')
    need(isinstance(record['rows'], list) and len(record['rows']) == 576, 'complete literal row list')
    seen, used = set(), set()
    for row in record['rows']:
        need(isinstance(row, list) and len(row) == 6 and type(row[0]) is str
             and all(type(v) is int for v in row[1:]), 'typed row')
        case, index = tuple(row[:5]), row[5]
        need(case in expected and case not in seen and 0 <= index < len(polys), 'valid unique case/index')
        seen.add(case)
        used.add(index)
    need(seen == expected and used == set(range(len(polys))), 'full cases and root-free basis coverage')
    need(type(record['maximum_gap_degree']) is int and record['maximum_gap_degree'] >= 0,
         'gap-degree format')
    need(type(record['maximum_Bezout_witness_degree']) is int and record['maximum_Bezout_witness_degree'] >= 0,
         'witness-degree format')
    return polys


def audit(record, start=0, stop=576, forward=None):
    polys = prepare(record)
    need(type(start) is int and type(stop) is int and 0 <= start < stop <= 576, 'bounded nonempty ordinal range')
    gap_degree = witness_degree = gram_count = norms = contacts = 0
    histogram = {}
    for ordinal in range(start, stop):
        row = record['rows'][ordinal]
        case, index = tuple(row[:5]), row[5]
        gram, f, g = backward(case)
        h, u, v = witness(f, g)
        need(h == polys[index], 'case-specific Bezout/root-free binding')
        gd, wd = max(max(f, default=-1), max(g, default=-1)), max(max(u, default=-1), max(v, default=-1))
        need(gd <= record['maximum_gap_degree'] and wd <= record['maximum_Bezout_witness_degree'], 'certified degree bounds')
        gap_degree, witness_degree = max(gap_degree, gd), max(witness_degree, wd)
        histogram[str(max(h))] = histogram.get(str(max(h)), 0) + 1
        norms += 12 if case[0] == 'S' else 13
        contacts += 21 if case[0] == 'S' else 23
        if forward is not None:
            producer_gram, producer_f, producer_g = forward(case)
            need([[dense(p) for p in r] for r in gram] == producer_gram, 'every Gram polynomial')
            need(dense(f) == producer_f and dense(g) == producer_g, 'both cross-gap polynomials')
            gram_count += len(gram) ** 2
    if start == 0 and stop == 576:
        need(gap_degree == record['maximum_gap_degree'] and witness_degree == record['maximum_Bezout_witness_degree'],
             'sharp recorded degree bounds')
    return {'status': 'complete_requested_range', 'start': start, 'stop': stop, 'cases': stop - start,
            'Bezout_identities': stop - start, 'reverse_norm_identities': norms,
            'reverse_patch_contact_identities': contacts, 'full_Gram_polynomial_comparisons': gram_count,
            'cross_gap_polynomial_comparisons': 2 * (stop - start) if forward is not None else 0,
            'observed_maximum_gap_degree': gap_degree, 'observed_maximum_Bezout_witness_degree': witness_degree,
            'root_free_degree_histogram': histogram, 'root_free_polynomials': len(polys),
            'whole_metadata_and_enumeration_checked': True}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int, default=576)
    args = parser.parse_args()
    record = json.loads((Path(__file__).parent / 'CERTIFICATE.json').read_text())
    from check import construct
    print(json.dumps(audit(record, args.start, args.stop, lambda case: construct(case, True)), sort_keys=True))


if __name__ == '__main__':
    main()
