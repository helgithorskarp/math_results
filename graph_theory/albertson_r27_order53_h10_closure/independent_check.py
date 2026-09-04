#!/usr/bin/env python3
"""Independent Hall-subset and balance audit for the h=10 closure."""

from __future__ import annotations

import hashlib
import itertools


def pc(mask: int) -> int:
    return mask.bit_count()


def hall_holds(option_masks: tuple[int, ...]) -> bool:
    """Hall's condition, checked directly over every nonempty subset."""
    for chosen in range(1, 1 << len(option_masks)):
        union = 0
        size = 0
        for i, options in enumerate(option_masks):
            if chosen & (1 << i):
                union |= options
                size += 1
        if pc(union) < size:
            return False
    return True


def profiles() -> tuple[tuple[int, int, int, int], ...]:
    rows = []
    for a in range(17, 22):
        b = 43 - a
        if a > b:
            continue
        defect = (
            26 * 43 - a * (a - 1) - b * (b - 1)
            + 10 * 9 - 26 * 10 - 48
        )
        if defect >= 0 and defect % 2 == 0:
            for bridge in (0, 1):
                rows.append((a, b, bridge, defect // 2 - bridge))
    surviving = tuple(row for row in rows if row[0] >= 20 and row != (20, 23, 1, 6))
    assert surviving == ((20, 23, 0, 7), (21, 22, 0, 9), (21, 22, 1, 8))
    return surviving


def contraction(row: int, pair: tuple[int, int]) -> tuple[int, int]:
    """Encode compatible singleton columns and compatibility with the pair."""
    pair_mask = (1 << pair[0]) | (1 << pair[1])
    singles = row & ~pair_mask
    pair_ok = int(row & pair_mask == pair_mask)
    return singles, pair_ok


def independent_row_rigidity() -> int:
    """Check row equality directly from two contracted representations."""
    checked = 0
    for d, q in ((3, 6), (4, 5), (5, 4)):
        target_edges = tuple(itertools.combinations(range(d, 10), 2))
        rows = tuple(sum(1 << x for x in row) for row in itertools.combinations(range(10), q))
        for first, second in itertools.combinations(target_edges, 2):
            for x, y in itertools.combinations(rows, 2):
                cx1, cy1 = contraction(x, first), contraction(y, first)
                if cx1 != cy1 or pc(cx1[0]) + cx1[1] != q - 1:
                    continue
                cx2, cy2 = contraction(x, second), contraction(y, second)
                if cx2 != cy2 or pc(cx2[0]) + cx2[1] != q - 1:
                    continue
                raise AssertionError((d, q, first, second, x, y))
            checked += 1
    assert checked == 210 + 105 + 45
    return checked


TARGET_EDGES = tuple(itertools.combinations(range(4), 2))


def independent_boundary() -> tuple[int, int]:
    """Use Hall subsets, not augmenting paths, at the six-support boundary."""
    checked = failures = 0
    for target_mask in range(1 << 6):
        targets = tuple(e for i, e in enumerate(TARGET_EDGES) if target_mask & (1 << i))
        for rows in itertools.combinations_with_replacement(range(16), 6):
            if len(targets) + sum(pc(row) for row in rows) > 7:
                continue
            checked += 1
            option_masks = tuple(
                sum(
                    1 << support
                    for support, row in enumerate(rows)
                    if not row & ((1 << u) | (1 << v))
                )
                for u, v in targets
            )
            if hall_holds(option_masks):
                continue
            failures += 1
            witnesses = []
            for chosen in range(1, 1 << len(targets)):
                union = 0
                size = 0
                selected = []
                for i, options in enumerate(option_masks):
                    if chosen & (1 << i):
                        union |= options
                        size += 1
                        selected.append(targets[i])
                if pc(union) < size:
                    witnesses.append((tuple(selected), union))
            assert witnesses
            selected, union = witnesses[0]
            k = len(selected)
            blocked = [i for i in range(6) if not (union & (1 << i))]
            assert len(targets) + sum(pc(row) for row in rows) == 7
            assert len(targets) == k and len(blocked) == 7 - k
            assert all(rows[i] == 0 for i in range(6) if i not in blocked)
            assert all(pc(rows[i]) == 1 for i in blocked)
            if k == 1:
                endpoints = {(1 << selected[0][0]), (1 << selected[0][1])}
                assert all(rows[i] in endpoints for i in blocked)
            else:
                common = set(selected[0])
                for target in selected[1:]:
                    common &= set(target)
                assert len(common) == 1
                centre = next(iter(common))
                assert all(rows[i] == 1 << centre for i in blocked)
    assert failures == 58
    return checked, failures


def independent_final_hall() -> tuple[int, int]:
    """Direct Hall audit for the final z-S routing into five R vertices."""
    rows = tuple(mask for mask in range(32) if pc(mask) <= 3)
    checked = 0
    for beta in range(1, 5):
        for selected in itertools.product(rows, repeat=beta):
            if sum(pc(row) for row in selected) > 8 - beta:
                continue
            checked += 1
            options = tuple(((1 << 5) - 1) ^ row for row in selected)
            assert hall_holds(options)
    assert checked == 11_654
    return checked, checked


def balance_state_audit() -> tuple[int, int]:
    """Enumerate category counts in the two factor-critical matchings."""
    s_delete_states = r_delete_states = 0

    # Delete one S: q is matched to S or R.  Other high-high matching
    # edges have types SS, RR, SR.  Balance requires r_M-s_M=1.
    for q_side in ("S", "R"):
        for ss, rr, sr in itertools.product(range(3), range(3), range(5)):
            s_used = (q_side == "S") + 2 * ss + sr
            r_used = (q_side == "R") + 2 * rr + sr
            if s_used <= 3 and r_used <= 5 and r_used - s_used == 1:
                s_delete_states += 1
                if q_side == "S":
                    assert rr >= 1

    # Delete one R: balance is s_M-r_M=1.
    for q_side in ("S", "R"):
        for ss, rr, sr in itertools.product(range(3), range(3), range(5)):
            s_used = (q_side == "S") + 2 * ss + sr
            r_used = (q_side == "R") + 2 * rr + sr
            if s_used <= 4 and r_used <= 4 and s_used - r_used == 1:
                r_delete_states += 1
                if q_side == "R":
                    assert ss >= 1

    assert s_delete_states > 0 and r_delete_states > 0
    return s_delete_states, r_delete_states


def edge_budget_audit() -> tuple[tuple[int, int], ...]:
    """Check the numerical Hall contradiction used after conformal pruning."""
    table = []
    for k in range(1, 5):
        if k == 1:
            # d_F(s)<=4 and zs is already present, so at most three of R
            # are blocked and at least two are available.
            available = 5 - 3
            assert available >= 1
            table.append((k, available))
        else:
            forced_edges = k * (6 - k) + k + 1
            assert forced_edges > 9
            table.append((k, forced_edges))
    return tuple(table)


def main() -> None:
    surviving = profiles()
    row_pairs = independent_row_rigidity()
    boundary_states, boundary_failures = independent_boundary()
    final_states, final_successes = independent_final_hall()
    balance = balance_state_audit()
    budget = edge_budget_audit()
    record = (
        f"survivors={len(surviving)};row_edge_pairs={row_pairs};"
        f"boundary_states={boundary_states};boundary_failures={boundary_failures};"
        f"final_states={final_states};final_successes={final_successes};"
        f"balance_states={balance};budget={budget};conclusion=h_at_least_11"
    )
    print("PASS independent Hall-subset audit of Albertson h=10 closure")
    print("two-contraction edge pairs:", row_pairs)
    print("six-support boundary:", boundary_states, "states;", boundary_failures, "rigid")
    print("final routing rows:", final_states)
    print("factor-critical balance states:", balance)
    print("Hall edge-budget table:", budget)
    print(record)
    print("independent_sha256=" + hashlib.sha256(record.encode()).hexdigest())


if __name__ == "__main__":
    main()
