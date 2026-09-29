#!/usr/bin/env python3
"""Independent exact reconstruction by rational tensor interpolation.

No import from verify.py. Evaluate each integral by multiplying its eight
linear factors in t, then invert the two rational Bernstein sample matrices.
Compare every certificate coefficient, rather than only coefficient counts.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError("Run this exact checker without Python optimization flags.")


def direct_value(k, a, u):
    m = 8 - k
    c = Q(1) + Q(8, m) * a * u
    t_coefficients = [Q(1)]
    for slope in [-a] * k + [-a * c] * m:
        new = [Q(0)] * (len(t_coefficients) + 1)
        for j, v in enumerate(t_coefficients):
            new[j] += (1 + a) * v
            new[j + 1] += slope * v
        t_coefficients = new
    return 9 * sum((v / (j + 1) for j, v in enumerate(t_coefficients)), Q(0)) - c ** m


@lru_cache(None)
def inverse_sampling_matrix(n):
    points = [Q(i, n) for i in range(n + 1)]
    a = [[Q(comb(n, j)) * x ** j * (1 - x) ** (n - j)
          for j in range(n + 1)] for x in points]
    rows = [row + [Q(i == j) for j in range(n + 1)] for i, row in enumerate(a)]
    for col in range(n + 1):
        pivot = next(i for i in range(col, n + 1) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        v = rows[col][col]
        rows[col] = [x / v for x in rows[col]]
        for i in range(n + 1):
            if i != col and rows[i][col]:
                v = rows[i][col]
                rows[i] = [x - v * y for x, y in zip(rows[i], rows[col])]
    assert [row[:n + 1] for row in rows] == [
        [Q(i == j) for j in range(n + 1)] for i in range(n + 1)]
    inverse = [row[n + 1:] for row in rows]
    # Audit the original sampling matrix as well as the row-reduced one.
    assert [[sum((inverse[i][r] * a[r][j] for r in range(n + 1)), Q(0))
             for j in range(n + 1)] for i in range(n + 1)] == [
        [Q(i == j) for j in range(n + 1)] for i in range(n + 1)]
    return inverse


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    assert certificate["format"] == "degree9-origin-bernstein-v1"
    assert len(certificate["profiles"]) == 8
    count = 0
    for k, profile in enumerate(certificate["profiles"]):
        assert profile["k"] == k
        d, e = 16 - k, 8 - k
        assert (profile["a_degree"], profile["u_degree"]) == (d, e)
        expected = [[Q(v) for v in row] for row in profile["coefficients"]]
        assert len(expected) == d + 1 and all(len(row) == e + 1 for row in expected)
        values = [[direct_value(k, Q(i, d), Q(j, e))
                   for j in range(e + 1)] for i in range(d + 1)]
        ia, iu = inverse_sampling_matrix(d), inverse_sampling_matrix(e)
        left = [[sum((ia[i][r] * values[r][j] for r in range(d + 1)), Q(0))
                 for j in range(e + 1)] for i in range(d + 1)]
        found = [[sum((left[i][s] * iu[j][s] for s in range(e + 1)), Q(0))
                  for j in range(e + 1)] for i in range(d + 1)]
        assert found == expected, f"entry-level interpolation mismatch for k={k}"
        assert all(v == 0 or v >= 8 for row in found for v in row)
        zeros = [(i, j) for i, row in enumerate(found) for j, v in enumerate(row) if not v]
        assert zeros == ([(d, e)] if k in (0, 7) else [])
        count += (d + 1) * (e + 1)
        print(f"PASS: independent tensor interpolation k={k}, entries={(d + 1) * (e + 1)}")
    assert count == 636
    # The two boundary profiles are the binomial and thin equality controls.
    assert direct_value(0, Q(1), Q(1)) == 0
    assert direct_value(7, Q(1), Q(1)) == 0
    assert all(direct_value(k, Q(0), Q(j, 8 - k)) == 8
               for k in range(8) for j in range(9 - k))
    print("PASS: all 636 certificate entries independently reconstructed")
    print("PASS: binomial/thin boundary controls and a=0 normalization")


if __name__ == "__main__":
    main()
