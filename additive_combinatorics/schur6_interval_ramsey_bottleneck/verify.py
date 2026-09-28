#!/usr/bin/env python3
"""Definition-level audits for the two-interval Ramsey bottleneck.

Python 3.10+, standard library only. This script does not decide S(6),
R_5(3), or the existence of the target interval colouring.
"""
from itertools import combinations, product
from collections import Counter
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


def general_independence(n, a):
    """Proved formula and an attaining set, for n >= 5a-4 and a>=2."""
    assert a >= 2 and n >= 5*a-4
    choices = [(min(j*a, n-a+1-(j-1)*(2*a-2)), j)
               for j in range(1, (n-a)//(2*a-1)+2)]
    size, count = max(choices)
    lengths = [1]*count
    extra = size-count
    for i in range(count):
        add = min(a-1, extra)
        lengths[i] += add
        extra -= add
    assert extra == 0
    points, start = [], 0
    for length in lengths:
        points.extend(range(start, start+length))
        start += length+2*a-2
    reserved = set(range(a, 2*a-1)) | set(range(n+1-a, n+1))
    assert len(points) == size and max(points) <= n-a
    assert all(y-x not in reserved for x, y in combinations(points, 2))
    return size, points


def audit_general_independence(n, a):
    reserved = set(range(a, 2*a-1)) | set(range(n+1-a, n+1))
    assert sum_free(reserved)
    neighbours = [sum(1 << y for y in range(n+1)
                      if abs(x-y) in reserved) for x in range(n+1)]
    good = bytearray(1 << (n+1))
    good[0] = 1
    maximum = 0
    for mask in range(1, len(good)):
        bit = mask & -mask
        rest = mask ^ bit
        if good[rest] and not neighbours[bit.bit_length()-1] & rest:
            good[mask] = 1
            maximum = max(maximum, mask.bit_count())
    predicted, points = general_independence(n, a)
    assert maximum == predicted and good[sum(1 << p for p in points)]
    return dict(n=n, a=a, all_subsets=len(good), maximum=maximum)


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
    general = [audit_general_independence(n, a) for n, a in
               ((6,2),(10,2),(14,2),(18,2),(11,3),(14,3),(18,3),(16,4),(18,4))]
    screen = [{'a':a, 'alpha':general_independence(537,a)[0]}
              for a in range(2,109)]
    least = min(row['alpha'] for row in screen)
    minimizers = [row['a'] for row in screen if row['alpha']==least]
    assert least == 156 and minimizers == [78]
    _, replacement_points = general_independence(537,78)
    assert replacement_points == list(range(78))+list(range(232,310))
    # Check the optional SAT encoder against complete literal assignments;
    # importing its generator needs no solver package.
    from complete import encoding
    encoding_assignments = 0
    for n,a,k in ((6,2,2),(7,2,2),(11,3,3),(12,3,3)):
        reserved,positions,clauses = encoding(n,a,k)
        for values in product(range(1,k+1),repeat=len(positions)):
            by_position = dict(zip(positions,values))
            word = [k+1 if v in reserved else by_position[v] for v in range(1,n+1)]
            names = {}
            canonical = tuple(names.setdefault(c,len(names)+1) for c in values)
            selected = {i*k+c for i,c in enumerate(values)}
            cnf_ok = all(any((lit in selected) if lit>0 else (-lit not in selected)
                            for lit in clause) for clause in clauses)
            assert cnf_ok == (literal_schur(word) and canonical==values)
            encoding_assignments += 1
    target_reserved,target_positions,target_clauses = encoding(537,78,5)
    # Distinct x-first sum pairs and z-first direct rows must agree exactly.
    target_rows = set()
    target_set = set(target_positions)
    for z in target_positions:
        for x in range(1,z//2+1):
            if x in target_set and z-x in target_set:
                target_rows.add((x,z-x,z))
    assert target_rows == schur_rows(target_set)
    assert len(target_rows)==27664 and len(target_clauses)==144050
    target_index = {v:i for i,v in enumerate(target_positions)}
    expected_clauses = Counter(tuple(sorted({-target_index[v]*5-c for v in row}))
                               for row in target_rows for c in range(1,6))
    actual_clauses = Counter(tuple(sorted(clause)) for clause in
                             target_clauses[-5*len(target_rows):])
    assert expected_clauses == actual_clauses
    output = dict(constraint_identities=identities,
                  assignment_audits=assignments,
                  total_assignments=sum(r['assignments'] for r in assignments),
                  total_valid=sum(r['valid'] for r in assignments),
                  independence_audits=independence,
                  positive_word32=''.join(map(str, word)),
                  smaller_supports=smaller,
                  general_independence_audits=general,
                  replacement_screen=dict(cases=len(screen), minimum_alpha=least,
                                          minimizers=minimizers,
                                          all_values=screen,
                                          witness=replacement_points),
                  optional_encoder=dict(complete_assignments=encoding_assignments,
                                        target_variables=len(target_positions)*5,
                                        target_clauses=len(target_clauses),
                                        target_schur_rows=len(target_rows)),
                  target_status='UNRESOLVED: no 537 word and no impossibility claim')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
