#!/usr/bin/env python3
"""Definition-level audits for the two-interval Ramsey bottleneck.

Python 3.10+, standard library only. This script does not decide S(6),
R_5(3), or the existence of the target interval colouring.
"""
from itertools import combinations, product
import json


def family(q):
    if q < 1:
        raise ValueError('q must be positive')
    n = 5*q + 2
    reserved = set(range(q+1, 2*q+1)) | set(range(4*q+2, n+1))
    remaining = set(range(1, n+1)) - reserved
    vertices = list(range(q+1)) + list(range(3*q+1, 4*q+2))
    return n, reserved, remaining, vertices


def sum_free(values):
    return all(x+y not in values for x in values for y in values)


def schur_rows(values):
    return {(x, y, x+y) for x in values for y in values
            if x <= y and x+y in values}


def triangle_rows(vertices):
    rows = set()
    for x, y, z in combinations(vertices, 3):
        a, b = y-x, z-y
        rows.add((min(a, b), max(a, b), z-x))
    return rows


def literal_schur(word):
    return all(word[x-1] != word[y-1] or word[x-1] != word[x+y-1]
               for x in range(1, len(word)+1)
               for y in range(x, len(word)-x+1))


def literal_triangles(vertices, colours):
    return all(not (colours[y-x] == colours[z-y] == colours[z-x])
               for x, y, z in combinations(vertices, 3))


def audit_constraint_identity(q):
    n, reserved, remaining, vertices = family(q)
    differences = {y-x for x, y in combinations(vertices, 2)}
    assert sum_free(reserved)
    assert differences == remaining
    direct = schur_rows(remaining)
    graph = triangle_rows(vertices)
    assert direct == graph
    return dict(q=q, n=n, reserved=len(reserved), variables=len(remaining),
                graph_vertices=len(vertices), schur_rows=len(direct),
                graph_triangles=len(vertices)*(len(vertices)-1)*(len(vertices)-2)//6)


def audit_assignments(q, k):
    n, reserved, remaining, vertices = family(q)
    positions = sorted(remaining)
    count = valid = 0
    for assignment in product(range(1, k+1), repeat=len(positions)):
        colours = dict(zip(positions, assignment))
        word = [k+1 if p in reserved else colours[p] for p in range(1, n+1)]
        integer_ok = literal_schur(word)
        graph_ok = literal_triangles(vertices, colours)
        low = [colours[p] for p in range(1, q+1)]
        high = [colours[p] for p in range(2*q+1, 4*q+2)]
        distance_ok = literal_schur(low) and all(
            not (high[i] == high[i+d] == low[d-1])
            for d in range(1, q+1) for i in range(len(high)-d))
        assert integer_ok == graph_ok == distance_ok
        count += 1
        valid += integer_ok
    return dict(q=q, k=k, assignments=count, valid=valid)


def audit_independence(q):
    """Enumerate every subset of [0,5q+2], independently of the proof."""
    n, reserved, _, witness = family(q)
    neighbours = [sum(1 << y for y in range(n+1)
                      if abs(x-y) in reserved) for x in range(n+1)]
    good = bytearray(1 << (n+1))
    good[0] = 1
    independent, maximum = 1, 0
    for mask in range(1, len(good)):
        bit = mask & -mask
        rest = mask ^ bit
        x = bit.bit_length()-1
        if good[rest] and not (neighbours[x] & rest):
            good[mask] = 1
            independent += 1
            maximum = max(maximum, mask.bit_count())
            # Check the proof's greedy decomposition on each valid set.
            points = [v for v in range(n+1) if mask >> v & 1]
            groups = []
            while points:
                left = points[0]
                group = [v for v in points if v <= left+q]
                groups.append(group)
                points = [v for v in points if v > left+q]
            assert len(groups) <= 2 and all(len(g) <= q+1 for g in groups)
    assert maximum == 2*q+2
    assert good[sum(1 << v for v in witness)]
    return dict(q=q, all_subsets=len(good), independent_subsets=independent,
                maximum=maximum)


def audit_smaller_supports():
    rows = []
    n, b = 537, 80
    for a in range(81, 127):
        reserved = set(range(a, a+b)) | set(range(n+1-a, n-a+b+1)) | {n}
        r = min(a, (n-2*a-b+2)//2)
        vertices = list(range(r)) + list(range(a+b+r-1, a+b+2*r-1))
        assert len(reserved) == 161 and sum_free(reserved)
        assert len(vertices) == 2*r and len(set(vertices)) == 2*r
        assert 0 <= min(vertices) <= max(vertices) <= n
        assert all(y-x not in reserved for x, y in combinations(vertices, 2))
        rows.append(dict(a=a, ramsey_graph_vertices=2*r,
                         consequent_R5_lower_bound=2*r+1))
    return rows


def main():
    identities = [audit_constraint_identity(q) for q in (1, 2, 3, 6, 21, 107)]
    assignments = [audit_assignments(q, k) for q in (1, 2, 3) for k in (2, 3)]
    independence = [audit_independence(q) for q in (1, 2, 3)]
    # A complete positive member of the family, obtained in the small pilot.
    q, k = 6, 3
    low, high = list(map(int, '123321')), list(map(int, '2213331221333'))
    word = low + [k+1]*q + high + [k+1]*(q+1)
    n, reserved, remaining, vertices = family(q)
    colours = {p: word[p-1] for p in remaining}
    assert len(word) == n == 32 and literal_schur(word)
    assert all(word[p-1] == 4 for p in reserved)
    assert literal_triangles(vertices, colours)
    assert not literal_schur([1, 1])  # Repeated summands must be rejected.
    smaller = audit_smaller_supports()
    output = dict(constraint_identities=identities,
                  assignment_audits=assignments,
                  total_assignments=sum(r['assignments'] for r in assignments),
                  total_valid=sum(r['valid'] for r in assignments),
                  independence_audits=independence,
                  positive_word32=''.join(map(str, word)),
                  smaller_supports=smaller,
                  target_status='UNRESOLVED: no 537 word and no impossibility claim')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
