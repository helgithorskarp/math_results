#!/usr/bin/env python3
"""Exact audit for the Albertson r=27 h=10--12 structural reduction."""

from hashlib import sha256
from itertools import combinations


K = 27
N = 53
EXCESS = 48


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

EXPECTED_CLOSED = {
    (10, 19, 24, 0, 3),
    (10, 19, 24, 1, 2),
    (10, 20, 23, 1, 6),
    (11, 18, 24, 1, 4),
    (12, 17, 24, 1, 6),
}


def edge(u: int, v: int) -> frozenset[int]:
    assert u != v
    return frozenset((u, v))


def profile_rows(h: int) -> tuple[tuple[int, int, int, int, int], ...]:
    """Return feasible (a,b,p,q,D=t+r) rows from the exact excess identity."""
    low = N - h
    minimum_block = K - h
    assert 2 * (minimum_block - 1) > K - 1
    assert low > K - 1
    assert 3 * minimum_block > low

    rows = []
    for a in range(minimum_block, K):
        b = low - a
        if not (a <= b < K and b >= minimum_block):
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
        D = defect // 2
        assert p + q == h - 1
        rows.append((a, b, p, q, D))
    return tuple(rows)


def exact_profiles():
    profiles = []
    for h in range(10, 13):
        rows = profile_rows(h)
        assert rows == EXPECTED[h]
        for a, b, p, q, D in rows:
            for bridge in (0, 1):
                r = D - bridge
                assert r >= 0
                profiles.append((h, a, b, p, q, bridge, r))
    assert len(profiles) == 22
    return tuple(profiles)


def closure_audit(profiles):
    closed = set()
    for h, a, b, p, q, bridge, r in profiles:
        if bridge == 0 and r <= min(p, q) + 1:
            closed.add((h, a, b, bridge, r))
        if bridge == 1 and r <= max(p, q):
            closed.add((h, a, b, bridge, r))
    assert closed == EXPECTED_CLOSED

    survivors_h10 = {
        (a, b, bridge, r)
        for h, a, b, _, _, bridge, r in profiles
        if h == 10 and (h, a, b, bridge, r) not in closed
    }
    assert survivors_h10 == {
        (20, 23, 0, 7),
        (21, 22, 0, 9),
        (21, 22, 1, 8),
    }
    return closed, survivors_h10


def matching(targets, available, support):
    """Return a target-to-support injection, or None."""
    ordered = sorted(targets, key=lambda item: (len(available[item]), tuple(item)))

    def extend(index, used, assignment):
        if index == len(ordered):
            return dict(assignment)
        target = ordered[index]
        for s in sorted(available[target] - used):
            assignment[target] = s
            result = extend(index + 1, used | {s}, assignment)
            if result is not None:
                return result
            del assignment[target]
        return None

    return extend(0, set(), {})


def rigid_witness(f_edges, support, target):
    """Verify the equality case of the boundary Hall count."""
    targets = {pair for pair in f_edges if pair <= target}
    available = {
        pair: {
            s
            for s in support
            if all(edge(s, endpoint) not in f_edges for endpoint in pair)
        }
        for pair in targets
    }
    for size in range(1, len(targets) + 1):
        for chosen_tuple in combinations(targets, size):
            chosen = set(chosen_tuple)
            union = set().union(*(available[pair] for pair in chosen))
            if len(union) >= size:
                continue
            blocked = support - union
            if len(blocked) != len(support) - size + 1:
                continue
            if len(chosen) >= 2:
                common = set.intersection(*(set(pair) for pair in chosen))
                if len(common) != 1:
                    continue
                center = next(iter(common))
                blockers = {edge(s, center) for s in blocked}
            else:
                sole = next(iter(chosen))
                blockers = {
                    pair
                    for pair in f_edges
                    if len(pair & support) == 1 and len(pair & sole) == 1
                }
                if {next(iter(pair & support)) for pair in blockers} != blocked:
                    continue
            if f_edges == chosen | blockers:
                return True
    return False


def boundary_hall_audit():
    """Exhaust the d=2, e(F)=3 case used at the h=10 boundary."""
    q_vertices = tuple(range(10))
    support = set(q_vertices[:2])
    target = set(q_vertices[2:])
    all_edges = tuple(edge(u, v) for u, v in combinations(q_vertices, 2))
    routed = rigid = all_target = 0

    for chosen in combinations(all_edges, 3):
        f_edges = set(chosen)
        targets = {pair for pair in f_edges if pair <= target}
        available = {
            pair: {
                s
                for s in support
                if all(edge(s, endpoint) not in f_edges for endpoint in pair)
            }
            for pair in targets
        }
        if matching(targets, available, support) is not None:
            routed += 1
        elif targets == f_edges:
            assert len(targets) == len(support) + 1
            all_target += 1
        else:
            assert rigid_witness(f_edges, support, target)
            rigid += 1

    assert routed + rigid + all_target == 14_190
    return routed, rigid, all_target


def main():
    assert 2 * 713 - 26 * 53 == EXCESS
    profiles = exact_profiles()
    closed, survivors = closure_audit(profiles)
    routed, rigid, all_target = boundary_hall_audit()
    record = (
        f"profiles={len(profiles)};closed={len(closed)};"
        f"h10_survivors={len(survivors)};hall_total={routed+rigid+all_target};"
        f"routed={routed};rigid={rigid};all_target={all_target}"
    )
    print("PASS Albertson r=27 h=10--12 structural reduction")
    print("closed profiles:", sorted(closed))
    print("h=10 survivors:", sorted(survivors))
    print(f"boundary Hall split: routed={routed}, rigid={rigid}, all_target={all_target}")
    print(record)
    print(f"certificate_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
