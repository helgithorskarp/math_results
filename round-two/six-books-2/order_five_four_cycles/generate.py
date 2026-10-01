"""Literal forbidden-book certificates for 18,250 normalized C5 templates.

The necessary block reduction is in PROOF.md. Generated witness reports
are local output, not public proof corpora. No verifier code is imported.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import time

ALL = 31
TOTAL = 18250
PAIRS = list(itertools.combinations(range(22), 2))


def rotate(mask, shift):
    return ((mask << shift) | (mask >> (5 - shift))) & ALL if shift else mask


def build(internal, cross, fixed):
    """Directly build red bitset rows on cyclic orbits and fixed points."""
    n = 20 + len(fixed)
    rows = [0] * n
    for i, j in itertools.combinations(range(n), 2):
        if j >= 20:
            red = 0 if i >= 20 else fixed[j - 20] >> (i // 5) & 1
        else:
            a, x = divmod(i, 5)
            b, y = divmod(j, 5)
            red = (internal[a] if a == b else cross[a, b]) >> ((y - x) % 5) & 1
        if red:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return rows


def pages(rows, i, j):
    red = rows[i] >> j & 1
    mask = (rows[i] & rows[j] if red else
            ((1 << len(rows)) - 1) & ~(rows[i] | rows[j]) & ~((1 << i) | (1 << j)))
    return red, mask


def first_book(rows):
    for i, j in itertools.combinations(range(len(rows)), 2):
        red, common = pages(rows, i, j)
        needed = 4 if red else 7
        if common.bit_count() >= needed:
            chosen = [k for k in range(len(rows)) if common >> k & 1][:needed]
            return [i, j, red, chosen], common.bit_count()
    return None, None


def templates():
    allowed = sorted({rotate(mask, shift) for mask in (3, 26) for shift in range(5)})
    for ac, ad, bc, bd in itertools.product((3, 26), allowed, allowed, allowed):
        cross = {(0, 1): 1, (0, 2): ac, (0, 3): ad,
                 (1, 2): bc, (1, 3): bd, (2, 3): 1}
        totals = [ac.bit_count() + ad.bit_count(), bc.bit_count() + bd.bit_count(),
                  ac.bit_count() + bc.bit_count(), ad.bit_count() + bd.bit_count()]
        choices = [(1, 2) if total == 5 else (1,) for total in totals]
        for generators in itertools.product(*choices):
            key = ['D'] + list(generators) + [ac, ad, bc, bd]
            internal = [(1 << g) | (1 << (5 - g)) for g in generators]
            yield key, internal, cross, [3, 12]
    size_two = [mask for mask in range(32) if mask.bit_count() == 2]
    size_three = [mask for mask in range(32) if mask.bit_count() == 3]
    for a, b, c, ad, bc, cd in itertools.product((1, 2), (1, 2), (1, 2),
                                               size_two, size_three, size_three):
        key = ['O', a, b, c, ad, bc, cd]
        cross = {(0, 1): ALL ^ (1 | (1 << a)), (0, 2): ALL ^ (1 | (1 << b)),
                 (0, 3): ad, (1, 2): bc, (1, 3): ALL ^ (1 | (1 << c)), (2, 3): cd}
        yield key, [0, 0, 0, 18], cross, [3, 5]


def baseline():
    # A positive 21-vertex control: KG(7,2) with cycle type 5^4 1.
    cross = {(0, 1): 4, (0, 2): 28, (0, 3): 28,
             (1, 2): 26, (1, 3): 26, (2, 3): 30}
    rows = build([12, 18, 0, 0], cross, [3])
    root_pairs = ([{t, (t + 1) % 5} for t in range(5)]
                  + [{t, (t + 2) % 5} for t in range(5)]
                  + [{t, 5} for t in range(5)] + [{t, 6} for t in range(5)] + [{5, 6}])
    for i, j in itertools.combinations(range(21), 2):
        if bool(rows[i] >> j & 1) != root_pairs[i].isdisjoint(root_pairs[j]):
            raise ValueError('Kneser control does not match literal root pairs')
    if first_book(rows)[0] is not None:
        raise ValueError('Kneser positive control failed')
    hist = {0: collections.Counter(), 1: collections.Counter()}
    for i, j in itertools.combinations(range(21), 2):
        red, common = pages(rows, i, j)
        hist[red][common.bit_count()] += 1
    if sum(row.bit_count() for row in rows) != 210 or any(row.bit_count() != 10 for row in rows):
        raise ValueError('Kneser degrees')
    if hist[1] != {3: 105} or hist[0] != {5: 105}:
        raise ValueError('Kneser page histograms')
    return {'red_edges': 105, 'red_pages': {'3': 105}, 'blue_pages': {'5': 105}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('literal_results.json'))
    parser.add_argument('--limit', type=int, default=TOTAL)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= TOTAL:
        parser.error('--limit must be between 1 and 18250')
    control = baseline()
    if args.controls:
        print('All 210 Kneser spines and the cyclic encoding matched literal root pairs')
        return
    start = time.perf_counter()
    records, survivors = [], []
    counts, hist = collections.Counter(), collections.Counter()
    for rank, (key, internal, cross, fixed) in enumerate(templates()):
        if rank == args.limit:
            break
        rows = build(internal, cross, fixed)
        counts[key[0]] += 1
        witness, actual_count = first_book(rows)
        if witness is None:
            survivors.append(key)
        else:
            records.append([key, witness])
            hist[key[0], witness[2], actual_count] += 1
    result = {
        'status': 'complete' if args.limit == TOTAL else 'partial',
        'method': 'literal-normalized', 'templates_scanned': sum(counts.values()),
        'counts': dict(counts), 'survivors': survivors, 'baseline': control,
        'records': records,
        'records_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
        'first_violation_histogram': [[list(key), value] for key, value in sorted(hist.items())],
        'seconds': round(time.perf_counter() - start, 3),
    }
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}, indent=2))


if __name__ == '__main__':
    main()
