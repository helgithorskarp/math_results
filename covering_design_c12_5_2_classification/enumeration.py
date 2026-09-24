"""Exact dual-incidence enumeration of nine-block (12,5,2) coverings.

Point signatures are subsets of the nine block positions.  The primary
enumeration first constructs the degree-three signatures and then adjoins
the signatures of degrees four and five.  All arithmetic is integral.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial


def digest(value):
    """Hash a deterministic JSON value, independently of pretty printing."""
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def mask(points):
    return sum(1 << p for p in points)


def row_actions(k):
    return [tuple(mask(perm[j] for j in range(k) if m >> j & 1)
                  for m in range(1 << k))
            for perm in permutations(range(k))]


def low_census():
    """All degree-three signature families, up to row and column permutations."""
    states = {(9,)}
    levels = []
    cases = {}
    for k in range(7):
        actions = row_actions(k + 1)
        new = set()
        seen = set()
        for counts in sorted(states):
            occupied = [m for m, n in enumerate(counts) if n]
            used = [sum(max(0, sum(counts[m] for m in occupied
                                   if m >> i & 1 and m >> j & 1) - 1)
                        for j in range(k) if j != i) for i in range(k)]
            selected = [0] * len(counts)

            def extend(i, left):
                if i == len(occupied):
                    if left:
                        return
                    overlap = [sum(selected[m] for m in occupied if m >> j & 1)
                               for j in range(k)]
                    if any(t < 1 or t > 2 or used[j] + t - 1 > 1
                           for j, t in enumerate(overlap)):
                        return
                    if sum(t - 1 for t in overlap) > 1:
                        return
                    out = tuple(counts[m] - selected[m] for m in range(1 << k)) + tuple(selected)
                    if out not in seen:
                        seen.add(out)
                        new.add(min(tuple(out[m] for m in action) for action in actions))
                    return
                m = occupied[i]
                for n in range(min(counts[m], left) + 1):
                    selected[m] = n
                    extend(i + 1, left - n)
                selected[m] = 0

            extend(0, 3)
        states = new
        levels.append(len(states))
        if k >= 2:
            cases[k + 1] = sorted(states)
    return levels, cases


def decode_low(counts, r):
    columns = [m for m, n in enumerate(counts) for _ in range(n)]
    rows = [mask(p for p, c in enumerate(columns) if c >> j & 1) for j in range(r)]
    return rows, columns


def column_actions(columns, r):
    """Every column permutation preserving the unordered low-signature family."""
    groups = {m: tuple(p for p, c in enumerate(columns) if c == m) for m in set(columns)}
    keys = sorted(groups)
    for perm in permutations(range(r)):
        action = {m: mask(perm[j] for j in range(r) if m >> j & 1) for m in keys}
        if any(action[m] not in groups or len(groups[action[m]]) != len(groups[m]) for m in keys):
            continue
        for choices in product(*(permutations(groups[action[m]]) for m in keys)):
            image = [None] * len(columns)
            for m, targets in zip(keys, choices):
                for old, new in zip(groups[m], targets):
                    image[old] = new
            yield tuple(image)


def move(row, action):
    return mask(action[p] for p in range(len(action)) if row >> p & 1)


SUBSETS = {d: tuple(mask(t) for t in combinations(range(9), d)) for d in (4, 5)}


def completions(counts, r):
    """Enumerate all labelled high-signature multisets, then take exact orbits."""
    low, columns = decode_low(counts, r)
    budget = [1 - sum((b & t).bit_count() - 1 for t in low if t != b) for b in low]
    margins = [5 - c.bit_count() for c in columns]
    sizes = [4] * (9 - 2 * (r - 3)) + [5] * (r - 3)
    actions = tuple(column_actions(columns, r))
    mappings = [{b: move(b, action) for b in SUBSETS[4] + SUBSETS[5]} for action in actions]
    candidates = {d: tuple(b for b in SUBSETS[d]
                           if all(1 <= (b & t).bit_count() <= 1 + e for t, e in zip(low, budget)))
                  for d in (4, 5)}
    bits = {b: tuple(p for p in range(9) if b >> p & 1) for b in SUBSETS[4] + SUBSETS[5]}
    extras = {b: tuple((b & t).bit_count() - 1 for t in low) for b in bits}
    labelled = set()
    representatives = set()
    chosen = []
    nodes = 0

    def visit(depth, domains):
        nonlocal nodes
        nodes += 1
        if depth == len(sizes):
            if any(margins):
                return
            labelled.add(tuple(sorted(chosen)))
            representatives.add(min(tuple(sorted(mp[b] for b in chosen)) for mp in mappings))
            return
        remaining = len(sizes) - depth
        if any(n < 0 or n > remaining for n in margins) or any(e < 0 for e in budget):
            return
        d = sizes[depth]
        available = domains[d]
        if not available:
            return
        counts_left = {s: sizes[depth:].count(s) for s in (4, 5)}
        for p, n in enumerate(margins):
            cap = sum(k for s, k in counts_left.items() if any(b >> p & 1 for b in domains[s]))
            forced = sum(k for s, k in counts_left.items()
                         if domains[s] and all(b >> p & 1 for b in domains[s]))
            if n > cap or n < forced:
                return
        for index, b in enumerate(available):
            if any(margins[p] <= 0 for p in bits[b]) or any(e > left for e, left in zip(extras[b], budget)):
                continue
            for p in bits[b]:
                margins[p] -= 1
            for j, e in enumerate(extras[b]):
                budget[j] -= e
            chosen.append(b)
            future = {}
            for s in (4, 5):
                source = available[index:] if s == d else domains[s]
                future[s] = tuple(t for t in source if t & b
                                  and all(margins[p] > 0 for p in bits[t])
                                  and all(e <= left for e, left in zip(extras[t], budget)))
            visit(depth + 1, future)
            chosen.pop()
            for p in bits[b]:
                margins[p] += 1
            for j, e in enumerate(extras[b]):
                budget[j] += e

    visit(0, candidates)
    summary = dict(low=low, labelled=len(labelled), labelled_sha256=digest(sorted(labelled)),
                   nodes=nodes, low_automorphisms=len(actions))
    return sorted(representatives), summary


def check_cover(rows):
    """Direct definition-level check, independent of search pruning."""
    if len(rows) != 12 or any(type(b) is not int or not 0 < b < 512 for b in rows):
        raise ValueError("malformed point signatures")
    if any(not b & t for b, t in combinations(rows, 2)):
        raise ValueError("uncovered pair")
    blocks = [mask(p for p, row in enumerate(rows) if row >> j & 1) for j in range(9)]
    if len(set(blocks)) != 9 or any(b.bit_count() != 5 for b in blocks):
        raise ValueError("blocks must be nine distinct five-subsets")
    return blocks


def design_record(low, high, columns, r):
    rows = list(low) + list(high)
    blocks = check_cover(rows)
    stabilizer = [action for action in column_actions(columns, r)
                  if sorted(move(b, action) for b in rows) == sorted(rows)]
    multiplicities = Counter(rows)
    order = len(stabilizer)
    for n in multiplicities.values():
        order *= factorial(n)
    point_orbits = []
    left = set(range(12))
    while left:
        p = min(left)
        images = {move(rows[p], action) for action in stabilizer}
        orbit = sorted(q for q in range(12) if rows[q] in images)
        left.difference_update(orbit)
        point_orbits.append(orbit)
    return dict(point_signatures=rows, blocks=blocks, automorphism_order=order, point_orbits=point_orbits)


def generate():
    levels, types = low_census()
    cases = []
    designs = []
    for r in range(3, 8):
        for index, counts in enumerate(types[r]):
            reps, summary = completions(counts, r)
            low, columns = decode_low(counts, r)
            cases.append(dict(degree3_points=r, low_type=index, classes=len(reps), **summary))
            for high in reps:
                designs.append(dict(id=len(designs), degree3_points=r, low_type=index,
                                    **design_record(low, high, columns, r)))
    return dict(low_levels=levels, cases=cases, designs=designs)
