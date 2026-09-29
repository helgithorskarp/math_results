#!/usr/bin/env python3
"""Exact power-basis generation and tensor Bernstein certificate verification."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
FORMAT = "degree9-origin-bernstein-v1"
if not __debug__:
    raise RuntimeError("Run this exact checker without Python optimization flags.")


def power_coefficients(k):
    """Expand the integral in PROOF.md (9) by binomial coefficients."""
    m = 8 - k
    c = defaultdict(F)
    for i in range(k + 1):
        for j in range(m + 1):
            v = F(9 * comb(k, i) * comb(m, j) * (-1) ** (i + j), i + j + 1)
            for ell in range(9 - i - j):
                for h in range(j + 1):
                    c[i + j + ell + h, h] += (
                        v * comb(8 - i - j, ell) * comb(j, h) * F(8, m) ** h
                    )
    for h in range(m + 1):
        c[h, h] -= comb(m, h) * F(8, m) ** h
    return {ij: v for ij, v in c.items() if v}


def bernstein_coefficients(c, d, e):
    """Use x^r=sum_i C(i,r)/C(d,r) B_i^d(x) in each variable."""
    return [
        [sum((v * F(comb(i, r), comb(d, r)) * F(comb(j, s), comb(e, s))
              for (r, s), v in c.items() if r <= i and s <= j), F(0))
         for j in range(e + 1)]
        for i in range(d + 1)
    ]


def generate():
    profiles = []
    for k in range(8):
        d, e = 16 - k, 8 - k
        c = power_coefficients(k)
        assert max(r for r, s in c) == d
        assert max(s for r, s in c) == e
        b = bernstein_coefficients(c, d, e)
        profiles.append({"k": k, "a_degree": d, "u_degree": e,
                         "coefficients": [[str(v) for v in row] for row in b]})
    return {"format": FORMAT, "profiles": profiles}


def verify_negative_bounds():
    # E(a)=a+c(a)=1+3a/4-a^2; c(a)=1-a^2-a/4.
    intervals = [(F(0), F(1, 2)), (F(1, 2), F(5, 8)), (F(5, 8), F(3, 4))]
    expected = [F(58871586708267913, 101330991615836160),
                F(43046721, 60817408), F(3939120870619581, 4503599627370496)]
    for (lo, hi), bound in zip(intervals, expected):
        vertex = max(lo, min(F(3, 8), hi))
        endpoint_max = 1 + F(3, 4) * vertex - vertex * vertex
        c_min = 1 - hi * hi - hi / 4
        assert c_min > 0
        assert endpoint_max ** 9 / (9 * c_min) == bound
        assert bound < 1
    print("PASS: all 3 exact negative-coordinate polar bounds are < 1")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true",
                        help="regenerate the small certificate before verifying it")
    args = parser.parse_args()
    calculated = generate()
    path = HERE / "certificate.json"
    if args.write_certificate:
        # One coefficient row per line; no transient or large output.
        lines = ['{', '  "format": "' + FORMAT + '",', '  "profiles": [']
        for index, p in enumerate(calculated["profiles"]):
            lines.extend(['    {', f'      "k": {p["k"]},',
                          f'      "a_degree": {p["a_degree"]},',
                          f'      "u_degree": {p["u_degree"]},',
                          '      "coefficients": ['])
            for i, row in enumerate(p["coefficients"]):
                lines.append('        ' + json.dumps(row) + (',' if i < len(p["coefficients"]) - 1 else ''))
            lines.extend(['      ]', '    }' + (',' if index < 7 else '')])
        lines.extend(['  ]', '}'])
        path.write_text('\n'.join(lines) + '\n')
    certificate = json.loads(path.read_text())
    assert certificate == calculated, "entry-level certificate mismatch"
    total = positives = 0
    for p in certificate["profiles"]:
        k, d, e = p["k"], p["a_degree"], p["u_degree"]
        b = [[F(v) for v in row] for row in p["coefficients"]]
        flat = [v for row in b for v in row]
        assert all(v >= 0 for v in flat)
        assert b[0] == [F(8)] * (e + 1)
        zeros = [(i, j) for i, row in enumerate(b) for j, v in enumerate(row) if not v]
        assert zeros == ([(d, e)] if k in (0, 7) else [])
        assert min(v for v in flat if v > 0) == 8
        total += len(flat)
        positives += sum(v > 0 for v in flat)
        print(f"PASS: k={k}, degrees=({d},{e}), coefficients={len(flat)}, zeros={len(zeros)}")
    assert (total, positives) == (636, 634)
    print("PASS: all 636 Bernstein coefficients, 634 positive, minimum positive 8")
    print("PASS: all a-index-zero rows equal 8; uniform origin gap follows")
    verify_negative_bounds()


if __name__ == "__main__":
    main()
