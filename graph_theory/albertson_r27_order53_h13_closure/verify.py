#!/usr/bin/env python3
"""Exact audit for the Albertson r=27 order-53 h=13 closure."""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb


K = 27
N = 53
M = 713
H = 13
LOW = N - H
EXCESS = 2 * M - (K - 1) * N

EXPECTED_ROWS = (
    (15, 25, 1, 11, 0),
    (16, 24, 2, 10, 9),
    (17, 23, 3, 9, 16),
    (18, 22, 4, 8, 21),
    (19, 21, 5, 7, 24),
    (20, 20, 6, 6, 25),
)


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def is_forest(order, edges):
    parent = list(range(order))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        ru, rv = root(u), root(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def large_block_audit():
    """Enumerate all large-clique covers allowed at the h=13 boundary."""
    outcomes = set()
    labelled = 0
    # Every block has at least 14 vertices.  A shared vertex belongs to two
    # K14 blocks and represents an edge of the large-block intersection
    # forest.  Four blocks have union at least 4*14-3=53>40.
    for count in range(1, 5):
        for sizes in combinations_with_replacement(range(14, 27), count):
            pairs = tuple(combinations(range(count), 2))
            for mask in range(1 << len(pairs)):
                overlaps = tuple(pairs[j] for j in range(len(pairs)) if mask >> j & 1)
                if not is_forest(count, overlaps):
                    continue
                if any(sizes[u] != 14 or sizes[v] != 14 for u, v in overlaps):
                    continue
                if sum(sizes) - len(overlaps) != LOW:
                    continue
                labelled += 1
                degree_sequence = tuple(
                    sorted(sum(v in pair for pair in overlaps) for v in range(count))
                )
                outcomes.add((sizes, len(overlaps), degree_sequence))

    expected = {
        ((a, LOW - a), 0, (0, 0)) for a in range(14, 21)
    } | {((14, 14, 14), 2, (1, 1, 2))}
    assert outcomes == expected
    assert labelled == 10  # seven two-block rows and three labelled K14 paths

    # Three K14 blocks in a path have distinct cut vertices.  There are no
    # further low edges, so the low degree sum alone forces too many edges.
    e_low = 3 * comb(14, 2)
    e_low_high = (K - 1) * LOW - 2 * e_low
    assert (e_low, e_low_high, e_low + e_low_high) == (273, 494, 767)
    assert e_low + e_low_high > M
    return labelled, outcomes


def profiles():
    """Reconstruct (a,b,d,e,D=t+r) from the exact edge identity."""
    rows = []
    variants = []
    for a in range(14, LOW // 2 + 1):
        b = LOW - a
        d = a + H - K
        e = b + H - K
        base_low_edges = comb(a, 2) + comb(b, 2)
        # With no bridge, the low degree sum determines e(G[Q]); D is the
        # number of missing high edges.  A bridge trades one missing high
        # edge for one additional low edge, hence D=t+r.
        e_high = M - ((K - 1) * LOW - base_low_edges)
        D = comb(H, 2) - e_high
        if D < 0:
            continue
        assert d + e == H - 1
        rows.append((a, b, d, e, D))
        for bridge in (0, 1):
            r = D - bridge
            if r >= 0:
                variants.append((a, b, d, e, bridge, r))
    assert tuple(rows) == EXPECTED_ROWS
    assert len(variants) == 11
    assert 2 * M - (K - 1) * N == EXCESS == 48
    return tuple(rows), tuple(variants)


def contracted_signature(row, pair):
    """High colour classes compatible with one fixed-size complement row."""
    u, v = pair
    singles = tuple(i for i in range(H) if i not in pair and row >> i & 1)
    paired = bool(row >> u & 1) and bool(row >> v & 1)
    return singles, paired


def contraction_rigidity_audit():
    """Two distinct failed contractions force equal original rows."""
    checked = 0
    vertices = range(H)
    pairs = tuple(combinations(vertices, 2))
    for first in pairs:
        outside = [v for v in vertices if v not in first]
        for outside_mask in range(1 << len(outside)):
            base = sum(
                1 << v for j, v in enumerate(outside) if outside_mask >> j & 1
            )
            row1 = base | (1 << first[0])
            row2 = base | (1 << first[1])
            assert row1.bit_count() == row2.bit_count()
            assert contracted_signature(row1, first) == contracted_signature(row2, first)
            for second in pairs:
                if second == first:
                    continue
                assert contracted_signature(row1, second) != contracted_signature(
                    row2, second
                )
                checked += 1
    assert checked == comb(H, 2) * 2 ** (H - 2) * (comb(H, 2) - 1)
    return checked


def one_target_audit(rows):
    """Check every support-incidence type used to route one missing edge."""
    counts = {"short": 0, "opposite": 0, "one_center": 0, "two_centers": 0}
    for a, b, d, e, D in rows:
        if D == 0:
            continue
        for support, opposite in ((d, b), (e, a)):
            assert support >= 2
            assert opposite - (25 - (support + 1)) == 2
            assert 2 * (30 - H) > opposite
            assert 29 - H >= 16
            for types in product(range(4), repeat=support):
                # 0: neither target endpoint is an H-neighbour; 1/2: one
                # endpoint; 3: both.  The proof gives a G-path in each case.
                if 0 in types:
                    counts["short"] += 1
                elif 1 in types and 2 in types:
                    counts["opposite"] += 1
                elif all(t in (1, 3) for t in types) ^ all(
                    t in (2, 3) for t in types
                ):
                    counts["one_center"] += 1
                else:
                    assert set(types) == {3}
                    counts["two_centers"] += 1
    return counts


def balance_audit(rows):
    """Check all low-side balances in the conformal-triangle argument."""
    checked = 0
    for a, b, d, e, D in rows:
        if D == 0:
            continue
        for s_matched_high in range(d):
            r_matched_high = s_matched_high + 1
            if r_matched_high <= e:
                assert a - (d - 1 - s_matched_high) == b - (
                    e - r_matched_high
                )
                checked += 1
        assert a - (d - 1) == (b - 1) - (e - 2) == 15
        assert (a - 1) - (d - 2) == b - (e - 1) == 15
        assert a - (d - 1) == b - (e - 1) == 15
    return checked


def add_complete(edges, left, right=None):
    pairs = combinations(left, 2) if right is None else product(left, right)
    for u, v in pairs:
        edges.add(edge(u, v))


def fill_cross(s_vertices, r_vertices, need, s_caps, r_caps, forbidden=()):
    """Find a deterministic simple bipartite graph with prescribed size/caps."""
    forbidden = {edge(*pair) for pair in forbidden}
    candidates = []
    for shift in range(len(r_vertices)):
        for i, s in enumerate(s_vertices):
            pair = (s, r_vertices[(i + shift) % len(r_vertices)])
            if edge(*pair) not in forbidden and pair not in candidates:
                candidates.append(pair)
    chosen = []
    s_used = {s: 0 for s in s_vertices}
    r_used = {r: 0 for r in r_vertices}

    def extend(index):
        if len(chosen) == need:
            return True
        if len(candidates) - index < need - len(chosen):
            return False
        for j in range(index, len(candidates)):
            s, r = candidates[j]
            if s_used[s] >= s_caps[s] or r_used[r] >= r_caps[r]:
                continue
            chosen.append((s, r))
            s_used[s] += 1
            r_used[r] += 1
            if extend(j + 1):
                return True
            r_used[r] -= 1
            s_used[s] -= 1
            chosen.pop()
        return False

    assert extend(0), (len(s_vertices), len(r_vertices), need)
    return tuple(chosen)


def graph_from_variant(variant, mode):
    a_size, b_size, d, e, bridge, r_total = variant
    assert mode in {"bridge", "double"}
    assert (mode == "bridge") == bool(bridge)
    a = tuple(f"a{i}" for i in range(a_size))
    b = tuple(f"b{i}" for i in range(b_size))
    s = tuple(f"s{i}" for i in range(d))
    rr = tuple(f"r{i}" for i in range(e))
    z = "z"
    vertices = a + b + s + rr + (z,)
    assert len(vertices) == N
    h_edges = set()
    add_complete(h_edges, a, b)
    add_complete(h_edges, a, s)
    add_complete(h_edges, b, rr)

    if bridge:
        h_edges.remove(edge(a[0], b[0]))
        h_edges.add(edge(a[0], z))
        h_edges.add(edge(b[0], z))
        cross = fill_cross(
            s,
            rr,
            r_total,
            {u: e - 1 for u in s},
            {v: d - 1 for v in rr},
        )
    else:
        h_edges.add(edge(z, s[0]))
        h_edges.add(edge(z, rr[0]))
        cross = fill_cross(
            s,
            rr,
            r_total - 2,
            {u: e - 1 - (u == s[0]) for u in s},
            {v: d - 1 - (v == rr[0]) for v in rr},
            forbidden=((s[0], rr[0]),),
        )
    for u, v in cross:
        h_edges.add(edge(u, v))

    all_edges = {edge(u, v) for u, v in combinations(vertices, 2)}
    g_edges = all_edges - h_edges
    assert len(g_edges) == M
    for v in a + b:
        assert sum(v in pair for pair in h_edges) == 26
    for v in s + rr + (z,):
        assert sum(v in pair for pair in h_edges) <= 25
    return a, b, s, rr, z, g_edges


def verify_tk(branch, paths, g_edges):
    branch = set(branch)
    missing = set(paths)
    for u, v in combinations(branch, 2):
        pair = edge(u, v)
        if pair not in missing:
            assert pair in g_edges
    used = set()
    for endpoints, path in paths.items():
        assert edge(path[0], path[-1]) == endpoints
        internal = set(path[1:-1])
        assert not internal & branch
        assert not internal & used
        used |= internal
        for u, v in zip(path, path[1:]):
            assert edge(u, v) in g_edges


def terminal_certificate_audit(variants):
    bridge_checked = double_checked = 0
    special_checked = 0
    for variant in variants:
        a_size, b_size, d, e, bridge, r_total = variant
        assert a_size - (d + 1) == b_size - (e + 1) == 13
        if r_total == 0:
            assert (a_size, b_size, d, e, bridge) == (15, 25, 1, 11, 0)
            # If either incidence matching is deficient, its rows are common
            # and the corresponding block plus Q minus that support is K27.
            assert a_size + (H - d) == b_size + (H - e) == K
            special_checked += 1
        elif bridge:
            a, b, s, rr, z, g_edges = graph_from_variant(variant, "bridge")
            missing = edge(a[0], z)
            verify_tk(
                a + rr + (z,),
                {missing: (a[0], b[0], b[1], z)},
                g_edges,
            )
            bridge_checked += 1
        else:
            a, b, s, rr, z, g_edges = graph_from_variant(variant, "double")
            missing = edge(z, s[0])
            verify_tk(
                b + s + (z,),
                {missing: (z, a[0], rr[0], s[0])},
                g_edges,
            )
            double_checked += 1
    assert (special_checked, bridge_checked, double_checked) == (1, 5, 5)
    return special_checked, bridge_checked, double_checked


def main():
    labelled, outcomes = large_block_audit()
    rows, variants = profiles()
    rigidity = contraction_rigidity_audit()
    target_types = one_target_audit(rows)
    balances = balance_audit(rows)
    special, bridge, double = terminal_certificate_audit(variants)
    record = (
        f"block_patterns={len(outcomes)};labelled={labelled};rows={len(rows)};"
        f"variants={len(variants)};rigidity={rigidity};"
        f"target_types={sorted(target_types.items())};balances={balances};"
        f"special={special};bridge={bridge};double={double}"
    )
    print("PASS Albertson r=27 order-53 h=13 closure audit")
    print("large-block alternatives: two disjoint cliques, or a three-K14 path")
    print("three-K14 low-edge budget: 273+494=767>713")
    print("two-clique rows:", rows)
    print(f"exact variants={len(variants)}; contraction comparisons={rigidity}")
    print(f"one-target types={target_types}; balance identities={balances}")
    print(f"terminal templates: special={special}, bridge={bridge}, double={double}")
    print(record)
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
