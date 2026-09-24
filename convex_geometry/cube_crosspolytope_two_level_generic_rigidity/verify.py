#!/usr/bin/env python3
"""Independent exact-rational checks for two-level resonance rigidity."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from json import dumps


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def candidates(q: int):
    for p in range(1, q):
        r = q - p
        for m in range(2, min(p, r) + 1):
            k, j = p - m, r - m
            for ell in range(r + 1):
                for i in range(p + 1):
                    if ell + k - j - i > 0:
                        yield p, r, m, k, ell, i, j


def boundary_numerator(entry, a: F) -> F:
    p, r, m, k, ell, i, j = entry
    return a * k + a * a * ell - i - a * j


def rational_samples(entry):
    q = entry[0] + entry[1]
    # At a=1 the integer boundary numerator is at least one.  Its derivative
    # has absolute value at most 3q on [0,1], so all three points are safely
    # inside the positive-boundary interval.
    samples = [F(12 * q - 1, 12 * q), F(18 * q - 1, 18 * q), F(24 * q - 1, 24 * q)]
    require(all(boundary_numerator(entry, a) > 0 for a in samples), "bad sample")
    return samples


def eta(moment: int, weight: F, lam: F) -> F:
    return weight**moment / (1 + weight + lam * weight) ** (moment + 1) - 1 / (
        weight * (1 + lam) ** (moment + 1)
    )


def check_instance(entry, a: F) -> tuple[F, F]:
    p, r, m, k, ell, i, j = entry
    q = p + r
    degree = q - m
    x = k - i + a * (ell - j)
    require(x > 0, "positive boundary did not imply X>0")

    # Reconstruct the logarithmic derivatives of the regularized transforms.
    unit_remaining = m + r - ell
    moving_remaining = p - i + m
    unit_principal_ratio = F(unit_remaining) - F(r - ell) * a / (1 - a)
    moving_principal_ratio = (
        a * moving_remaining + F(p - i) * a / (1 - a)
    )

    zero = F(0)
    lam = (1 - a) / a
    unit_tail_ratio = (
        k * eta(1, F(1), zero) / eta(0, F(1), zero)
        + ell * eta(1, a, zero) / eta(0, a, zero)
    )
    moving_tail_ratio = (
        i * eta(1, F(1), lam) / eta(0, F(1), lam)
        + j * eta(1, a, lam) / eta(0, a, lam)
    )

    unit_shift = 2 * x / (1 - a)
    moving_shift = 2 * a * x / (1 - a)
    common = F(m - 1, degree + 1)
    unit_ratio = common * (unit_principal_ratio + unit_tail_ratio) / unit_shift
    moving_ratio = common * (
        moving_principal_ratio + moving_tail_ratio
    ) / moving_shift

    margin = q * (1 + a) ** 2 - 4 * a * (i + ell)
    positive_form = q * (1 - a) ** 2 + 4 * a * (q - i - ell)
    require(margin == positive_form and margin > 0, "margin positivity failed")
    expected = -F(m - 1) * margin / (
        4 * x * (degree + 1) * (1 + a)
    )
    require(unit_ratio - moving_ratio == expected, "ratio identity failed")
    require(expected < 0, "rigidity sign failed")
    return expected, margin


def main() -> None:
    candidate_count = 0
    instance_count = 0
    parity_relevant = 0
    smallest_margin = None
    largest_dimension_count = 0
    dimension_counts = {}
    for q in range(4, 21):
        local = list(candidates(q))
        dimension_counts[str(q)] = len(local)
        largest_dimension_count = len(local)
        candidate_count += len(local)
        for entry in local:
            p, r, m, k, ell, i, j = entry
            if (r - ell) % 2:
                parity_relevant += 1
            for a in rational_samples(entry):
                _, margin = check_instance(entry, a)
                smallest_margin = (
                    margin if smallest_margin is None else min(smallest_margin, margin)
                )
                instance_count += 1

    payload = {
        "status": "TWO_LEVEL_GENERIC_RIGIDITY_VERIFIED",
        "dimensions": [4, 20],
        "candidate_types": candidate_count,
        "rational_instances": instance_count,
        "parity_relevant_types": parity_relevant,
        "dimension_20_candidate_types": largest_dimension_count,
        "dimension_counts": dimension_counts,
        "smallest_tested_positive_margin": [
            smallest_margin.numerator,
            smallest_margin.denominator,
        ],
        "arithmetic": "fractions.Fraction only",
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
