#!/usr/bin/env python3
"""Exact checker for named-coordinate defect in the exact-nine branch."""

from __future__ import annotations

from collections import Counter
from math import factorial
from pathlib import Path


def multinomial(parts: tuple[int, ...]) -> int:
    answer = factorial(sum(parts))
    for part in parts:
        answer //= factorial(part)
    return answer


def generated_certificate() -> list[tuple[int, int, int, int, int, int]]:
    rows = []
    for before in range(8):
        for between in range(8 - before):
            after = 7 - before - between
            modulus = multinomial((before, between, after))
            remainder = 560 % modulus
            defect = min(remainder, modulus - remainder) if remainder else 0
            if defect:
                rows.append(
                    (before, between, after, modulus, remainder, defect)
                )
    return rows


def load_certificate() -> list[tuple[int, int, int, int, int, int]]:
    lines = Path(__file__).with_name("DEFECT_BOUNDS.tsv").read_text(
        encoding="ascii"
    ).splitlines()
    assert lines[0] == (
        "before\tbetween\tafter\tmultinomial\tremainder\tminimum_l1_defect"
    )
    return [tuple(map(int, line.split("\t"))) for line in lines[1:]]

def main() -> None:
    all_compositions = [
        (a, b, 7 - a - b)
        for a in range(8)
        for b in range(8 - a)
    ]
    assert len(all_compositions) == 36

    generated = generated_certificate()
    recorded = load_certificate()
    assert recorded == generated
    assert len(recorded) == 18

    by_modulus = Counter(row[3] for row in recorded)
    assert by_modulus == {21: 6, 42: 3, 105: 6, 210: 3}
    defect_per_link = sum(row[5] for row in recorded)
    assert defect_per_link == 504
    assert 9 * len(recorded) == 162
    assert 9 * defect_per_link == 4536

    first = next(row for row in recorded if row[:3] == (0, 2, 5))
    assert first == (0, 2, 5, 21, 14, 7)
    assert 560 == 26 * 21 + 14

    print("ordered composition layers: 36")
    print("forced asymmetric layers per exceptional link: 18")
    print("modulus multiplicities: 21:6 42:3 105:6 210:3")
    print("minimum L1 defect per exceptional link: 504")
    print("forced asymmetric layers across nine links: 162")
    print("minimum L1 defect across nine links: 4536")
    print("(0,2,5) certificate: 21 cells, remainder 14, defect 7")
    print("automorphism consequence: no 2-homogeneous coordinate action")
    print("all checks passed")


if __name__ == "__main__":
    main()
