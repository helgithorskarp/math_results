#!/usr/bin/env python3
"""Small positive and negative controls for the exact gate."""
from verify import L, ROWS, analyse, circumcircle_denominator, distance2


def rejected(rows):
    try:
        analyse(rows)
    except ValueError:
        return True
    return False


def main():
    # Q(sqrt(33)) arithmetic and the unit-triangle radius formula.
    assert L(1, 1) * L(1, -1) == -32
    unit_sides = (L(1), L(1), L(1))
    assert circumcircle_denominator(unit_sides) == 3
    assert unit_sides[0] * unit_sides[1] * unit_sides[2] != 3

    # Published unit and nonunit pairs.
    assert distance2(ROWS[0], ROWS[1]) == 1
    assert distance2(ROWS[0], ROWS[3]) != 1

    # Four malformed coordinate fixtures must fail the source checks.
    cases = []
    duplicate = list(ROWS); duplicate[6] = duplicate[5]; cases.append(tuple(duplicate))
    for index, coordinate in ((1, 0), (4, 3), (6, 1)):
        changed = [list(row) for row in ROWS]
        changed[index][coordinate] += 1
        cases.append(tuple(tuple(row) for row in changed))
    assert all(rejected(case) for case in cases)
    print('{"controls_passed":7,"malformed_fixtures_rejected":4}')


if __name__ == "__main__":
    main()
