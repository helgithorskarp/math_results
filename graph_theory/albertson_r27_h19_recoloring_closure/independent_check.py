#!/usr/bin/env python3
"""Independent labelled-colour audit of the h=19 recolouring argument."""

from hashlib import sha256


def preserves_profile(profile, source, target, weight):
    moved = list(profile)
    moved[source] -= weight
    moved[target] += weight
    return sorted(moved) == sorted(profile)


def main():
    b = 19
    all_active = (b,) * 8
    one_zero = (0,) + (b,) * 8
    surviving_moves = []

    for profile_name, profile in (
        ("eight_active", all_active),
        ("eight_active_one_zero", one_zero),
    ):
        for source, source_total in enumerate(profile):
            if source_total != b:
                continue
            for target in range(len(profile)):
                if target == source:
                    continue
                for weight in range(1, b + 1):
                    if preserves_profile(profile, source, target, weight):
                        surviving_moves.append(
                            (profile_name, source, target, weight)
                        )

    assert surviving_moves
    assert all(row[0] == "eight_active_one_zero" for row in surviving_moves)
    assert all(row[2] == 0 and row[3] == b for row in surviving_moves)
    assert len(surviving_moves) == 8

    degree_rows = []
    for zero_weight_vertices in range(20):
        positive = 19 - zero_weight_vertices
        lower_sum = sum(
            [7] * positive + [12] * zero_weight_vertices
        )
        degree_rows.append((zero_weight_vertices, lower_sum))
        assert lower_sum >= 133
        assert lower_sum > 112

    payload = repr((surviving_moves, degree_rows)).encode()
    digest = sha256(payload).hexdigest()
    print("PASS independent labelled recolouring audit")
    print(
        "profile_preserving_moves="
        f"{len(surviving_moves)}; all_are_full_weight_active_zero_swaps=True"
    )
    print(
        f"degree_sum_range={degree_rows[0][1]}..{degree_rows[-1][1]}; "
        f"certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
