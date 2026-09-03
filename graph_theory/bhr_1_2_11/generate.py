#!/usr/bin/env python3
"""Generate the finite growable-realization certificate for {1,2,11}."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
from typing import Any

from cp_search import solve
from verify import U, admissible


def increments(
    base: tuple[int, int, int], varying: tuple[int, ...], max_order: int
) -> list[tuple[int, int, int]]:
    candidates = []
    maxima = [
        (max_order - sum(base)) // x + 1 if x in varying else 1 for x in U
    ]
    for ks in product(*(range(mx) for mx in maxima)):
        p = tuple(base[i] + ks[i] * U[i] for i in range(3))
        if sum(p) + 1 <= max_order and admissible(p):
            candidates.append(p)
    return sorted(candidates, key=lambda p: (sum(p), p))


@lru_cache(maxsize=None)
def solve_cached(
    p: tuple[int, int, int], required: tuple[int, ...]
) -> dict[str, object] | None:
    result, status = solve(p, required)
    if status not in ("INFEASIBLE", "OPTIMAL"):
        raise RuntimeError(f"search did not finish for {p}, grow={required}: {status}")
    return result


def find(
    base: tuple[int, int, int],
    varying: tuple[int, ...],
    required: tuple[int, ...],
    max_order: int,
) -> dict[str, Any] | None:
    for p in increments(base, varying, max_order):
        result = solve_cached(p, tuple(sorted(required)))
        if result:
            return {
                "counts": p,
                "grow": tuple(required),
                "path": result["path"],
                "growth": result["growth"],
            }
    return None


def replace(
    p: tuple[int, int, int], x: int, value: int
) -> tuple[int, int, int]:
    q = list(p)
    q[U.index(x)] = value
    return tuple(q)


def never_admissible_on_ray(p: tuple[int, int, int], varying: int) -> bool:
    """Exact criterion for this support (not a finite-search heuristic)."""
    a, b, _ = p
    return varying == 11 and (sum(p) + 1) % 11 == 0 and a + b < 10


def case_step(
    dp: tuple[int, int, int], fixed: int, max_order: int
) -> list[dict[str, Any]]:
    """Cover the residue-class plane whose ``fixed`` coordinate equals dp."""
    x, y = tuple(u for u in U if u != fixed)
    out = []
    corner = find(dp, (x, y), (x, y), max_order)
    if corner is None:
        raise RuntimeError(f"no two-axis corner from {dp}, fixed={fixed}")
    out.append(corner)
    x_corner = corner["counts"][U.index(x)]
    y_corner = corner["counts"][U.index(y)]

    xv = dp[U.index(x)]
    while xv < x_corner:
        strip = replace(dp, x, xv)
        ray = find(strip, (y,), (y,), max_order)
        if ray is None:
            if never_admissible_on_ray(strip, y):
                xv += x
                continue
            raise RuntimeError(f"no {y}-ray from {strip}")
        out.append(ray)
        y_ray = ray["counts"][U.index(y)]
        yv = dp[U.index(y)]
        while yv < y_ray:
            point = replace(strip, y, yv)
            if admissible(point):
                witness = find(point, (), (), max_order)
                if witness is None:
                    raise RuntimeError(f"no point witness for {point}")
                out.append(witness)
            yv += y
        xv += x

    yv = dp[U.index(y)]
    while yv < y_corner:
        strip = replace(dp, y, yv)
        ray = find(strip, (x,), (x,), max_order)
        if ray is None:
            if never_admissible_on_ray(strip, x):
                yv += y
                continue
            raise RuntimeError(f"no {x}-ray from {strip}")
        out.append(ray)
        x_ray = ray["counts"][U.index(x)]
        xv = dp[U.index(x)]
        while xv < x_ray:
            point = replace(strip, x, xv)
            if admissible(point):
                witness = find(point, (), (), max_order)
                if witness is None:
                    raise RuntimeError(f"no point witness for {point}")
                out.append(witness)
            xv += x
        yv += y
    return out


def make_case(
    base: tuple[int, int, int], max_order: int
) -> dict[str, Any]:
    cap = find(base, U, U, max_order)
    if cap is None:
        raise RuntimeError(f"no cap from {base}")
    out = [cap]
    current = base
    cap_counts = tuple(cap["counts"])
    while current != cap_counts:
        for x in U:
            i = U.index(x)
            if current[i] < cap_counts[i]:
                out.extend(case_step(current, x, max_order))
                current = replace(current, x, current[i] + x)
    unique = {}
    for witness in out:
        key = (tuple(witness["counts"]), tuple(witness["grow"]))
        unique[key] = witness
    return {"base": base, "cap": cap_counts, "witnesses": list(unique.values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-order", type=int, default=40)
    args = parser.parse_args()
    cases = []
    for b0 in (1, 2):
        for c0 in range(1, 12):
            base = (1, b0, c0)
            case = make_case(base, args.max_order)
            cases.append(case)
            print(
                f"case {base}: cap={case['cap']}, "
                f"witnesses={len(case['witnesses'])}",
                flush=True,
            )
    certificate = {"underlying_set": U, "cases": cases}
    args.output.write_text(
        json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    total = sum(len(case["witnesses"]) for case in cases)
    print(f"wrote {args.output}: {total} witnesses")


if __name__ == "__main__":
    main()
