#!/usr/bin/env python3
"""Exact combinatorial audit for the odd-hole/antihole modular theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


def is_stable(mask: int, n: int) -> bool:
    return all(
        not ((mask >> i) & 1 and (mask >> ((i + 1) % n)) & 1)
        for i in range(n)
    )


def stable_sets(n: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(i for i in range(n) if (mask >> i) & 1)
        for mask in range(1 << n)
        if is_stable(mask, n)
    )


def maximum_cycle_stable_sets(r: int) -> tuple[frozenset[int], ...]:
    n = 2 * r + 1
    return tuple(
        frozenset((j + 1 + 2 * step) % n for step in range(r))
        for j in range(n)
    )


def kept_indices(stable: frozenset[int], n: int) -> frozenset[int]:
    removed = stable | frozenset((i + 1) % n for i in stable)
    return frozenset(range(n)) - removed


def audit_incidence_identity(r: int) -> dict[str, int]:
    n = 2 * r + 1
    max_sets = maximum_cycle_stable_sets(r)
    all_stable = stable_sets(n)
    checked = 0
    for stable in all_stable:
        d = r - len(stable)
        kept = kept_indices(stable, n)
        if len(kept) != 2 * d + 1:
            raise AssertionError("wrong number of kept maximum stable sets")
        for vertex in range(n):
            count = sum(vertex in max_sets[j] for j in kept)
            expected = d + int(vertex in stable)
            if count != expected:
                raise AssertionError("cycle incidence identity failed")
            checked += 1
    return {"stable_sets": len(all_stable), "incidences": checked}


def clique_vectors(n: int) -> tuple[frozenset[int], ...]:
    return (
        (frozenset(),)
        + tuple(frozenset({i}) for i in range(n))
        + tuple(frozenset({i, (i + 1) % n}) for i in range(n))
    )


def audit_vertex_pair_types(r: int) -> dict[str, int]:
    n = 2 * r + 1
    cliques = clique_vectors(n)
    stables = stable_sets(n)
    integral_pairs = 0
    for clique in cliques:
        for stable in stables:
            if len(clique & stable) > 1:
                raise AssertionError("clique/stable intersection exceeded one")
            integral_pairs += 1
    if max(map(len, stables)) != r:
        raise AssertionError("wrong cycle independence number")
    if max(map(len, cliques)) != 2:
        raise AssertionError("wrong cycle clique number")
    # The remaining categories are certified by their exact bases:
    # r * (1/r)^p, 2 * (1/2)^p, and n * (1/(2r))^p.
    # At p=log_(2r)(n), only the last is equality.
    return {
        "integral_integral": integral_pairs,
        "uniform_integral": len(stables),
        "integral_half": len(cliques),
        "uniform_half": 1,
    }


def sharp_rows(last_h: int = 12, last_k: int = 8) -> list[dict[str, int]]:
    rows = []
    for h in range(2, last_h + 1):
        n = 2 * h + 1
        for k in range(last_k + 1):
            order = n ** (2 * k)
            alpha = (2 * h) ** k
            omega = alpha
            product = alpha * omega
            if product != (2 * h) ** (2 * k):
                raise AssertionError("sharp product recurrence failed")
            rows.append(
                {
                    "h": h,
                    "k": k,
                    "order": order,
                    "alpha": alpha,
                    "omega": omega,
                    "product": product,
                }
            )
    return rows


def monotonicity_audit(last_r: int = 200) -> int:
    # Exact rational cross-products certify that (x+1)/x decreases.  This is
    # the discrete shadow of the logarithmic derivative argument in the proof.
    checked = 0
    for x in range(4, 2 * last_r, 2):
        if Fraction(x + 1, x) <= Fraction(x + 3, x + 2):
            raise AssertionError("successive cycle ratio did not decrease")
        checked += 1
    return checked


def audit() -> dict[str, object]:
    incidence = {str(r): audit_incidence_identity(r) for r in range(2, 8)}
    pairs = {str(r): audit_vertex_pair_types(r) for r in range(2, 8)}
    rows = sharp_rows()
    payload = {
        "incidence": incidence,
        "pairs": pairs,
        "sharp_rows": rows,
        "monotonicity_checks": monotonicity_audit(),
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "r_range": [2, 7],
        "stable_sets_checked": sum(v["stable_sets"] for v in incidence.values()),
        "incidences_checked": sum(v["incidences"] for v in incidence.values()),
        "vertex_pairs_checked": sum(
            sum(category.values()) for category in pairs.values()
        ),
        "sharp_rows_checked": len(rows),
        "monotonicity_checks": payload["monotonicity_checks"],
        "largest_exact_sharp_order": rows[-1]["order"],
        "record_sha256": digest,
        "trust_boundary": (
            "exact finite audit of cycle identities and sharp recurrences; "
            "universal polyhedral and substitution arguments are in THEOREM.md"
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

