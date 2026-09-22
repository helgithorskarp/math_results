#!/usr/bin/env python3
"""Exact verification for the full Lucas equal-area theorem package."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import direct
import layers

HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def partitions(total: int, least: int = 1, largest: int | None = None):
    """Nondecreasing tuples, so multiplicities and maps are unambiguous."""
    if type(total) is not int or total < 0 or type(least) is not int or least < 1:
        raise ValueError("invalid partition parameters")
    if largest is None:
        largest = total
    if total == 0:
        yield ()
        return
    for first in range(least, min(largest, total)+1):
        for rest in partitions(total-first, first, largest):
            yield (first,)+rest


@lru_cache(maxsize=None)
def all_partitions(total: int) -> tuple[tuple[int, ...], ...]:
    return tuple(partitions(total))


def stable_sources(a: int, b: int, total: int) -> tuple[tuple[int, ...], ...]:
    return tuple(part for part in partitions(total, 2, b)
                 if part and part[-1] > a)


def decrement(part: tuple[int, ...]) -> tuple[int, ...]:
    values = list(part)
    index = next(i for i, value in enumerate(values) if value > 2)
    values[index] -= 1
    return tuple(sorted(values))


def audit_partition_map() -> dict[str, int | str]:
    records = []
    maximum = 0
    sources = 0
    for a in range(1, 11):
        for b in range(a+1, 13):
            for i in range(a+1, 40, 2):  # adjusted below to i == a+1 (mod 2)
                if (i-(a+1)) % 2:
                    continue
                fibres: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
                targets = set(stable_sources(a, b, i))
                for source in stable_sources(a, b, i+1):
                    target = decrement(source)
                    require(target in targets, "map leaves target class")
                    fibres[target].append(source)
                    sources += 1
                local = max(map(len, fibres.values()), default=0)
                require(local <= 2, "partition-map fibre exceeds two")
                maximum = max(maximum, local)
                records.append((a, b, i, len(fibres), sum(map(len, fibres.values())), local))
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return {"cases": len(records), "sources": sources, "maximum_fibre": maximum,
            "record_sha256": digest}


def count_rectangle(total: int, width: int, height: int) -> int:
    return sum(1 for part in all_partitions(total) if len(part) <= height
               and (not part or part[-1] <= width))


def audit_rectangle_decomposition() -> dict[str, int | str]:
    records = []
    for width in range(1, 9):
        for height in range(1, 11):
            for total in range(0, 41):
                current = count_rectangle(total, width, height)
                before = count_rectangle(total-1, width, height) if total else 0
                no_one = tuple(part for part in partitions(total, 2, width))
                p_width = len(no_one)
                too_long = sum(len(part) > height for part in no_one)
                exact = (sum(1 for part in all_partitions(total-1) if len(part) == height
                             and part[-1] <= width) if total else 0)
                delta = current-before
                require(delta == p_width-too_long-exact,
                        "rectangle boundary decomposition failure")
                records.append((width, height, total, delta, p_width, too_long, exact))
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return {"identities": len(records), "record_sha256": digest}


def audit_kernel() -> dict[str, int]:
    two = three = 0
    for m in range(3, 301):
        fm = layers.lucas_schur(m-1)
        shifted = (0,)+layers.lucas_schur(m-3)
        require(all(x >= 2*(shifted[r] if r < len(shifted) else 0)
                    for r, x in enumerate(fm)), "twofold kernel failure")
        two += len(fm)
        if m >= 4:
            require(all(x >= 3*(shifted[r] if r < len(shifted) else 0)
                        for r, x in enumerate(fm)), "threefold kernel failure")
            three += len(fm)
    return {"twofold_coefficients": two, "threefold_coefficients": three}


def audit_boundary() -> tuple[dict[str, int | str], list[dict[str, object]]]:
    expected = json.loads((HERE / "BOUNDARY.json").read_text())
    parameters = tuple(tuple(row["parameters"]) for row in expected)
    require(parameters == layers.boundary_parameters(), "boundary list is not exhaustive")
    actual = []
    all_records = []
    for row in expected:
        a, b, c, d = row["parameters"]
        require(d == b*c//a, "bad boundary area")
        first = a+1
        left = layers.comparison(a, b, c)
        right = direct.comparison(a, b, c)
        require(left == right, "independent boundary algorithms disagree")
        ref1, ref2 = layers.reference(a, b, c), direct.reference(a, b, c)
        require(ref1 == ref2, "independent references disagree")
        margin = tuple(6*x-y for x, y in zip(left, ref1))
        require(not any(margin[:first]) and min(margin[first:]) > 0,
                "boundary margin failure")
        require(list(margin[first:]) == row["margin_coefficients"],
                "boundary certificate mismatch")
        require(not any(left[:first]) and left[first] == 1 and min(left[first:]) > 0,
                "boundary support failure")
        actual.append({"parameters": [a,b,c,d],
                       "margin_coefficients": list(margin[first:])})
        all_records.extend((a,b,c,d,r,left[r],ref1[r],margin[r])
                           for r in range(len(left)))
    digest = hashlib.sha256(json.dumps(all_records, separators=(",", ":")).encode()).hexdigest()
    return ({"cases": len(actual), "coefficients": len(all_records),
             "maximum_degree": max(row[1]*row[2] for row in parameters),
             "record_sha256": digest}, actual)


def regression_parameters() -> tuple[tuple[int, int, int], ...]:
    return tuple((a,b,c) for a in range(1, 15) for b in range(a+1, 16)
                 for c in range(b, 26) if b*c <= 180 and b*c % a == 0)


def audit_regressions() -> dict[str, int | str]:
    records = []
    for a, b, c in regression_parameters():
        left, right = layers.comparison(a,b,c), direct.comparison(a,b,c)
        require(left == right, "independent regression algorithms disagree")
        ref1, ref2 = layers.reference(a,b,c), direct.reference(a,b,c)
        require(ref1 == ref2, "independent regression references disagree")
        first = a+1
        margin = tuple(6*x-y for x,y in zip(left,ref1))
        require(not any(left[:first]) and left[first] == 1 and min(left[first:]) > 0,
                "regression support failure")
        require(not any(margin[:first]) and min(margin[first:]) >= 0,
                "regression margin failure")
        records.extend((a,b,c,r,left[r],ref1[r],margin[r]) for r in range(len(left)))
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return {"cases": len(regression_parameters()), "coefficients": len(records),
            "maximum_degree": max(b*c for a,b,c in regression_parameters()),
            "record_sha256": digest}


def main() -> None:
    boundary, certificate = audit_boundary()
    result = {"claim": "6D-G is Schur-positive for every canonical equal-area comparison",
              "boundary": boundary, "partition_map": audit_partition_map(),
              "rectangle_decomposition": audit_rectangle_decomposition(),
              "kernel": audit_kernel(), "tail_budget": layers.tail_budget(),
              "regressions": audit_regressions(), "all_checks": True}
    require(certificate == json.loads((HERE / "BOUNDARY.json").read_text()),
            "boundary replay mismatch")
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    require(result == expected, "output differs from EXPECTED.json")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
