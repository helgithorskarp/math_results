"""Exact local14 exclusion: word rows, multiset join, red stars.

Actual author six-books-3, researcher. Python 3.11+, standard library.
The nine core masks are a credited premise, not a new local census.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE_MASKS = (30083408, 51316320, 51317328, 54986080, 54987088,
              55740996, 126126276, 126158020, 126158146)
PAIRS = tuple(combinations(range(10), 2))
F_EDGES = tuple(combinations(range(8), 2))


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def local_graph(mask):
    neighbors = [set() for _ in range(10)]
    for bit, (i, j) in enumerate(F_EDGES):
        if mask >> bit & 1:
            neighbors[i + 2].add(j + 2)
            neighbors[j + 2].add(i + 2)
    for low, pair in ((0, (2, 3)), (1, (4, 5))):
        for i in pair:
            neighbors[low].add(i)
            neighbors[i].add(low)
    need(tuple(map(len, neighbors)) == (2, 2) + (3,) * 8,
         'Core degrees differ')
    need(all(not neighbors[i] & neighbors[j]
             for i in range(10) for j in neighbors[i]), 'Core has a triangle')
    return neighbors


def capacities(neighbors):
    h = tuple(map(len, neighbors))
    return [[h[i] + 2 if i == j else
             h[i] + h[j] - (5 if j in neighbors[i] else 2)
             - len(neighbors[i] & neighbors[j])
             for j in range(10)] for i in range(10)]


def row_words(neighbors, upper):
    for z in range(1024):
        size = z.bit_count()
        if not 4 <= size <= 8:
            continue
        if any(tuple(z >> i & 1 for i in triple) not in
               ((1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1))
               for triple in ((0, 2, 3), (1, 4, 5))):
            continue
        if any(upper[i][j] < 1 for i, j in PAIRS
               if z >> i & 1 and z >> j & 1):
            continue
        if any(size > len(neighbors[i]) + 5
               - sum(not (z >> j & 1) for j in neighbors[i])
               for i in range(10) if not (z >> i & 1)):
            continue
        if any(sum(z >> j & 1 for j in neighbors[i]) < size - 7
               for i in range(10) if z >> i & 1):
            continue
        yield z


def cut_score(cut, row):
    return (cut['gamma']
            + sum(a * (row >> i & 1) for i, a in enumerate(cut['alpha']))
            + sum(q for i, j, q in cut['beta'] if row >> i & 1 and row >> j & 1))


def check_cut(cut, neighbors, upper, rows):
    need(len(cut['alpha']) == 10, 'Cut dimension differs')
    need(all(type(a) is int for a in cut['alpha']), 'Noninteger coefficient')
    need(type(cut['gamma']) is int and type(cut['rhs']) is int,
         'Noninteger constant')
    need(len({(i, j) for i, j, q in cut['beta']}) == len(cut['beta']),
         'Repeated weighted pair')
    need(all(type(i) is int and type(j) is int and type(q) is int
             and 0 <= i < j < 10 and q > 0 for i, j, q in cut['beta']),
         'Invalid nonnegative pair coefficient')
    need(all(cut_score(cut, z) >= 0 for z in rows), 'Negative row score')
    rhs = (11 * cut['gamma']
           + sum(a * upper[i][i] for i, a in enumerate(cut['alpha']))
           + sum(q * upper[i][j] for i, j, q in cut['beta']))
    need(rhs == cut['rhs'] and rhs <= 0, 'Cut bound differs')
    return [z for z in rows if cut_score(cut, z) == 0] if rhs == 0 else []


def digest(records):
    return hashlib.sha256(b''.join(json.dumps(r, separators=(',', ':')).encode('ascii')
                                  + b'\n' for r in records)).hexdigest()


def histogram(rows):
    return {str(k): v for k, v in sorted(Counter(z.bit_count() for z in rows).items())}


def incidence_join(zero_rows, upper):
    """Independently capped low/high multisets joined on all ten columns."""
    fours = [z for z in zero_rows if z.bit_count() == 4]
    high = [z for z in zero_rows if z.bit_count() > 4]
    need(not any(z.bit_count() == 8 for z in high), 'Unexpected size-eight row')
    target = [upper[i][i] for i in range(10)]
    pair_caps = [upper[i][j] for i, j in PAIRS]
    info = {z: ([i for i in range(10) if z >> i & 1],
                [p for p, (i, j) in enumerate(PAIRS) if z >> i & 1 and z >> j & 1])
            for z in zero_rows}
    column = [0] * 10
    pairs = [0] * 45
    selected = []
    lookups = {}
    four_counts = {}
    high_counts = Counter()
    matrices = []

    def fits(z):
        cs, ps = info[z]
        return (all(column[i] < target[i] for i in cs)
                and all(pairs[p] < pair_caps[p] for p in ps))

    def add(z, sign):
        cs, ps = info[z]
        for i in cs:
            column[i] += sign
        for p in ps:
            pairs[p] += sign

    for wanted in (7, 8, 9):
        lookup = defaultdict(list)
        total = 0

        def low_visit(first, left):
            nonlocal total
            if left == 0:
                total += 1
                lookup[tuple(column)].append((tuple(selected), bytes(pairs)))
                return
            for ix in range(first, len(fours)):
                z = fours[ix]
                if fits(z):
                    add(z, 1)
                    selected.append(z)
                    low_visit(ix, left - 1)
                    selected.pop()
                    add(z, -1)

        low_visit(0, wanted)
        lookups[wanted] = lookup
        four_counts[str(wanted)] = total

    def high_visit(first, surplus):
        if surplus == 0:
            pattern = tuple(sorted((z.bit_count() for z in selected), reverse=True))
            high_counts[pattern] += 1
            key = tuple(t - c for t, c in zip(target, column))
            wanted = 11 - len(selected)
            need(wanted in lookups, 'Uncovered row-size pattern')
            for low, low_pairs in lookups[wanted].get(key, []):
                if all(a + b <= cap for a, b, cap in zip(pairs, low_pairs, pair_caps)):
                    matrices.append(sorted(list(low) + selected))
            return
        for ix in range(first, len(high)):
            z = high[ix]
            extra = z.bit_count() - 4
            if extra <= surplus and fits(z):
                add(z, 1)
                selected.append(z)
                high_visit(ix, surplus - extra)
                selected.pop()
                add(z, -1)

    high_visit(0, 4)
    matrices.sort()
    need(len(matrices) == len({tuple(r) for r in matrices}), 'Duplicate matrix')
    return matrices, four_counts, [[list(k), v] for k, v in sorted(high_counts.items())]


def star_count(rows, b, neighbors):
    """All red neighborhoods of b: only A--b book caps are used."""
    z = rows[b]
    size = z.bit_count()
    count = 0
    for star in combinations([c for c in range(11) if c != b], size):
        star = set(star)
        good = True
        for i in range(10):
            if not (z >> i & 1):
                pages = (sum(not (z >> j & 1) for j in neighbors[i])
                         + sum(not (rows[c] >> i & 1) for c in star))
                if pages > 3:
                    good = False
                    break
            else:
                pages = (sum(z >> j & 1 and j not in neighbors[i]
                             for j in range(10) if j != i)
                         + sum(rows[c] >> i & 1 for c in range(11)
                               if c != b and c not in star))
                if pages > 6:
                    good = False
                    break
        count += int(good)
    return count


def run(cut_path=HERE / 'cuts.json'):
    cuts = json.loads(cut_path.read_text())
    need(cuts['schema'] == 1, 'Certificate schema differs')
    need(tuple(c['F_mask'] for c in cuts['cuts']) == CORE_MASKS,
         'Nine credited core masks differ')
    core_records = []
    survivors = []
    for cut in cuts['cuts']:
        neighbors = local_graph(cut['F_mask'])
        upper = capacities(neighbors)
        rows = list(row_words(neighbors, upper))
        zero = check_cut(cut, neighbors, upper, rows)
        core_records.append({'F_mask': cut['F_mask'], 'row_sizes': histogram(rows),
                             'rows_sha256': digest(rows), 'cut_rhs': cut['rhs'],
                             'zero_row_sizes': histogram(zero)})
        if zero:
            survivors.append((cut['F_mask'], neighbors, upper, zero))
    need(len(survivors) == 1, 'Unexpected number of zero faces')
    mask, neighbors, upper, zero = survivors[0]
    matrices, four_counts, high_counts = incidence_join(zero, upper)
    records = []
    star_tests = 0
    for rows in matrices:
        b = next((b for b in range(11) if star_count(rows, b, neighbors) == 0), None)
        need(b is not None, 'An incidence matrix has no empty A--B star')
        from math import comb
        star_tests += comb(10, rows[b].bit_count())
        records.append({'rows': rows, 'empty_star_row': b})
    pattern = lambda rows: tuple(sorted((z.bit_count() for z in rows if z.bit_count() > 4),
                                       reverse=True))
    patterns = Counter(pattern(rows) for rows in matrices)
    summary = {'schema': 1, 'agent': 'six-books-3', 'role': 'researcher',
               'complete': True, 'cores': core_records, 'surviving_F_mask': mask,
               'four_multisets': four_counts, 'high_multisets': high_counts,
               'incidence_matrices': len(matrices), 'incidences_sha256': digest(matrices),
               'incidence_patterns': [[list(k), v] for k, v in sorted(patterns.items())],
               'empty_star_records': len(records), 'selected_star_tests': star_tests,
               'extendible_matrices': 0}
    return summary, {'schema': 1, 'F_mask': mask, 'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cuts', type=Path, default=HERE / 'cuts.json')
    parser.add_argument('--write', action='store_true', help='Explicitly regenerate compact fixtures')
    args = parser.parse_args()
    summary, incidences = run(args.cuts)
    for name, value in (('expected.json', summary), ('incidences.json', incidences)):
        data = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('ascii')
        if args.write:
            (HERE / name).write_bytes(data)
        else:
            need(data == (HERE / name).read_bytes(), 'Exact fixture differs: ' + name)
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
