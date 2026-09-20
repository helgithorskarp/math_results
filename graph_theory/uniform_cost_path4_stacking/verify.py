#!/usr/bin/env python3
"""Exact finite checks for the uniform-cost P4 stacking theorem.

Only the Python standard library is used.  The main theorem is proved in the
README; these checks exercise its transfer arithmetic, local inequalities,
equality cases, and a low-mass raw-move control.
"""

from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def transfer(s: int, k: int) -> int:
    return k * s - (k * k - 1) * max(1, ceil_div(s, k))


def scores(c: tuple[int, ...], k: int) -> tuple[int, ...]:
    """All target scores on a path, with the empty-branch convention."""
    n = len(c)
    left = [0] * n
    right = [0] * n
    mass = 0
    for i in range(n - 1):
        mass += c[i]
        if mass:
            left[i] = transfer(c[i] + (left[i - 1] if i else 0), k)
    mass = 0
    for i in range(n - 1, 0, -1):
        mass += c[i]
        if mass:
            right[i] = transfer(c[i] + (right[i + 1] if i + 1 < n else 0), k)
    return tuple(
        c[i]
        + (left[i - 1] if i else 0)
        + (right[i + 1] if i + 1 < n else 0)
        for i in range(n)
    )


def nonstackable(c: tuple[int, ...], k: int) -> bool:
    return max(scores(c, k)) <= 0


def weak_compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from weak_compositions(total - first, parts - 1, prefix + (first,))


def raw_oracle(k: int):
    """Direct legal-move oracle; no transfer messages occur here."""

    @lru_cache(maxsize=None)
    def stacks(c: tuple[int, ...]) -> bool:
        if sum(value > 0 for value in c) == 1:
            return True
        n = len(c)
        for i, value in enumerate(c):
            if value < k:
                continue
            for j in (i - 1, i + 1):
                if 0 <= j < n:
                    child = list(c)
                    child[i] -= k
                    child[j] += 1
                    if stacks(tuple(child)):
                        return True
        return False

    return stacks


def formula_checks() -> int:
    checks = 0
    for k in range(3, 257):
        M = k * k - 1
        lam = k * k - k - 1
        A = k**3 - k - 1
        H = k**4 - k
        need(transfer(1, k) == -lam, "unit-message identity")
        need(transfer(-lam, k) == -A, "first negative identity")
        need(transfer(-A, k) == -(H - 1), "second negative identity")
        need(transfer(H - 1, k) == A, "heavy-message identity")
        need(transfer(A, k) == lam, "first positive identity")
        need(transfer(lam, k) == -1, "terminal positive identity")
        need(2 * (k - 1) * M < H, "two-pair strict inequality")
        need(k * M + (k - 1) * (M - 1) < H, "negative-message gap")
        for r in range(k - 1):
            c = (H - 1 - r, 0, 0, 1)
            need(scores(c, k) == (-r, -k * r, -r, -k * r),
                 "final-window score identity")
            checks += 1
    return checks


def branch_envelope_checks() -> int:
    checked = 0
    # This is deliberately wider than every branch used in the P3 censuses.
    for k in range(3, 10):
        M = k * k - 1
        A = k**3 - k - 1
        T = k**3 - k * k
        for x in range(2 * A + 1):
            for y in range(2 * A + 1):
                if x == y == 0:
                    continue
                p = 0 if y == 0 else transfer(y, k)
                m = transfer(x + p, k)
                X = m + A
                need(X >= 0, "negative branch excess")
                if X <= T:
                    # In this branch X/k is exact for realizable X, but use
                    # cross multiplication to keep the audit integer-only.
                    need(k * (x + y - 1) <= k * X,
                         "lower branch-envelope piece")
                else:
                    b = k * X - M * (k * k - k)
                    need(x + y <= 1 + k * b,
                         "upper branch-envelope piece")
                checked += 1
    return checked


def p3_checks() -> tuple[int, list[dict[str, int]]]:
    checked = 0
    rows = []
    for k in range(3, 8):
        M = k * k - 1
        A = k**3 - k - 1
        H3 = k**3 - k
        rhs = 1 + k * A
        bad_at_top = 0
        largest_bad = 0
        for mass in range(H3 + 2):
            for c in weak_compositions(mass, 3):
                q = scores(c, k)
                bad = max(q) <= 0
                if bad:
                    largest_bad = mass
                    if mass == H3:
                        bad_at_top += 1
                    if c[0] > 0:
                        D = -q[0]
                        need(mass + (k - 1) * c[0] + M * (D // k) <= rhs,
                             "left endpoint-deficit inequality")
                    if c[2] > 0:
                        D = -q[2]
                        need(mass + (k - 1) * c[2] + M * (D // k) <= rhs,
                             "right endpoint-deficit inequality")
                checked += 1
        need(largest_bad == H3, "P3 largest bad mass")
        need(bad_at_top == 2 * (k - 1), "P3 critical count")
        rows.append(
            {
                "cost": k,
                "largest_bad_mass": largest_bad,
                "critical_configurations": bad_at_top,
            }
        )
    return checked, rows


def p4_boundary_checks() -> tuple[int, list[dict[str, int]]]:
    checked = 0
    rows = []
    for k in (3, 4):
        H = k**4 - k
        counts = []
        examples = []
        for mass in (H, H + 1):
            bad = []
            for c in weak_compositions(mass, 4):
                if nonstackable(c, k):
                    bad.append(c)
                checked += 1
            counts.append(len(bad))
            examples.append(bad)
        expected = {(H - 1, 0, 0, 1), (1, 0, 0, H - 1)}
        need(set(examples[0]) == expected, "P4 critical classification")
        need(examples[1] == [], "P4 next-mass upper bound")
        rows.append(
            {
                "cost": k,
                "largest_bad_mass": H,
                "bad_at_largest_mass": counts[0],
                "bad_at_next_mass": counts[1],
            }
        )
    return checked, rows


def raw_move_controls() -> tuple[int, int]:
    compared = 0
    cache_states = 0
    for k, max_mass in ((3, 12), (4, 10)):
        stacks = raw_oracle(k)
        for mass in range(max_mass + 1):
            for c in weak_compositions(mass, 4):
                need(stacks(c) == (not nonstackable(c, k)),
                     "raw oracle/transfer disagreement")
                compared += 1
        # The final-window examples are separately checked by the raw rules.
        H = k**4 - k
        for r in range(k - 1):
            need(not stacks((H - 1 - r, 0, 0, 1)),
                 "raw left final-window witness")
            need(not stacks((1, 0, 0, H - 1 - r)),
                 "raw right final-window witness")
        cache_states += stacks.cache_info().currsize
    return compared, cache_states


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()

    formula_instances = formula_checks()
    branch_instances = branch_envelope_checks()
    p3_instances, p3_rows = p3_checks()
    p4_instances, p4_rows = p4_boundary_checks()
    raw_instances, raw_cache = raw_move_controls()
    result = {
        "status": "PASS",
        "formula_instances": formula_instances,
        "branch_configurations": branch_instances,
        "p3_configurations": p3_instances,
        "p3_rows": p3_rows,
        "p4_boundary_configurations": p4_instances,
        "p4_rows": p4_rows,
        "raw_move_comparisons": raw_instances,
        "raw_move_cached_states": raw_cache,
    }
    if args.check_expected:
        expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
        need(result == expected, "summary differs from expected.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
