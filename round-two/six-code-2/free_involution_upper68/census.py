"""Primary exact cover: choose optional-only rows, then mandatory pairs.

The fixed high-pair budget proves at most two optional-only rows occur.
All selected and generated records use actual quadruples, not hash verdicts.
"""
from itertools import combinations
from common import Guard, require, bits

def solve(data, case, nodes=200000, seconds=10):
    columns = tuple(tuple(q) for q in case['columns'])
    quota = tuple(case['quota'])
    pairs = tuple(data['eligible'])
    pair_index = {p: i for i, p in enumerate(pairs)}
    mandatory = sum(1 << pair_index[tuple(p)] for p in case['mandatory'])
    high = set(case.get('high',list(case.get('other_high',[]))+[14]))
    masks = [sum(1 << pair_index[p] for p in combinations(q, 2)) for q in columns]
    high_cost = [sum(set(p) <= high for p in combinations(q, 2)) for q in columns]
    point_rows = [sum(1 << i for i, q in enumerate(columns) if v in q) for v in range(15)]
    pair_rows = [sum(1 << i for i, m in enumerate(masks) if m >> e & 1) for e in range(len(pairs))]
    conflicts = [sum(1 << j for j, n in enumerate(masks) if m & n) for m in masks]
    zero = [i for i, mask in enumerate(masks) if not(mask & mandatory)]
    require(all(high_cost[i] >= 3 for i in zero), 'optional-only high cost')
    positive = sum(1 << i for i in range(len(columns)) if i not in zero)
    budget = case.get('covered_high_budget',6) - case['already_high']
    guard = Guard(nodes, seconds)
    covers = []

    def search(pool, left, need, chosen):
        guard.tick()
        if not need:
            if not any(left):
                covers.append(tuple(sorted(chosen)))
            return
        if any((pool & point_rows[v]).bit_count() < n for v, n in enumerate(left)):
            return
        options = None
        for e in bits(need):
            possible = pool & pair_rows[e]
            if not possible:
                return
            if options is None or possible.bit_count() < options.bit_count():
                options = possible
        for i in bits(options):
            after = list(left)
            active = pool & ~conflicts[i]
            for v in columns[i]:
                after[v] -= 1
                require(after[v] >= 0, 'quota underflow')
                if not after[v]:
                    active &= ~point_rows[v]
            search(active, tuple(after), need & ~masks[i], chosen + (i,))

    zero_configs = [()]
    for size in (1, 2):
        for selected in combinations(zero, size):
            if sum(high_cost[i] for i in selected) > budget:
                continue
            if any(masks[i] & masks[j] for i, j in combinations(selected, 2)):
                continue
            zero_configs.append(selected)
    for selected in zero_configs:
        left = list(quota)
        pool = positive
        for i in selected:
            pool &= ~conflicts[i]
            for v in columns[i]:
                left[v] -= 1
        if min(left) < 0:
            continue
        for v, n in enumerate(left):
            if not n:
                pool &= ~point_rows[v]
        search(pool, tuple(left), mandatory, selected)
    require(len(covers) == len(set(covers)), 'duplicate covers')
    return sorted(covers), guard.nodes, len(zero), len(zero_configs)
