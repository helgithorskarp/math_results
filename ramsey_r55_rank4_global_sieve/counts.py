"""Exact labeled matrix counts; no enumeration or solver status is imported."""
from functools import lru_cache
from math import comb, prod
from fractions import Fraction
import json


def gaussian(r, k):
    if not 0 <= k <= r:
        return 0
    return prod(2**r - 2**i for i in range(k)) // prod(2**k - 2**i for i in range(k))


@lru_cache(None)
def bins(m, n, cap):
    """Ordered words of length m on n letters, each used at most cap times."""
    a = [1] + [0] * m
    for _ in range(n):
        a = [sum(comb(j, t) * a[j-t] for t in range(min(j, cap)+1))
             for j in range(m+1)]
    return a[m]


def nonzero_span(m, r, cap):
    return sum(gaussian(r, k) * (-1)**(r-k) * 2**comb(r-k, 2)
               * bins(m, 2**k-1, cap) for k in range(r+1))


def affine_span(m, r, cap):
    """Spanning words in a fixed nonzero affine hyperplane of F2^r; m>0."""
    if m <= 0 or r < 1:
        raise ValueError("positive length and rank required")
    d = r-1
    return sum(2**(d-k) * gaussian(d, k) * (-1)**(d-k) * 2**comb(d-k, 2)
               * bins(m, 2**k, cap) for k in range(d+1))


def group_order(r):
    return prod(2**r - 2**i for i in range(r))


def total_span(m, r):
    return prod(2**m - 2**i for i in range(r))


def pair_count(m, n, r, acap, bcap, azero, bzero):
    """Full-rank factor pairs, no simultaneous zero entries; quotient by GL."""
    na = nonzero_span(m, r, acap)
    nb = nonzero_span(n, r, bcap)
    a = sum(comb(m, z)*nonzero_span(m-z, r, acap) for z in range(1, azero+1))
    b = sum(comb(n, z)*nonzero_span(n-z, r, bcap) for z in range(bzero+1))
    numerator = na*b + a*nb
    q, rem = divmod(numerator, group_order(r))
    if rem:
        raise ArithmeticError("nonintegral basis quotient")
    return q


def lower_complement(m, n, r, acap, bcap):
    numerator = (2**r-1)*2**(r-1)*affine_span(m, r, acap)*affine_span(n, r, bcap)
    q, rem = divmod(numerator, group_order(r))
    if rem:
        raise ArithmeticError("nonintegral complementary-rank quotient")
    return q


def compute():
    r, m, n = 4, 20, 23
    from math import factorial
    affine = 15*comb(15, 5)*factorial(20)*factorial(23)//(2**13*group_order(4))
    total = total_span(m, r)*total_span(n, r)//group_order(r)
    zero = pair_count(m, n, r, m, n, m, n)
    blue_low = lower_complement(m, n, r, m, n)
    rows = []
    for name, ac, bc, az, bz in [
        ("current_baseline", 20, 23, 20, 23),
        ("zero_multiplicity_caps", 20, 23, 1, 2),
        ("also_all_row_classes_at_most_four", 4, 23, 1, 2),
        ("also_all_column_classes_at_most_five", 4, 5, 1, 2),
    ]:
        raw = pair_count(m, n, r, ac, bc, az, bz)
        low = lower_complement(m, n, r, ac, bc)
        rows.append({"stage": name, "raw_zero_filtered": raw,
                     "complement_rank_three_overlap": low,
                     "previous_affine_family": affine, "remaining": raw-low-affine})
    baseline, remaining = rows[0]["remaining"], rows[-1]["remaining"]
    removed = baseline-remaining
    frac = Fraction(removed, baseline)
    return {"status": "EXACT_RANK4_GLOBAL_SIEVE_COUNTS", "rank4_total": total,
            "zero_pair_survivors": zero, "previous_complement_rank_three": blue_low,
            "previous_affine_family": affine, "stages": rows,
            "baseline": baseline, "remaining": remaining, "removed": removed,
            "removed_fraction": [frac.numerator, frac.denominator],
            "internal_free_bits": 443}


if __name__ == "__main__":
    print(json.dumps(compute(), indent=2, sort_keys=True))
