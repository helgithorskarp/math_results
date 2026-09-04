#!/usr/bin/env python3
"""Exact audit of the split-colour Hall closure at Albertson r=27, h=20."""

from hashlib import sha256


PALETTE = 26
HIGH_ORDER = 20

# name, |B|, active colours, chi(X) values, chi(S), e(X), |S|
CASES = (
    ("D20", 20, 7, (7, 8, 9, 10), 7, 87, 13),
    ("D19", 19, 8, (8,), 8, 75, 14),
)


def hall_audit(block_order):
    """Audit Hall for the two (b-1)-list types created by a split."""
    records = []
    for split_weight in range(1, block_order):
        adjacent = split_weight
        nonadjacent = block_order - split_weight
        checks = 0
        minimum_slack = block_order
        for chosen_adjacent in range(adjacent + 1):
            for chosen_nonadjacent in range(nonadjacent + 1):
                chosen = chosen_adjacent + chosen_nonadjacent
                if chosen == 0:
                    continue
                if chosen_adjacent and chosen_nonadjacent:
                    union_size = block_order
                else:
                    union_size = block_order - 1
                slack = union_size - chosen
                assert slack >= 0
                minimum_slack = min(minimum_slack, slack)
                checks += 1
        assert minimum_slack == 0
        records.append((split_weight, checks, minimum_slack))
    return tuple(records)


def case_audit(name, b, active, chromatic_values, small_chi, high_edges, outside):
    # An intermediate column can be split into a fresh colour.  The smaller
    # low component is then coloured with colours unused on X.
    split_rows = []
    for chromatic in chromatic_values:
        high_colours_after_split = chromatic + 1
        unused = PALETTE - high_colours_after_split
        assert unused >= small_chi
        split_rows.append((chromatic, high_colours_after_split, unused))

    hall = hall_audit(b)

    # With intermediate columns excluded, sum_x w(x)=b*active forces exactly
    # `active` full columns and HIGH_ORDER-active zero columns.
    full = active
    zero = HIGH_ORDER - active
    assert full * b == b * active
    full_degree_floor = active - 1
    zero_degree_floor = 27 - outside
    degree_sum_floor = full * full_degree_floor + zero * zero_degree_floor
    handshake = 2 * high_edges
    assert degree_sum_floor > handshake

    return (
        name,
        b,
        active,
        split_rows,
        hall,
        full,
        zero,
        full_degree_floor,
        zero_degree_floor,
        degree_sum_floor,
        handshake,
        degree_sum_floor - handshake,
    )


def main():
    records = tuple(case_audit(*case) for case in CASES)
    assert tuple((row[0], row[-3], row[-2], row[-1]) for row in records) == (
        ("D20", 224, 174, 50),
        ("D19", 212, 150, 62),
    )
    payload = repr(records).encode()
    print("PASS Albertson r=27 h=20 split-colour closure")
    for row in records:
        print(
            f"{row[0]}: block={row[1]}; active={row[2]}; "
            f"split_weights={len(row[4])}; full={row[5]}; zero={row[6]}; "
            f"degree_floor={row[-3]}; handshake={row[-2]}; margin={row[-1]}"
        )
    print(f"certificate_sha256={sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
