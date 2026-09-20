#!/usr/bin/env python3
"""Exact supplemental checks, not a finite proof of the universal theorem."""

import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def turn(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def validate_points(points):
    require(len(points) >= 2, "at least two points required")
    require(all(len(p) == 2 and all(type(c) is int for c in p) for p in points),
            "integer coordinate pairs required")
    require(all(points[i][0] < points[i + 1][0] for i in range(len(points) - 1)),
            "strictly increasing first coordinates required")
    require(all(turn(a, b, c) != 0 for a, b, c in itertools.combinations(points, 3)),
            "general position required")


def hull_size(points):
    """Monotone-chain hull; input points already sorted by first coordinate."""
    if len(points) <= 2:
        return len(points)
    chains = []
    for seq in (points, list(reversed(points))):
        chain = []
        for p in seq:
            while len(chain) >= 2 and turn(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        chains.append(chain)
    return len(chains[0]) + len(chains[1]) - 2


def subset_ranks(points):
    """Definition-level exhaustive convex-subset check; singleton ranks are one."""
    n = len(points)
    left = [1] * n       # rightmost endpoint, a left-gon
    right = [1] * n      # leftmost endpoint, a right-gon
    largest = 1
    convex_masks = []
    for mask in range(1, 1 << n):
        indices = [i for i in range(n) if (mask >> i) & 1]
        size = len(indices)
        if hull_size([points[i] for i in indices]) == size:
            left[indices[-1]] = max(left[indices[-1]], size)
            right[indices[0]] = max(right[indices[0]], size)
            largest = max(largest, size)
            convex_masks.append((mask, size))
    return left, right, largest, convex_masks


def chain_ranks(points):
    """Independent endpoint ranks via longest cups and caps, without hulls/subsets."""
    n = len(points)
    left, right = [1] * n, [1] * n
    for start in range(n - 1):
        chains = {}
        for sign in (-1, 1):
            dp = {(start, b): 2 for b in range(start + 1, n)}
            best = {}
            for b in range(start + 1, n):
                for a in range(start + 1, b):
                    dp[a, b] = max(
                        (dp[h, a] + 1 for h in range(start, a)
                         if dp[h, a] > 0
                         and sign * turn(points[h], points[a], points[b]) > 0),
                        default=0,
                    )
                best[b] = max(dp[a, b] for a in range(start, b))
            chains[sign] = best
        for end in range(start + 1, n):
            # A cup and cap with common endpoints have disjoint interiors.
            size = chains[-1][end] + chains[1][end] - 2
            left[end] = max(left[end], size)
            right[start] = max(right[start], size)
    return left, right


def blowup_size(v, m, x):
    require(type(m) is int and m >= 3, "m must be an integer at least three")
    require(type(x) is int and x >= 1, "x must be a positive integer")
    require(len(v) == m and v[0] == 0 and v[1] == 2,
            "profile must have indices 0..m-1, v0=0, v1=2")
    require(all(type(a) is int and a >= 0 for a in v), "nonnegative integer profile")
    k = m + 2 * x
    return (2 * sum(math.comb(k - 2, ell) for ell in range(x + 1))
            + sum(v[j] * math.comb(k - j - 1, x) for j in range(2, m)))


def excess_terms(v, m, x):
    k = m + 2 * x
    terms = [math.comb(2 * x, x) * (sum(v) - 2 ** (m - 2))]
    terms += [math.comb(k - j - 2, x - 1) * (sum(v[:j + 1]) - 2 ** j)
              for j in range(2, m - 1)]
    return terms


def check_profile(v, m, x):
    excess = blowup_size(v, m, x) - 2 ** (m + 2 * x - 2)
    terms = excess_terms(v, m, x)
    require(excess == sum(terms), "excess identity failed")
    if excess > 0:
        require(any(t > 0 for t in terms), "positive-excess extraction failed")
    if all(t <= 0 for t in terms):
        require(excess <= 0, "conditional bound failed")
        require((excess == 0) == all(t == 0 for t in terms), "equality criterion failed")
    return excess


def verify_binary_partition():
    """Count the actual words, not just two equivalent binomial sums."""
    words_checked = 0
    parameters = 0
    for x in range(1, 4):
        for m in range(3, 9):
            k = m + 2 * x
            n = k - 2
            buckets = {"few_zero": 0, "few_one": 0}
            buckets.update({str(j): 0 for j in range(2, m - 1)})
            for word in itertools.product((0, 1), repeat=n):
                words_checked += 1
                ones = sum(word)
                if n - ones <= x:
                    buckets["few_zero"] += 1
                elif ones <= x:
                    buckets["few_one"] += 1
                else:
                    zeros = ones = 0
                    for t, bit in enumerate(reversed(word), start=1):
                        zeros += (bit == 0)
                        ones += (bit == 1)
                        if min(zeros, ones) >= x + 1:
                            buckets[str(k - t)] += 1
                            break
                    else:
                        raise ValueError("suffix classification failed")
            tail = sum(math.comb(n, ell) for ell in range(x + 1))
            require(buckets["few_zero"] == buckets["few_one"] == tail, "tail count")
            for j in range(2, m - 1):
                require(buckets[str(j)] == 2 ** (j - 1) * math.comb(k - j - 1, x),
                        "suffix bucket count")
            require(sum(buckets.values()) == 2 ** n, "partition completeness")
            parameters += 1
    return {"parameters": parameters, "words": words_checked}


def main():
    formal_cases = positive_controls = conditional_cases = 0
    # Deliberately includes many nongeometric profiles. These check algebra,
    # and must never be reported as realizable point-set counterexamples.
    for m in range(3, 9):
        for tail in itertools.product(range(4), repeat=m - 2):
            v = [0, 2] + list(tail)
            for x in range(1, 6):
                excess = check_profile(v, m, x)
                formal_cases += 1
                positive_controls += (excess > 0)
                conditional_cases += all(t <= 0 for t in excess_terms(v, m, x))
    # Wider integer identity check on reference profiles, not geometric census.
    reference_cases = 0
    for m in range(3, 31):
        v = [0, 2] + [2 ** (j - 1) for j in range(2, m - 1)] + [0]
        for x in range(1, 31):
            require(check_profile(v, m, x) == 0, "sharp reference profile")
            reference_cases += 1

    results = []
    subset_total = thresholds = geometric_checks = sublevel_checks = 0
    fixtures = json.loads((HERE / "fixtures.json").read_text())
    for fixture in fixtures:
        points = fixture["points"]
        validate_points(points)
        n = len(points)
        left, right, largest, masks = subset_ranks(points)
        dp_left, dp_right = chain_ranks(points)
        require(left == dp_left and right == dp_right, "rank algorithm disagreement")
        subset_total += (1 << n) - 1
        m = largest + 1
        profiles = []
        for L in range(1, n):
            rank = left[:L] + right[L:]
            v = [rank.count(j) for j in range(m)]
            require(v[0] == 0 and v[1] == 2 and sum(v) == n, "rank convention")
            thresholds += 1
            # Directly verify each endpoint sublevel's forbidden-convexity
            # claim against the precomputed full list of convex subsets.
            for j in range(1, m):
                for indices in (range(L), range(L, n)):
                    mask = sum(1 << i for i in indices if rank[i] <= j)
                    require(all(size <= j for sub, size in masks if sub & mask == sub),
                            "sublevel contains forbidden polygon")
                    sublevel_checks += 1
            deficits = []
            for x in range(1, 5):
                deficit = check_profile(v, m, x)
                deficits.append(deficit)
                geometric_checks += 1
                # Every supplied seed also meets the local cardinality bounds.
                require(all(t <= 0 for t in excess_terms(v, m, x)),
                        "fixture unexpectedly violates a seed cardinality bound")
            profiles.append({"threshold": L, "v": v[1:], "excess_x_1_to_4": deficits})
        results.append({"name": fixture["name"], "n": n, "largest_convex": largest,
                        "left_ranks": left, "right_ranks": right, "profiles": profiles})
    eq = next(r for r in results if r["name"] == "concave_four_equality")
    require(eq["largest_convex"] == 3, "concave control must avoid a quadrilateral")
    require(eq["profiles"][1]["excess_x_1_to_4"] == [0] * 4, "geometric equality control")
    strict = next(r for r in results if r["name"] == "convex_four_strict")
    require(all(e < 0 for p in strict["profiles"] for e in p["excess_x_1_to_4"]),
            "strict geometric control")

    rejected = 0
    invalid = [
        lambda: validate_points([[0, 0], [1, 1], [2, 2]]),
        lambda: validate_points([[0, 0], [0, 1]]),
        lambda: validate_points([[0, 0]]),
        lambda: blowup_size([0, 2, 0], 3, 0),
        lambda: blowup_size([0, 3, 0], 3, 1),
        lambda: blowup_size([0, 2, -1], 3, 1),
    ]
    for call in invalid:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed input accepted")
    canonical = json.dumps(results, sort_keys=True, separators=(",", ":")).encode()
    summary = {
        "status": "PASS",
        "claim_scope": "supplemental exact checks; universal result proved in PROOF.md",
        "formal_profiles_parameter_cases": formal_cases,
        "nongeometric_positive_excess_controls": positive_controls,
        "formal_cases_meeting_local_bounds": conditional_cases,
        "reference_profile_parameter_cases": reference_cases,
        "binary_partition": verify_binary_partition(),
        "geometric_fixtures": len(results),
        "nonempty_subsets_examined": subset_total,
        "thresholds_checked": thresholds,
        "geometric_parameter_cases": geometric_checks,
        "sublevel_avoidance_checks": sublevel_checks,
        "endpoint_rank_algorithms_agree": True,
        "geometric_equality_control": eq,
        "geometric_details_sha256": hashlib.sha256(canonical).hexdigest(),
        "malformed_inputs_rejected": rejected,
    }
    expected = HERE / "expected.json"
    require(summary == json.loads(expected.read_text()), "expected summary mismatch")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
