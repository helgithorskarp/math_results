"""Exact finite validation for the prose theorem; Python 3.11+, standard library."""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json

from audit import check, demand
from forcing import certificate, threshold


def polynomials():
    # Rational evaluations on an interpolation grid, with degree at most
    # (3,3,2) in (m,q,h), check identity (7) coefficientwise by interpolation.
    for m, q, h in product(range(4), range(4), range(3)):
        ell = m + q
        k = 2 * ell + 1 + h
        u = k - ell
        F = k * k + (Q((ell + 1) * (ell - 2), 2) + 2) * k + ell * (ell - 2)
        Us = Q(ell * (ell + 1), 2) + ell * m - Q(m * (m + 1), 2)
        Ws = (q + 1) * (Us + u * (2 * m + 1)) + m * (m + 1) + Q(q * (q - 1), 2) + 2 * (u - 1)
        P = 2 * m**3 - 2 * m * q * q + q**3
        T = m * m + 4 * m * q + 4 * q * q - 5 * m - q + 2
        demand(2 * (F - Ws) == P + T + h * ((m - q)**2 + 3 * m + 5 * q) + 2 * h * h, 'polynomial gap identity')
    for a, b in product(range(4), repeat=2):
        m, q, r = a + b, a, b
        demand(2*m**3 - 2*m*q*q + q**3 == q**3 + 4*q*q*r + 6*q*r*r + 2*r**3, 'first cubic identity')
        m, q, r = a, a + b, b
        demand(2*m**3 - 2*m*q*q + q**3 == m*(m-r)**2 + m*m*r + r**3, 'second cubic identity')
        m, q, x, y = a + 1, b + 1, a, b
        demand(m*m+4*m*q+4*q*q-5*m-q+2 == x*x+4*x*y+4*y*y+x+11*y+5, 'quadratic identity')
    return 96


def compression(k, ell, B):
    R = [i for i in range(1, 2 * ell) if i not in B][:ell]
    if R == list(range(1, ell + 1)) or R == list(range(1, 2 * ell, 2)):
        return False
    m = len(B)
    q = ell - m
    a = next(R[i] for i in range(ell - 1) if R[i + 1] == R[i] + 1)
    v, u = min(B), k - ell
    U = sum(R)
    demand(U == ell*(ell+1)//2 + sum(max(ell+i-b, 0) for i, b in enumerate(B, 1)), 'rank identity')
    d = 2*m+1-a
    demand(d >= 0, 'first adjacency bound')
    for i, b in enumerate(B, 1):
        demand(2*i-d <= b <= ell+q+i-1, 'blue rank bounds')
    S = U + u*a
    W = sum(B)+(q+1)*S+q*(q-1)//2+(u-1)*v
    Us = ell*(ell+1)//2+ell*m-m*(m+1)//2
    Ws = (q+1)*(Us+u*(2*m+1))+m*(m+1)+q*(q-1)//2+2*(u-1)
    demand(W <= Ws < threshold(k, ell), 'compression/range inequality')
    if R not in ([1, 3, 4], [1, 4, 5]):
        r = next(r for r in R if r > v and r not in (a, a+1))
        demand(0 < r-v <= ell+1 <= u, 'terminal gap')
    return True


def lower_control(k, ell):
    N = threshold(k, ell) - 1
    T = k + (ell+1)*(ell-2)//2
    colors = [[x for x in range(1, N+1) if (x <= T or x > (k+1)*T) == red] for red in (True, False)]
    mask = (1 << (N+1)) - 1
    for values in colors:
        dp = [[0]*(ell+1) for _ in range(k+1)]
        dp[0][0] = 1
        for value in values:
            nxt = [row[:] for row in dp]
            for t in range(k):
                for d in range(ell+1):
                    if not dp[t][d]:
                        continue
                    for copies in range(1, min(k-t, N//value)+1):
                        nxt[t+copies][min(ell, d+1)] |= (dp[t][d] << (copies*value)) & mask
            dp = nxt
        color_bits = sum(1 << x for x in values)
        demand(dp[k][ell] & color_bits == 0, 'at-least-distinct lower coloring')
    return N


def negative_controls():
    k, ell, B = 7, 3, []
    original = list(certificate(k, ell, B))
    cases = []
    bad = [row[:] for row in original]; bad[0] = [(1, 5), (2, 1), (3, 0)]; cases.append((bad, threshold(k, ell)))
    bad = [row[:] for row in original]; bad[0] = [(1, 4), (2, 1), (3, 1)]; cases.append((bad, threshold(k, ell)))
    bad = [row[:] for row in original]; bad[0] = [(1, 4), (1, 1), (3, 2)]; cases.append((bad, threshold(k, ell)))
    bad = [row[:] for row in original]; bad[0] = [(1, 4), (2, 1), (70, 2)]; cases.append((bad, threshold(k, ell)))
    cases.append(([], threshold(k, ell)))
    cases.append((original, threshold(k, ell)-1))
    rejected = 0
    for sums, bound in cases:
        try:
            check(k, ell, B, sums, bound)
        except ValueError:
            rejected += 1
    demand(rejected == len(cases), 'invalid certificate accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-ell', type=int, default=9)
    args = parser.parse_args()
    demand(args.max_ell >= 3, 'max ell')
    polynomials()
    digest = hashlib.sha256()
    rows = []
    total = total_steps = total_compression = 0
    for ell in range(3, args.max_ell+1):
        instances = steps = compressions = 0
        for m in range(ell):
            for B in combinations(range(1, 2*ell), m):
                # The three consecutive k values also cover every residue in
                # the exceptional mod-3 construction.
                for k in range(2*ell+1, 2*ell+4):
                    checked = check(k, ell, B, certificate(k, ell, B), threshold(k, ell))
                    comp = compression(k, ell, B)
                    digest.update(json.dumps([ell, k, B, checked, comp], separators=(',', ':')).encode())
                    instances += 1; steps += checked; compressions += comp
        rows.append({'ell': ell, 'instances': instances, 'checked_sums': steps, 'compression_cases': compressions})
        total += instances; total_steps += steps; total_compression += compressions
    # Large parameters validate that the generator stores multiplicities,
    # rather than enumerating k summands or assuming machine-sized integers.
    large_cases = [(10**30+7, 3, [2,3]), (10**30+8, 3, [2,5]),
                   (10**30+9, 12, [2,4,6,8,10]), (10**30+10, 12, [])]
    for k, ell, B in large_cases:
        check(k, ell, B, certificate(k, ell, B), threshold(k, ell))
    lower = [{'k': k, 'ell': ell, 'avoiding_interval': lower_control(k, ell)} for k, ell in [(7,3), (8,3), (9,4), (11,5)]]
    result = {'status': 'ALL_EXACT_CHECKS_PASSED', 'scope': 'finite validation of a prose theorem',
              'prefix_instances': total, 'checked_sums': total_steps,
              'compression_cases': total_compression, 'by_ell': rows,
              'record_sha256': digest.hexdigest(), 'large_integer_cases': len(large_cases),
              'lower_construction_controls': lower, 'invalid_certificates_rejected': negative_controls(),
              'main_polynomial_grid_nodes': 48, 'auxiliary_polynomial_grid_nodes': 48}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
