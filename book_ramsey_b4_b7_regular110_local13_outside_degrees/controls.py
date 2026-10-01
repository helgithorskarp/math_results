"""Literal regular-graph identities and deliberately invalid certificates.

Actual author six-books-3, researcher. These controls validate identities
on arbitrary ten-regular graphs, most of which fail the book caps; they
are not evidence of a new Ramsey construction.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import copy
import json
import random
import check

HERE = Path(__file__).resolve().parent


def expect_rejection(function, message):
    try:
        function()
    except RuntimeError:
        return
    raise RuntimeError('accepted deliberately invalid input: ' + message)


def controls():
    counts = Counter()
    for number, steps in enumerate(combinations(range(1, 11), 5)):
        red = [{(i + sign * step) % 22 for sign in (-1, 1) for step in steps}
               for i in range(22)]
        rng = random.Random(970013 + number)
        for attempt in range(80):
            a, b, c, d = rng.sample(range(22), 4)
            if b in red[a] and d in red[c] and c not in red[a] and d not in red[b]:
                for u, v in ((a, b), (c, d)):
                    red[u].remove(v)
                    red[v].remove(u)
                for u, v in ((a, c), (b, d)):
                    red[u].add(v)
                    red[v].add(u)
                counts['degree_preserving_switches'] += 1
        check.need(all(len(r) == 10 for r in red), 'control graph is not ten-regular')
        blue = [set(range(22)) - red[i] - {i} for i in range(22)]
        for root in (0, 1, 4, 9, 17):
            a, b = sorted(red[root]), sorted(blue[root])
            local = [red[i] & set(a) for i in a]
            h = list(map(len, local))
            miss = [set(a) - red[j] for j in b]
            column = [sum(i in row for row in miss) for i in a]
            check.need(column == [x + 2 for x in h], 'literal column identity failed')
            check.need(sum(map(len, miss)) == sum(h) + 20, 'literal total miss count failed')
            counts['column_identities'] += 10
            for j, row in zip(b, miss):
                check.need(len(row) == len(red[j] & set(b)), 'literal outside degree failed')
                counts['outside_degree_identities'] += 1
            eps = [[0] * 10 for _ in range(10)]
            forced = [[0] * 10 for _ in range(10)]
            gram = [[sum(a[i] in row and a[j] in row for row in miss)
                     for j in range(10)] for i in range(10)]
            for i in range(10):
                forced[i][i] = h[i] + 2
            for i, j in combinations(range(10), 2):
                is_red = a[j] in red[a[i]]
                slack = (3 - len(red[a[i]] & red[a[j]]) if is_red
                         else 6 - len(blue[a[i]] & blue[a[j]]))
                eps[i][j] = eps[j][i] = slack
                value = h[i] + h[j] - (5 if is_red else 2) - len(local[i] & local[j])
                forced[i][j] = forced[j][i] = value
                check.need(value - slack == gram[i][j], 'literal pair identity failed')
                counts['pair_identities'] += 1
            for i in range(10):
                excess = sum(len(row) - 4 for row in miss if a[i] in row)
                neighbor_h = sum(h[j] for j in range(10) if a[j] in local[i])
                check.need(sum(eps[i]) == 3 * h[i] + sum(h) - 24 - neighbor_h - excess,
                           'literal incident slack identity failed')
                counts['incident_slack_identities'] += 1
            for chosen, z in enumerate(miss):
                if len(z) != 6:
                    continue
                literal = [[sum(a[i] in row and a[j] in row for k, row in enumerate(miss) if k != chosen)
                            for j in range(10)] for i in range(10)]
                reconstructed = [[forced[i][j] - eps[i][j] - int(a[i] in z and a[j] in z)
                                  for j in range(10)] for i in range(10)]
                check.need(literal == reconstructed, 'literal distinguished-row residual failed')
                check.need([literal[i][i] for i in range(10)] ==
                           [column[i] - int(a[i] in z) for i in range(10)], 'literal residual diagonal failed')
                counts['size_six_literal_residuals'] += 1
                counts['size_six_residual_entries'] += 100
            counts['regular_graph_root_controls'] += 1
    expected = json.loads((HERE / 'expected.json').read_text())
    cert = json.loads((HERE / 'negative_vectors.json').read_text())
    cases = expected['cases']
    index = next(i for i, rec in enumerate(cert['records']) if rec['vectors'])
    for kind in ('zero', 'short', 'boolean', 'nonprimitive', 'wrong_index'):
        forged = copy.deepcopy(cert)
        if kind == 'zero':
            forged['records'][index]['vectors'][0] = [0] * 10
        elif kind == 'short':
            forged['records'][index]['vectors'][0].pop()
        elif kind == 'boolean':
            forged['records'][index]['vectors'][0][0] = True
        elif kind == 'nonprimitive':
            forged['records'][index]['vectors'][0] = [2 * x for x in forged['records'][index]['vectors'][0]]
        else:
            forged['records'][index]['index'] = -1
        expect_rejection(lambda: check.validate_vectors(forged, cases), kind)
        counts['deliberately_invalid_certificates_rejected'] += 1
    identity = [[int(i == j) for j in range(10)] for i in range(10)]
    expect_rejection(lambda: check.check_forms(identity, cert['records'][index]['vectors']), 'positive identity')
    counts['deliberately_invalid_certificates_rejected'] += 1
    base, degrees = check.case_base(cases[index])
    expect_rejection(lambda: check.literal_residual(base, degrees, ()), 'missing slack degree')
    counts['deliberately_invalid_certificates_rejected'] += 1
    return dict(sorted(counts.items()))


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True))
