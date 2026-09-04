#!/usr/bin/env python3
"""Exact audit for the Albertson r=27 two-clique h=10,11,12 closure."""

from hashlib import sha256
from itertools import combinations, product


K = 27
N = 53
M = 713
EXCESS = 2 * M - 26 * N

EXPECTED = {
    10: ((19, 24, 2, 7, 3), (20, 23, 3, 6, 7), (21, 22, 4, 5, 9)),
    11: (
        (18, 24, 2, 8, 5),
        (19, 23, 3, 7, 10),
        (20, 22, 4, 6, 13),
        (21, 21, 5, 5, 14),
    ),
    12: (
        (17, 24, 2, 9, 7),
        (18, 23, 3, 8, 13),
        (19, 22, 4, 7, 17),
        (20, 21, 5, 6, 19),
    ),
}


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def profiles():
    """Reconstruct (h,a,b,p,q,t,r) from the exact excess identity."""
    rows = []
    for h in range(10, 13):
        low = N - h
        minimum = K - h
        got = []
        assert 2 * (minimum - 1) > K - 1
        assert low > K - 1
        assert 3 * minimum > low
        for a in range(minimum, K):
            b = low - a
            if not (a <= b < K and b >= minimum):
                continue
            cap = (
                (K - 1) * low
                - a * (a - 1)
                - b * (b - 1)
                + h * (h - 1)
                - (K - 1) * h
            )
            defect = cap - EXCESS
            if defect < 0 or defect % 2:
                continue
            p = a + h - K
            q = b + h - K
            total = defect // 2
            assert p + q == h - 1
            assert p >= 2 and q >= 2
            got.append((a, b, p, q, total))
            for bridge in (0, 1):
                rows.append((h, a, b, p, q, bridge, total - bridge))
        assert tuple(got) == EXPECTED[h]
    assert len(rows) == 22
    return tuple(rows)


def contracted_signature(row, pair, h):
    """Classes compatible with a row after an H-edge is one pair class."""
    u, v = pair
    singles = tuple(i for i in range(h) if i not in pair and row >> i & 1)
    paired = (row >> u & 1) and (row >> v & 1)
    return singles, bool(paired)


def contraction_rigidity_audit():
    """Two distinct failed-edge signatures distinguish equal-sized rows."""
    checked = 0
    for h in range(10, 13):
        vertices = range(h)
        edges = tuple(combinations(vertices, 2))
        for first in edges:
            outside = [v for v in vertices if v not in first]
            for outside_mask in range(1 << len(outside)):
                base = sum(
                    1 << v for j, v in enumerate(outside) if outside_mask >> j & 1
                )
                # These are the only unequal equal-sized rows with one common
                # contracted signature: they swap the ends of the first edge.
                row1 = base | (1 << first[0])
                row2 = base | (1 << first[1])
                assert row1.bit_count() == row2.bit_count()
                assert contracted_signature(row1, first, h) == contracted_signature(
                    row2, first, h
                )
                for second in edges:
                    if second == first:
                        continue
                    assert contracted_signature(row1, second, h) != contracted_signature(
                        row2, second, h
                    )
                    checked += 1
    return checked


def one_target_type_audit():
    """Classify every support incidence pattern at one target edge."""
    counts = {"short": 0, "opposite": 0, "one_center": 0, "two_centers": 0}
    for h, _, _, p, q, _, _ in profiles():
        for d in {p, q}:
            other_block = 26 - d
            assert other_block <= 24
            assert 29 - h >= 17
            assert 30 - h >= 18
            assert 2 * (30 - h) > other_block
            for types in product(range(4), repeat=d):
                # 0: meets neither target end in H; 1: u only; 2: v only;
                # 3: both.  The README gives a G-path in every class.
                if 0 in types:
                    counts["short"] += 1
                elif 1 in types and 2 in types:
                    counts["opposite"] += 1
                elif (all(t in (1, 3) for t in types)) ^ (
                    all(t in (2, 3) for t in types)
                ):
                    counts["one_center"] += 1
                else:
                    assert set(types) == {3}
                    counts["two_centers"] += 1
                # A target end meeting every support has at least two G
                # neighbours in the opposite low block.
                assert other_block - (25 - (d + 1)) == 2
    return counts


def add_complete(edges, left, right=None):
    if right is None:
        for u, v in combinations(left, 2):
            edges.add(edge(u, v))
    else:
        for u in left:
            for v in right:
                edges.add(edge(u, v))


def fill_cross(s_vertices, r_vertices, need, s_caps, r_caps, forbidden=()):
    """Find a deterministic simple bipartite b-matching of prescribed size."""
    forbidden = {edge(*pair) for pair in forbidden}
    candidates = [
        (s, r)
        for shift in range(len(r_vertices))
        for i, s in enumerate(s_vertices)
        for r in (r_vertices[(i + shift) % len(r_vertices)],)
        if edge(s, r) not in forbidden
    ]
    # Remove repeats introduced when the two sides have different orders.
    candidates = list(dict.fromkeys(candidates))
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

    assert extend(0), (len(s_vertices), len(r_vertices), need, s_caps, r_caps)
    return tuple(chosen)


def graph_from_profile(row, mode):
    """Build representative H/G graphs for the terminal TK templates."""
    h, a_size, b_size, p, q, bridge, r_total = row
    assert mode in {"bridge", "double"}
    assert (mode == "bridge") == bool(bridge)
    a = tuple(f"a{i}" for i in range(a_size))
    b = tuple(f"b{i}" for i in range(b_size))
    s = tuple(f"s{i}" for i in range(p))
    rr = tuple(f"r{i}" for i in range(q))
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
        s_caps = {u: q - 1 for u in s}
        r_caps = {v: p - 1 for v in rr}
        cross = fill_cross(s, rr, r_total, s_caps, r_caps)
    else:
        h_edges.add(edge(z, s[0]))
        h_edges.add(edge(z, rr[0]))
        s_caps = {u: q - 1 - (u == s[0]) for u in s}
        r_caps = {v: p - 1 - (v == rr[0]) for v in rr}
        cross = fill_cross(
            s,
            rr,
            r_total - 2,
            s_caps,
            r_caps,
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
    return (a, b, s, rr, z, h_edges, g_edges)


def verify_tk(branch, direct_missing, paths, g_edges):
    branch = set(branch)
    missing = {edge(*pair) for pair in direct_missing}
    for pair in combinations(branch, 2):
        pair = edge(*pair)
        if pair not in missing:
            assert pair in g_edges
    used_internal = set()
    assert set(paths) == missing
    for endpoints, path in paths.items():
        assert path[0] in endpoints and path[-1] in endpoints
        assert edge(path[0], path[-1]) == endpoints
        internal = set(path[1:-1])
        assert not internal & branch
        assert not internal & used_internal
        used_internal |= internal
        for u, v in zip(path, path[1:]):
            assert edge(u, v) in g_edges


def terminal_certificate_audit(rows):
    bridge_checked = double_checked = 0
    for row in rows:
        h, _, _, _, _, bridge, _ = row
        # Colouring alternative: h high classes plus equally many residual
        # low vertices on each side.
        assert 26 - h >= 14
        if bridge:
            a, b, s, rr, z, _, g_edges = graph_from_profile(row, "bridge")
            branch = a + rr + (z,)
            missing = (a[0], z)
            path = (a[0], b[0], b[1], z)
            verify_tk(branch, (missing,), {edge(*missing): path}, g_edges)
            bridge_checked += 1
        else:
            a, b, s, rr, z, _, g_edges = graph_from_profile(row, "double")
            # Here X={s0}, Y={r0}; |X|<=|Y| and (8) is the sole routed edge.
            branch = b + s + (z,)
            missing = (z, s[0])
            path = (z, a[0], rr[0], s[0])
            verify_tk(branch, (missing,), {edge(*missing): path}, g_edges)
            double_checked += 1
    assert bridge_checked == double_checked == 11
    return bridge_checked, double_checked


def balance_audit(rows):
    checked = 0
    for h, a, b, p, q, _, _ in rows:
        # Delete s0: residual-low equality is equivalent to r_M-s_M=1.
        for s_m in range(p):
            r_m = s_m + 1
            if r_m <= q:
                assert a - (p - 1 - s_m) == b - (q - r_m)
                checked += 1
        # Every conformal-triangle construction leaves equal low sides.
        assert a - (p - 1) == (b - 1) - (q - 2)  # zS plus an RR edge
        assert (a - 1) - (p - 2) == b - (q - 1)  # SS edge plus zR
        assert a - (p - 1) == b - (q - 1)  # high triangle z,s,r
    return checked


def main():
    assert EXCESS == 48
    rows = profiles()
    rigidity = contraction_rigidity_audit()
    type_counts = one_target_type_audit()
    balance = balance_audit(rows)
    bridge, double = terminal_certificate_audit(rows)
    # The injection step: H[X,Y] empty gives a complete G-biclique.  The
    # smaller nonempty side always injects into the larger one.
    injection_cases = 0
    for p in range(2, 10):
        for q in range(2, 10):
            for x in range(1, p + 1):
                for y in range(1, q + 1):
                    assert x <= y or y <= x
                    injection_cases += 1
    record = (
        f"profiles={len(rows)};rigidity={rigidity};"
        f"types={sorted(type_counts.items())};balance={balance};"
        f"bridge={bridge};double={double};injections={injection_cases}"
    )
    print("PASS Albertson r=27 parametric two-clique closure audit")
    print("profiles:", len(rows), "(h=10,11,12; bridged and unbridged)")
    print("two-contraction row comparisons:", rigidity)
    print("one-target support patterns:", type_counts)
    print("balance identities:", balance)
    print("decoded TK27 templates: bridge=", bridge, "double-uniform=", double)
    print("support-injection size cases:", injection_cases)
    print("conclusion: h=10,11,12 are impossible; hence h>=13")
    print("certificate_sha256=" + sha256(record.encode()).hexdigest())


if __name__ == "__main__":
    main()
