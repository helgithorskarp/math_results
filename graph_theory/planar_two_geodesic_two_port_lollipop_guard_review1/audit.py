#!/usr/bin/env python3
"""Independent finite audit of the two-port transfer and weighted guard.

Uses only Python's standard library and imports no target code.  The proof of
arbitrary order, all edge deletions, and real masses remains the written proof.
"""

from collections import deque
from random import Random


def add(g, u, v):
    g.setdefault(u, set()).add(v)
    g.setdefault(v, set()).add(u)


def family(r, m=11):
    g = {u: set() for u in range(6 + r * (m + 1))}
    for u, v in ((0, 1), (1, 2), (2, 3), (3, 0)):
        add(g, u, v)
    for pole in (4, 5):
        for equator in range(4):
            add(g, pole, equator)
    gadgets = []
    for j in range(r):
        C = tuple(6 + j * (m + 1) + i for i in range(m + 1))
        for i in range(m):
            add(g, C[i], C[(i + 1) % m])
        add(g, C[0], C[m])
        add(g, C[1], 0)
        add(g, C[3], 1)
        gadgets.append(C)
    assert len(g) == 6 + r * (m + 1)
    assert sum(map(len, g.values())) // 2 == 12 + r * (m + 3)
    return g, gadgets


def distance_path(g, source, target, allowed=None):
    if allowed is not None and (source not in allowed or target not in allowed):
        return None
    parent = {source: None}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        if u == target:
            path = [u]
            while parent[u] is not None:
                u = parent[u]
                path.append(u)
            return tuple(reversed(path))
        for v in g[u]:
            if v not in parent and (allowed is None or v in allowed):
                parent[v] = u
                queue.append(v)
    return None


def components(g, allowed):
    unseen = set(allowed)
    answer = []
    while unseen:
        first = unseen.pop()
        todo = [first]
        piece = {first}
        while todo:
            for v in g[todo.pop()] & unseen:
                unseen.remove(v)
                todo.append(v)
                piece.add(v)
        answer.append(piece)
    return answer


def model(g, C):
    Cset = set(C)
    a, b = C[1], C[3]
    allowed = set(g) - Cset | {a, b}
    outside = distance_path(g, a, b, allowed)
    J = {u: g[u] & Cset for u in C}
    if outside is not None:
        ear = (a,) + tuple(-i for i in range(1, len(outside) - 1)) + (b,)
        assert len(ear) == len(outside)
        for u, v in zip(ear, ear[1:]):
            add(J, u, v)
    for u in C:
        for v in C:
            host = distance_path(g, u, v)
            reduced = distance_path(J, u, v)
            assert (None if host is None else len(host)) == (None if reduced is None else len(reduced))
    return J, outside


def anchored_geodesics(J, C):
    Cset = set(C)
    paths = {}
    for source in C:
        distances = {source: 0}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in J[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        stack = [(source, (source,), {source})]
        while stack:
            u, path, seen = stack.pop()
            if u in Cset and len(path) - 1 == distances[u]:
                paths.setdefault(frozenset(seen & Cset), path)
            for v in J[u] - seen:
                stack.append((v, path + (v,), seen | {v}))
    return tuple(paths.values())


def lift(path, C, outside):
    if outside is None:
        assert all(v in C for v in path)
        return path
    a, b = C[1], C[3]
    out = [path[0]]
    i = 0
    while i < len(path) - 1:
        if path[i + 1] < 0:
            j = i + 1
            while path[j] < 0:
                j += 1
            segment = outside if path[i] == a else tuple(reversed(outside))
            assert segment[0] == path[i] and segment[-1] == path[j]
            out.extend(segment[1:])
            i = j
        else:
            out.append(path[i + 1])
            i += 1
    return tuple(out)


def anchored_covers(g, C):
    J, outside = model(g, C)
    paths = anchored_geodesics(J, C)
    covers = {}
    for D in components(g, C):
        pair = next(((p, q) for p in paths for q in paths
                     if D <= set(p) | set(q)), None)
        assert pair is not None, D
        pair = tuple(lift(path, C, outside) for path in pair)
        for path in pair:
            assert len(path) == len(set(path))
            assert all(v in g[u] for u, v in zip(path, path[1:]))
            assert len(path) == len(distance_path(g, path[0], path[-1]))
        assert D <= set(pair[0]) | set(pair[1])
        covers[frozenset(D)] = pair
    return covers, outside


def guard(g, gadgets, cached, w):
    W = sum(w.values())
    mass = lambda D: sum(w[v] for v in D)

    def heavy(removed):
        return [D for D in components(g, set(g) - removed) if 2 * mass(D) > W]

    first = heavy(set())
    assert len(first) <= 1
    if not first:
        return "initial"
    core = sorted(set(range(4)) & first[0])
    initial = []
    for i in range(0, len(core), 2):
        if i + 1 < len(core):
            initial.append(distance_path(g, core[i], core[i + 1]))
        else:
            initial.append((core[i],))
    assert all(path is not None for path in initial)
    removed = set().union(*(set(path) for path in initial)) if initial else set()
    second = heavy(removed)
    assert len(second) <= 1
    if not second:
        return "core"
    D = second[0]
    if len(D) == 1 and D <= {4, 5}:
        pair = (tuple(D),)
    else:
        j = next(j for j, C in enumerate(gadgets) if D <= set(C))
        pair = next(paths for fragment, paths in cached[j].items() if D <= fragment)
    assert len(pair) <= 2 and D <= set().union(*(set(path) for path in pair))
    removed = set().union(*(set(path) for path in pair))
    assert not heavy(removed)
    return "replacement"


def sample_subgraphs(g, gadgets, trials=120):
    rng = Random(2026092821)
    edges = [(u, v) for u in g for v in g[u] if u < v]
    reductions = covers = no_route = longer_route = 0
    decisions = {"initial": 0, "core": 0, "replacement": 0}
    for trial in range(trials):
        H = {u: set() for u in g}
        retain = 0.4 + (trial % 12) / 20
        for u, v in edges:
            if rng.random() < retain:
                add(H, u, v)
        cache = []
        for C in gadgets:
            pair, outside = anchored_covers(H, C)
            assert outside is None or len(outside) - 1 >= 3
            no_route += outside is None
            longer_route += outside is not None and len(outside) - 1 > 3
            cache.append(pair)
            reductions += 1
            covers += len(pair)
        profiles = [{u: rng.randrange(6) for u in H} for _ in range(6)]
        profiles += [{u: int(u in C) for u in H} for C in gadgets]
        for w in profiles:
            decisions[guard(H, gadgets, cache, w)] += 1
    return reductions, covers, no_route, longer_route, decisions


def main():
    for r in (1, 5, 8):
        g, gadgets = family(r)
        for C in gadgets:
            J, outside = model(g, C)
            assert outside is not None and len(outside) - 1 == 3
            induced = {u: g[u] & set(C) for u in C}
            for u in C:
                for v in C:
                    assert len(distance_path(g, u, v)) == len(distance_path(induced, u, v))
        print(f"family r={r} vertices={len(g)} edges={sum(map(len, g.values())) // 2} ports=3 isometric=yes")
    g, gadgets = family(2)
    reductions, covers, no_route, longer_route, decisions = sample_subgraphs(g, gadgets)
    print(f"sampled_subgraphs=120 distance_reductions={reductions} anchored_covers={covers} "
          f"no_exterior_route={no_route} longer_exterior_route={longer_route} "
          f"weighted_profiles={sum(decisions.values())} "
          f"guard_initial={decisions['initial']} guard_core={decisions['core']} "
          f"guard_replacement={decisions['replacement']} PASS")
    assert decisions["replacement"]


if __name__ == "__main__":
    main()
