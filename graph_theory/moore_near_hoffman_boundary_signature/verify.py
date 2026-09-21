#!/usr/bin/env python3
"""Exact audits for the Moore near-Hoffman and boundary-signature theorems."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache


BRANCH_TYPES = (
    (7, 0, 0),
    (5, 1, 0),
    (3, 2, 0),
    (1, 3, 0),
    (4, 0, 1),
    (2, 1, 1),
    (0, 2, 1),
    (1, 0, 2),
)


def uniform_parameters(r: int) -> dict[str, int]:
    if r < 1:
        raise ValueError("r must be positive")
    k = r * r + r + 1
    v = k * k + 1
    alpha = r * k + 1
    s = alpha - 1
    outside = v - s
    D = r * r + 2 * r + 2
    Q = 2 * r * r + 3 * r + 2
    return {
        "r": r,
        "k": k,
        "v": v,
        "alpha": alpha,
        "s": s,
        "outside": outside,
        "D": D,
        "Q": Q,
    }


def audit_uniform_extension(r: int) -> None:
    p = uniform_parameters(r)
    k, v, alpha = p["k"], p["v"], p["alpha"]
    s, outside, D, Q = p["s"], p["outside"], p["D"], p["Q"]

    assert v == k * k + 1
    assert alpha == (r + 1) * (r * r + 1) == r * k + 1
    assert v * (r + 1) == alpha * (k + r + 1)
    assert s == r * k
    assert outside == k * (r * r + 1) + 1

    sum_a = k * s
    sum_a2 = s * (s - 1) + sum_a
    sum_z = sum_a - (r + 1) * outside
    sum_z2 = sum_a2 - 2 * (r + 1) * sum_a + (r + 1) ** 2 * outside
    assert sum_z == -D
    assert sum_z2 == Q
    assert sum_z + sum_z2 == k - 1 == r * (r + 1)

    if r >= 5:
        positive_upper_twice = r * (r + 1)
        positive_lower_twice = 2 * ((r - 1) ** 2 + 1)
        assert positive_lower_twice - positive_upper_twice == (r - 1) * (r - 4)
        assert positive_lower_twice > positive_upper_twice

    rayleigh_numerator = (r * Q + D) ** 2 - (k - 1) * Q * Q
    expected_numerator = (r + 1) * (3 * r**3 + 8 * r * r + 8 * r + 4)
    assert rayleigh_numerator == expected_numerator > 0

    support_lower = k + 1
    excess = D - support_lower
    assert excess == r
    assert r * r + r - excess == excess * excess

    profile = {0: 1, r: k, r + 1: k * r * r}
    assert sum(profile.values()) == outside
    assert sum(value * count for value, count in profile.items()) == sum_a
    assert sum(value * (value - 1) * count for value, count in profile.items()) == s * (s - 1)


def branch_multisets(t: int) -> tuple[tuple[int, ...], ...]:
    if t not in range(4):
        raise ValueError("t must lie in {0,1,2,3}")
    target_b = 9 - 3 * t

    @lru_cache(maxsize=None)
    def rec(i: int, branches: int, twos: int, threes: int):
        if i == len(BRANCH_TYPES):
            return ((),) if (branches, twos, threes) == (0, 0, 0) else ()
        _, b, c = BRANCH_TYPES[i]
        output = []
        for count in range(branches + 1):
            if count * b > twos or count * c > threes:
                break
            for tail in rec(
                i + 1,
                branches - count,
                twos - count * b,
                threes - count * c,
            ):
                output.append((count,) + tail)
        return tuple(output)

    return rec(0, 24, target_b, t)


def mandatory_weight_three_matching(counts: tuple[int, ...]) -> bool:
    expanded = []
    for branch_type, count in zip(BRANCH_TYPES, counts):
        expanded.extend([branch_type] * count)
    assert len(expanded) == 24
    for i, (a_i, _, c_i) in enumerate(expanded):
        for j, (a_j, _, c_j) in enumerate(expanded):
            if i != j and (c_i > a_j or c_j > a_i):
                return False
    return True


def surviving_signatures(t: int) -> tuple[tuple[int, ...], ...]:
    return tuple(c for c in branch_multisets(t) if mandatory_weight_three_matching(c))


def odd_partition_min_pairs(n: int, blocks: int) -> int:
    if blocks <= 0 or n < blocks or (n - blocks) % 2:
        raise ValueError("positive odd block sizes cannot have these margins")
    increments, remainder = divmod((n - blocks) // 2, blocks)
    small = 1 + 2 * increments
    large = small + 2
    return (blocks - remainder) * small * (small - 1) // 2 + remainder * large * (large - 1) // 2


def boundary_summary(t: int) -> dict[str, int]:
    odd_negative = 150 + 4 * t
    code_weight = 34 + odd_negative
    minimum_pairs = odd_partition_min_pairs(odd_negative, 24) + 33 * odd_partition_min_pairs(odd_negative, 56)
    n2 = 9 - 3 * t
    max_e22 = n2 * (n2 - 1) // 2
    max_odd_edges = 531 + 50 * t + 4 * max_e22
    available_nonedge_pairs = odd_negative * (odd_negative - 1) // 2 - max_odd_edges
    return {
        "odd_negative": odd_negative,
        "code_weight": code_weight,
        "minimum_resolution_pairs": minimum_pairs,
        "available_nonedge_pairs": available_nonedge_pairs,
        "pair_slack": available_nonedge_pairs - minimum_pairs,
    }


def signature_digest() -> str:
    payload = {
        str(t): [list(signature) for signature in surviving_signatures(t)]
        for t in range(4)
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def main() -> None:
    for r in range(5, 201):
        audit_uniform_extension(r)
    p = uniform_parameters(7)
    print("uniform extension algebra r=5..200: PASS")
    print(f"r=7 profile: 0^1, 7^{p['k']}, 8^{p['k'] * 49}")

    raw_counts = []
    surviving_counts = []
    for t in range(4):
        raw = len(branch_multisets(t))
        surviving = len(surviving_signatures(t))
        raw_counts.append(raw)
        surviving_counts.append(surviving)
        summary = boundary_summary(t)
        print(
            f"t={t}: code_weight={summary['code_weight']}, "
            f"odd_resolution_support={summary['odd_negative']}, "
            f"signatures={raw}->{surviving}, "
            f"pair_slack={summary['pair_slack']}"
        )
    assert raw_counts == [12, 16, 11, 2]
    assert surviving_counts == [12, 16, 8, 2]
    print(f"canonical_signature_sha256={signature_digest()}")
    print("Moore near-Hoffman boundary audit: PASS")


if __name__ == "__main__":
    main()
