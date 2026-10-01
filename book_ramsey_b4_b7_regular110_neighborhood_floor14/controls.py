"""Literal signed identities and forgery controls, author six-books-3, researcher.

The arbitrary regular control graphs generally fail the book caps.
They validate formulas, not construction or exhaustive-coverage claims.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import copy
import json
import random
import check

HERE = Path(__file__).resolve().parent


def reject(function, name):
    try:
        function()
    except RuntimeError:
        return
    raise RuntimeError('accepted deliberately invalid certificate: ' + name)


def run():
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
        check.c.need(all(len(row) == 10 for row in red), 'control is not ten-regular')
        blue = [set(range(22)) - red[i] - {i} for i in range(22)]
        for root in (0, 1, 4, 9, 17):
            a, b = sorted(red[root]), sorted(blue[root])
            local = [red[i] & set(a) for i in a]
            h = list(map(len, local))
            miss = [set(a) - red[j] for j in b]
            column = [sum(i in row for row in miss) for i in a]
            check.c.need(column == [x + 2 for x in h], 'literal column identity failed')
            check.c.need(sum(map(len, miss)) == sum(h) + 20, 'literal total misses failed')
            counts['column_identities'] += 10
            for j, row in zip(b, miss):
                check.c.need(len(row) == len(red[j] & set(b)), 'literal outside degree failed')
                counts['outside_degree_identities'] += 1
            eps = [[0] * 10 for _ in range(10)]
            s0 = [[0] * 10 for _ in range(10)]
            for i in range(10):
                s0[i][i] = h[i] + 2
            for i, j in combinations(range(10), 2):
                is_red = a[j] in red[a[i]]
                slack = (3 - len(red[a[i]] & red[a[j]]) if is_red
                         else 6 - len(blue[a[i]] & blue[a[j]]))
                eps[i][j] = eps[j][i] = slack
                value = h[i] + h[j] - (5 if is_red else 2) - len(local[i] & local[j])
                s0[i][j] = s0[j][i] = value
                check.c.need(value - slack == sum(a[i] in row and a[j] in row for row in miss),
                             'literal pair identity failed')
                counts['pair_identities'] += 1
            for i in range(10):
                excess = sum(len(row) - 4 for row in miss if a[i] in row)
                neighbor_h = sum(h[j] for j in range(10) if a[j] in local[i])
                check.c.need(sum(eps[i]) == 3 * h[i] + sum(h) - 24 - neighbor_h - excess,
                             'literal incident slack identity failed')
                counts['incident_slack_identities'] += 1
            five = [k for k, row in enumerate(miss) if len(row) == 5]
            for first, second in combinations(five, 2):
                x, y = miss[first], miss[second]
                literal = [[sum(a[i] in row and a[j] in row for k, row in enumerate(miss)
                                if k not in (first, second)) for j in range(10)] for i in range(10)]
                rebuilt = [[s0[i][j] - eps[i][j] - int(a[i] in x and a[j] in x) -
                            int(a[i] in y and a[j] in y) for j in range(10)] for i in range(10)]
                check.c.need(literal == rebuilt, 'literal two5 residual differs')
                check.c.need([literal[i][i] for i in range(10)] ==
                             [column[i] - int(a[i] in x) - int(a[i] in y) for i in range(10)],
                             'literal two5 diagonal differs')
                counts['literal_two5_row_removals'] += 1
                counts['literal_two5_entries'] += 100
            counts['regular_root_controls'] += 1
    expected = json.loads((HERE / 'expected.json').read_text())
    cert = json.loads((HERE / 'negative_vectors.json').read_text())
    profiles = expected['profiles']
    index = next(i for i, rec in enumerate(cert['profiles']) if rec['vector_indices'])
    for kind in ('zero', 'short', 'boolean', 'nonprimitive', 'duplicate', 'bad_index', 'bad_profile', 'missing_pool'):
        fake = copy.deepcopy(cert)
        if kind == 'zero':
            fake['vectors'][0] = [0] * 10
        elif kind == 'short':
            fake['vectors'][0].pop()
        elif kind == 'boolean':
            fake['vectors'][0][0] = True
        elif kind == 'nonprimitive':
            fake['vectors'][0] = [2 * x for x in fake['vectors'][0]]
        elif kind == 'duplicate':
            fake['vectors'].append(fake['vectors'][0][:])
        elif kind == 'bad_index':
            fake['profiles'][index]['vector_indices'][0] = len(fake['vectors'])
        elif kind == 'bad_profile':
            fake['profiles'][index]['index'] = -1
        else:
            fake['profiles'][index]['vector_indices'].clear()
        reject(lambda: check.validate_certificate(fake, profiles), kind)
        counts['forged_certificates_rejected'] += 1
    identity = [[int(i == j) for j in range(10)] for i in range(10)]
    reject(lambda: check.c.need(any(check.is_negative(identity, check.integer_form(v))
                                 for v in cert['vectors']), 'positive identity has no negative form'), 'positive identity')
    counts['forged_certificates_rejected'] += 1
    selected = next(p for p in profiles if p['row_pairs'])
    left, right, base, degrees = next(check.selected_pairs(selected['F_mask'], selected['stars']))
    reject(lambda: check.residual(base, degrees, ()), 'missing literal slack')
    counts['forged_certificates_rejected'] += 1
    counts['baseline_primary21_passed'] = int(bool(check.c.baseline()))
    return dict(sorted(counts.items()))


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
