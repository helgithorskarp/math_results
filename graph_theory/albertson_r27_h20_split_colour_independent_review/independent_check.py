#!/usr/bin/env python3
"""Independent exhaustive audit of the Albertson r=27 split-colour step."""

from hashlib import sha256


PALETTE_SIZE = 26
Q_ORDER = 20

# name, |B|, active classes, chi(X) values, chi(S), e(X), |S|
CASES = (
    ("D20", 20, 7, (7, 8, 9, 10), 7, 87, 13),
    ("D19", 19, 8, (8,), 8, 75, 14),
)


def available_list_masks(block_order, active_count, split_weight):
    """Construct the two list types after splitting an intermediate column."""
    palette = (1 << PALETTE_SIZE) - 1
    old_colour = 0
    # Use a canonical colour that is absent from every target colouring
    # (all have at most ten colours); the Hall instance is invariant under
    # relabelling this fresh colour.
    fresh_colour = PALETTE_SIZE - 1
    active = (1 << active_count) - 1
    unsplit = palette ^ active
    split = palette ^ ((active ^ (1 << old_colour)) | (1 << fresh_colour))
    assert unsplit.bit_count() == split.bit_count() == block_order - 1
    assert (unsplit | split).bit_count() == block_order
    assert (unsplit & split).bit_count() == block_order - 2
    return (split,) * split_weight + (unsplit,) * (block_order - split_weight)


def exhaustive_hall_audit(block_order, active_count):
    """Check Hall's inequality for every vertex subset and split weight."""
    checked_subsets = 0
    minimum_slack = block_order
    for split_weight in range(1, block_order):
        lists = available_list_masks(block_order, active_count, split_weight)
        unions = [0] * (1 << block_order)
        for subset in range(1, 1 << block_order):
            least_bit = subset & -subset
            vertex = least_bit.bit_length() - 1
            unions[subset] = unions[subset ^ least_bit] | lists[vertex]
            slack = unions[subset].bit_count() - subset.bit_count()
            assert slack >= 0
            minimum_slack = min(minimum_slack, slack)
            checked_subsets += 1
    assert minimum_slack == 0
    return checked_subsets, minimum_slack


def exhaustive_endpoint_audit(block_order, active_count, outside, high_edges):
    """Enumerate all endpoint masks satisfying the incidence total."""
    target_weight = block_order * active_count
    zero_floor = 27 - outside
    full_floor = active_count - 1
    feasible_masks = 0
    minimum_degree_sum = None
    for full_mask in range(1 << Q_ORDER):
        full_count = full_mask.bit_count()
        if block_order * full_count != target_weight:
            continue
        zero_count = Q_ORDER - full_count
        degree_sum = full_count * full_floor + zero_count * zero_floor
        feasible_masks += 1
        if minimum_degree_sum is None or degree_sum < minimum_degree_sum:
            minimum_degree_sum = degree_sum
    assert minimum_degree_sum is not None
    assert minimum_degree_sum > 2 * high_edges
    return feasible_masks, minimum_degree_sum, 2 * high_edges


def main():
    records = []
    for name, b, active, chromatic_values, small_chi, high_edges, outside in CASES:
        # An optimal c-colouring is surjective.  The old class remains nonempty
        # because an intermediate column has weight below its class total b.
        palette_rows = []
        for chromatic in chromatic_values:
            fresh_colour = chromatic
            assert active <= chromatic < PALETTE_SIZE
            unused_after_split = PALETTE_SIZE - (chromatic + 1)
            assert unused_after_split >= small_chi
            palette_rows.append((chromatic, fresh_colour, unused_after_split))

        hall_subsets, minimum_slack = exhaustive_hall_audit(b, active)
        endpoint_masks, degree_floor, handshake = exhaustive_endpoint_audit(
            b, active, outside, high_edges
        )
        records.append(
            (
                name,
                b,
                active,
                tuple(palette_rows),
                hall_subsets,
                minimum_slack,
                endpoint_masks,
                degree_floor,
                handshake,
            )
        )

    records = tuple(records)
    assert tuple((row[0], row[4], row[6], row[7], row[8]) for row in records) == (
        ("D20", 19 * ((1 << 20) - 1), 77520, 224, 174),
        ("D19", 18 * ((1 << 19) - 1), 125970, 212, 150),
    )
    print("PASS independent exhaustive split-colour audit")
    for row in records:
        print(
            f"{row[0]}: hall_subsets={row[4]}; min_hall_slack={row[5]}; "
            f"endpoint_masks={row[6]}; degree_floor={row[7]}; handshake={row[8]}"
        )
    print(f"certificate_sha256={sha256(repr(records).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
