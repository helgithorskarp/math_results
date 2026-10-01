#!/usr/bin/env python3
"""Exact support checks for the ordinary cubic-row-cap proof; no solver."""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def weak_compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def partitions(total, least=0):
    if total == 0:
        yield ()
    else:
        for first in range(max(1, least), total + 1):
            for rest in partitions(total - first, first):
                yield (first,) + rest


def outer(word):
    return [[int(i in word and j in word) for j in range(10)]
            for i in range(10)]


def add(*matrices):
    return [[sum(m[i][j] for m in matrices) for j in range(10)]
            for i in range(10)]


def gram(rows):
    return add(*[outer(row) for row in rows])


def run():
    labels = list(combinations(range(5), 2))
    sets = [set(x) for x in labels]
    p = [[int(not sets[i] & sets[j]) for j in range(10)]
         for i in range(10)]
    p2 = [[sum(p[i][h] * p[h][j] for h in range(10))
           for j in range(10)] for i in range(10)]
    for i in range(10):
        require(sum(p[i]) == 3, 'Petersen degree')
        for j in range(10):
            require(p2[i][j] + p[i][j] == 2 * (i == j) + 1,
                    'P^2+P=2I+J')
    k = [[2 * (i == j) + 2 - 2 * p[i][j] for j in range(10)]
         for i in range(10)]
    s0 = [[k[i][j] + 1 for j in range(10)] for i in range(10)]
    stars = [frozenset(i for i, pair in enumerate(labels) if t in pair)
             for t in range(5)]
    independent = [frozenset(z) for z in combinations(range(10), 4)
                   if all(p[i][j] == 0 for i, j in combinations(z, 2))]
    require(set(independent) == set(stars), 'independent four-set coverage')
    shapes = []
    for excess in partitions(6):
        if len(excess) <= 11:
            shape = tuple(sorted([4] * (11 - len(excess)) +
                                 [4 + x for x in excess]))
            if max(shape) >= 9:
                shapes.append(shape)
    require(shapes == [(4,) * 9 + (5, 9), (4,) * 10 + (10,)],
            'complete large-row partitions')

    def margin_solutions(total, target):
        return [mu for mu in weak_compositions(total, 5)
                if all(mu[u] + mu[v] == target[i]
                       for i, (u, v) in enumerate(labels))]

    mu10 = margin_solutions(10, [4] * 10)
    require(mu10 == [(2,) * 5], 'ten-row multiplicity completeness')
    rows10 = [frozenset(range(10))] + [stars[t] for t in range(5)
                                                    for _ in range(2)]
    require(gram(rows10) == s0, 'ten-row Gram')
    require(gram(rows10[1:]) == k, 'ten-row contraction')

    records = []
    margin_rejects = 0
    red_support_rejects = 0
    matrix_entry_checks = 200
    for a in range(10):
        z = frozenset(range(10)) - {a}
        for qtuple in combinations(range(10), 5):
            q = frozenset(qtuple)
            fdegree = [6 - 5 * (i in z) - (i in q) for i in range(10)]
            require(sum(fdegree) == 10, 'F total degree')
            if fdegree[a] > 5:
                margin_rejects += 1
                continue
            require(a in q and fdegree[a] == 5, 'F center equality')
            r = q - {a}
            if any(p[i][j] for i, j in combinations(r, 2)):
                red_support_rejects += 1
                continue
            require(r in stars, 'virtual independent row is a star')
            t = stars.index(r)
            left = frozenset(range(10)) - q
            f = [[int(i == a and j in left) + int(j == a and i in left)
                  for j in range(10)] for i in range(10)]
            require([sum(row) for row in f] == fdegree, 'F star margins')
            target = [4 - (i in r) for i in range(10)]
            mus = margin_solutions(9, target)
            wanted = tuple(1 if u == t else 2 for u in range(5))
            require(mus == [wanted], 'nine-row multiplicity completeness')
            small = [stars[u] for u in range(5) for _ in range(wanted[u])]
            rows = [z, q] + small
            require(all(sum(i in row for row in rows) == 5
                        for i in range(10)), 'full-degree columns')
            require(add(outer(z), outer(q), f) == add(outer(range(10)),
                                                       outer(r)),
                    'zz^t+qq^t+F=J+rr^t')
            require(add(gram(small), outer(r)) == k, 'R+rr^t=K')
            require(add(gram(rows), f) == s0, 'M^tM+F=S0')
            matrix_entry_checks += 300
            records.append({'omitted': a, 'star': t,
                            'rows': [sorted(row) for row in rows],
                            'multiplicities': list(wanted)})
    require(len(records) == 30 and margin_rejects == 1260 and
            red_support_rejects == 1230, 'complete nine-row cover')
    digest = hashlib.sha256(json.dumps(records, sort_keys=True,
                                       separators=(',', ':')).encode()).hexdigest()
    return {'independent_four_sets': len(independent),
            'large_row_shapes': [list(x) for x in shapes],
            'ten_row_multiplicity_solutions': len(mu10),
            'nine_row_candidates': 2520,
            'nine_row_F_margin_rejections': margin_rejects,
            'nine_row_red_support_rejections': red_support_rejects,
            'nine_row_canonical_incidences': len(records),
            'matrix_entry_checks': matrix_entry_checks,
            'nine_row_records_sha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--derive', action='store_true')
    args = parser.parse_args()
    result = run()
    if not args.derive:
        expected = json.loads(args.expected.read_text())['gram']
        require(json.dumps(result, sort_keys=True) ==
                json.dumps(expected, sort_keys=True), 'exact expected Gram result')
    print(json.dumps({'gram': result}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
