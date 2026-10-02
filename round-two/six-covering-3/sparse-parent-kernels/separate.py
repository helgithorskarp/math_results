"""Complete separator for the minimal <=3-parent13-point product kernels.

This is a necessary test for owned P. Passing does not establish completion.
The classification and CRT capacity proof are in proof.md. The search visits
all increasing tuples, with only necessary projection/color prunings.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521) if 2520 % n == 0 and
             n not in {n for n, a in PREFIX})


def need(ok, message):
    if not ok:
        raise ValueError(message)


def balanced_rainbow(points, k):
    need(type(k) is int and k in (4, 5) and isinstance(points, list) and
         points == sorted(set(points)) and
         all(type(y) is int and 0 <= y < 315 for y in points),
         'invalid balanced-rainbow domain')
    if any(len({y % d for y in points}) < k for d in (5, 7, 9)):
        return None
    if sum(min(2, sum(y % 3 == a for y in points)) for a in range(3)) < k:
        return None
    masks = {d: [sum(1 << y for y in range(a, 315, d)) for a in range(d)]
             for d in (5, 7, 9)}
    thirds = [sum(1 << y for y in range(a, 315, 3)) for a in range(3)]

    def visit(chosen, remaining, counts):
        if len(chosen) == k:
            return chosen
        if remaining.bit_count() < k - len(chosen):
            return None
        while remaining:
            bit = remaining & -remaining
            y = bit.bit_length() - 1
            remaining -= bit
            c = y % 3
            if counts[c] == 2:
                continue
            colors = counts.copy()
            colors[c] += 1
            forbidden = masks[5][y % 5] | masks[7][y % 7] | masks[9][y % 9]
            if colors[c] == 2:
                forbidden |= thirds[c]
            answer = visit(chosen + [y], remaining & ~forbidden, colors)
            if answer is not None:
                return answer
        return None

    return visit([], sum(1 << y for y in points), [0, 0, 0])


def separate(phases):
    need(isinstance(phases, list) and len(phases) == 36 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        sorted(n for n, a in phases) == list(BASE), 'wrong original BASE inventory')
    fibers = [[] for _ in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in (*PREFIX, *phases)):
            need(x % 8 != 0, 'unexpected parent0')
            fibers[x % 8 - 1].append(x % 315)
    for H in fibers:
        H.sort()
    # Initial P admits a balanced rainbow5 only at parent4: odd parents
    # have only four allowed mod5 values; parents2/6 have only two mod3
    # values, each with quota2. Thus the5/5/3 profile is impossible here.
    large = balanced_rainbow(fibers[3], 5)
    if large is not None:
        small = {r: balanced_rainbow(fibers[r-1], 4)
                 for r in (1, 2, 3, 5, 6, 7)}
        for r, s in combinations(small, 2):
            if small[r] is None or small[s] is None:
                continue
            kernel = [[] for _ in range(7)]
            kernel[3] = large
            kernel[r-1] = small[r]
            kernel[s-1] = small[s]
            physical = [x for x in range(10080) if x % 8 != 0 and
                        x % 315 in kernel[x % 8 - 1]]
            need(len(physical) == 52, 'wrong full-product lift count')
            need(all(all(x % n != a for n, a in (*PREFIX, *phases))
                     for x in physical), 'kernel escaped the actual residual')
            capacities = []
            D = [d for d in range(1, 316) if 315 % d == 0]
            for n in sorted([16*d for d in D] + [32*d for d in D]):
                hits = [0]*n
                for x in physical:
                    hits[x % n] += 1
                capacities.append([n, max(hits)])
            need(sum(c for n, c in capacities) == 51, 'wrong sparse-kernel capacity')
            points = [x for x in physical if x < 2520]
            clause = [[n, a] for n in BASE for a in sorted({x % n for x in points})]
            need(not any(row in clause for row in phases), 'BASE did not leave clause violated')
            return {'status': 'MINIMAL_THREE_PARENT13_KERNEL', 'kernel': kernel,
                    'physical_demand': 52, 'tail_capacity_budget': 51,
                    'clause': clause, 'clause_sha256': sha256(json.dumps(
                        clause, separators=(',', ':')).encode()).hexdigest(),
                    'scope': 'This BASE assignment is nonextendible; owned P remains open.'}
    return {'status': 'NO_MINIMAL_LE3_PARENT13_KERNEL',
            'tail_feasibility_asserted': False,
            'larger_or_weighted_kernel_excluded': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-json', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = separate(json.loads(args.base_json.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'clause'}, sort_keys=True))
