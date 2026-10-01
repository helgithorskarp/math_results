"""Actual point maps by high assignments and complete low constraint search.

The upper proof only requires a checked positive map for every root packing
into one of fixtures.json's stars. It does not require their distinctness or
completeness of a claimed automorphism group.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import json
import time


def structure(quads):
    quads = tuple(sorted(tuple(sorted(q)) for q in quads))
    pairs = {p for q in quads for p in combinations(q, 2)}
    high = tuple(v for v in range(17) if sum(v in q for q in quads) < 5)
    leave = set(combinations(range(17), 2)) - pairs
    core = {p for p in leave if set(p) <= set(high)}
    low = tuple(v for v in range(17) if v not in high)
    attach = {}
    for v in low:
        neighbors = [w for w in high if tuple(sorted((v, w))) in leave]
        if len(neighbors) != 1:
            raise ValueError('not an all-unit zero-low-leave object')
        attach[v] = neighbors[0]
    return quads, high, low, core, attach


def point_maps(first, second, stop_after_first=False):
    A, HA, LA, CA, attachA = structure(first)
    B, HB, LB, CB, attachB = structure(second)
    if sorted(sum(v in p for p in CA) for v in HA) != sorted(sum(v in p for p in CB) for v in HB):
        return [], 0
    targets = {}
    for q in B:
        key = tuple(v for v in q if v in HB)
        lows = tuple(v for v in q if v in LB)
        targets.setdefault(key, []).extend(permutations(lows))
    output = []
    nodes = 0
    started = time.monotonic()
    for placement in permutations(HB):
        high_map = dict(zip(HA, placement))
        if any(sum(v in q for q in A)!=sum(high_map[v] in q for q in B) for v in HA):
            continue
        if {tuple(sorted(high_map[v] for v in p)) for p in CA} != CB:
            continue
        domains = {v: {w for w in LB if attachB[w] == high_map[attachA[v]]} for v in LA}
        constraints = []
        possible = True
        for q in A:
            lows = tuple(v for v in q if v in LA)
            key = tuple(sorted(high_map[v] for v in q if v in HA))
            rows = [tuple(row) for row in targets.get(key, ()) if len(row) == len(lows)]
            if not rows:
                possible = False
                break
            constraints.append((lows, rows))
        if not possible:
            continue

        def search(dom):
            nonlocal nodes
            nodes += 1
            if nodes > 200000 or time.monotonic()-started > 10:
                raise TimeoutError('INCOMPLETE isomorphism coverage')
            dom = {v: set(values) for v, values in dom.items()}
            changed = True
            while changed:
                changed = False
                if any(not values for values in dom.values()):
                    return
                assigned = [next(iter(values)) for values in dom.values() if len(values) == 1]
                if len(assigned) != len(set(assigned)):
                    return
                used = set(assigned)
                for v, values in dom.items():
                    if len(values) > 1:
                        after = values - used
                        changed |= after != values
                        dom[v] = after
                        if not after:
                            return
                for lows, rows in constraints:
                    legal = [row for row in rows if all(w in dom[v] for v, w in zip(lows, row))]
                    if not legal:
                        return
                    for i, v in enumerate(lows):
                        after = dom[v] & {row[i] for row in legal}
                        changed |= after != dom[v]
                        dom[v] = after
                        if not after:
                            return
            if all(len(values) == 1 for values in dom.values()):
                mapping = [high_map.get(v) for v in range(17)]
                for v in LA:
                    mapping[v] = next(iter(dom[v]))
                p = tuple(mapping)
                if sorted(p) != list(range(17)) or {tuple(sorted(p[v] for v in q)) for q in A} != set(B):
                    raise ValueError('bad positive point map')
                output.append(p)
                return
            v = min((v for v in LA if len(dom[v]) > 1), key=lambda v: (len(dom[v]), v))
            for w in sorted(dom[v]):
                child = dict(dom)
                child[v] = {w}
                search(child)
                if stop_after_first and output:
                    return

        search(domains)
        if stop_after_first and output:
            break
    if len(output) != len(set(output)):
        raise ValueError('repeated point maps')
    return output, nodes
