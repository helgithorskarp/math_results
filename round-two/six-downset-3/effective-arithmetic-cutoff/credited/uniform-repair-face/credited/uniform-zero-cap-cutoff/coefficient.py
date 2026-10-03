"""Deletion-count separation for the lower Schur coefficient.

All arithmetic is exact. Uniform original-space and limit bridges must
be written separately; controls are not an extrapolation in q or k.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import sys

import reduce as r
require = r.require


def trivial(q, kappa):
    """Full S_q trivial bc-outside eigenvalue, with the zero-kappa gauge."""
    D = r.forms(q, 0)
    C, _ = r.evaluate(D, kappa, F(0), F(0))
    T = [D['keys'].index(key) for key in r.T_KEYS]
    target = D['keys'].index((6, 0, 1))
    keep = [i for i in range(len(D['keys'])) if i not in T]
    gauge = None
    if kappa == 0:
        gauge = D['keys'].index((0, 0, 1))
        keep.remove(gauge)
    G = r.submatrix(C, keep)
    j = keep.index(target)
    S, B, Y = r.schur(G, [j], [i for i in range(len(keep)) if i != j])
    require(S[0][0] > 0 and r.schur_psd(B) == len(B), 'full positive trivial target shorting')
    return S[0][0]/q, {'trivial_shorting': S, 'untouched_sha256': r.exact.digest(r.encode(B)),
                      'solve_sha256': r.exact.digest(r.encode(Y)), 'zero_kappa_gauge': gauge,
                      'full_fixed_dimension': len(D['keys']), 'shorted_untouched_dimension': len(B)}


GROUPS = ((0,), (0,), (1,), (2, 4), (3, 5), (6,))
TYPES = ((0, 1), (0, 2), (1, 1), (1, 1), (2, 1), (2, 1))


def standard_gram(q, kappa):
    """Original f(1)=1,f(2)=-1 standard frame; b/c-even multiplicity six."""
    tab, s = r.table(q), 3*q+4
    G = [[F(0)]*6 for _ in range(6)]
    for i, (core, size) in enumerate(TYPES):
        norm = 2*(q-2) if size == 2 else 2
        G[i][i] += s*len(GROUPS[i])*norm
        for j, (other_core, other_size) in enumerate(TYPES):
            count = sum(not (c & cc) for c in GROUPS[i] for cc in GROUPS[j])
            if not count:
                continue
            outside = -2 if size == other_size == 1 else (
                      -2*(q-2)*(q-3) if size == other_size == 2 else -2*(q-2))
            base, slope = tab[tuple(sorted((TYPES[i], TYPES[j])))]
            G[i][j] += count*outside*(base+kappa*slope)
    require(all(G[i][j] == G[j][i] for i in range(6) for j in range(6)), 'every standard Gram symmetry position')
    return G


def standard(q, kappa):
    G = standard_gram(q, kappa)
    S, B, Y = r.schur(G, [5], list(range(5)))
    nu = S[0][0]/2
    require(nu > 0 and r.schur_psd(G) == 6, 'full standard positivity and target coefficient')
    s, ww = F(3*q+4), F(3*q+4-F(3*q+2, q), q-1)
    A = r.submatrix(G, [0, 1])
    e = [G[0][5], G[1][5]]
    theta = sum(x*y[0] for x, y in zip(e, r.solve(A, [[x] for x in e])))
    closed = 2*(s*s-ww*ww)*(s-ww-3*theta)/(2*s*(s-ww)-(5*s-ww)*theta)
    require(nu == closed and theta > 0 and s-ww-3*theta > 0,
            'complete two-outside plus two-core-pair closed standard identity')
    return nu, {'standard_gram': G, 'theta': theta, 'closed_nu': closed,
                'untouched_sha256': r.exact.digest(r.encode(B)),
                'solve_sha256': r.exact.digest(r.encode(Y)), 'standard_frame_norms': [2, 2*(q-2), 2, 4, 4, 2]}


def separated(q, k, kappa):
    require(type(q) is int and type(k) is int and q >= 4 and 1 <= k <= q and
            type(kappa) in (int,F) and 0 <= kappa <= F(1, 8),
            'credited exact lower-coefficient domain')
    tau, trivial_record = trivial(q, kappa)
    nu, standard_record = standard(q, kappa)
    a = F(q*k)*nu*tau/((q-k)*tau+k*nu)
    require(a > 0 and 1/a == F(q-k, q*k)/nu+1/(q*tau), 'exact reciprocal deletion-count formula')
    return a, {'q': q, 'k': k, 'kappa': kappa, 'a': a, 'tau': tau, 'nu': nu,
               'trivial': trivial_record, 'standard': standard_record}


def direct(q, k, kappa):
    """Whole actual counted lower block, independent of separated formula."""
    D = r.forms(q, k)
    C, _ = r.evaluate(D, kappa, F(0), F(0))
    T = [D['keys'].index(key) for key in r.T_KEYS]
    keep = [i for i in range(len(D['keys'])) if i != T[0]]
    if kappa == 0:
        gauge = next(i for i, key in enumerate(D['keys']) if key[0] == 0 and key[1]+key[2] == 1)
        keep.remove(gauge)
    support = [keep.index(i) for i in T[1:]]
    G = r.submatrix(C, keep)
    S, B, Y = r.schur(G, support, [i for i in range(len(keep)) if i not in support])
    V = [[F(x) for x in row] for row in [[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]]]
    parts = r.congruence(S, V)
    a, b = parts[0][0], parts[2][2]
    require(parts == [[a,a,0,0],[a,a,0,0],[0,0,b,-b],[0,0,-b,b]] and
            b == r.odd_coefficient(q) and a > 0, 'ALL direct whole lower parity positions')
    return a
