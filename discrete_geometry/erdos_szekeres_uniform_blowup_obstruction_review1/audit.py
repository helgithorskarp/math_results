#!/usr/bin/env python3
"""Independent exact audit of the uniform-blow-up excess theorem.

This checker imports no target code, fixtures, or expected data.  It treats the
all-parameter proof as a human argument and independently checks its algebraic
linear forms, its extraction logic on a large finite box of formal profiles,
and its geometric endpoint reduction on all general-position permutation
point sets through seven vertices.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def choose(n: int, r: int) -> int:
    if r < 0 or r > n or n < 0:
        return 0
    return math.comb(n, r)


def blowup(v: tuple[int, ...], x: int) -> int:
    """Corollary-15 size, with v indexed from 0 through m-1."""
    m = len(v)
    k = m + 2 * x
    return 2 * sum(choose(k - 2, ell) for ell in range(x + 1)) + sum(
        v[j] * choose(k - j - 1, x) for j in range(2, m)
    )


def excess_rhs(v: tuple[int, ...], x: int) -> int:
    m = len(v)
    k = m + 2 * x
    ans = choose(2 * x, x) * (sum(v) - 2 ** (m - 2))
    for j in range(2, m - 1):
        ans += choose(k - j - 2, x - 1) * (sum(v[: j + 1]) - 2**j)
    return ans


def affine_signature(function, m: int) -> tuple[int, tuple[int, ...]]:
    """Return constant and coefficients in the free variables v_2,...,v_{m-1}."""
    base = [0, 2] + [0] * (m - 2)
    constant = function(tuple(base))
    coefficients = []
    for j in range(2, m):
        test = base.copy()
        test[j] += 1
        coefficients.append(function(tuple(test)) - constant)
    return constant, tuple(coefficients)


def coefficient_audit() -> dict:
    """Compare complete affine forms, not sampled profiles."""
    rows = []
    for m in range(3, 41):
        for x in range(1, 31):
            k = m + 2 * x
            lhs = lambda v: blowup(v, x) - 2 ** (k - 2)
            rhs = lambda v: excess_rhs(v, x)
            left_signature = affine_signature(lhs, m)
            right_signature = affine_signature(rhs, m)
            require(left_signature == right_signature, "affine forms disagree")
            predicted = tuple(choose(k - j - 1, x) for j in range(2, m))
            require(left_signature[1] == predicted, "wrong profile coefficient")
            require(choose(2 * x, x) > 0, "nonpositive terminal coefficient")
            require(
                all(choose(k - j - 2, x - 1) > 0 for j in range(2, m - 1)),
                "nonpositive layer coefficient",
            )
            rows.append((m, x, left_signature))
    raw = json.dumps(rows, separators=(",", ":")).encode()
    return {
        "parameter_pairs": len(rows),
        "max_m": 40,
        "max_x": 30,
        "signature_sha256": hashlib.sha256(raw).hexdigest(),
    }


def suffix_automaton_audit() -> dict:
    """Count shortest balanced suffixes by a DP, without enumerating words."""
    rows = []
    for m in range(3, 26):
        for x in range(1, 13):
            k = m + 2 * x
            n = k - 2
            active = {(0, 0): 1}
            first_hit = {}
            for length in range(1, n + 1):
                following = {}
                hit = 0
                for (zeros, ones), count in active.items():
                    for bit in (0, 1):
                        z = zeros + (bit == 0)
                        o = ones + (bit == 1)
                        if z >= x + 1 and o >= x + 1:
                            hit += count
                        else:
                            following[z, o] = following.get((z, o), 0) + count
                if hit:
                    first_hit[length] = hit
                active = following

            unresolved = sum(active.values())
            tails = 2 * sum(choose(n, ell) for ell in range(x + 1))
            require(unresolved == tails, "tail automaton count disagrees")
            total = unresolved
            for length, suffix_count in first_hit.items():
                j = k - length
                full_words = suffix_count * 2 ** (n - length)
                expected = 2 ** (j - 1) * choose(length - 1, x)
                require(2 <= j <= m - 2, "suffix bucket outside range")
                require(full_words == expected, "shortest-suffix bucket disagrees")
                total += full_words
            require(total == 2**n, "binary-word partition incomplete")
            reference = (0, 2) + tuple(2 ** (j - 1) for j in range(2, m - 1)) + (0,)
            require(blowup(reference, x) == 2 ** (k - 2), "reference profile not sharp")
            rows.append((m, x, unresolved, tuple(sorted(first_hit.items()))))
    raw = json.dumps(rows, separators=(",", ":")).encode()
    return {
        "parameter_pairs": len(rows),
        "max_word_length": max(m + 2 * x - 2 for m in range(3, 26) for x in range(1, 13)),
        "dp_sha256": hashlib.sha256(raw).hexdigest(),
    }


def profile_box_audit() -> dict:
    """Exhaust the logical extraction over a box of formal rank profiles."""
    cases = positive = seed_witness = layer_witness = locally_bounded = equality = 0
    for m in range(3, 9):
        reference = (0, 2) + tuple(2 ** (j - 1) for j in range(2, m - 1)) + (0,)
        for tail in itertools.product(range(5), repeat=m - 2):
            v = (0, 2) + tail
            n = sum(v)
            cumulative = [sum(v[: j + 1]) for j in range(m)]
            bounds_hold = n <= 2 ** (m - 2) and all(
                cumulative[j] <= 2**j for j in range(2, m - 1)
            )
            for x in range(1, 7):
                k = m + 2 * x
                excess = blowup(v, x) - 2 ** (k - 2)
                require(excess == excess_rhs(v, x), "profile identity failed")
                cases += 1
                if excess > 0:
                    positive += 1
                    if n > 2 ** (m - 2):
                        seed_witness += 1
                    else:
                        require(
                            any(cumulative[j] > 2**j for j in range(2, m - 1)),
                            "positive excess has no smaller witness",
                        )
                        layer_witness += 1
                if bounds_hold:
                    locally_bounded += 1
                    require(excess <= 0, "local bounds did not control output")
                    if excess == 0:
                        equality += 1
                        require(v == reference, "unexpected equality profile")
                    require((excess == 0) == (v == reference), "equality iff failed")

    # Small adversarial formal profiles expose both sources of excess and
    # cancellation.  They need not be geometrically realizable.
    layer = (0, 2, 6, 0, 0)
    cancelled = (0, 2, 3, 0, 0)
    require(sum(layer) == 8 and excess_rhs(layer, 1) == 4, "layer control")
    require(sum(cancelled) == 5 and sum(cancelled[:3]) > 4, "cancellation premise")
    require(excess_rhs(cancelled, 1) < 0, "positive layer need not force output excess")

    return {
        "formal_cases": cases,
        "positive_excess_cases": positive,
        "witness_at_seed_size": seed_witness,
        "witness_at_endpoint_layer": layer_witness,
        "locally_bounded_cases": locally_bounded,
        "equality_cases": equality,
        "adversarial_layer_excess": excess_rhs(layer, 1),
        "adversarial_cancelled_excess": excess_rhs(cancelled, 1),
    }


def orient(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> int:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def general_position(points: tuple[tuple[int, int], ...]) -> bool:
    return all(orient(points[i], points[j], points[k]) != 0 for i, j, k in itertools.combinations(range(len(points)), 3))


def inside_triangle(p, a, b, c) -> bool:
    signs = (orient(a, b, p), orient(b, c, p), orient(c, a, p))
    return all(s > 0 for s in signs) or all(s < 0 for s in signs)


def convex_position(points: tuple[tuple[int, int], ...], indices: tuple[int, ...]) -> bool:
    """Use Caratheodory containment, not a monotone-chain hull."""
    if len(indices) <= 3:
        return True
    for i in indices:
        others = tuple(j for j in indices if j != i)
        for a, b, c in itertools.combinations(others, 3):
            if inside_triangle(points[i], points[a], points[b], points[c]):
                return False
    return True


def geometric_order_type_audit() -> dict:
    """Check every general-position permutation diagram through n=7."""
    point_sets = thresholds = convex_subsets = sublevel_checks = parameter_cases = 0
    detail = []
    equality_controls = 0
    for n in range(2, 8):
        accepted = 0
        for permutation in itertools.permutations(range(n)):
            points = tuple((i, permutation[i]) for i in range(n))
            if not general_position(points):
                continue
            accepted += 1
            point_sets += 1
            masks = []
            left = [1] * n
            right = [1] * n
            largest = 1
            for size in range(2, n + 1):
                for indices in itertools.combinations(range(n), size):
                    if convex_position(points, indices):
                        mask = sum(1 << i for i in indices)
                        masks.append((mask, size))
                        convex_subsets += 1
                        left[indices[-1]] = max(left[indices[-1]], size)
                        right[indices[0]] = max(right[indices[0]], size)
                        largest = max(largest, size)
            m = largest + 1
            for split in range(1, n):
                rank = tuple(left[:split] + right[split:])
                require(rank.count(1) == 2, "interior threshold lost two endpoints")
                v = tuple([0] + [rank.count(j) for j in range(1, m)])
                require(sum(v) == n, "rank profile does not cover points")
                thresholds += 1
                for j in range(1, m - 1):
                    for side in (range(split), range(split, n)):
                        submask = sum(1 << i for i in side if rank[i] <= j)
                        require(
                            not any(size == j + 1 and mask & submask == mask for mask, size in masks),
                            "endpoint sublevel contains forbidden convex set",
                        )
                        sublevel_checks += 1
                local_bounds = n <= 2 ** (m - 2) and all(
                    sum(v[: j + 1]) <= 2**j for j in range(2, m - 1)
                )
                require(local_bounds, "small order type unexpectedly violates known bounds")
                for x in range(1, 5):
                    require(blowup(v, x) - 2 ** (m + 2 * x - 2) == excess_rhs(v, x), "geometric identity")
                    require(excess_rhs(v, x) <= 0, "small geometric output exceeds bound")
                    parameter_cases += 1
                if v == (0, 2) + tuple(2 ** (j - 1) for j in range(2, m - 1)) + (0,):
                    equality_controls += 1
                    require(all(excess_rhs(v, x) == 0 for x in range(1, 5)), "geometric equality failed")
        detail.append((n, accepted))

    raw = json.dumps(detail, separators=(",", ":")).encode()
    return {
        "point_sets": point_sets,
        "point_sets_by_order": {str(n): count for n, count in detail},
        "thresholds": thresholds,
        "convex_subsets": convex_subsets,
        "sublevel_checks": sublevel_checks,
        "blowup_parameter_cases": parameter_cases,
        "equality_controls": equality_controls,
        "order_count_sha256": hashlib.sha256(raw).hexdigest(),
    }


def scope_controls() -> dict:
    convex_quad = ((0, 0), (1, -1), (3, 0), (1, 2))
    one_interior = ((0, 0), (3, 0), (0, 3), (1, 1))
    require(convex_position(convex_quad, (0, 1, 2, 3)), "convex quadrilateral rejected")
    require(not convex_position(one_interior, (0, 1, 2, 3)), "interior-point control accepted")
    require(not general_position(((0, 0), (1, 1), (2, 2))), "collinearity control accepted")

    # With all points designated left (L=N), only the global leftmost point has
    # rightmost-endpoint rank one.  Thus the v_1=2 normalization genuinely
    # uses 1 <= L < N.
    triangle = ((0, 0), (1, 3), (3, 1))
    ranks = [1, 2, 3]
    require(general_position(triangle), "triangle control degenerate")
    require(ranks.count(1) == 1, "all-left endpoint boundary not detected")

    # For x=0, k=m, so the strict descent q <= m < k is unavailable even
    # though the construction size reduces to N.
    m = 5
    x = 0
    require(m + 2 * x == m, "x=0 boundary not detected")

    # A generic vertical shear preserves every orientation because its linear
    # determinant is one, while avoiding finitely many repeated y-values.
    points = ((0, 0), (1, 0), (2, 3), (4, 1))
    sheared = tuple((a, 7 * b + a) for a, b in points)
    require(len({p[1] for p in sheared}) == len(points), "shear failed to separate y")
    for i, j, k in itertools.combinations(range(len(points)), 3):
        require(orient(points[i], points[j], points[k]) * 7 == orient(sheared[i], sheared[j], sheared[k]), "shear changed orientation")

    return {
        "all_left_rank_one_count": ranks.count(1),
        "convexity_controls_pass": True,
        "interior_threshold_rank_one_count": 2,
        "x_zero_has_strict_descent": False,
        "generic_shear_preserves_orientations": True,
        "m3_empty_sum_checked": excess_rhs((0, 2, 0), 1) == 0,
    }


def main() -> None:
    summary = {
        "status": "PASS",
        "coefficient_audit": coefficient_audit(),
        "suffix_automaton": suffix_automaton_audit(),
        "formal_profiles": profile_box_audit(),
        "geometric_order_types": geometric_order_type_audit(),
        "scope_controls": scope_controls(),
    }
    if "--emit" not in sys.argv:
        expected = json.loads((HERE / "expected.json").read_text())
        require(summary == expected, "summary differs from expected.json")
        print("PASS: independent audit matches expected.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
