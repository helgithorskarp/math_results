#!/usr/bin/env python3
"""Independent Hall-subset audit of the h=9 finite certificate kernel."""

from hashlib import sha256
from itertools import combinations


Q = frozenset(range(9))
EDGES = tuple(frozenset(e) for e in combinations(Q, 2))


def route_hall(d: int, f: frozenset[frozenset[int]]) -> bool:
    s_part = frozenset(range(d))
    t_part = Q - s_part
    missing = tuple(e for e in f if e <= t_part)
    available = {
        e: frozenset(
            s for s in s_part if all(frozenset((s, x)) not in f for x in e)
        )
        for e in missing
    }
    for size in range(1, len(missing) + 1):
        for chosen in combinations(missing, size):
            if len(frozenset().union(*(available[e] for e in chosen))) < size:
                return False
    return True


def route_counts() -> tuple[int, int, int, int]:
    ordinary = star_boundary = all_target = 0
    total = 0
    for d, r in ((2, 1), (6, 1), (3, 4), (5, 4), (4, 5)):
        t_part = Q - frozenset(range(d))
        for chosen in combinations(EDGES, r):
            f = frozenset(chosen)
            total += 1
            if route_hall(d, f):
                ordinary += 1
            elif sum(e <= t_part for e in f) == d + 1:
                all_target += 1
            else:
                star_boundary += 1
    assert (total, ordinary, star_boundary, all_target) == (
        494_874,
        492_357,
        900,
        1_617,
    )
    return total, ordinary, star_boundary, all_target


def contraction_signature(
    row: frozenset[int], f: frozenset[frozenset[int]]
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    signature = []
    for pair in sorted(f, key=lambda e: tuple(sorted(e))):
        pair_available = int(pair <= row)
        singleton_available = tuple(sorted(row - pair))
        signature.append((pair_available, singleton_available))
    return tuple(signature)


def signature_count() -> int:
    checked = 0
    for d, q in ((3, 5), (4, 4)):
        target = Q - frozenset(range(d))
        target_edges = tuple(frozenset(e) for e in combinations(target, 2))
        for chosen in combinations(target_edges, d + 1):
            f = frozenset(chosen)
            seen: dict[tuple[tuple[int, tuple[int, ...]], ...], frozenset[int]] = {}
            for row_tuple in combinations(Q, q):
                row = frozenset(row_tuple)
                # A simultaneous contracted-matching obstruction requires
                # the row to meet every contracted edge.
                if not all(row & e for e in f):
                    continue
                signature = contraction_signature(row, f)
                assert signature not in seen or seen[signature] == row
                seen[signature] = row
                checked += 1
    assert checked == 92_385
    return checked


def bridged_count() -> int:
    count = 0
    for d, r in ((2, 0), (3, 3), (4, 4)):
        for chosen in combinations(EDGES, r):
            f = frozenset(chosen)
            assert route_hall(d, f)
            count += 1
    assert count == 66_046
    return count


def main() -> None:
    total, ordinary, star, all_target = route_counts()
    signatures = signature_count()
    bridged = bridged_count()
    record = (
        f"total={total};ordinary={ordinary};star={star};"
        f"all_target={all_target};signatures={signatures};bridged={bridged}"
    )
    print("PASS independent Hall-subset and contraction-signature audit")
    print(record)
    print(f"audit_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
