#!/usr/bin/env python3
"""Exact arithmetic checks for the r=27 conformal-complement note."""

from itertools import product


def verify_class_sizes():
    k = 27
    # Subtract the required two vertices from each of k-1 classes.  The
    # residual totals are respectively zero and one, so these are all the
    # possible ordered layouts without a large stars-and-bars enumeration.
    odd = [(2,) * (k - 1)]
    even = []
    for triple_position in range(k - 1):
        layout = [2] * (k - 1)
        layout[triple_position] += 1
        even.append(tuple(layout))
    assert set(odd) == {(2,) * (k - 1)}
    assert len(even) == k - 1
    assert all(sorted(c) == [2] * (k - 2) + [3] for c in even)
    return len(odd), len(even)


def verify_matching_balance():
    # In a perfect matching on equal sides, the numbers of internal edges
    # on the two sides agree.  After deleting one A vertex and matching the
    # root to another A vertex, B has two more remaining vertices, so it
    # uses exactly one more internal edge.
    q = 26
    equal_solutions = []
    deleted_a_solutions = []
    for p_a, p_b, cross in product(
        range(q // 2 + 1), range(q // 2 + 1), range(q + 1)
    ):
        if 2 * p_a + cross == q and 2 * p_b + cross == q:
            equal_solutions.append((p_a, p_b, cross))
            assert p_a == p_b
        if 2 * p_a + cross == q - 2 and 2 * p_b + cross == q:
            deleted_a_solutions.append((p_a, p_b, cross))
            assert p_b == p_a + 1
    assert len(equal_solutions) == q // 2 + 1
    assert len(deleted_a_solutions) == q // 2
    return len(equal_solutions), len(deleted_a_solutions)


def verify_order53():
    rows = []
    n = 53
    max_h_degree = 26
    shadow_cap = max_h_degree * (max_h_degree - 1) // 2
    for m, expected_low, expected_cross, lo_diff, hi_diff in (
        (713, 5, 314, -37, 11),
        (714, 3, 313, -38, 12),
        (715, 1, 312, -39, 13),
    ):
        excess = 2 * m - 26 * n
        low_count = n - excess
        e_h = n * (n - 1) // 2 - m
        local_sum = e_h - max_h_degree
        cross_lower = local_sum - shadow_cap
        # Substitute z=local_sum-x-y into the two degree-capacity bounds.
        upper_diff = 26 * 25 - local_sum
        lower_diff = -(26 * 26 - local_sum)
        assert (low_count, cross_lower, lower_diff, upper_diff) == (
            expected_low,
            expected_cross,
            lo_diff,
            hi_diff,
        )

        feasible = []
        for x in range(shadow_cap + 1):
            for y in range(1, shadow_cap + 1 - x):
                z = local_sum - x - y
                if not 0 <= z <= 26 * 26:
                    continue
                if 2 * x + z > 26 * 25 or 2 * y + z > 26 * 26:
                    continue
                feasible.append((x, y, z))
                assert z >= expected_cross
                assert lo_diff <= x - y <= hi_diff
        assert feasible
        rows.append((m, e_h, excess, low_count, local_sum, cross_lower))
    return rows


def verify_order54():
    n, m = 54, 726
    excess = 2 * m - 26 * n
    low_count = n - excess
    e_h = n * (n - 1) // 2 - m
    local_sum = e_h - 27
    assert (excess, low_count, e_h, local_sum) == (48, 6, 705, 678)

    feasible = []
    for x in range(1, 27 * 26 // 2 + 1):
        for y in range(26 * 25 // 2 + 1):
            z = local_sum - x - y
            if not 27 <= z <= 27 * 26:
                continue
            if 2 * x + z > 27 * 26 or 2 * y + z > 26 * 27:
                continue
            feasible.append((x, y, z))
            assert abs(x - y) <= 24
    assert feasible
    return e_h, excess, low_count, local_sum, len(feasible)


def main():
    odd_layouts, even_layouts = verify_class_sizes()
    equal_balances, deleted_balances = verify_matching_balance()
    rows53 = verify_order53()
    row54 = verify_order54()
    print("PASS: Stehlik class-size distributions")
    print(f"  order 53: {odd_layouts} ordered layout")
    print(f"  order 54: {even_layouts} ordered placements of the triple")
    print("PASS: perfect-matching side-balance identities")
    print(f"  equal sides: {equal_balances} count profiles")
    print(f"  after deleting A and matching the root: {deleted_balances} profiles")
    print("PASS: order-53 paired-shadow arithmetic")
    for m, e_h, excess, low, local_sum, cross_lower in rows53:
        print(
            f"  m={m}: e(H)={e_h}, excess={excess}, low>={low}, "
            f"x+y+z={local_sum}, z>={cross_lower}"
        )
    e_h, excess, low, local_sum, profiles = row54
    print("PASS: order-54 conformal-diamond arithmetic")
    print(
        f"  e(H)={e_h}, excess={excess}, low>={low}, "
        f"x+y+z={local_sum}, arithmetic profiles={profiles}"
    )


if __name__ == "__main__":
    main()
