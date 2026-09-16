#!/usr/bin/env python3
"""Small exact controls for the independent opposed241 pair-gate review."""

import itertools
import json
from fractions import Fraction

import independent_check as review


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


# The multiquadratic multiplication table is associative on every basis triple.
for i, j, k in itertools.product(range(8), repeat=3):
    left = [0] * 8
    middle = [0] * 8
    right = [0] * 8
    left[i] = middle[j] = right[k] = 1
    need(
        review.multiply(review.multiply(tuple(left), tuple(middle)), tuple(right))
        == review.multiply(tuple(left), review.multiply(tuple(middle), tuple(right))),
        "basis associativity",
    )

# Direct sign fixtures straddle sqrt(33).
sign_fixtures = (
    (1, 0, 1), (-1, 0, -1), (0, 1, 1), (0, -1, -1),
    (6, -1, 1), (5, -1, -1), (-6, 1, -1), (-5, 1, 1),
)
for a, b, expected in sign_fixtures:
    need(review.sign_a_plus_b_sqrt33(a, b) == expected, "quadratic sign")

# The two-copy rotation identities hold exactly for sample squared radii.
for squared_radius in (Fraction(1, 4), Fraction(1, 3), Fraction(1), Fraction(7, 3)):
    real = 1 - 1 / (2 * squared_radius)
    imaginary_squared = (4 * squared_radius - 1) / (4 * squared_radius * squared_radius)
    need(real * real + imaginary_squared == 1, "rotation has unit modulus")
    need((1 - real) ** 2 + imaginary_squared == 1 / squared_radius,
         "rotated tips have unit separation")

report = review.construct_report()
need(report["submitted_unique_pair_counts_by_word"] == [7, 1, 5, 5, 11, 10, 8, 14],
     "submitted row-irredundance controls")
need(report["fresh_family_first_minimum_subset"] == [1, 2, 3, 4, 5, 7, 8, 13, 14],
     "fresh subfamily control")

print(json.dumps({
    "status": "CONTROLS_OK",
    "basis_associativity_triples": 512,
    "quadratic_sign_fixtures": len(sign_fixtures),
    "spindle_identity_fixtures": 4,
    "submitted_essential_rows": 8,
    "fresh_separating_subfamily_size": 9,
}, indent=2, sort_keys=True))
