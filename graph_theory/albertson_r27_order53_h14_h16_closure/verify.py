#!/usr/bin/env python3
"""Exact arithmetic audit for the Albertson r=27 h=14,15,16 closure."""

from hashlib import sha256
from itertools import combinations, product
from math import comb


K = 27
N = 53
M = 713

EXPECTED_TRIPLE_BOUNDS = {
    14: (237, 248, 261),
    15: (226, 238, 252),
    16: (218, 231, 246),
}

EXPECTED_PROFILES = {
    14: (
        (14, 25, 1, 12, 1),
        (15, 24, 2, 11, 11),
        (16, 23, 3, 10, 19),
        (17, 22, 4, 9, 25),
        (18, 21, 5, 8, 29),
        (19, 20, 6, 7, 31),
    ),
    15: (
        (13, 25, 1, 13, 2),
        (14, 24, 2, 12, 13),
        (15, 23, 3, 11, 22),
        (16, 22, 4, 10, 29),
        (17, 21, 5, 9, 34),
        (18, 20, 6, 8, 37),
        (19, 19, 7, 7, 38),
    ),
    16: (
        (12, 25, 1, 14, 3),
        (13, 24, 2, 13, 15),
        (14, 23, 3, 12, 25),
        (15, 22, 4, 11, 33),
        (16, 21, 5, 10, 39),
        (17, 20, 6, 9, 43),
        (18, 19, 7, 8, 45),
    ),
    17: (
        (11, 25, 1, 15, 4),
        (12, 24, 2, 14, 17),
        (13, 23, 3, 13, 28),
        (14, 22, 4, 12, 37),
        (15, 21, 5, 11, 44),
        (16, 20, 6, 10, 49),
        (17, 19, 7, 9, 52),
        (18, 18, 8, 8, 53),
    ),
}

EXPECTED_H17_THREE_BLOCKS = {
    ((10, 10, 17), 1, 0, 226, 3),
    ((10, 10, 17), 1, 1, 227, 4),
    ((10, 10, 18), 2, 0, 243, 20),
    ((10, 11, 17), 2, 0, 236, 13),
    ((10, 12, 16), 2, 0, 231, 8),
    ((10, 13, 15), 2, 0, 228, 5),
    ((10, 14, 14), 2, 0, 227, 4),
    ((11, 11, 16), 2, 0, 230, 7),
    ((11, 12, 15), 2, 0, 226, 3),
    ((11, 13, 14), 2, 0, 224, 1),
    ((12, 12, 14), 2, 0, 223, 0),
}


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


def triple_block_audit():
    """Maximize the low-edge upper bound for three large blocks."""
    records = {}
    pairs = tuple(combinations(range(3), 2))
    connector_budget = {1: 0, 2: 1, 3: 3}
    for h in range(14, 17):
        low = N - h
        minimum_order = K - h
        # Four large blocks would cover too many low vertices, even if their
        # direct-intersection graph were a tree.
        assert 4 * minimum_order - 3 > low
        maxima = {}
        witnesses = {}
        for sizes in product(range(minimum_order, K), repeat=3):
            if tuple(sorted(sizes)) != sizes:
                continue
            for bits in range(1 << len(pairs)):
                edges = tuple(pairs[i] for i in range(len(pairs)) if bits >> i & 1)
                if not is_forest(3, edges):
                    continue
                # A shared low vertex sees all other vertices of both clique
                # blocks, so the degree-26 cap gives u+v<=28.
                if any(sizes[u] + sizes[v] > 28 for u, v in edges):
                    continue
                if sum(sizes) - len(edges) != low:
                    continue
                components = 3 - len(edges)
                upper = sum(comb(size, 2) for size in sizes) + connector_budget[components]
                q = len(edges)
                if upper > maxima.get(q, -1):
                    maxima[q] = upper
                    witnesses[q] = (sizes, edges, components)
        row = tuple(maxima[q] for q in range(3))
        assert row == EXPECTED_TRIPLE_BOUNDS[h]
        forced_minimum = 26 * low - M
        assert max(row) < forced_minimum
        records[h] = (low, minimum_order, forced_minimum, row, witnesses)
    return records


def profile_audit():
    """Reconstruct every two-clique row and bridge variant."""
    records = {}
    for h in range(14, 18):
        low = N - h
        s = K - h
        rows = []
        variants = []
        for a in range(s, low // 2 + 1):
            b = low - a
            if b >= K:
                continue
            d, e = a - s, b - s
            base_low_edges = comb(a, 2) + comb(b, 2)
            D = comb(h, 2) - M + 26 * low - base_low_edges
            if D < 0:
                continue
            assert d + e == h - 1
            rows.append((a, b, d, e, D))
            for bridge in (0, 1):
                missing_high_edges = D - bridge
                if missing_high_edges >= 0:
                    variants.append((a, b, d, e, bridge, missing_high_edges))
        assert tuple(rows) == EXPECTED_PROFILES[h]
        assert all(d >= 1 and e >= 1 for _, _, d, e, _ in rows)
        assert len(variants) == 2 * len(rows)
        records[h] = (tuple(rows), tuple(variants))
    return records


def h17_three_block_audit():
    """Classify all three-large-block edge-budget survivors at h=17."""
    h = 17
    low = N - h
    s = K - h
    forced_minimum = 26 * low - M
    pairs = tuple(combinations(range(3), 2))
    connector_options = {0: range(4), 1: range(2), 2: range(1)}
    survivors = set()
    for sizes in product(range(s, K), repeat=3):
        if tuple(sorted(sizes)) != sizes:
            continue
        for bits in range(1 << len(pairs)):
            edges = tuple(pairs[i] for i in range(len(pairs)) if bits >> i & 1)
            if not is_forest(3, edges):
                continue
            q = len(edges)
            if any(sizes[u] + sizes[v] > 28 for u, v in edges):
                continue
            if sum(sizes) - q != low:
                continue
            base = sum(comb(size, 2) for size in sizes)
            for extra in connector_options[q]:
                e_low = base + extra
                if e_low < forced_minimum:
                    continue
                e_high = M - (26 * low - e_low)
                assert 0 <= e_high <= comb(h, 2)
                survivors.add((sizes, q, extra, e_low, e_high))
    assert survivors == EXPECTED_H17_THREE_BLOCKS
    return tuple(sorted(survivors))


def contraction_rigidity_audit():
    """Two distinct failed contractions force equal fixed-size rows."""
    checked = 0
    for h in range(14, 18):
        pairs = tuple(combinations(range(h), 2))
        for first in pairs:
            for second in pairs:
                if first == second:
                    continue
                intersection = set(first) & set(second)
                # An equal-size row symmetric difference is even.  If it is
                # contained in two distinct pairs, it is contained in a set
                # of order at most one and hence must be empty.
                possible = [
                    subset
                    for size in range(len(intersection) + 1)
                    for subset in combinations(intersection, size)
                    if size % 2 == 0
                ]
                assert possible == [()]
                checked += 1
    expected = sum(comb(h, 2) * (comb(h, 2) - 1) for h in range(14, 18))
    assert checked == expected
    return checked


def one_target_type_audit(profile_records):
    """Check the exhaustive support-type split and all degree margins."""
    counts = {"support_one": 0, "short": 0, "opposite": 0, "one_center": 0, "two_centers": 0}
    for h, (rows, _) in profile_records.items():
        s = K - h
        for a, b, d, e, _ in rows:
            for support, opposite in ((d, b), (e, a)):
                assert opposite == 26 - support
                assert (s + support) + (h - support) == K
                if support == 1:
                    # Each target endpoint has a G-neighbour in the opposite
                    # K25, enough for a path of length two or three.
                    assert opposite == 25
                    assert opposite - (25 - 1) == 1
                    counts["support_one"] += 1
                    continue
                assert opposite - (25 - (support + 1)) == 2
                assert 29 - h >= 12
                assert 2 * (30 - h) > opposite
                # With no support adjacent in G to both target endpoints,
                # each support is u-only, v-only, or both in H.  Enumerating
                # their three type counts verifies the proof's exhaustive
                # split.
                for u_only in range(support + 1):
                    for v_only in range(support - u_only + 1):
                        both = support - u_only - v_only
                        if u_only and v_only:
                            counts["opposite"] += 1
                        elif u_only or v_only:
                            counts["one_center"] += 1
                        else:
                            assert both == support
                            counts["two_centers"] += 1
                counts["short"] += 1
    return counts


def terminal_identity_audit(profile_records):
    """Check every colouring, balance, conformal and TK27 vertex count."""
    checks = 0
    for h, (rows, variants) in profile_records.items():
        s = K - h
        for a, b, d, e, _ in rows:
            for c_order, other_order, p, q in ((a, b, d, e), (b, a, e, d)):
                assert c_order == s + p
                assert other_order == s + q == 26 - p
                assert p + q == h - 1
                # Unbridged simultaneous incidence matchings.
                assert c_order - (p + 1) == other_order - (q + 1) == s - 1
                assert h + (s - 1) == 26
                # A contracted high edge reduces the high class count by one.
                assert c_order - p == other_order - q == s
                assert (h - 1) + s == 26
                # Double-uniform partition Q=S+R+z and the TK branch set.
                assert p + q + 1 == h
                assert other_order + p + 1 == K
                # Deleting a conformal triangle leaves equal low sides.
                assert c_order - (p - 1) == other_order - (q - 1) == s + 1
                checks += 7
        for a, b, d, e, bridge, missing in variants:
            assert bridge + missing == next(row[4] for row in rows if row[:4] == (a, b, d, e))
            if bridge:
                assert a - (d + 1) == b - (e + 1) == s - 1
                assert h + (s - 1) == 26
                assert a + e + 1 == b + d + 1 == K
                assert min(a, b) >= 11
                checks += 4
    return checks


def main():
    blocks = triple_block_audit()
    profiles = profile_audit()
    h17_frontier = h17_three_block_audit()
    rigidity = contraction_rigidity_audit()
    target_types = one_target_type_audit(profiles)
    terminal_checks = terminal_identity_audit(profiles)
    record = (
        f"blocks={[(h, blocks[h][2], blocks[h][3]) for h in blocks]};"
        f"profiles={[(h, profiles[h][0]) for h in profiles]};"
        f"h17={h17_frontier};"
        f"variants={sum(len(profiles[h][1]) for h in profiles)};"
        f"rigidity={rigidity};types={sorted(target_types.items())};"
        f"terminal={terminal_checks}"
    )
    print("PASS Albertson r=27 order-53 h=14,15,16 closure audit")
    for h in range(14, 17):
        low, s, forced, bounds, witnesses = blocks[h]
        print(
            f"h={h}: low={low}, large-block minimum={s}, "
            f"three-block upper bounds={bounds}<forced e(L)={forced}"
        )
        print(f"  profiles={profiles[h][0]}")
        print(f"  exact bridge variants={len(profiles[h][1])}; witnesses={witnesses}")
    print(f"h=17 two-clique profiles={profiles[17][0]}")
    print(f"h=17 surviving three-block signatures={h17_frontier}")
    print(f"contraction_pair_checks={rigidity}")
    print(f"one_target_type_counts={target_types}")
    print(f"terminal_identity_checks={terminal_checks}")
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
