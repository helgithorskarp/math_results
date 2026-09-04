#!/usr/bin/env python3
"""Exact finite checks for the Albertson r=27 order-53 h=9 closure."""

from __future__ import annotations

import hashlib
import itertools
from collections.abc import Iterable


Q = tuple(range(9))
ALL_Q_EDGES = tuple(itertools.combinations(Q, 2))


def edge(u: int | str, v: int | str) -> frozenset[int | str]:
    assert u != v
    return frozenset((u, v))


def profiles() -> list[tuple[int, int, int, int]]:
    """Derive (a,b,t,r) from the exact Gallai excess cap."""
    result = []
    for a in range(18, 27):
        b = 44 - a
        if not (a <= b <= 26):
            continue
        cap = 26 * 44 - a * (a - 1) - b * (b - 1) + 9 * 8 - 26 * 9
        defect = cap - 48
        if defect < 0 or defect % 2:
            continue
        for bridge in (0, 1):
            missing_q = defect // 2 - bridge
            if missing_q >= 0:
                result.append((a, b, bridge, missing_q))
    expected = [
        (20, 24, 0, 1),
        (20, 24, 1, 0),
        (21, 23, 0, 4),
        (21, 23, 1, 3),
        (22, 22, 0, 5),
        (22, 22, 1, 4),
    ]
    assert result == expected
    for a, b, _, _ in result:
        p, q = a - 18, b - 18
        assert p + q == 8
        assert a - (p + 1) == b - (q + 1) == 17
        assert a - p == b - q == 18
    return result


def saturating_assignment(
    f_edges: set[frozenset[int]], support: set[int], target: set[int]
) -> dict[frozenset[int], int] | None:
    """Match every F[target] edge to a nonincident support vertex."""
    missing = [e for e in f_edges if e <= target]
    options = {
        e: tuple(
            s
            for s in support
            if all(edge(s, endpoint) not in f_edges for endpoint in e)
        )
        for e in missing
    }
    missing.sort(key=lambda e: (len(options[e]), tuple(sorted(e))))

    def search(index: int, used: set[int]) -> dict[frozenset[int], int] | None:
        if index == len(missing):
            return {}
        current = missing[index]
        for s in options[current]:
            if s in used:
                continue
            tail = search(index + 1, used | {s})
            if tail is not None:
                return {current: s, **tail}
        return None

    return search(0, set())


def check_tk27(
    graph_edges: set[frozenset[int | str]],
    branches: set[int | str],
    paths: Iterable[list[int | str]],
) -> None:
    assert len(branches) == 27
    missing = {
        edge(u, v)
        for u, v in itertools.combinations(branches, 2)
        if edge(u, v) not in graph_edges
    }
    routed: set[frozenset[int | str]] = set()
    internal: set[int | str] = set()
    for path in paths:
        pair = edge(path[0], path[-1])
        assert pair in missing and pair not in routed
        assert all(edge(u, v) in graph_edges for u, v in zip(path, path[1:]))
        new_internal = set(path[1:-1])
        assert len(new_internal) == len(path) - 2
        assert not new_internal & branches
        assert not new_internal & internal
        routed.add(pair)
        internal |= new_internal
    assert routed == missing


def forced_unbridged_graph(
    low_size: int,
    support: set[int],
    f_edges: set[frozenset[int]],
) -> tuple[set[frozenset[int | str]], set[int | str]]:
    low = {f"a{i}" for i in range(low_size)}
    target = set(Q) - support
    branches: set[int | str] = low | target
    graph_edges: set[frozenset[int | str]] = {
        edge(u, v) for u, v in itertools.combinations(low, 2)
    }
    graph_edges |= {edge(a, q) for a in low for q in target}
    graph_edges |= {
        edge(u, v)
        for u, v in itertools.combinations(Q, 2)
        if edge(u, v) not in f_edges
    }
    return graph_edges, branches


def is_rigid_star_failure(
    f_edges: set[frozenset[int]], support: set[int], target: set[int]
) -> tuple[int, list[frozenset[int]], list[int]] | None:
    """Recognize the Hall-equality star when at most d target edges occur."""
    target_edges = [e for e in f_edges if e <= target]
    d, k = len(support), len(target_edges)
    if not (1 <= k <= d and len(f_edges) == d + 1):
        return None
    if k == 1:
        target_edge = target_edges[0]
        # Every support vertex has exactly one edge to one endpoint; for a
        # single target edge either endpoint can serve as its blocker.
        cross = f_edges - {target_edge}
        if len(cross) != d:
            return None
        for s in support:
            incident = [e for e in cross if s in e]
            if len(incident) != 1 or not (incident[0] - {s}) <= target_edge:
                return None
        s0 = min(support)
        center = next(iter(next(e for e in cross if s0 in e) - {s0}))
        return center, target_edges, sorted(support)
    common = set.intersection(*(set(e) for e in target_edges))
    for center in sorted(common):
        blocking = sorted(s for s in support if edge(s, center) in f_edges)
        available = sorted(support - set(blocking))
        expected = set(target_edges) | {edge(s, center) for s in blocking}
        if (
            f_edges == expected
            and len(blocking) == d - k + 1
            and len(available) == k - 1
        ):
            return center, target_edges, blocking
    return None


def verify_unbridged_routing() -> tuple[int, int, int]:
    """Exhaust every labeled F in all deficient-side regimes."""
    regimes = {(2, 1), (6, 1), (3, 4), (5, 4), (4, 5)}
    checked = routed = star_routed = contraction_cases = 0
    represented: set[tuple[int, int]] = set()
    for d, r in sorted(regimes):
        support = set(Q[:d])
        target = set(Q[d:])
        low_size = d + 18
        other_size = 44 - low_size
        for f_tuple in itertools.combinations(ALL_Q_EDGES, r):
            f_edges = {edge(u, v) for u, v in f_tuple}
            checked += 1
            assignment = saturating_assignment(f_edges, support, target)
            if assignment is not None:
                target_edges = {e for e in f_edges if e <= target}
                assert set(assignment) == target_edges
                assert len(set(assignment.values())) == len(assignment)
                assert set(assignment.values()) <= support
                for e, s in assignment.items():
                    assert all(edge(s, endpoint) not in f_edges for endpoint in e)
                # Run the full generic TK decoder once in every regime; the
                # exhaustive loop above checks the varying Hall certificates.
                if (d, r) not in represented:
                    graph_edges, branches = forced_unbridged_graph(
                        low_size, support, f_edges
                    )
                    paths = []
                    for e, s in assignment.items():
                        u, v = tuple(e)
                        paths.append([u, s, v])
                    check_tk27(graph_edges, branches, paths)
                    represented.add((d, r))
                routed += 1
                continue

            target_edges = [e for e in f_edges if e <= target]
            if len(target_edges) <= d:
                rigid = is_rigid_star_failure(f_edges, support, target)
                assert rigid is not None
                center, rigid_edges, blocking = rigid
                available = sorted(support - set(blocking))
                assert len(available) == len(rigid_edges) - 1
                long_edge = rigid_edges[0]
                graph_edges, branches = forced_unbridged_graph(
                    low_size, support, f_edges
                )
                if len(rigid_edges) == 1:
                    u, v = tuple(long_edge)
                    blocked_at_u = [s for s in support if edge(s, u) in f_edges]
                    blocked_at_v = [s for s in support if edge(s, v) in f_edges]
                    assert len(blocked_at_u) + len(blocked_at_v) == d
                    if blocked_at_u and blocked_at_v:
                        # s_v is G-adjacent to u; s_u is G-adjacent to v.
                        paths = [[u, blocked_at_v[0], blocked_at_u[0], v]]
                    else:
                        center = u if blocked_at_u else v
                        leaf = v if blocked_at_u else u
                        s0 = (blocked_at_u or blocked_at_v)[0]
                        b1, b2 = "b0", "b1"
                        graph_edges |= {
                            edge(center, b1),
                            edge(b1, b2),
                            edge(b2, s0),
                        }
                        paths = [[center, b1, b2, s0, leaf]]
                        assert sum(center in e for e in f_edges) == d + 1
                else:
                    leaf = next(iter(set(long_edge) - {center}))
                    s0 = blocking[0]
                    b1, b2 = "b0", "b1"
                    graph_edges |= {
                        edge(center, b1),
                        edge(b1, b2),
                        edge(b2, s0),
                    }
                    paths = [[center, b1, b2, s0, leaf]]
                    assert sum(center in e for e in f_edges) == d + 1
                for e, s in zip(rigid_edges[1:], available):
                    u, v = tuple(e)
                    paths.append([u, s, v])
                check_tk27(graph_edges, branches, paths)

                # Degree-cap availability whenever the long B path is used.
                if len(rigid_edges) > 1 or not (blocked_at_u and blocked_at_v):
                    b_size = other_size
                    assert b_size - (25 - (d + 1)) >= 2
                    assert b_size - (25 - (low_size + 1)) >= 20
                star_routed += 1
            else:
                # Here all d+1 complement edges lie in T.  The proof uses
                # one contracted high-edge color and the opposite incidence.
                assert len(target_edges) == d + 1 == r
                assert d in (3, 4)
                q = other_size - 18
                assert len(target) == q + 1
                contraction_cases += 1
    assert checked == 494_874
    assert routed == 492_357
    assert star_routed == 900
    assert contraction_cases == 1_617
    return checked, star_routed, contraction_cases


def contracted_classes(pair: frozenset[int]) -> tuple[frozenset[int], ...]:
    return (pair,) + tuple(frozenset((q,)) for q in Q if q not in pair)


def row_classes(row: frozenset[int], pair: frozenset[int]) -> frozenset[int]:
    classes = contracted_classes(pair)
    return frozenset(i for i, cls in enumerate(classes) if cls <= row)


def verify_contraction_escape() -> tuple[int, int]:
    """Check row-signature uniqueness and every common-row TK fallback."""
    signatures_checked = certificates = 0
    for d, q in ((3, 5), (4, 4)):
        support = set(Q[:d])
        target = set(Q[d:])
        for f_tuple in itertools.combinations(itertools.combinations(target, 2), d + 1):
            f_edges = {edge(u, v) for u, v in f_tuple}
            ordered_f = sorted(f_edges, key=lambda e: tuple(sorted(e)))
            signatures: dict[tuple[frozenset[int], ...], frozenset[int]] = {}
            for row_tuple in itertools.combinations(Q, q):
                row = frozenset(row_tuple)
                mapped = tuple(row_classes(row, pair) for pair in ordered_f)
                assert all(len(neighbors) in (q - 1, q) for neighbors in mapped)
                # A simultaneous obstruction must have degree q-1 for every
                # contraction.  Its complete signature identifies the row.
                if not all(len(neighbors) == q - 1 for neighbors in mapped):
                    continue
                assert mapped not in signatures or signatures[mapped] == row
                signatures[mapped] = row
                signatures_checked += 1

            # If all opposite rows share R, either the opposite block itself
            # gives K27 or one missing edge routes through it and the rest
            # route through the deficient block's support.
            low_a = {f"a{i}" for i in range(d + 18)}
            low_b = {f"b{i}" for i in range(q + 18)}
            target_a = set(target)
            for row in signatures.values():
                outside_row = set(Q) - set(row)
                outside_edges = [e for e in f_edges if e <= outside_row]
                if not outside_edges:
                    branches: set[int | str] = low_b | outside_row
                    graph_edges: set[frozenset[int | str]] = {
                        edge(u, v) for u, v in itertools.combinations(low_b, 2)
                    }
                    graph_edges |= {edge(b, x) for b in low_b for x in outside_row}
                    graph_edges |= {
                        edge(u, v)
                        for u, v in itertools.combinations(Q, 2)
                        if edge(u, v) not in f_edges
                    }
                    check_tk27(graph_edges, branches, [])
                else:
                    direct = outside_edges[0]
                    graph_edges, branches = forced_unbridged_graph(
                        d + 18, support, f_edges
                    )
                    b0 = "b0"
                    u, v = tuple(direct)
                    graph_edges |= {edge(u, b0), edge(b0, v)}
                    paths: list[list[int | str]] = [[u, b0, v]]
                    remaining = [e for e in ordered_f if e != direct]
                    assert len(remaining) == d
                    for pair, s in zip(remaining, sorted(support)):
                        x, y = tuple(pair)
                        paths.append([x, s, y])
                    check_tk27(graph_edges, branches, paths)
                certificates += 1
    return signatures_checked, certificates


def coloring_from_attachments(
    a_size: int,
    b_size: int,
    q_classes: list[set[int]],
    attach_a: dict[int, int],
    attach_b: dict[int, int],
    bridge: bool,
) -> list[set[int | str]]:
    """Decode the proof's generic coloring certificate."""
    a_vertices = [f"a{i}" for i in range(a_size)]
    b_vertices = [f"b{i}" for i in range(b_size)]
    classes: list[set[int | str]] = [set(cls) for cls in q_classes]
    for class_index, low_index in attach_a.items():
        classes[class_index].add(a_vertices[low_index])
    for class_index, low_index in attach_b.items():
        classes[class_index].add(b_vertices[low_index])
    used_a = set(attach_a.values())
    used_b = set(attach_b.values())
    residual_a = [v for i, v in enumerate(a_vertices) if i not in used_a]
    residual_b = [v for i, v in enumerate(b_vertices) if i not in used_b]
    assert len(residual_a) == len(residual_b)
    if bridge and "a0" in residual_a and "b0" in residual_b:
        zero = residual_b.index("b0")
        swap = 0 if residual_a[0] != "a0" else 1
        residual_b[zero], residual_b[swap] = residual_b[swap], residual_b[zero]
    classes.extend({a, b} for a, b in zip(residual_a, residual_b))
    return classes


def check_coloring_template(
    classes: list[set[int | str]],
    a_size: int,
    b_size: int,
    q_classes: list[set[int]],
    attach_a: dict[int, int],
    attach_b: dict[int, int],
    bridge: bool,
) -> None:
    """Check the decoder against exactly the complement edges it invokes."""
    a_vertices = [f"a{i}" for i in range(a_size)]
    b_vertices = [f"b{i}" for i in range(b_size)]
    h_edges: set[frozenset[int | str]] = {
        edge(a, b)
        for a in a_vertices
        for b in b_vertices
        if not (bridge and a == "a0" and b == "b0")
    }
    for q_class in q_classes:
        h_edges |= {edge(u, v) for u, v in itertools.combinations(q_class, 2)}
    for class_index, low_index in attach_a.items():
        h_edges |= {
            edge(a_vertices[low_index], q_vertex)
            for q_vertex in q_classes[class_index]
        }
    for class_index, low_index in attach_b.items():
        h_edges |= {
            edge(b_vertices[low_index], q_vertex)
            for q_vertex in q_classes[class_index]
        }
    assert len(classes) == 26
    assert sum(map(len, classes)) == 53
    assert len(set().union(*classes)) == 53
    for color_class in classes:
        assert all(edge(u, v) in h_edges for u, v in itertools.combinations(color_class, 2))


def verify_coloring_templates() -> int:
    checked = 0
    for a, b, bridge, _ in profiles():
        p, q = a - 18, b - 18
        # Nine singleton classes, p+1 and q+1 attachments, 17 low pairs.
        singleton = [{x} for x in Q]
        attach_a = {i: i for i in range(p + 1)}
        attach_b = {i: i + (1 if bridge else 0) for i in range(q + 1)}
        color = coloring_from_attachments(
            a,
            b,
            singleton,
            attach_a,
            attach_b,
            bool(bridge),
        )
        check_coloring_template(
            color, a, b, singleton, attach_a, attach_b, bool(bridge)
        )
        checked += 1

        if not bridge and (p, q) in ((3, 5), (4, 4)):
            # Eight high classes after contracting one complement edge;
            # p and q low attachments leave 18 residual pairs.
            pair_classes = [{0, 1}] + [{x} for x in Q[2:]]
            attach_a = {i + 1: i for i in range(p)}
            attach_b = {i: i for i in range(q)}
            color = coloring_from_attachments(
                a,
                b,
                pair_classes,
                attach_a,
                attach_b,
                False,
            )
            check_coloring_template(
                color, a, b, pair_classes, attach_a, attach_b, False
            )
            checked += 1
    assert checked == 8
    return checked


def verify_bridged_routing() -> int:
    checked = 0
    represented: set[tuple[int, int, int]] = set()
    for a, b, bridge, r in profiles():
        if not bridge:
            continue
        p, q = a - 18, b - 18
        assert r <= p
        support_a = set(Q[:p])
        qstar = Q[p]
        support_b = set(Q[p + 1 :])
        assert len(support_b) == q
        branch_q = support_b | {qstar}
        low_a = {f"a{i}" for i in range(a)}
        low_b = {f"b{i}" for i in range(b)}
        branches: set[int | str] = low_a | branch_q
        for f_tuple in itertools.combinations(ALL_Q_EDGES, r):
            f_edges = {edge(u, v) for u, v in f_tuple}
            assignment = saturating_assignment(f_edges, support_a, branch_q)
            assert assignment is not None
            target_edges = {e for e in f_edges if e <= branch_q}
            assert set(assignment) == target_edges
            assert len(set(assignment.values())) == len(assignment)
            for e, s in assignment.items():
                assert s in support_a
                assert all(edge(s, endpoint) not in f_edges for endpoint in e)
            key = (a, b, r)
            if key not in represented:
                graph_edges: set[frozenset[int | str]] = {
                    edge(u, v) for u, v in itertools.combinations(low_a, 2)
                }
                graph_edges |= {
                    edge(a_vertex, q_vertex)
                    for a_vertex in low_a
                    for q_vertex in branch_q
                    if not (a_vertex == "a0" and q_vertex == qstar)
                }
                graph_edges |= {
                    edge(u, v)
                    for u, v in itertools.combinations(Q, 2)
                    if edge(u, v) not in f_edges
                }
                graph_edges |= {
                    edge("a0", "b0"),
                    edge("b0", "b1"),
                    edge("b1", qstar),
                }
                paths = [["a0", "b0", "b1", qstar]]
                for e, s in assignment.items():
                    u, v = tuple(e)
                    paths.append([u, s, v])
                check_tk27(graph_edges, branches, paths)
                represented.add(key)
            checked += 1
    assert checked == 66_046
    return checked


def main() -> None:
    profile_list = profiles()
    colorings = verify_coloring_templates()
    unbridged, star, contractions = verify_unbridged_routing()
    signatures, escape = verify_contraction_escape()
    bridged = verify_bridged_routing()
    summary = (
        f"profiles={len(profile_list)};colorings={colorings};"
        f"unbridged_F={unbridged};star_TK={star};"
        f"all_target={contractions};row_signatures={signatures};"
        f"common_row_TK={escape};"
        f"bridged_F={bridged};conclusion=m713_h_at_least_10"
    )
    digest = hashlib.sha256(summary.encode()).hexdigest()
    print("PASS Albertson r=27 order-53 h=9 closure")
    print(f"exact Gallai profiles checked: {len(profile_list)}")
    print(f"normalized coloring decoders checked: {colorings}")
    print(f"unbridged high-complement graphs checked: {unbridged}")
    print(f"rigid star TK27 templates checked: {star}")
    print(f"all-target contraction cases checked: {contractions}")
    print(f"contracted row signatures checked: {signatures}")
    print(f"common-row TK27 fallbacks checked: {escape}")
    print(f"bridged high-complement graphs checked: {bridged}")
    print(f"certificate_sha256={digest}")
    print("conclusion: every remaining counterexample has at least ten high vertices")


if __name__ == "__main__":
    main()
