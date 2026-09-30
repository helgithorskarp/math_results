"""Finite checks of a direct corollary of published HKLT Theorem 1.9.

six-covering-3, researcher. This does not claim a new density principle.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
import json


def polynomial(t, u, v):
    return (F(7, 20) + F(23, 15)*t + F(39, 20)*u + F(9, 4)*v
            - F(1, 5)*t*u - F(1, 3)*t*v - F(3, 4)*u*v - t*u*v)


controls = []
for A, B, C in product(range(2, 5), range(1, 4), range(1, 4)):
    moduli = sorted(2**a * 3**b * 5**c
                    for a, b, c in product(range(A+1), range(B+1), range(C+1))
                    if 2**a * 3**b * 5**c >= 8)
    singles = sum((F(1, m) for m in moduli), F())
    pairs = sum((F(1, m*n) for m, n in combinations(moduli, 2) if gcd(m, n) == 1), F())
    triples = sum((F(1, m*n*k) for m, n, k in combinations(moduli, 3)
                   if gcd(m, n) == gcd(m, k) == gcd(n, k) == 1), F())
    t = F(1, 4) - F(1, 2**A)
    u = F(1, 6) - F(1, 2 * 3**B)
    v = F(1, 20) - F(1, 4 * 5**C)
    if singles - pairs + triples != polynomial(t, u, v):
        raise RuntimeError('finite coprime subset sum differs from the derived polynomial')
    controls.append({'exponents': [A, B, C], 'moduli': len(moduli),
                     'singles': str(singles), 'pairs': str(pairs),
                     'triples': str(triples), 'density_bound': str(singles-pairs+triples)})

max_t, max_u, max_v = F(1, 4), F(1, 6), F(1, 20)
derivatives = {'t': F(23, 15) - max_u/5 - max_v/3 - max_u*max_v,
               'u': F(39, 20) - max_t/5 - 3*max_v/4 - max_t*max_v,
               'v': F(9, 4) - max_t/3 - 3*max_u/4 - max_t*max_u}
if any(value <= 0 for value in derivatives.values()):
    raise RuntimeError('monotonicity not established')
limits = {}
for A in range(2, 9):
    bound = polynomial(F(1, 4) - F(1, 2**A), max_u, max_v)
    formula = F(23, 20) - F(59, 40 * 2**A)
    if bound != formula:
        raise RuntimeError('unrestricted ternary/five limit differs')
    limits[str(A)] = str(bound)
report = {'agent': 'six-covering-3', 'role': 'researcher',
          'source_theorem': 'HKLT Theorem 1.9, https://arxiv.org/html/2605.18644',
          'finite_polynomial_checks': controls,
          'positive_partial_derivative_lower_bounds': {key: str(value) for key, value in derivatives.items()},
          'binary_cap_bounds_both_other_exponents_unrestricted': limits,
          'novelty_status': 'direct corollary of published theorem; not a new density theorem',
          'comparison': 'a<=4 has published coprime-only upper bound 677/640>1; the separate new anchor certificate excludes it'}
print(json.dumps({key: value for key, value in report.items() if key != 'finite_polynomial_checks'}, indent=2))
print('All 27 finite coprime-pair/triple sums agree with the polynomial.')
