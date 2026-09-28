"""Directly check three adversarial 537-colour strings, including x=y."""

from __future__ import annotations

import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def decode(text: str, length: int) -> list[int]:
    digits = text.strip()
    require(len(digits) == length and set(digits) == set("123456"),
            f"expected {length} colours 1,...,6")
    return [0] + [int(char) for char in digits]


def integer_violations(colour: list[int]) -> list[tuple[int, int, int]]:
    n = len(colour) - 1
    return [(x, y, x + y)
            for x in range(1, n + 1)
            for y in range(x, n - x + 1)
            if colour[x] == colour[y] == colour[x + y]]


def main() -> None:
    baseline = decode((HERE / "baseline.txt").read_text(encoding="ascii"), 536)
    require(not integer_violations(baseline), "536 baseline is not sum-free")

    # Fredricksen--Sweet's symmetric partition is also modular sum-free on
    # nonzero residues modulo 537. This validates the multiplier seed rule.
    modular_checks = 0
    for x in range(1, 537):
        for y in range(x, 537):
            z = (x + y) % 537
            if z:
                require(baseline[x] != baseline[y] or baseline[x] != baseline[z],
                        f"modular baseline violation {(x, y, z)}")
                modular_checks += 1

    fixtures = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
    require(isinstance(fixtures, list) and len(fixtures) == 3, "expected three fixtures")
    multipliers = set()
    observed = []
    for fixture in fixtures:
        m = fixture["multiplier"]
        require(type(m) is int and 1 <= m < 537 and gcd(m, 537) == 1,
                "invalid multiplier")
        require(m not in multipliers, "duplicate multiplier")
        multipliers.add(m)
        colour = decode(fixture["colors"], 537)
        bad = integer_violations(colour)
        claimed = tuple(fixture["expected_bad_triple"])
        require(len(bad) == 1 and bad[0] == claimed and claimed[0] == claimed[1],
                f"wrong violation set for multiplier {m}: {bad}")
        observed.append(f"{m}:{claimed[0]}+{claimed[1]}={claimed[2]}")

    require(multipliers == {190, 347, 359}, "unexpected fixture provenance")
    print(f"PASS baseline_triples=71824 modular_checks={modular_checks} "
          f"fixtures={len(fixtures)} defects=" + ",".join(observed))


if __name__ == "__main__":
    main()
