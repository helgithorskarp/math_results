"""Independent literal replay of the low-prefix barrier; Python>=3.11, stdlib.
Actual author six-covering-1, researcher. Read proof.md for the complete reduction.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import time


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check(rows, fixture, seed_sha):
    start = time.monotonic()
    period, cutoff, bound = 15120, 360, 83
    need(all(len(row) == 2 and all(type(v) is int for v in row) for row in rows), 'Malformed seed')
    need([m for a, m in rows] == [m for m in range(8, period + 1) if period % m == 0], 'Wrong eligible moduli')
    need(all(0 <= a < m for a, m in rows), 'Phase outside its modulus')
    need(fixture['period'] == period and fixture['cutoff'] == cutoff and fixture['hole_bound'] == bound
         and fixture['seed_sha256'] == seed_sha, 'Wrong certificate scope')
    low = [m for a, m in rows if m < cutoff]
    high = [m for a, m in rows if m >= cutoff]
    old = {m: a for a, m in rows}
    holes = [x for x in range(period) if all(x % m != a for a, m in rows)]
    need(len(holes) == 84, 'Seed does not attain84 holes')
    forced, nonforced = [], []
    for m0 in low:
        free = set(high + [m0])
        fixed = [(a, m) for a, m in rows if m not in free]
        points = [x for x in range(period) if all(x % m != a for a, m in fixed)]
        hist = {m: Counter(x % m for x in points) for m in free}
        caps = {m: max(h.values(), default=0) for m, h in hist.items()}
        slack = sum(caps.values()) - len(points) + bound
        need(slack >= 0 and caps[m0] - hist[m0][old[m0]] <= slack, 'Incorrect old-phase screen')
        alternatives = [a for a in range(m0) if a != old[m0] and caps[m0] - hist[m0][a] <= slack]
        (nonforced if alternatives else forced).append(m0)
    need(fixture['forced_old_cases'] == forced, 'Incomplete forced-phase cases')
    trees = fixture['trees']
    need([tree['extra'] for tree in trees] == [None] + nonforced, 'Incomplete exceptional trees')
    total_nodes = leaves = branches = 0
    for tree in trees:
        free = high if tree['extra'] is None else sorted(high + [tree['extra']])
        fixed = [(a, m) for a, m in rows if m not in free]
        points = tuple(x for x in range(period) if all(x % m != a for a, m in fixed))
        records = tree['decisions']
        need(isinstance(records, list) and 0 < len(records) <= 5000, 'Wrong tree size')
        cursor = 0

        def visit(residual, remaining):
            nonlocal cursor, leaves, branches
            need(time.monotonic() - start < 20, 'Incomplete checker at explicit deadline')
            need(cursor < len(records), 'Missing phase child')
            node = records[cursor]
            cursor += 1
            hist = {m: Counter(x % m for x in residual) for m in remaining}
            caps = {m: max(h.values(), default=0) for m, h in hist.items()}
            total = sum(caps.values())
            if node == ['L']:
                need(len(residual) - total > bound, 'Nonstrict capacity leaf')
                leaves += 1
                return
            need(isinstance(node, list) and len(node) == 3 and node[0] == 'B', 'Unclosed tree node')
            m, phases = node[1:]
            need(type(m) is int and m in remaining, 'Repeated or nonexistent branch modulus')
            slack = total - len(residual) + bound
            need(slack >= 0, 'Invalid nonnegative-slack branch')
            required = {a for a, mass in hist[m].items() if mass >= max(1, caps[m] - slack)}
            need(isinstance(phases, list) and all(type(a) is int and 0 <= a < m for a in phases)
                 and len(set(phases)) == len(phases) and set(phases) == required and bool(required), 'Nonexhaustive phase branch')
            branches += 1
            rest = tuple(label for label in remaining if label != m)
            for a in phases:
                child = tuple(x for x in residual if x % m != a)
                visit(child, rest)

        visit(points, tuple(sorted(free)))
        need(cursor == len(records), 'Extra or unreachable proof node')
        total_nodes += cursor
    return dict(status='EXACT_LOW_PREFIX_84_HOLE_BARRIER_CHECKED', period=period,
        labels=len(rows), minimum_exactly=min(m for a, m in rows), actual_lcm=math.lcm(*(m for a, m in rows)),
        seed_holes=len(holes), low_labels=len(low), unrestricted_high_labels=len(high),
        forced_old_cases=len(forced), one_low_tree_cases=len(nonforced), complete_one_low_cases=len(low),
        tree_nodes=total_nodes, strict_leaves=leaves, branch_nodes=branches,
        minimum_holes_with_at_most_one_low_change=84, covering_low_seed_matches_at_most=46,
        normalized_nonanchor_low_seed_matches_at_most=44)


def controls(rows, fixture, seed_sha):
    invalid = []
    data = copy.deepcopy(fixture); data['forced_old_cases'].pop(); invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'].pop(); invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'][0]['decisions'][0][2] = []; invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'][0]['decisions'][0][1] = 8; invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'][0]['decisions'].pop(); invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'][0]['decisions'].append(['L']); invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['hole_bound'] = 84; invalid.append((rows, data))
    data = copy.deepcopy(fixture); data['trees'][0]['decisions'][0] = ['L']; invalid.append((rows, data))
    bad = copy.deepcopy(rows); bad[0] = (8, 8); invalid.append((bad, fixture))
    bad = copy.deepcopy(rows); bad[1] = bad[0]; invalid.append((bad, fixture))
    bad = copy.deepcopy(rows); bad.pop(0); invalid.append((bad, fixture))
    bad = copy.deepcopy(rows); bad[0] = (True, 8); invalid.append((bad, fixture))
    rejected = 0
    for seed, data in invalid:
        try:
            check(seed, data, seed_sha)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed compact certificate accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    seed, instance = root / 'seed.tsv', root / 'input.json'
    expected = json.loads((root / 'expected.json').read_text())
    seed_sha = hashlib.sha256(seed.read_bytes()).hexdigest()
    need(seed_sha == expected['seed_sha256'], 'Seed hash mismatch')
    need(hashlib.sha256(instance.read_bytes()).hexdigest() == expected['input_sha256'], 'Fixture hash mismatch')
    rows = [tuple(map(int, line.split())) for line in seed.read_text().splitlines()]
    fixture = json.loads(instance.read_text())
    result = check(rows, fixture, seed_sha)
    need(result == expected['summary'], 'Unexpected complete mathematical output')
    if args.controls:
        rejected = controls(rows, fixture, seed_sha)
        need(rejected == 12, 'Incomplete negative controls')
        result['malformed_controls_rejected'] = rejected
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
