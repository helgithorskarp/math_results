#!/usr/bin/env python3
"""Small exact definition-level and rejection controls, not graph enumeration."""

from fractions import Fraction as F
from math import comb
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory
import check


def main():
    polynomials = [(1, 4, 1, -11, -10, -1),
                   (1, 4, 2, -4, -11, -24)]
    intervals = [(F(1, 2), F(3, 5)), (F(1, 2), F(119, 200))]
    comparisons = 0
    for p, (lo, hi) in zip(polynomials, intervals):
        b = check.bernstein(p, lo, hi)
        n = len(p) - 1
        for j in range(13):
            t = F(j, 12)
            # Direct basis definition, independent of the coefficient conversion.
            in_basis = sum((b[k]*comb(n, k)*t**k*(1-t)**(n-k)
                            for k in range(n+1)), F(0))
            x = lo + (hi-lo)*t
            direct = sum((F(a)*x**k for k, a in enumerate(p)), F(0))
            check.require(in_basis == direct, "Bernstein definition mismatch")
            comparisons += 1

    raw = Path(__file__).with_name("incumbent_decimal.csv").read_text()
    rows = raw.splitlines()
    fixtures = {
        "duplicate": "\n".join([rows[1], *rows[1:]]),
        "zero_vector": "\n".join(["0,0,0", *rows[1:]]),
        "missing_point": "\n".join(rows[:-1]),
        "wrong_dimension": "\n".join(["1,2", *rows[1:]]),
    }
    rejected = []
    with TemporaryDirectory(dir=environ.get("TAMMES_CONTROL_SCRATCH")) as directory:
        for name, contents in fixtures.items():
            path = Path(directory)/f"{name}.csv"
            path.write_text(contents)
            try:
                check.coordinate_check(path)
            except RuntimeError:
                rejected.append(name)
            else:
                raise RuntimeError(f"invalid fixture accepted: {name}")
    check.require(len(rejected) == len(fixtures), "incomplete rejection control")
    print(f"PASS: {comparisons} exact Bernstein definition checks; "
          f"{len(rejected)} invalid coordinate fixtures rejected")


if __name__ == "__main__":
    main()
