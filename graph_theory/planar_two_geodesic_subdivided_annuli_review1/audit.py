#!/usr/bin/env python3
"""Independent exact checks for the subdivided-annulus separator proof.

Uses only Python's standard library.  It does not import the target checker.
The finite calculations audit proof branches; the written inequalities
remain the justification for arbitrary order, lengths, and real masses.
"""

from collections import defaultdict
from fractions import Fraction
from heapq import heappop, heappush
from random import Random


def edge(g, u, v, length):
    assert length > 0 and v not in g[u]
    g[u][v] = length
    g[v][u] = length


def shortest(g, source, target):
    heap = [(0, source)]
    distance = {source: 0}
    parent = {}
    while heap:
        length, u = heappop(heap)
        if length != distance[u]:
            continue
        if u == target:
            path = [u]
            while u != source:
                u = parent[u]
                path.append(u)
            return length, tuple(reversed(path))
        for v, cost in g[u].items():
            trial = length + cost
            if trial < distance.get(v, float("inf")):
                distance[v] = trial
                parent[v] = u
                heappush(heap, (trial, v))
    raise AssertionError("disconnected")


def geodesic(g, path):
    assert len(path) == len(set(path)), path
    length = sum(g[u][v] for u, v in zip(path, path[1:]))
    assert length == shortest(g, path[0], path[-1])[0], path


def components(g, removed):
    unseen = set(g) - set(removed)
    answer = []
    while unseen:
        todo = [unseen.pop()]
        piece = set(todo)
        while todo:
            for v in g[todo.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    todo.append(v)
                    piece.add(v)
        answer.append(piece)
    return answer


def make_annulus(k, rng):
    g = defaultdict(dict)
    r = "r"
    a = [f"a{i}" for i in range(k)]
    c = [f"c{i}" for i in range(k)]
    lam = 4
    for i in range(k):
        edge(g, r, a[i], lam)
        edge(g, a[i], a[(i + 1) % k], lam)
        edge(g, a[i], c[i], lam)
        edge(g, a[i], c[(i + 1) % k], lam)
    arcs = []
    for i in range(k):
        length = rng.choice([0, 1, 2, 3])
        chain = [c[i]] + [f"t{i}_{j}" for j in range(length)] + [c[(i + 1) % k]]
        costs = [lam] if length == 0 else [rng.randint(1, 5) for _ in range(length + 1)]
        if length:
            costs[-1] += max(0, 2 * lam - sum(costs))
        for u, v, cost in zip(chain, chain[1:], costs):
            edge(g, u, v, cost)
        arcs.append(tuple(chain))
    core = set(g)
    # One component of each permitted boundary type in every sector.
    outside = []
    for i in range(k):
        for name, boundary in ((f"single{i}", (r, a[i])),
                               (f"sector{i}", (r, a[i], a[(i + 1) % k])),
                               (f"pair{i}", (a[i], a[(i + 1) % k]))):
            for v in boundary:
                edge(g, name, v, lam)
            outside.append({name})
    edge(g, "root_only", r, lam)
    outside.append({"root_only"})
    for u in core:
        for v in core:
            assert shortest(g, u, v)[0] == shortest({x: {y: z for y, z in g[x].items() if y in core}
                                                        for x in core}, u, v)[0]
    return g, r, a, c, arcs, core, outside


def cover_three_portal(g, left, right):
    assert left[-1] == right[-1]
    assert all(len(g[v]) == 2 for v in left[1:-1] + right[1:-1])
    u, m, v = left[0], left[-1], right[0]
    A = [0]
    B = [0]
    for chain, coords in ((left, A), (right, B)):
        for x, y in zip(chain, chain[1:]):
            coords.append(coords[-1] + g[x][y])
    p, q, s = (shortest(g, x, y)[0] for x, y in ((u, m), (m, v), (u, v)))
    z = Fraction(2 * A[-1] - p + q - s, 4)
    t = Fraction(2 * B[-1] + p - q - s, 4)
    assert 0 <= z <= A[-1] and 0 <= t <= B[-1]
    x = max(i for i, d in enumerate(A) if d <= z)
    xx = min(i for i, d in enumerate(A) if d >= z)
    y = max(i for i, d in enumerate(B) if d <= t)
    yy = min(i for i, d in enumerate(B) if d >= t)
    bridge = shortest(g, u, v)[1]
    outer = tuple(reversed(left[:x + 1])) + bridge[1:] + right[1:y + 1]
    inner = left[xx:] + tuple(reversed(right[yy:]))[1:]
    geodesic(g, outer)
    geodesic(g, inner)
    assert set(left + right) <= set(outer + inner)
    return (outer, inner)


def system(g, r, a, c, original, core, outside, shift, direction):
    k = len(a)
    A = [a[(shift + direction * i) % k] for i in range(k)]
    C = [c[(shift + i) % k] if direction == 1 else c[(shift + 1 - i) % k]
         for i in range(k)]
    arcs = [original[(shift + i) % k] if direction == 1 else
            tuple(reversed(original[(shift - i) % k])) for i in range(k)]
    assert all(arcs[i][0] == C[i] and arcs[i][-1] == C[(i + 1) % k]
               for i in range(k))
    P = (r, A[0], C[0])
    alpha = [set() for _ in range(k)]
    gamma = [set() for _ in range(k)]
    tau = [set(path[1:-1]) for path in arcs]
    kappa = [set() for _ in range(k)]
    discarded = set()
    for i in range(1, k):
        alpha[i].add(A[i])
        gamma[i].add(C[i])
    for K in outside:
        boundary = set().union(*(set(g[v]) for v in K)) & core
        active = boundary & set(A)
        if not active or active == {A[0]}:
            discarded |= K
        elif len(active) == 1:
            alpha[A.index(next(iter(active)))] |= K
        else:
            i = next(i for i in range(k) if active == {A[i], A[(i + 1) % k]})
            kappa[i] |= K
    represented = set(g) - set(P) - discarded
    groups = alpha + gamma + tau + kappa
    assert set().union(*groups) == represented
    assert sum(map(len, groups)) == len(represented)

    def bounds(i):
        left = set().union(*(alpha[j] | gamma[j] | tau[j] | kappa[j] for j in range(i)))
        right = represented - left - (alpha[i] | gamma[i] if i < k else set())
        return left, right

    def candidate(path, sides):
        geodesic(g, path)
        parts = components(g, set(P) | set(path))
        for K in parts:
            if K & core:
                assert any(K <= side for side in sides), (P, path, K)
            else:
                assert K in outside
        return (path, sides, parts)

    sequence, options, patches, covers = [], [], [], []
    for i in range(k):
        L, R = bounds(i)
        LV = L | gamma[i] | tau[i]
        RV = R - gamma[(i + 1) % k] - tau[i]
        sequence.append(candidate((r, A[i], C[i]), (L, R)))
        sequence.append(candidate((r, A[i], C[(i + 1) % k]), (LV, RV)))
        arc = arcs[i]
        total = sum(g[u][v] for u, v in zip(arc, arc[1:]))
        coords = [0]
        for u, v in zip(arc, arc[1:]):
            coords.append(coords[-1] + g[u][v])
        lo = max(j for j, d in enumerate(coords) if 2 * d <= total)
        hi = min(j for j, d in enumerate(coords) if 2 * d >= total)
        removed_left = set(arc[1:lo + 1])
        removed_right = set(arc[hi:-1])
        mu = candidate((r, A[i]) + arc[:lo + 1], (L, R - removed_left))
        mv = candidate((r, A[i]) + tuple(reversed(arc[hi:])),
                       (L | gamma[i] | (tau[i] - removed_right), RV))
        assert not (mu[1][1] & mv[1][0])
        options.append((mu, mv))
        LN, RN = bounds(i + 1)
        patch = tau[i] | {C[(i + 1) % k]} | tau[(i + 1) % k]
        patches.append(patch)
        covers.append(cover_three_portal(g, arcs[i], tuple(reversed(arcs[(i + 1) % k]))))
        if tau[i] or tau[(i + 1) % k]:
            Q = (C[i], A[i], A[(i + 1) % k], C[(i + 2) % k])
            options.append((candidate(Q, (LV, RN, patch)),))
        else:
            plus = (A[i], A[(i + 1) % k], C[(i + 2) % k])
            minus = (A[(i + 1) % k], A[i], C[i])
            options.append((candidate(plus, (LV | gamma[(i + 1) % k], RN)),
                            candidate(minus, (LV, RN | gamma[(i + 1) % k]))))
    sequence.append(candidate(P, bounds(k)))
    return sequence, options, patches, covers, represented


def check_masses(g, sequence, options, patches, covers, outside, rng):
    profiles = [[rng.randrange(6) for _ in g] for _ in range(40)]
    profiles += [[int(v in patch) for v in g] for patch in patches]
    profiles += [[int(v in K) for v in g] for K in outside]
    profiles += [[int(v in {f"sector{i}", f"pair{i}"}) for v in g]
                 for i in range(len(patches))]
    vertices = tuple(g)
    counts = [0, 0, 0, 0, 0]
    for profile in profiles:
        w = dict(zip(vertices, profile))
        W = sum(profile)
        mass = lambda S: sum(w[v] for v in S)
        if any(2 * mass(K) > W for K in outside):
            continue  # The separate width-three centroid case.
        heavy = next((i for i, patch in enumerate(patches) if 2 * mass(patch) > W), None)
        if heavy is not None:
            removed = set(covers[heavy][0]) | set(covers[heavy][1])
            assert all(2 * mass(K) <= W for K in components(g, removed))
            counts[0] += 1
            continue
        balanced = lambda item: all(2 * mass(S) <= W for S in item[1])
        chosen = next((item for item in sequence if balanced(item)), None)
        if chosen is None:
            crossings = [j for j in range(len(sequence) - 1)
                         if 2 * mass(sequence[j][1][1]) > W
                         and 2 * mass(sequence[j + 1][1][0]) > W]
            assert crossings
            chosen = next((item for item in options[crossings[0]] if balanced(item)), None)
            assert chosen is not None
            if crossings[0] % 2 == 0:
                counts[1] += 1  # midpoint transition
            elif len(options[crossings[0]]) == 1:
                counts[2] += 1  # subdivided sector detour
            else:
                counts[3] += 1  # unsubdivided sector exchange
        else:
            counts[4] += 1
        assert all(2 * mass(K) <= W for K in chosen[2])
    return counts


def main():
    rng = Random(20260928)
    counts = [0, 0, 0, 0, 0]
    # Independent general three-terminal metric models, beyond annuli.
    for trial in range(500):
        model = defaultdict(dict)
        for u, v in (("u", "m"), ("m", "v"), ("u", "v")):
            edge(model, u, v, rng.randint(1, 30))
        ears = []
        for start in ("u", "v"):
            chain = [start] + [f"{trial}_{start}_{j}" for j in range(rng.randint(1, 5))] + ["m"]
            for u, v in zip(chain, chain[1:]):
                edge(model, u, v, rng.randint(1, 20))
            ears.append(tuple(chain))
        cover_three_portal(model, *ears)
    systems = covers = 0
    for k in range(5, 10):
        for trial in range(6):
            g, r, a, c, arcs, core, outside = make_annulus(k, rng)
            for shift in range(k):
                for direction in (-1, 1):
                    seq, opts, patches, paths, represented = system(
                        g, r, a, c, arcs, core, outside, shift, direction)
                    subtotal = check_masses(g, seq, opts, patches, paths, outside, rng)
                    counts = [x + y for x, y in zip(counts, subtotal)]
                    systems += 1
                    covers += len(paths)
    assert all(counts)
    print(f"metric_models=500 systems={systems} three_portal_covers={covers} "
          f"heavy_patch={counts[0]} midpoint={counts[1]} "
          f"subdivided_sector={counts[2]} unsubdivided_sector={counts[3]} "
          f"spokes={counts[4]} PASS")


if __name__ == "__main__":
    main()
