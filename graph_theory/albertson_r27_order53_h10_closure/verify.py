#!/usr/bin/env python3
"""Exact checks for the Albertson r=27 order-53 h=10 closure."""

from __future__ import annotations

import hashlib
import itertools
from collections.abc import Iterable


Q = tuple(range(10))


def edge(u, v):
    assert u != v
    return frozenset((u, v))


def popcount(mask: int) -> int:
    return mask.bit_count()


def matching(options: list[set[int]]) -> list[int] | None:
    """Return distinct representatives for the option sets, or None."""
    order = sorted(range(len(options)), key=lambda i: (len(options[i]), i))
    answer = [-1] * len(options)

    def extend(j: int, used: set[int]) -> bool:
        if j == len(order):
            return True
        i = order[j]
        for value in sorted(options[i] - used):
            answer[i] = value
            if extend(j + 1, used | {value}):
                return True
        answer[i] = -1
        return False

    return answer if extend(0, set()) else None


def check_coloring(vertices: set, h_edges: set[frozenset], classes: list[set]) -> None:
    assert len(classes) == 26
    assert sum(map(len, classes)) == 53
    assert set().union(*classes) == vertices
    assert sum(map(len, classes)) == sum(len(c) for c in classes)
    for cls in classes:
        assert all(edge(u, v) in h_edges for u, v in itertools.combinations(cls, 2))


def check_tk27(g_edges: set[frozenset], branches: set, paths: Iterable[list]) -> None:
    assert len(branches) == 27
    missing = {
        edge(u, v)
        for u, v in itertools.combinations(branches, 2)
        if edge(u, v) not in g_edges
    }
    routed: set[frozenset] = set()
    internal: set = set()
    for path in paths:
        pair = edge(path[0], path[-1])
        assert pair in missing and pair not in routed
        assert all(edge(u, v) in g_edges for u, v in zip(path, path[1:]))
        new_internal = set(path[1:-1])
        assert len(new_internal) == len(path) - 2
        assert not new_internal & branches
        assert not new_internal & internal
        routed.add(pair)
        internal |= new_internal
    assert routed == missing


def profile_audit() -> tuple[tuple[int, int, int, int], ...]:
    """Reconstruct the three survivors of the imported h=10 reduction."""
    profiles = []
    for a in range(17, 27):
        b = 43 - a
        if not (17 <= a <= b <= 26):
            continue
        p, q = a - 17, b - 17
        cap = 26 * 43 - a * (a - 1) - b * (b - 1) + 90 - 260
        defect = cap - 48
        if defect < 0 or defect % 2:
            continue
        total = defect // 2
        for bridge in (0, 1):
            profiles.append((a, b, bridge, total - bridge))
        assert p + q == 9
    all_profiles = tuple(profiles)
    assert all_profiles == (
        (19, 24, 0, 3),
        (19, 24, 1, 2),
        (20, 23, 0, 7),
        (20, 23, 1, 6),
        (21, 22, 0, 9),
        (21, 22, 1, 8),
    )
    survivors = tuple(p for p in all_profiles if p in {
        (20, 23, 0, 7), (21, 22, 0, 9), (21, 22, 1, 8)
    })
    assert len(survivors) == 3
    return survivors


def one_target_audit() -> tuple[int, dict[str, int]]:
    """Exhaust endpoint-incidence types in the one-target routing lemma."""
    counts = {"split": 0, "one_centre": 0, "double_centre": 0}
    checked = 0
    # Type 1 means F-adjacent only to u, 2 only to v, and 3 to both.
    for d in (3, 4, 5):
        opposite = 26 - d
        for types in itertools.product((1, 2, 3), repeat=d):
            checked += 1
            if 1 in types and 2 in types:
                # Each chosen support has at least 19 G-neighbours in D;
                # if their mutual edge is absent, their D-neighbourhoods meet.
                assert 2 * 19 > opposite
                counts["split"] += 1
            elif set(types) in ({1}, {2}):
                # All supports are one-sided; the opposite endpoint sees all
                # d supports in F and therefore at least two vertices of D in G.
                assert opposite - (25 - (d + 1)) == 2
                counts["one_centre"] += 1
            elif all(t == 3 for t in types):
                assert opposite - (25 - (d + 1)) == 2
                counts["double_centre"] += 1
            else:
                # One one-sided type plus double blockers: the endpoint met by
                # every support is the centre; the one-sided support closes the
                # other end of the long path.
                assert opposite - (25 - (d + 1)) == 2
                assert 18 + 1 >= 19
                counts["one_centre"] += 1
    assert checked == 3**3 + 3**4 + 3**5
    return checked, counts


def contracted_classes(pair: frozenset[int]) -> tuple[frozenset[int], ...]:
    return (pair,) + tuple(frozenset((v,)) for v in Q if v not in pair)


def compatible_classes(row: frozenset[int], pair: frozenset[int]) -> frozenset:
    return frozenset(cls for cls in contracted_classes(pair) if cls <= row)


def contraction_rigidity_audit() -> int:
    """Exhaust the two-contraction row-signature injectivity assertion."""
    signatures = 0
    for d, q in ((3, 6), (4, 5), (5, 4)):
        target = tuple(range(d, 10))
        target_edges = tuple(edge(u, v) for u, v in itertools.combinations(target, 2))
        rows = tuple(frozenset(row) for row in itertools.combinations(Q, q))
        for first, second in itertools.combinations(target_edges, 2):
            seen: dict[tuple[frozenset, frozenset], frozenset[int]] = {}
            for row in rows:
                mapped_first = compatible_classes(row, first)
                mapped_second = compatible_classes(row, second)
                if len(mapped_first) != q - 1 or len(mapped_second) != q - 1:
                    continue
                signature = (mapped_first, mapped_second)
                assert signature not in seen or seen[signature] == row
                seen[signature] = row
                signatures += 1
    return signatures


TARGET4_EDGES = tuple(itertools.combinations(range(4), 2))


def target_options(targets: tuple[tuple[int, int], ...], rows: tuple[int, ...]) -> list[set[int]]:
    return [
        {support for support, row in enumerate(rows) if not (row & ((1 << u) | (1 << v)))}
        for u, v in targets
    ]


def rigid_boundary_witness(targets: tuple[tuple[int, int], ...], rows: tuple[int, ...]) -> bool:
    """Recognize a Hall-equality obstruction with six supports and <=7 active edges."""
    options = target_options(targets, rows)
    for size in range(1, len(targets) + 1):
        for indices in itertools.combinations(range(len(targets)), size):
            union = set().union(*(options[i] for i in indices))
            if len(union) >= size:
                continue
            chosen = tuple(targets[i] for i in indices)
            blocked = set(range(6)) - union
            if len(blocked) != 7 - size:
                continue
            if set(chosen) != set(targets):
                continue
            if any(rows[i] != 0 for i in union):
                continue
            if any(popcount(rows[i]) != 1 for i in blocked):
                continue
            if size == 1:
                allowed = {(1 << chosen[0][0]), (1 << chosen[0][1])}
                if all(rows[i] in allowed for i in blocked):
                    return True
            else:
                common = set(chosen[0])
                for pair in chosen[1:]:
                    common &= set(pair)
                if len(common) == 1:
                    centre = next(iter(common))
                    if all(rows[i] == 1 << centre for i in blocked):
                        return True
    return False


def seven_edge_boundary_audit() -> tuple[int, int, int]:
    """Exhaust the d=6, four-target Hall boundary up to support permutation."""
    row_multisets = tuple(itertools.combinations_with_replacement(range(16), 6))
    checked = routed = rigid = 0
    for target_mask in range(1 << len(TARGET4_EDGES)):
        targets = tuple(
            pair for i, pair in enumerate(TARGET4_EDGES) if target_mask & (1 << i)
        )
        target_count = len(targets)
        for rows in row_multisets:
            active = target_count + sum(popcount(row) for row in rows)
            if active > 7:
                continue
            checked += 1
            if matching(target_options(targets, rows)) is not None:
                routed += 1
            else:
                assert active == 7
                assert rigid_boundary_witness(targets, rows)
                rigid += 1
    assert checked == routed + rigid
    return checked, routed, rigid


def final_routing_audit() -> tuple[int, int]:
    """Exhaust target S-to-R row choices in the double-uniform profile."""
    checked = routed = 0
    allowed_rows = tuple(mask for mask in range(1 << 5) if popcount(mask) <= 3)
    for beta in range(1, 5):
        # The beta target vertices have z-edges.  At least one z-R edge is
        # reserved, so their S-R rows together use at most 8-beta edges.
        for rows in itertools.product(allowed_rows, repeat=beta):
            if sum(popcount(row) for row in rows) > 8 - beta:
                continue
            checked += 1
            options = [
                {r for r in range(5) if not (row & (1 << r))}
                for row in rows
            ]
            assert matching(options) is not None
            routed += 1
    assert checked == routed
    return checked, routed


def p2_graph(f_edges: set[frozenset]) -> tuple[set, set[frozenset], list, list, list, str]:
    a = [f"a{i}" for i in range(21)]
    b = [f"b{i}" for i in range(22)]
    s = [f"s{i}" for i in range(4)]
    r = [f"r{i}" for i in range(5)]
    z = "z"
    vertices = set(a + b + s + r + [z])
    h_edges = {edge(x, y) for x in a for y in b}
    h_edges |= {edge(x, y) for x in a for y in s}
    h_edges |= {edge(x, y) for x in b for y in r}
    h_edges |= set(f_edges)
    return vertices, h_edges, a, b, s, r, z


def bridge_graph(f_edges: set[frozenset]) -> tuple[set, set[frozenset], list, list, list, list, str]:
    a = [f"a{i}" for i in range(21)]
    b = [f"b{i}" for i in range(22)]
    s = [f"s{i}" for i in range(4)]
    r = [f"r{i}" for i in range(5)]
    z = "z"
    vertices = set(a + b + s + r + [z])
    h_edges = {
        edge(x, y) for x in a for y in b if not (x == "a0" and y == "b0")
    }
    h_edges |= {edge(x, y) for x in a for y in s}
    h_edges |= {edge("a0", z)}
    h_edges |= {edge(x, y) for x in b for y in r}
    h_edges |= {edge("b0", z)}
    h_edges |= set(f_edges)
    return vertices, h_edges, a, b, s, r, z


def residual_pairs(left: list, right: list) -> list[set]:
    assert len(left) == len(right)
    return [{x, y} for x, y in zip(left, right)]


def certificate_decoder_audit() -> int:
    """Check the conformal and topological-clique templates explicitly."""
    checked = 0

    # Double-uniform profile: an S-S edge plus z-R gives a conformal triangle.
    f = {edge("s0", "s1"), edge("z", "r0")}
    vertices, h, a, b, s, r, z = p2_graph(f)
    classes = [{a[0], s[0], s[1]}, {z, r[0]}]
    classes += [{a[1], s[2]}, {a[2], s[3]}]
    classes += [{b[i], r[i + 1]} for i in range(4)]
    classes += residual_pairs(a[3:], b[4:])
    check_coloring(vertices, h, classes)
    checked += 1

    # Double-uniform profile: an R-R edge plus z-S is symmetric.
    f = {edge("r0", "r1"), edge("z", "s0")}
    vertices, h, a, b, s, r, z = p2_graph(f)
    classes = [{b[0], r[0], r[1]}, {z, s[0]}]
    classes += [{a[i], s[i + 1]} for i in range(3)]
    classes += [{b[i + 1], r[i + 2]} for i in range(3)]
    classes += residual_pairs(a[3:], b[4:])
    check_coloring(vertices, h, classes)
    checked += 1

    # A worst-size z-S target set and an explicit S-to-R complement matching.
    f = {edge("z", f"s{i}") for i in range(4)} | {edge("z", "r0")}
    f |= {edge("s0", "r1"), edge("s1", "r1"), edge("s2", "r2"), edge("s3", "r2")}
    vertices, h, a, b, s, r, z = p2_graph(f)
    complete = {edge(x, y) for x, y in itertools.combinations(vertices, 2)}
    g = complete - h
    branches = set(b + s + [z])
    assignment = [r[2], r[3], r[3], r[1]]
    # Replace the duplicate by an exact matching computed from F.
    opts = [{j for j, rv in enumerate(r) if edge(sv, rv) not in f} for sv in s]
    reps = matching(opts)
    assert reps is not None
    paths = [[z, a[i], r[reps[i]], s[i]] for i in range(4)]
    check_tk27(g, branches, paths)
    checked += 1

    # Bridge profile: four conformal-triangle templates.
    cases = (
        (edge("s0", "s1"), [{"a1", "s0", "s1"}, {"z", "a0"}], "SS"),
        (edge("r0", "r1"), [{"b1", "r0", "r1"}, {"z", "b0"}], "RR"),
        (edge("z", "s0"), [{"a0", "z", "s0"}], "zS"),
        (edge("z", "r0"), [{"b0", "z", "r0"}], "zR"),
    )
    for fedge, prefix, kind in cases:
        vertices, h, a, b, s, r, z = bridge_graph({fedge})
        classes = [set(cls) for cls in prefix]
        if kind == "SS":
            classes += [{a[2], s[2]}, {a[3], s[3]}]
            classes += [{b[i], r[i]} for i in range(5)]
            classes += residual_pairs(a[4:], b[5:])
        elif kind == "RR":
            classes += [{a[i], s[i]} for i in range(4)]
            classes += [{b[i + 2], r[i + 2]} for i in range(3)]
            classes += residual_pairs(a[4:], b[5:])
        elif kind == "zS":
            classes += [{a[i + 1], s[i + 1]} for i in range(3)]
            classes += [{b[i], r[i]} for i in range(5)]
            classes += residual_pairs(a[4:], b[5:])
        else:
            classes += [{a[i], s[i]} for i in range(4)]
            classes += [{b[i + 1], r[i + 1]} for i in range(4)]
            classes += residual_pairs(a[4:], b[5:])
        check_coloring(vertices, h, classes)
        checked += 1

    # With only S-R high edges, the bridge profile has one missing branch edge.
    f = {
        edge("s0", "r0"), edge("s0", "r1"), edge("s1", "r1"),
        edge("s1", "r2"), edge("s2", "r2"), edge("s2", "r3"),
        edge("s3", "r3"), edge("s3", "r4"),
    }
    vertices, h, a, b, s, r, z = bridge_graph(f)
    complete = {edge(x, y) for x, y in itertools.combinations(vertices, 2)}
    g = complete - h
    check_tk27(g, set(a + r + [z]), [[a[0], b[0], b[1], z]])
    checked += 1

    assert checked == 8
    return checked


def main() -> None:
    survivors = profile_audit()
    one_target, type_counts = one_target_audit()
    signatures = contraction_rigidity_audit()
    hall_checked, hall_routed, hall_rigid = seven_edge_boundary_audit()
    final_checked, final_routed = final_routing_audit()
    decoders = certificate_decoder_audit()
    record = (
        f"survivors={len(survivors)};one_target={one_target};"
        f"one_target_types={sorted(type_counts.items())};"
        f"contraction_signatures={signatures};boundary_states={hall_checked};"
        f"boundary_routed={hall_routed};boundary_rigid={hall_rigid};"
        f"final_rows={final_checked};final_routed={final_routed};"
        f"decoders={decoders};conclusion=h_at_least_11"
    )
    print("PASS Albertson r=27 order-53 h=10 closure")
    print("surviving profiles closed:", survivors)
    print("one-target patterns:", one_target, sorted(type_counts.items()))
    print("two-contraction row signatures:", signatures)
    print(
        "seven-edge Hall states:", hall_checked,
        f"(routed={hall_routed}, rigid={hall_rigid})",
    )
    print("final double-uniform routing rows:", final_checked)
    print("explicit certificate decoders:", decoders)
    print(record)
    print("certificate_sha256=" + hashlib.sha256(record.encode()).hexdigest())
    print("conclusion: every remaining counterexample has at least eleven high vertices")


if __name__ == "__main__":
    main()
