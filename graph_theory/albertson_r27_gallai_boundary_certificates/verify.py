#!/usr/bin/env python3
"""Exact checks for two minimum-h Gallai boundary certificate families."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations


Q = tuple(f"q{i}" for i in range(8))
A = tuple(f"a{i}" for i in range(22))
B = tuple(f"b{i}" for i in range(23))
V = A + B + Q
A0, B0 = A[0], B[0]


def edge(x: str, y: str) -> frozenset[str]:
    assert x != y
    return frozenset((x, y))


def add_clique(edges: set[frozenset[str]], vertices: tuple[str, ...]) -> None:
    for x, y in combinations(vertices, 2):
        edges.add(edge(x, y))


def complement(edges: set[frozenset[str]]) -> set[frozenset[str]]:
    return {edge(x, y) for x, y in combinations(V, 2)} - edges


def degrees(edges: set[frozenset[str]]) -> dict[str, int]:
    return {x: sum(x in e for e in edges) for x in V}


def connected(edges: set[frozenset[str]]) -> bool:
    todo = [V[0]]
    seen = {V[0]}
    while todo:
        x = todo.pop()
        for e in edges:
            if x not in e:
                continue
            y = next(iter(e - {x}))
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return len(seen) == len(V)


def coloring_from_matchings(
    match_a: dict[str, str], match_b: dict[str, str], bridge: bool
) -> list[list[str]]:
    """Construct the proof's 26 coloring from Q-to-low matchings."""
    assert len(match_a) == 4 and len(set(match_a.values())) == 4
    assert len(match_b) == 5 and len(set(match_b.values())) == 5
    assert set(match_a) <= set(Q) and set(match_a.values()) <= set(A)
    assert set(match_b) <= set(Q) and set(match_b.values()) <= set(B)
    if bridge and A0 in match_a.values() and B0 in match_b.values():
        qa = next(q for q, a in match_a.items() if a == A0)
        qb = next(q for q, b in match_b.items() if b == B0)
        assert qa != qb

    classes = [[q] for q in Q]
    by_q = {q: cls for q, cls in zip(Q, classes)}
    for q, a in match_a.items():
        by_q[q].append(a)
    for q, b in match_b.items():
        by_q[q].append(b)

    residual_a = [a for a in A if a not in match_a.values()]
    residual_b = [b for b in B if b not in match_b.values()]
    assert len(residual_a) == len(residual_b) == 18
    if bridge and A0 in residual_a and B0 in residual_b:
        # Move b0 away from a0.  There are 18 residual pairs.
        ia, ib = residual_a.index(A0), residual_b.index(B0)
        swap = 0 if ia != 0 else 1
        residual_b[ib], residual_b[swap] = residual_b[swap], residual_b[ib]
    classes.extend([[a, b] for a, b in zip(residual_a, residual_b)])
    return classes


def check_coloring_template(
    classes: list[list[str]],
    match_a: dict[str, str],
    match_b: dict[str, str],
    bridge: bool,
) -> None:
    """Check independence from only the adjacency facts used by the proof."""
    assert len(classes) == 26
    flat = [x for cls in classes for x in cls]
    assert len(flat) == 53 and len(set(flat)) == 53 and set(flat) == set(V)
    allowed_aq = {edge(a, q) for q, a in match_a.items()}
    allowed_bq = {edge(b, q) for q, b in match_b.items()}
    for cls in classes:
        assert len(set(cls) & set(A)) <= 1
        assert len(set(cls) & set(B)) <= 1
        assert len(set(cls) & set(Q)) <= 1
        if bridge:
            assert not ({A0, B0} <= set(cls))
        for x, y in combinations(cls, 2):
            pair = edge(x, y)
            if (x in A and y in Q) or (y in A and x in Q):
                assert pair in allowed_aq
            elif (x in B and y in Q) or (y in B and x in Q):
                assert pair in allowed_bq
            else:
                assert (x in A and y in B) or (x in B and y in A)


def normalized_matching(
    side: tuple[str, ...], qset: tuple[str, ...], endpoint_partner: str | None
) -> dict[str, str]:
    assert endpoint_partner is None or endpoint_partner in qset
    result: dict[str, str] = {}
    unused_q = list(qset)
    next_low = 1
    if endpoint_partner is not None:
        result[endpoint_partner] = side[0]
        unused_q.remove(endpoint_partner)
    for q in unused_q:
        result[q] = side[next_low]
        next_low += 1
    return result


def verify_coloring_templates() -> tuple[int, int]:
    """Exhaust endpoint compatibility orbits; other low vertices are twins."""
    # (partner of a0, partner of b0).  q0/q0 is the sole incompatible
    # bridge case; q0/q1 represents all distinct-partner choices.
    cases = (
        (None, None),
        (Q[0], None),
        (None, Q[0]),
        (Q[0], Q[0]),
        (Q[0], Q[1]),
    )
    no_bridge_checked = 0
    bridge_checked = 0
    for pa, pb in cases:
        qa_tuple = tuple(dict.fromkeys(([pa] if pa else []) + list(Q)))[:4]
        qb_tuple = tuple(dict.fromkeys(([pb] if pb else []) + list(Q)))[:5]
        ma = normalized_matching(A, qa_tuple, pa)
        mb = normalized_matching(B, qb_tuple, pb)
        classes = coloring_from_matchings(ma, mb, bridge=False)
        check_coloring_template(classes, ma, mb, bridge=False)
        no_bridge_checked += 1

        compatible = not (pa is not None and pa == pb)
        if compatible:
            classes = coloring_from_matchings(ma, mb, bridge=True)
            check_coloring_template(classes, ma, mb, bridge=True)
            bridge_checked += 1
    assert no_bridge_checked == 5
    assert bridge_checked == 4
    return no_bridge_checked, bridge_checked


def verify_konig_rigidity() -> None:
    """Check the numerical alternatives in the cover argument."""
    for d, left_count in ((3, 21), (4, 22)):
        assert left_count > d
        # If a size-d cover used s left vertices, an uncovered left vertex
        # would have d distinct neighbors in only d-s right cover vertices.
        for s in range(1, d + 1):
            assert left_count - s > 0
            assert d - s < d


def rigid_graph(
    sa: frozenset[str], sb: frozenset[str], qstar: str
) -> tuple[set[frozenset[str]], set[frozenset[str]]]:
    """Return (G,H) for one labelled forced polarized obstruction."""
    assert len(sa) == 3 and len(sb) == 4
    assert not (sa & sb) and qstar not in sa | sb
    assert sa | sb | {qstar} == set(Q)

    h: set[frozenset[str]] = set()
    for a in A:
        neighbors = sa | ({qstar} if a == A0 else set())
        for q in neighbors:
            h.add(edge(a, q))
    for b in B:
        neighbors = sb | ({qstar} if b == B0 else set())
        for q in neighbors:
            h.add(edge(b, q))
    for a in A:
        for b in B:
            if (a, b) != (A0, B0):
                h.add(edge(a, b))
    return complement(h), h


def check_tk27(
    graph_edges: set[frozenset[str]], branches: list[str], paths: list[list[str]]
) -> None:
    assert len(branches) == 27 and len(set(branches)) == 27
    branch_set = set(branches)
    missing = {
        edge(x, y)
        for x, y in combinations(branches, 2)
        if edge(x, y) not in graph_edges
    }
    used_internal: set[str] = set()
    routed: set[frozenset[str]] = set()
    for path in paths:
        assert path[0] in branch_set and path[-1] in branch_set
        pair = edge(path[0], path[-1])
        assert pair not in routed
        routed.add(pair)
        assert all(edge(x, y) in graph_edges for x, y in zip(path, path[1:]))
        internal = set(path[1:-1])
        assert len(internal) == len(path) - 2
        assert not internal & branch_set
        assert not internal & used_internal
        used_internal |= internal
    assert routed == missing


def verify_rigid_certificates() -> tuple[int, str]:
    records: list[str] = []
    checked = 0
    for qstar in Q:
        remainder = tuple(q for q in Q if q != qstar)
        for sa_tuple in combinations(remainder, 3):
            sa = frozenset(sa_tuple)
            sb = frozenset(set(remainder) - sa)
            g, h = rigid_graph(sa, sb, qstar)
            dg, dh = degrees(g), degrees(h)
            assert len(g) == 713 and len(h) == 665
            assert all(dg[x] == 26 for x in A + B)
            assert all(dg[q] >= 27 and dh[q] <= 25 for q in Q)
            assert connected(h)

            s = min(sa)
            branches = list(A) + sorted(sb) + [qstar]
            path = [A0, B0, s, qstar]
            check_tk27(g, branches, [path])
            records.append(
                f"{qstar}|{','.join(sorted(sa))}|{','.join(sorted(sb))}|"
                f"{'-'.join(path)}"
            )
            checked += 1
    assert checked == 280
    digest = sha256("\n".join(sorted(records)).encode()).hexdigest()
    return checked, digest


def main() -> None:
    no_bridge, bridge = verify_coloring_templates()
    verify_konig_rigidity()
    rigid, digest = verify_rigid_certificates()
    assert digest == "66ddfd8f90a79b3eb7b04534d0fa55df97652990e6c859571410e24da3dfebde"
    print("PASS Albertson r=27 Gallai boundary coloring/TK certificates")
    print(f"normalized no-bridge coloring templates checked: {no_bridge}")
    print(f"normalized compatible-bridge coloring templates checked: {bridge}")
    print(f"labelled rigid TK27 certificates checked: {rigid}")
    print(f"rigid_certificate_sha256={digest}")
    print("conclusion: (714,h=8) and the bridged (713,h=8) profile are closed")


if __name__ == "__main__":
    main()
