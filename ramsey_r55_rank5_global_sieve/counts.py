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


STAGES = [
    ('no_zero_pair',20,23,20,23),
    ('zero_multiplicity_caps',20,23,1,2),
    ('previous_row_cap_four',4,23,1,2),
    ('column_cap_five',4,5,1,2),
    ('new_row_cap_three',3,5,1,2),
]


def compute():
    m,n,r=20,23,5
    gl=group_order(r)
    numerator=total_span(m,r)*total_span(n,r)
    total,rem=divmod(numerator,gl)
    if rem: raise ArithmeticError('nonintegral full-rank quotient')
    low=lower_complement(m,n,r,m,n)
    stages=[{'stage':'rank_five_with_blue_rank_at_least_five',
             'raw':total,'complement_rank_four':low,'remaining':total-low}]
    for name,ac,bc,az,bz in STAGES:
        raw=pair_count(m,n,r,ac,bc,az,bz)
        low=lower_complement(m,n,r,ac,bc)
        stages.append({'stage':name,'raw':raw,'complement_rank_four':low,'remaining':raw-low})
    baseline=stages[0]['remaining'];remaining=stages[-1]['remaining']
    removed=baseline-remaining;f=Fraction(removed,baseline)
    incremental=stages[-2]['remaining']-remaining
    q=Fraction(incremental,stages[-2]['remaining'])
    return {'status':'EXACT_RANK5_GLOBAL_SIEVE_COUNTS','rank5_total':total,
            'factor_fiber':gl,'stages':stages,'baseline':baseline,
            'removed':removed,'remaining':remaining,'removed_fraction':[f.numerator,f.denominator],
            'quadruple_additional_removed':incremental,
            'quadruple_fraction_after_old_caps':[q.numerator,q.denominator],
            'internal_free_bits':443}


if __name__ == '__main__':
    print(json.dumps(compute(),indent=2,sort_keys=True))
