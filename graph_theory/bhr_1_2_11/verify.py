#!/usr/bin/env python3
"""Definition-level verifier for the finite {1,2,11} BHR certificate."""

from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

U = (1, 2, 11)


class CertificateError(ValueError):
    """Raised when any certificate obligation fails."""


def require(condition: bool, message: object) -> None:
    if not condition:
        raise CertificateError(str(message))


def bdiff(x: int, y: int, n: int) -> int:
    d = abs(x - y)
    return min(d, n - d)


def is_stretched(u: int, w: int, x: int, m: int, n: int) -> bool:
    old = bdiff(u, w, n)
    uu = u if u <= m else u + x
    ww = w if w <= m else w + x
    return bdiff(uu, ww, n + x) != old


def verify_growth(path: list[int], x: int, m: int) -> None:
    n = len(path)
    require(x - 1 <= m <= n - 1 - x, ("growth range", n, x, m))
    interval = set(range(m - x + 1, m + 1))
    incidences: Counter[int] = Counter()
    for u, w in zip(path, path[1:]):
        if is_stretched(u, w, x, m, n):
            require(u in interval or w in interval, ("outside stretch", n, x, m, u, w))
            if u in interval:
                incidences[u] += 1
            if w in interval:
                incidences[w] += 1
    require(
        all(incidences[y] == 1 for y in interval),
        ("growth incidence", n, x, m, incidences),
    )


def grow_once(path: list[int], x: int, m: int) -> list[int]:
    """Apply the constructive step in the growable-realization lemma."""
    n = len(path)
    interval = set(range(m - x + 1, m + 1))
    embedded = {y: y if y <= m else y + x for y in range(n)}
    out = [embedded[path[0]]]
    for u, w in zip(path, path[1:]):
        if is_stretched(u, w, x, m, n):
            inside = [y for y in (u, w) if y in interval]
            require(len(inside) == 1, ("growth insertion", n, x, m, u, w))
            out.append(inside[0] + x)
        out.append(embedded[w])
    return out


def admissible(p: tuple[int, int, int]) -> bool:
    a, b, c = p
    v = a + b + c + 1
    return v >= 22 and (v % 11 != 0 or a + b >= 10)


def covers(witness: dict[str, Any], q: tuple[int, int, int]) -> bool:
    p = tuple(witness["counts"])
    grow = set(witness["grow"])
    for pi, qi, x in zip(p, q, U):
        if x in grow:
            if qi < pi or (qi - pi) % x:
                return False
        elif qi != pi:
            return False
    return True


def pattern_has_admissible_lift(
    q: tuple[int, int, int], high: tuple[bool, bool, bool]
) -> bool:
    """Decide whether an admissible triple maps to this clamped pattern."""
    if not any(high):
        return admissible(q)
    # A high a or b can vary v modulo 11.  If only c is high, its increments
    # are multiples of 11, so both v mod 11 and a+b remain fixed.
    if high[0] or high[1]:
        return True
    a, b, _ = q
    return (sum(q) + 1) % 11 != 0 or a + b >= 10


def verify_case(case: dict[str, Any]) -> int:
    base = tuple(case["base"])
    witnesses = case["witnesses"]
    require(
        len(base) == 3 and base[0] == 1 and base[1] in (1, 2) and 1 <= base[2] <= 11,
        ("bad base", base),
    )
    seen = set()
    for witness in witnesses:
        counts = tuple(witness["counts"])
        grow = tuple(witness["grow"])
        path = witness["path"]
        growth = {int(x): m for x, m in witness["growth"].items()}
        key = (counts, grow)
        require(key not in seen, ("duplicate witness", key))
        seen.add(key)
        require(len(counts) == 3 and all(c >= 1 for c in counts), ("bad counts", counts))
        require(
            all((c - r) % x == 0 for c, r, x in zip(counts, base, U)),
            ("wrong residue class", base, counts),
        )
        require(len(grow) == len(set(grow)) and set(grow) <= set(U), ("bad grow set", grow))
        require(set(growth) == set(grow), ("bad growth positions", grow, growth))
        n = sum(counts) + 1
        require(sorted(path) == list(range(n)), ("not a permutation", counts))
        actual = Counter(bdiff(u, v, n) for u, v in zip(path, path[1:]))
        expected = Counter(dict(zip(U, counts)))
        require(actual == expected, ("wrong edge counts", counts, actual))
        for x in grow:
            verify_growth(path, x, growth[x])
            grown = grow_once(path, x, growth[x])
            require(sorted(grown) == list(range(n + x)), ("bad grown permutation", counts, x))
            grown_actual = Counter(
                bdiff(u, v, n + x) for u, v in zip(grown, grown[1:])
            )
            enlarged = expected.copy()
            enlarged[x] += x
            require(grown_actual == enlarged, ("bad grown edge counts", counts, x))

    cap = tuple(case["cap"])
    require(
        any(tuple(w["counts"]) == cap and set(w["grow"]) == set(U) for w in witnesses),
        ("missing cap", base, cap),
    )

    # For each coordinate, max+step is a sentinel representing every larger
    # value in the residue class.  See the completeness argument in README.md.
    maxima = tuple(max(w["counts"][i] for w in witnesses) for i in range(3))
    axes = []
    for residue, step, maximum in zip(base, U, maxima):
        values = list(range(residue, maximum + 1, step))
        values.append(maximum + step)
        axes.append(values)
    checked = 0
    for q in itertools.product(*axes):
        high = tuple(q[i] > maxima[i] for i in range(3))
        if pattern_has_admissible_lift(q, high):
            require(any(covers(w, q) for w in witnesses), ("uncovered pattern", base, q, high))
            checked += 1
    return checked


def verify_certificate(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    require(tuple(data["underlying_set"]) == U, "wrong underlying set")
    cases = data["cases"]
    expected_cases = {(1, b, c) for b in (1, 2) for c in range(1, 12)}
    require({tuple(case["base"]) for case in cases} == expected_cases, "missing residue class")
    require(len(cases) == 22, "duplicate residue class")
    checked = sum(verify_case(case) for case in cases)
    witnesses = sum(len(case["witnesses"]) for case in cases)
    maximum_order = max(
        sum(w["counts"]) + 1 for case in cases for w in case["witnesses"]
    )
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "cases": len(cases),
        "witnesses": witnesses,
        "maximum_order": maximum_order,
        "admissible_symbolic_patterns_checked": checked,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    summary = verify_certificate(args.certificate)
    print(f"certificate_sha256={summary['certificate_sha256']}")
    print(
        f"cases={summary['cases']} witnesses={summary['witnesses']} "
        f"maximum_order={summary['maximum_order']}"
    )
    print(
        "admissible_symbolic_patterns_checked="
        f"{summary['admissible_symbolic_patterns_checked']}"
    )
    print("VERIFIED")


if __name__ == "__main__":
    main()
