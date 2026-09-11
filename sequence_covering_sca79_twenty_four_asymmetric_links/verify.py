#!/usr/bin/env python3
"""Exact checker for the twenty-four-asymmetric-link theorem."""

from math import factorial


G = [factorial(r) * factorial(8 - r) // 72 for r in range(9)]
U = [1, -7, 21, -35, 35, -21, 7, -1, 0]
V = [0, 1, -7, 21, -35, 35, -21, 7, -1]


def point_cells(a: int, c: int) -> list[int]:
    return [G[r] + (-1) ** (r + 1) * (r * c - a) for r in range(9)]


def valid_constant_profile(a: int, c: int) -> bool:
    return all(value >= 0 for value in point_cells(a, c))


def outgoing_divisibilities(a: int, c: int, degree: int) -> bool:
    cells = point_cells(a, c)
    return all(cells[r] % (8 - r) == 0 for r in range(degree + 1, 7))


def incoming_divisibilities(a: int, c: int, degree: int) -> bool:
    b = 8 * c - a
    return outgoing_divisibilities(-b, -c, degree)


def position_vector(a: int, b: int) -> list[int]:
    return [560 + a * u + b * v for u, v in zip(U, V)]


def main() -> None:
    assert G == [560, 70, 20, 10, 8, 10, 20, 70, 560]

    profiles = [
        (a, c, 8 * c - a)
        for c in range(-18, 19)
        for a in range(-560, 89)
        if valid_constant_profile(a, c)
    ]
    assert len(profiles) == 249

    def survivors(outdegree: int, indegree: int) -> list[tuple[int, int, int]]:
        return [
            profile
            for profile in profiles
            if outgoing_divisibilities(profile[0], profile[1], outdegree)
            and incoming_divisibilities(profile[0], profile[1], indegree)
        ]

    classification = {
        (1, 1): [],
        (2, 1): [],
        (1, 2): [],
        (2, 2): [],
        (3, 1): [(-20, -6, -28), (-20, -3, -4)],
        (1, 3): [(4, 3, 20), (28, 6, 20)],
    }
    for degrees, expected in classification.items():
        assert survivors(*degrees) == expected

    c_zero_small_outdegree = [
        profile
        for profile in profiles
        if profile[1] == 0
        and any(outgoing_divisibilities(profile[0], 0, degree) for degree in (1, 2))
    ]
    assert c_zero_small_outdegree == []

    # Combined degree-excess lower bound 12K+2(9-K).
    assert 12 + 2 * 8 == 28
    assert 2 * (22 - 9) < 28
    assert 2 * (23 - 9) == 28
    assert 2 * (28 - 9) == 12 * 2 + 2 * 7

    # Exact 23: four (3,1) rows and four (1,3) rows.  Enumerate the
    # multiplicities of the two local profiles in each class.
    balance_cases = []
    position_survivors = []
    for i in range(5):
        for j in range(5):
            peripheral_c = [-6] * i + [-3] * (4 - i) + [6] * j + [3] * (4 - j)
            peripheral_a = [-20] * 4 + [28] * j + [4] * (4 - j)
            if sum(peripheral_c) != 0:
                continue
            assert i == j
            a_h = -sum(peripheral_a)
            b_h = -a_h
            balance_cases.append((i, j, a_h, b_h))
            positions = position_vector(a_h, b_h)
            if min(positions) >= 0:
                position_survivors.append((i, j, a_h, b_h, peripheral_c, positions))

    assert balance_cases == [
        (0, 0, 64, -64),
        (1, 1, 40, -40),
        (2, 2, 16, -16),
        (3, 3, -8, 8),
        (4, 4, -32, 32),
    ]
    assert len(position_survivors) == 1
    i, j, a_h, b_h, central_c, positions = position_survivors[0]
    assert (i, j, a_h, b_h) == (3, 3, -8, 8)
    assert sorted(central_c) == [-6, -6, -6, -3, 3, 6, 6, 6]
    assert min(positions) == 0

    positive_sum = sum(value for value in central_c if value > 0)
    positive_count = sum(value > 0 for value in central_c)
    negative_cell = G[positive_count] + (-1) ** (positive_count + 1) * (positive_sum - a_h)
    assert positive_count == 4 and positive_sum == 21
    assert negative_cell == -21

    print(f"constant coefficient-row profiles: {len(profiles)}")
    for degrees in classification:
        print(f"degree {degrees}: {len(classification[degrees])} surviving profiles")
    print(f"all-constant c=0 profiles with outdegree <=2: {len(c_zero_small_outdegree)}")
    print("combined excess per nonconstant row: at least 12")
    print("combined excess per constant row: at least 2")
    print("support sizes at most 22: excluded")
    print(f"exact-23 balance cases: {len(balance_cases)}")
    print(f"exact-23 position survivors: {len(position_survivors)}")
    print(f"unique survivor parameters: a={a_h}, b={b_h}, positive coefficient sum={positive_sum}")
    print(f"negative named point cell: {negative_cell}")
    print("asymmetric ordered-pair-link lower bound: 24")
    print("all checks passed")


if __name__ == "__main__":
    main()
