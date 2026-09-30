#!/usr/bin/env python3
"""Complete nine-edge carrier, streamed per C/core; no exclusion."""
from itertools import combinations
import time


def normalize(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def low_matchings(low, size, triple_of):
    if size == 0:
        yield ()
        return
    if len(low) < 2 * size:
        return
    u, tail = low[0], low[1:]
    yield from low_matchings(tail, size, triple_of)
    for i, v in enumerate(tail):
        if triple_of[u] == triple_of[v]:
            continue
        rest = tail[:i] + tail[i + 1:]
        for matching in low_matchings(rest, size - 1, triple_of):
            yield ((u, v),) + matching


def cores(c, p, triple_of):
    possible = [e for e in combinations(c, 2)
                if not (e[0] in triple_of and e[1] in triple_of
                        and triple_of[e[0]] == triple_of[e[1]])]
    for e in range(p, 4):
        for core in combinations(possible, e):
            yield tuple(core)


def carrier(triples, c):
    """Core, then low matching, then capacity-constrained attachments."""
    c = tuple(sorted(c))
    triple_of = {z: i for i, t in enumerate(triples) for z in t}
    low = tuple(sorted(set(triple_of) - set(c)))
    p = len(set(c) & set(triple_of))
    degrees = {z: 4 if z in triple_of else 3 for z in c}
    result = []
    records = []
    for core in cores(c, p, triple_of):
        started = time.monotonic()
        remaining = {z: degrees[z] - sum(z in e for e in core) for z in c}
        nodes = 0
        answers = []
        for matching in low_matchings(low, len(core) - p, triple_of):
            matched = set().union(*(set(e) for e in matching)) if matching else set()
            unpaired = tuple(z for z in low if z not in matched)
            if len(unpaired) != sum(remaining.values()):
                raise RuntimeError('degree/core/matching balance failure')
            eligible_a = [z for z in unpaired if not (c[0] in triple_of and triple_of[c[0]] == triple_of[z])]
            for first in combinations(eligible_a, remaining[c[0]]):
                pool = tuple(z for z in unpaired if z not in first)
                eligible_b = [z for z in pool if not (c[1] in triple_of and triple_of[c[1]] == triple_of[z])]
                for second in combinations(eligible_b, remaining[c[1]]):
                    nodes += 1
                    if nodes > 200000 or time.monotonic() - started > 10:
                        raise RuntimeError('INCOMPLETE carrier core node/time guard')
                    third = tuple(z for z in pool if z not in second)
                    if len(third) != remaining[c[2]] or any(
                            c[2] in triple_of and triple_of[c[2]] == triple_of[z] for z in third):
                        continue
                    edges = normalize(core + matching + tuple((c[0], z) for z in first)
                                      + tuple((c[1], z) for z in second) + tuple((c[2], z) for z in third))
                    answers.append(edges)
        if len(set(answers)) != len(answers):
            raise RuntimeError('carrier duplicate')
        result.extend(answers)
        records.append(dict(core=core, e=len(core), m=len(core) - p, nodes=nodes,
                            leaves=len(answers), seconds=round(time.monotonic() - started, 6)))
    if len(set(result)) != len(result):
        raise RuntimeError('carrier duplicate across distinct cores')
    return sorted(result), records


def carrier_independent(triples, c):
    """Core, then high neighborhoods, then a perfect matching of leftover lows."""
    c = tuple(sorted(c))
    triple_of = {z: i for i, t in enumerate(triples) for z in t}
    low = tuple(sorted(set(triple_of) - set(c)))
    p = len(set(c) & set(triple_of))
    degrees = {z: 4 if z in triple_of else 3 for z in c}
    all_core_pairs = list(combinations(c, 2))
    result = []
    records = []
    # Independent bit selections retain every C-core and reject degrees later.
    for bits in range(8):
        core = tuple(e for i, e in enumerate(all_core_pairs) if bits >> i & 1)
        if any(a in triple_of and b in triple_of and triple_of[a] == triple_of[b] for a, b in core):
            continue
        remaining = [degrees[z] - sum(z in e for e in core) for z in c]
        if any(k < 0 for k in remaining) or sum(remaining) > len(low):
            continue
        nodes = 0
        answers = []
        started = time.monotonic()

        def match_tail(pool, edges):
            nonlocal nodes
            nodes += 1
            if nodes > 200000 or time.monotonic() - started > 10:
                raise RuntimeError('INCOMPLETE independent carrier core guard')
            if not pool:
                answers.append(normalize(core + edges))
                return
            u = min(pool)
            for v in sorted(pool - {u}):
                if triple_of[u] != triple_of[v]:
                    match_tail(pool - {u, v}, edges + ((u, v),))

        def attach(j, pool, edges):
            nonlocal nodes
            nodes += 1
            if nodes > 200000 or time.monotonic() - started > 10:
                raise RuntimeError('INCOMPLETE independent carrier core guard')
            if j == 3:
                if len(pool) % 2 == 0:
                    match_tail(pool, edges)
                return
            eligible = sorted(z for z in pool if c[j] not in triple_of or triple_of[c[j]] != triple_of[z])
            for chosen in combinations(eligible, remaining[j]):
                attach(j + 1, pool - set(chosen), edges + tuple((c[j], z) for z in chosen))

        attach(0, set(low), ())
        if len(set(answers)) != len(answers):
            raise RuntimeError('independent carrier duplicate')
        result.extend(answers)
        records.append(dict(core=core, nodes=nodes, leaves=len(answers),
                            seconds=round(time.monotonic() - started, 6)))
    if len(set(result)) != len(result):
        raise RuntimeError('independent carrier duplicate across cores')
    return sorted(result), records


def validate_h(triples, c, h):
    vertices = range(1, 17)
    t = set().union(*(set(q) for q in triples))
    forbidden = set().union(*(set(combinations(sorted(q), 2)) for q in triples))
    if len(h) != 9 or len(set(h)) != 9 or set(h) & forbidden:
        raise RuntimeError('bad nine-edge leave')
    actual = {z: sum(z in e for e in h) for z in vertices}
    expected = {z: (4 if z in t else 3) if z in c else (1 if z in t else 0) for z in vertices}
    if actual != expected:
        raise RuntimeError('bad nine-edge degree profile')
