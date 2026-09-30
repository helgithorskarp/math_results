#!/usr/bin/env python3
"""Exact algebra and constants supporting the written analytic proof.

Standard-library Python 3.10+. No numerical roots, target imports, solver,
private data or inferred universal inequality from test configurations.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import comb


def cmul(v: tuple[F, F], w: tuple[F, F]) -> tuple[F, F]:
    return v[0] * w[0] - v[1] * w[1], v[0] * w[1] + v[1] * w[0]


def origin_by_multiplication() -> dict[tuple[int, ...], tuple[F, F]]:
    """Multiply formal (1-at(x_j+i y_j)) then integrate t exactly.

    A key selects none/x_j/y_j in each coordinate. Its number of nonzero
    entries fixes both the power of a and the power of t before integration.
    """
    result = {(): (F(1), F(0))}
    for _ in range(8):
        updated = {}
        for key, value in result.items():
            for choice, factor in ((0, (F(1), F(0))),
                                   (1, (F(-1), F(0))),
                                   (2, (F(0), F(-1)))):
                updated[key + (choice,)] = cmul(value, factor)
        result = updated
    return {key: (9 * v[0] / (sum(x != 0 for x in key) + 1),
                  9 * v[1] / (sum(x != 0 for x in key) + 1))
            for key, v in result.items()}


def origin_by_subsets() -> dict[tuple[int, ...], tuple[F, F]]:
    """Direct elementary-symmetric expansion, including every monomial."""
    result = {}
    units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    for k in range(9):
        for subset in combinations(range(8), k):
            for choices in product((1, 2), repeat=k):
                key = [0] * 8
                for index, choice in zip(subset, choices):
                    key[index] = choice
                imag_count = choices.count(2)
                unit = units[imag_count % 4]
                coefficient = F(9 * (-1) ** k, k + 1)
                result[tuple(key)] = (coefficient * unit[0],
                                      coefficient * unit[1])
    return result


def poly_add(*items: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    result = {}
    for item in items:
        for key, value in item.items():
            result[key] = result.get(key, F(0)) + value
    return {key: value for key, value in result.items() if value}


def poly_scale(item: dict[tuple[int, ...], F], scale: F) -> dict[tuple[int, ...], F]:
    return {key: scale * value for key, value in item.items() if scale * value}


def poly_mul(left: dict[tuple[int, ...], F],
             right: dict[tuple[int, ...], F]) -> dict[tuple[int, ...], F]:
    result = {}
    for i, v in left.items():
        for j, w in right.items():
            key = tuple(x + y for x, y in zip(i, j))
            result[key] = result.get(key, F(0)) + v * w
    return {key: value for key, value in result.items() if value}


def pair_identities() -> tuple[dict, dict]:
    # Four free real variables are c, r, x, y. Subtract the displayed
    # multiple of x^2+y^2-r^2, so vanishing is a formal polynomial identity.
    one = {(0, 0, 0, 0): F(1)}
    c = {(1, 0, 0, 0): F(1)}
    r = {(0, 1, 0, 0): F(1)}
    x = {(0, 0, 1, 0): F(1)}
    y = {(0, 0, 0, 1): F(1)}
    squared_norm = poly_add(poly_mul(x, x), poly_mul(y, y),
                            poly_scale(poly_mul(r, r), F(-1)))
    first = poly_add(one, poly_scale(poly_mul(c, x), F(-1)))
    second = poly_add(one, poly_scale(poly_mul(c, r), F(-1)))
    d = poly_add(r, poly_scale(x, F(-1)))
    pair = poly_add(poly_mul(first, first),
                    poly_mul(poly_mul(c, c), poly_mul(y, y)),
                    poly_scale(poly_mul(second, second), F(-1)),
                    poly_scale(poly_mul(c, d), F(-2)),
                    poly_scale(poly_mul(poly_mul(c, c), squared_norm), F(-1)))
    phase_energy = poly_add(poly_mul(d, d), poly_mul(y, y),
                            poly_scale(poly_mul(r, d), F(-2)),
                            poly_scale(squared_norm, F(-1)))
    return pair, phase_energy


def require_mutation_rejected(check) -> None:
    try:
        check()
    except AssertionError:
        return
    raise AssertionError("A deliberately altered certificate was accepted")


def equal_maps(left, right) -> None:
    assert left == right


def envelope_margin(constant: int, kstar: F) -> None:
    assert kstar / constant < F(9, 32)


def run() -> dict:
    multiplied = origin_by_multiplication()
    direct = origin_by_subsets()
    assert len(multiplied) == len(direct) == 3 ** 8 == 6561
    equal_maps(multiplied, direct)
    real_terms = sum(v[0] != 0 for v in direct.values())
    imag_terms = sum(v[1] != 0 for v in direct.values())
    assert (real_terms, imag_terms) == (3281, 3280)
    assert direct[(1, 0, 0, 0, 0, 0, 0, 0)] == (F(-9, 2), F(0))
    pair, energy = pair_identities()
    assert pair == energy == {}

    even_terms = {k: 9 * F(k, k + 1) * comb(7, k - 1) * F(15, 14) ** (k - 1)
                  for k in (2, 4, 6, 8)}
    kstar = sum(even_terms.values())
    assert even_terms == {2: F(45), 4: F(30375, 98),
                          6: F(61509375, 268912),
                          8: F(170859375, 13176688)}
    assert kstar == F(3930935355, 6588344) < 600
    envelope_margin(2400, kstar)
    assert F(9, 32) - F(600, 2400) == F(1, 32)
    assert 4 * F(1, 9600) == F(1, 2400)
    assert F(1, 2000 ** 2) < F(1, 2400)

    polar = [F(73, 64) ** 9 / (9 * F(5, 8)),
             F(9, 8) ** 9 / (9 * F(29, 64)),
             F(69, 64) ** 9 / (9 * F(1, 4))]
    assert polar == [F(58871586708267913, 101330991615836160),
                     F(43046721, 60817408),
                     F(3939120870619581, 4503599627370496)]
    assert all(value < 1 for value in polar)

    # Formal example polynomial in z,e; both representations have free e.
    pe = {(9, 0): F(1), (0, 0): F(-1), (8, 1): F(-1),
          (1, 1): F(1), (7, 1): F(2), (2, 1): F(-2)}
    derivative = {(z - 1, e): z * value
                  for (z, e), value in pe.items() if z}
    assert derivative == {(8, 0): F(9), (7, 1): F(-8),
                           (6, 1): F(14), (1, 1): F(-4), (0, 1): F(1)}
    assert {(9 - z, e): value for (z, e), value in pe.items()} == poly_scale(pe, F(-1))
    evaluate_one = {}
    for (_, e), value in pe.items():
        evaluate_one[e] = evaluate_one.get(e, F(0)) + value
    assert all(value == 0 for value in evaluate_one.values())
    at_one_derivative = {}
    for (_, e), value in derivative.items():
        at_one_derivative[e] = at_one_derivative.get(e, F(0)) + value
    assert at_one_derivative == {0: F(9), 1: F(3)}

    epsilon = F(1, 10 ** 6)
    assert F(1, 5) - F(8, 5 ** 7) == F(15617, 78125) > 0
    assert F(9, 5 ** 8) - 11 * epsilon == F(301, 25000000) > 0
    assert 3 * epsilon < F(1, 2)
    assert 9 - 8 * epsilon > 0
    # Bernoulli lower bound: (1-e/100)^8(9+3e) >=
    # (1-2e/25)(9+3e) = 9+57e/25-6e^2/25.
    bernoulli_product = poly_mul({(0,): F(1), (1,): F(-2, 25)},
                                 {(0,): F(9), (1,): F(3)})
    assert bernoulli_product == {(0,): F(9), (1,): F(57, 25), (2,): F(-6, 25)}
    assert F(57, 25) - F(6, 25) * epsilon > 0
    radius = 1 - epsilon / 100
    distance_product = radius ** 8 * (9 + 3 * epsilon)
    assert distance_product > 9
    assert radius > F(99, 100)
    assert epsilon / 9 > F(1, 10) ** 8
    assert epsilon / 9 != 1

    # First-order exact Taylor coefficients for the credited paired family:
    # B=1-5u+9u^2, B^(-1/2)=1+(5/2)u+O(u^2),
    # (1-3u)/B=1+2u+O(u^2). Analyticity near u=0 is in the proof.
    bracket_linear = F(5, 2) - (F(-3) + F(5))
    assert bracket_linear == F(1, 2)
    assert 2 * bracket_linear == 1
    assert 8 * bracket_linear == 4
    assert F(1, 4000) < F(1, 2400)
    assert F(4, 4000) > F(1, 1250)

    # Mutation checks cover an origin odd sign, the pair identity, and the
    # unsupported replacement of the angular denominator by 2000.
    altered_origin = dict(direct)
    altered_origin[(1, 0, 0, 0, 0, 0, 0, 0)] = (F(9, 2), F(0))
    require_mutation_rejected(lambda: equal_maps(multiplied, altered_origin))
    require_mutation_rejected(lambda: equal_maps(
        {(1, 1, 0, 0): F(4), (1, 0, 1, 0): F(-4)}, pair))
    require_mutation_rejected(lambda: envelope_margin(2000, kstar))

    return {
        "origin_formal_complex_monomials": len(direct),
        "origin_formal_real_monomials": real_terms,
        "origin_formal_imaginary_monomials": imag_terms,
        "pair_and_phase_energy_identities": "exact formal polynomial identities",
        "even_envelope_terms": {str(k): str(value) for k, value in even_terms.items()},
        "K_star": str(kstar),
        "K_star_upper_bound": 600,
        "angular_loss_denominator": 2400,
        "sector_squared_angle_denominator": 9600,
        "origin_margin_after_uniform_angular_loss": "(1-a)/32",
        "polar_upper_bounds": [str(value) for value in polar],
        "example_epsilon_endpoint": str(epsilon),
        "example_scaled_radius": str(radius),
        "example_product_of_other_root_distances_minus_9": str(distance_product - 9),
        "example_monotonicity_middle_margin": "301/25000000",
        "weighted_scope_example_A_over_delta_limit": "1/4000",
        "weighted_scope_example_epsilon_squared_over_delta_limit": "1/1000",
        "mutations_rejected": 3,
        "analytic_bridges": "written proof; not formalized",
        "input_certificate": "636 Bernstein coefficients checked in the cited preceding source"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print compact reproducible evidence JSON")
    args = parser.parse_args()
    result = run()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: all 6561 formal origin monomials; pair and phase identities; exact bounds; 3 mutations rejected.")
        print("PASS: K*=3930935355/6588344<600; angular denominator 2400; sector denominator 9600.")
        print("PASS: admissible monotone-family constants and strict product-distance separation.")
