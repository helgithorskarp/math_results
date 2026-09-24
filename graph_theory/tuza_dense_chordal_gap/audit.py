#!/usr/bin/env python3
"""Supplementary exact audit; the universal proof is PROOF.md.

No third-party dependencies. Exhausts labeled graphs on <=5 vertices,
checks chordality by two definitions, enumerates feasible zero-edge sets,
and solves triangle packing LPs by rational simplex with primal/dual checks.
Also checks split multiplicity capping and nonvacuous larger explicit
fractional packing/cut families. No asymptotic cutoff is tested or asserted.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import json


def peo(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    left = (1 << n) - 1
    order = []
    while left:
        for v in range(n):
            if not (left >> v & 1):
                continue
            nb = adj[v] & left
            if all((nb ^ (1 << w)) & ~adj[w] == 0
                   for w in range(n) if nb >> w & 1):
                order.append(v)
                left ^= 1 << v
                break
        else:
            return None
    return order


def no_induced_long_cycle(n, edges):
    """Independent recognition, not another elimination implementation."""
    edge_set = set(edges)
    for size in range(4, n + 1):
        for verts in combinations(range(n), size):
            adj = {v: set() for v in verts}
            for u, v in combinations(verts, 2):
                if (u, v) in edge_set:
                    adj[u].add(v)
                    adj[v].add(u)
            if not all(len(adj[v]) == 2 for v in verts):
                continue
            seen = {verts[0]}
            todo = [verts[0]]
            while todo:
                for w in adj[todo.pop()]:
                    if w not in seen:
                        seen.add(w)
                        todo.append(w)
            if len(seen) == size:
                return False
    return True


def triangles(n, edges):
    ids = {e: j for j, e in enumerate(edges)}
    result = []
    for vs in combinations(range(n), 3):
        es = list(combinations(vs, 2))
        if all(e in ids for e in es):
            result.append(sum(1 << ids[e] for e in es))
    return result


def fractional_pair(m, ts):
    """Exact primal simplex; every returned primal/dual pair is rechecked."""
    t = len(ts)
    rows = [[Q(bool(tr >> e & 1)) for tr in ts]
            + [Q(e == j) for j in range(m)] + [Q(1)]
            for e in range(m)]
    obj = [-Q(1)] * t + [Q(0)] * (m + 1)
    basis = list(range(t, t + m))
    pivots = 0
    while any(x < 0 for x in obj[:-1]):
        enter = next(j for j, x in enumerate(obj[:-1]) if x < 0)
        cand = [i for i in range(m) if rows[i][enter] > 0]
        assert cand, 'bounded edge-capacity packing LP became unbounded'
        leave = min(cand, key=lambda i: (rows[i][-1] / rows[i][enter], basis[i]))
        pivot = rows[leave][enter]
        rows[leave] = [x / pivot for x in rows[leave]]
        for i in range(m):
            if i != leave and rows[i][enter]:
                a = rows[i][enter]
                rows[i] = [x - a * y for x, y in zip(rows[i], rows[leave])]
        a = obj[enter]
        obj = [x - a * y for x, y in zip(obj, rows[leave])]
        basis[leave] = enter
        pivots += 1
        assert pivots < 10000
    primal = [Q(0)] * t
    for i, b in enumerate(basis):
        if b < t:
            primal[b] = rows[i][-1]
    dual = obj[t:t + m]
    loads = [sum(primal[j] for j, tr in enumerate(ts) if tr >> e & 1)
             for e in range(m)]
    assert all(x >= 0 for x in primal)
    assert all(x <= 1 for x in loads)
    assert all(0 <= x <= 1 for x in dual)
    assert all(sum(dual[e] for e in range(m) if tr >> e & 1) >= 1 for tr in ts)
    assert sum(primal) == sum(dual) == obj[-1]
    assert all(loads[e] == 1 for e in range(m) if dual[e] > 0)
    return obj[-1], dual


def integer_packing(m, ts):
    @lru_cache(None)
    def solve(avail):
        return max([0] + [1 + solve(avail ^ tr) for tr in ts if avail & tr == tr])
    return solve((1 << m) - 1)


def small_graphs():
    counts = []
    zero_sets = lp_cases = positive_unit = 0
    for n in range(6):
        complete = list(combinations(range(n), 2))
        chordal_count = 0
        for mask in range(1 << len(complete)):
            es = [e for j, e in enumerate(complete) if mask >> j & 1]
            order = peo(n, es)
            assert (order is not None) == no_induced_long_cycle(n, es)
            if order is None:
                continue
            chordal_count += 1
            m = len(es)
            ts = triangles(n, es)
            rank = {v: i for i, v in enumerate(order)}
            max_tf = 0
            for zmask in range(1 << m):
                if any(zmask & tr == tr for tr in ts):
                    continue
                zero_sets += 1
                max_tf = max(max_tf, zmask.bit_count())
                forced = 0
                for tr in ts:
                    if (tr & zmask).bit_count() == 2:
                        forced |= tr & ~zmask
                # Explicit feasible cover: 0 on Z, 1 on forced edges,
                # and 1/2 elsewhere. Store twice each weight as an integer.
                twice = [0 if zmask >> e & 1 else 2 if forced >> e & 1 else 1
                         for e in range(m)]
                assert all(sum(twice[e] for e in range(m) if tr >> e & 1) >= 2
                           for tr in ts)
                ds = [0] * n
                for e, (u, v) in enumerate(es):
                    if zmask >> e & 1:
                        ds[u if rank[u] < rank[v] else v] += 1
                h = forced.bit_count()
                assert all(d * (d - 1) // 2 <= h for d in ds)
                z = zmask.bit_count()
                assert sum(ds) == z
                if z > n:
                    assert (z - n) ** 2 <= 2 * h * n * n
            tau = m - max_tf  # Exhaustive triangle-free surviving subgraphs.
            frac, f = fractional_pair(m, ts)
            nu = integer_packing(m, ts)
            assert nu <= frac <= tau
            h = sum(x == 1 for x in f)
            z = sum(x == 0 for x in f)
            positive_unit += h > 0
            gap = 2 * frac - tau
            assert gap >= h
            assert gap >= Q(m, 6) - Q(2 * z, 3)
            if n:
                assert gap >= Q(m * m, 50 * n * n) - Q(2 * n, 3)
            lp_cases += 1
        counts.append(chordal_count)
    assert counts == [1, 1, 2, 8, 61, 822]
    # Negative controls: nonchordal C4 and K3,3 must be rejected. The latter
    # has a feasible all-zero cover but z=9>n=6 at h=0, so omitting the
    # chordal hypothesis would break the key bound. Three zero edges on a
    # triangle are infeasible.
    assert peo(4, [(0, 1), (0, 3), (1, 2), (2, 3)]) is None
    k33 = [(u, v) for u in range(3) for v in range(3, 6)]
    assert peo(6, k33) is None and not triangles(6, k33)
    assert len(k33) > 6
    assert any(7 & tr == tr for tr in triangles(3, [(0, 1), (0, 2), (1, 2)]))
    return dict(chordal_graph_counts=counts, exact_lp_pairs=lp_cases,
                feasible_zero_sets=zero_sets, lp_pairs_with_unit_edges=positive_unit,
                negative_controls=3)


@lru_cache(None)
def clique_cores(k):
    es = list(combinations(range(k), 2))
    ts = triangles(k, es)
    cores = []
    for mask in range(1 << len(es)):
        if any(mask & tr == tr for tr in ts):
            continue
        alpha = []
        for s in range(1 << k):
            best = 0
            a = s
            while True:
                if not any(mask >> j & 1 and a >> u & 1 and a >> v & 1
                           for j, (u, v) in enumerate(es)):
                    best = max(best, a.bit_count())
                if not a:
                    break
                a = (a - 1) & s
            alpha.append(best)
        cores.append((mask.bit_count(), alpha))
    return cores


def split_tau(k, centers):
    q = k * (k - 1) // 2
    E = sum(s.bit_count() for s in centers)
    return q + E - max(e + sum(alpha[s] for s in centers)
                       for e, alpha in clique_cores(k))


def direct_cover(n, es):
    ts = triangles(n, es)
    for size in range(len(es) + 1):
        for chosen in combinations(range(len(es)), size):
            mask = sum(1 << e for e in chosen)
            if all(mask & tr for tr in ts):
                return size
    raise AssertionError('all edges must cover')


def cap_audit():
    cases = changed = independent_checks = 0
    for k in range(2, 5):
        active = [s for s in range(1 << k) if s.bit_count() >= 2]
        for p in range(5):
            for centers in combinations_with_replacement(active, p):
                counts = Counter(centers)
                capped = tuple(s for s, m in sorted(counts.items())
                               for _ in range(min(m, s.bit_count() - 1)))
                tau = split_tau(k, centers)
                assert tau == split_tau(k, capped)
                r = len(counts)
                E = sum(s.bit_count() for s in capped)
                assert len(capped) ** 2 <= r * E
                changed += len(capped) < p
                if k + p <= 6:
                    es = list(combinations(range(k), 2))
                    es += [(v, k + i) for i, s in enumerate(centers)
                           for v in range(k) if s >> v & 1]
                    assert tau == direct_cover(k + p, es)
                    independent_checks += 1
                cases += 1
    return dict(split_cap_cases=cases, cap_changed_cases=changed,
                direct_edge_cover_crosschecks=independent_checks)


def larger_families():
    """Explicit optimal fractional packings and valid cuts, no solver.

    Complete split graph K_k joined to p independent vertices. For
    p<=k-1, every centered triangle has weight 1/(k-1); remaining clique
    capacity is packed uniformly. For p>=k-1 use weight 1/p on centered
    triangles. Duals are respectively all-1/3 and clique-1/spoke-0.
    """
    cases = nonvacuous_chordal = nonvacuous_type = 0
    for k in range(3, 161):
        q = k * (k - 1) // 2
        for p in sorted({0, 1, k // 4, k // 2, k - 1, k, 2 * k}):
            frac = min(Q(q), Q(q + p * k, 3))
            U = min(q - a * (k - a) + p * min(a, k - a)
                    for a in range(k + 1))
            n, m = k + p, q + k * p
            bound = Q(m * m, 50 * n * n) - Q(2 * n, 3)
            assert 2 * frac - U >= bound
            typ = Q(k * k - 2 * k - 64, 152)  # r=1
            assert 2 * frac - U >= typ
            nonvacuous_chordal += bound > 0
            nonvacuous_type += typ > 0
            cases += 1
    # Exact scalar parts of the rounding budget at the asserted r=3 values.
    assert Q(1, 64 * 35 * 16) == Q(1, 35840)
    assert 26 * 26 < 8 * 26 + 128 * 4
    assert 27 * 27 >= 8 * 27 + 128 * 4
    assert Q(3, 32 * 35) - Q(1, 32 * 35) == Q(1, 560)
    return dict(explicit_fractional_packing_cut_cases=cases,
                positive_chordal_bounds=nonvacuous_chordal,
                positive_one_type_bounds=nonvacuous_type)


def main():
    out = dict(status='PASS', arithmetic='exact Python int and Fraction',
               scope='supplementary finite audit; universal proof is PROOF.md',
               asymptotic_cutoff_computed=False)
    out.update(small_graphs())
    out.update(cap_audit())
    out.update(larger_families())
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
