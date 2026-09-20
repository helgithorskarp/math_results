#!/usr/bin/env python3
"""Independent exact checks for the reciprocal torus-box theorem.

This checker deliberately does not import the submission's code.  Its main
continuum check builds the complete endpoint arrangement in every circle and
tests every product stratum directly.  It therefore does not use the
submission's coordinate-mask intersection reduction.

All arithmetic is fractions.Fraction arithmetic; no floating point is used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


if not __debug__:
    raise RuntimeError("this audit uses assertions; rerun Python without -O")


ONE = Fraction(1)


def mod1(x: Fraction) -> Fraction:
    return x % ONE


def prefix_data(ms: Sequence[int]) -> tuple[list[int], int]:
    """Return coefficients (1,m1,m1*m2,...) and claimed cover size."""
    coeffs = [1]
    for m in ms[:-1]:
        coeffs.append(coeffs[-1] * m)
    n_cover = 1
    product = 1
    for m in ms:
        product *= m
        n_cover += product
    return coeffs, n_cover


def centers(ms: Sequence[int]) -> list[tuple[Fraction, ...]]:
    coeffs, n_cover = prefix_data(ms)
    return [
        tuple(Fraction(c * j, n_cover) % ONE for c in coeffs)
        for j in range(n_cover)
    ]


def tails_and_q(ms: Sequence[int]) -> tuple[list[int], list[Fraction]]:
    """Return b_0,...,b_n and the half-open side lengths q_1,...,q_n."""
    n = len(ms)
    b = [0] * (n + 1)
    b[n] = 1
    for k in range(n - 1, -1, -1):
        b[k] = ms[k] * b[k + 1] + 1
    coeffs, n_cover = prefix_data(ms)
    q = []
    for k in range(n):
        r_minus_one = b[k] - b[k + 1]
        q.append(ONE - Fraction(r_minus_one * coeffs[k], n_cover))
    return b, q


def circle_strata(
    coordinate_centers: Sequence[Fraction], width: Fraction
) -> list[Fraction]:
    """One exact representative of every endpoint and open-cell stratum."""
    cuts = sorted(
        set(coordinate_centers)
        | {mod1(c + width) for c in coordinate_centers}
    )
    assert cuts
    representatives = set(cuts)
    for i, left in enumerate(cuts):
        right = cuts[(i + 1) % len(cuts)]
        if i + 1 == len(cuts):
            right += ONE
        representatives.add(mod1((left + right) / 2))
    return sorted(representatives)


def contains(
    center: Sequence[Fraction],
    point: Sequence[Fraction],
    widths: Sequence[Fraction],
    boundary: str,
) -> bool:
    for c, x, width in zip(center, point, widths):
        distance = mod1(x - c)
        if boundary == "open":
            if not (0 < distance < width):
                return False
        elif boundary == "left-open-right-closed":
            if not (0 < distance <= width):
                return False
        else:
            raise ValueError(boundary)
    return True


def exact_arrangement_check(
    ms: Sequence[int],
    *,
    widths: Sequence[Fraction] | None = None,
    boundary: str = "open",
    omit: int | None = None,
) -> tuple[bool, int, tuple[Fraction, ...] | None]:
    """Check the union on the full product endpoint arrangement.

    Membership in every translate is constant on every product of one-circle
    strata.  Consequently this finite test is equivalent to continuum
    coverage for the specified centers and boundary convention.
    """
    all_centers = centers(ms)
    if omit is not None:
        all_centers = [c for i, c in enumerate(all_centers) if i != omit]
    if widths is None:
        widths = [Fraction(1, m) for m in ms]
    reps = [
        circle_strata([c[i] for c in all_centers], widths[i])
        for i in range(len(ms))
    ]
    count = 0
    for point in itertools.product(*reps):
        count += 1
        if not any(
            contains(center, point, widths, boundary) for center in all_centers
        ):
            return False, count, point
    return True, count, None


def cyclic_gaps(values: Iterable[Fraction]) -> list[Fraction]:
    ordered = sorted(values)
    assert ordered
    if len(ordered) == 1:
        return [ONE]
    return [
        (ordered[(i + 1) % len(ordered)] - ordered[i]) % ONE
        for i in range(len(ordered))
    ]


def trace_decoder(ms: Sequence[int], target: Sequence[Fraction]) -> None:
    """Independently replay and assert every invariant in the proof decoder."""
    assert list(ms) == sorted(ms, reverse=True)
    coeffs, n_cover = prefix_data(ms)
    b, q = tails_and_q(ms)
    retained = list(range(n_cover))

    for k, m in enumerate(ms):
        old_delta = Fraction(coeffs[k], n_cover)
        old_projected = [Fraction(coeffs[k] * j, n_cover) % ONE for j in retained]
        assert len(set(old_projected)) == b[k]
        assert min(cyclic_gaps(old_projected)) >= old_delta

        # Increasing (a-x) mod 1 puts equality first and points immediately
        # behind x last.  The proof retains precisely the final b[k+1].
        ordered = sorted(
            retained,
            key=lambda j: mod1(Fraction(coeffs[k] * j, n_cover) - target[k]),
        )
        r = b[k] - b[k + 1] + 1
        retained = ordered[r - 1 :]
        assert len(retained) == b[k + 1]

        backward = [
            mod1(target[k] - Fraction(coeffs[k] * j, n_cover))
            for j in retained
        ]
        assert all(0 < d <= q[k] < Fraction(1, m) for d in backward)

        next_coeff = coeffs[k] * m
        new_projected = [Fraction(next_coeff * j, n_cover) % ONE for j in retained]
        assert len(set(new_projected)) == b[k + 1]
        assert min(cyclic_gaps(new_projected)) >= Fraction(next_coeff, n_cover)

    assert len(retained) == 1
    chosen = centers(ms)[retained[0]]
    assert contains(chosen, target, q, "left-open-right-closed")


def arithmetic_audit() -> dict[str, int]:
    sorted_tuples = 0
    orderings = 0
    decoder_targets = 0

    # Exhaust the proof's b, q, D, and strict wrap-gap inequalities on a
    # substantial finite family, including many repeated denominators and 1s.
    for n in range(1, 6):
        for ms in itertools.product(range(1, 6), repeat=n):
            if list(ms) != sorted(ms, reverse=True):
                continue
            sorted_tuples += 1
            coeffs, n_cover = prefix_data(ms)
            b, q = tails_and_q(ms)
            assert b[0] == n_cover
            prefix_sum = 0
            for k, m in enumerate(ms):
                d = coeffs[k] - (m - 1) * prefix_sum
                assert d >= 1
                r_minus_one = b[k] - b[k + 1]
                assert q[k] == Fraction(1, m) - Fraction(d, m * n_cover)
                assert 0 < q[k] < Fraction(1, m)
                assert m * r_minus_one * Fraction(coeffs[k], n_cover) > m - 1
                prefix_sum += coeffs[k]

    # Sorting decreasingly must maximize every resulting total prefix sum.
    for n in range(1, 6):
        for raw in itertools.product(range(1, 5), repeat=n):
            orderings += 1
            sorted_value = prefix_data(sorted(raw, reverse=True))[1]
            assert prefix_data(raw)[1] <= sorted_value

    # The ordering premise is material, not decorative: the smallest useful
    # adversary (1,3) makes D_2 negative in the raw order.
    raw = (1, 3)
    coeffs, _ = prefix_data(raw)
    d2 = coeffs[1] - (raw[1] - 1) * coeffs[0]
    assert d2 == -1

    # Exercise the actual selection invariants at endpoints, just to either
    # side of endpoints, at zero, and across the circle seam.
    trace_cases = [(1,), (2,), (1, 1), (2, 1), (2, 2), (3, 2), (3, 2, 1)]
    for ms in trace_cases:
        cs = centers(ms)
        widths = [Fraction(1, m) for m in ms]
        coordinate_values: list[list[Fraction]] = []
        for k in range(len(ms)):
            values = {Fraction(0), Fraction(1, 2), Fraction(1, 97), Fraction(96, 97)}
            for c in cs[: min(4, len(cs))]:
                values.add(c[k])
                values.add(mod1(c[k] + widths[k]))
            coordinate_values.append(sorted(values))
        targets = list(itertools.product(*coordinate_values))
        if len(targets) > 4000:
            targets = targets[:2000] + targets[-2000:]
        for target in targets:
            trace_decoder(ms, target)
            decoder_targets += 1

    return {
        "sorted_arithmetic_tuples": sorted_tuples,
        "raw_orderings": orderings,
        "decoder_targets": decoder_targets,
    }


def run_checks() -> dict[str, object]:
    arithmetic = arithmetic_audit()
    reciprocal_cases = [
        (1,),
        (2,),
        (3,),
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (3, 3),
        (2, 1, 1),
        (2, 2, 1),
        (2, 2, 2),
        (3, 2, 1),
        (1, 1, 1, 1),
    ]
    arrangement_points = 0
    case_rows = []
    for ms in reciprocal_cases:
        ok, tested, witness = exact_arrangement_check(ms)
        assert ok, (ms, witness)
        arrangement_points += tested

        b, q = tails_and_q(ms)
        assert b[0] == len(centers(ms))
        half_ok, half_tested, half_witness = exact_arrangement_check(
            ms, widths=q, boundary="left-open-right-closed"
        )
        assert half_ok, (ms, half_witness)
        arrangement_points += half_tested
        case_rows.append(
            {
                "m": list(ms),
                "N": len(centers(ms)),
                "open_strata": tested,
                "half_open_strata": half_tested,
                "q": [str(x) for x in q],
            }
        )

    # Definition-sensitive negative controls.  At q in dimension one, open
    # right endpoints leave holes whereas (0,q] covers.  Removing one proposed
    # center also leaves a hole in each selected construction.
    boundary_controls = 0
    for ms in [(1,), (2,), (3,)]:
        _, q = tails_and_q(ms)
        ok, _, witness = exact_arrangement_check(ms, widths=q, boundary="open")
        assert not ok and witness is not None
        boundary_controls += 1

    deletion_controls = 0
    deletion_witnesses = []
    for ms in [(1,), (2,), (1, 1), (2, 1), (2, 2), (3, 2), (2, 2, 1)]:
        ok, tested, witness = exact_arrangement_check(ms, omit=0)
        assert not ok and witness is not None
        deletion_controls += 1
        deletion_witnesses.append(
            {"m": list(ms), "strata_until_hole": tested, "hole": [str(x) for x in witness]}
        )

    return {
        **arithmetic,
        "continuum_cases": len(reciprocal_cases),
        "arrangement_strata_checked": arrangement_points,
        "boundary_negative_controls": boundary_controls,
        "deletion_negative_controls": deletion_controls,
        "cases": case_rows,
        "deletion_witnesses": deletion_witnesses,
        "status": "PASS",
    }


def canonical_json(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare output with EXPECTED.json")
    parser.add_argument("--write-expected", action="store_true", help="print candidate EXPECTED.json")
    args = parser.parse_args()

    result = run_checks()
    rendered = canonical_json(result)
    expected_path = Path(__file__).with_name("EXPECTED.json")
    if args.check:
        expected = expected_path.read_text(encoding="utf-8")
        assert rendered == expected, "computed output differs from EXPECTED.json"
    print(rendered, end="")
    if args.write_expected:
        print("sha256=" + hashlib.sha256(rendered.encode()).hexdigest())


if __name__ == "__main__":
    main()
