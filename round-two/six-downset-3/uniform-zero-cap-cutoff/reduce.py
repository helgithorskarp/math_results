"""Exact uniform untouched floors and small coupled forms.

Ordinary whole-domain bridges are in LOWER-REDUCTION.md. Finite controls
validate the implementation, not unbounded positivity or completeness.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import sys

PARENT = Path(__file__).resolve().parent/'ancestral/core-edge-six-cutoff'
# The complete published tree is checked against the pinned committed manifest.
MANIFEST_SHA256 = '8a2e2a2970883fbc8474d24729fd63efd7173edd803840c7e6bad59ee5ecf3b5'
if hashlib.sha256((PARENT/'SHA256SUMS').read_bytes()).hexdigest() != MANIFEST_SHA256:
    raise ValueError('Changed credited manifest from commit d2d8a094e389a51668026b7646d046c50c91eff0')
for line in (PARENT/'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ', 1)
    if hashlib.sha256((PARENT/name).read_bytes()).hexdigest() != digest:
        raise ValueError('Changed whole credited source: '+name)
sys.path.insert(0, str(PARENT))
from forms import *
import polycap as poly

T_KEYS = [(1, 0, 0), (2, 0, 0), (4, 0, 0), (3, 0, 0), (5, 0, 0)]
ANCHOR = [[F(x) for x in row] for row in
          [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1]]]


def transpose(A):
    return [list(row) for row in zip(*A)]


def multiply(A, B):
    return [[sum(x*y for x, y in zip(row, col)) for col in transpose(B)] for row in A]


def subtract(A, B):
    require(len(A) == len(B) and all(len(a) == len(b) for a, b in zip(A, B)), 'matrix dimensions')
    return [[x-y for x, y in zip(a, b)] for a, b in zip(A, B)]


def submatrix(A, rows, cols=None):
    return [[A[i][j] for j in (rows if cols is None else cols)] for i in rows]


def solve(A, B):
    """Exact Gauss solve, checking every original equation afterward."""
    n, r = len(A), len(B[0])
    require(len(B) == n and all(len(row) == n for row in A), 'full solve dimensions')
    work = [list(a)+list(b) for a, b in zip(A, B)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        require(pivot is not None, 'singular solve: range bridge not justified')
        work[j], work[pivot] = work[pivot], work[j]
        p = work[j][j]
        work[j] = [x/p for x in work[j]]
        for i in range(n):
            if i != j:
                factor = work[i][j]
                work[i] = [x-factor*y for x, y in zip(work[i], work[j])]
    result = [row[n:] for row in work]
    require(multiply(A, result) == B, 'EVERY original rational solve equation')
    return result


def congruence(A, V):
    return multiply(transpose(V), multiply(A, V))


def schur(A, support, untouched):
    B = submatrix(A, untouched)
    X = submatrix(A, untouched, support)
    Y = solve(B, X)
    S = subtract(submatrix(A, support), multiply(transpose(X), Y))
    n = len(A)
    V = [[F(0)]*n for _ in range(n)]
    for j, i in enumerate(untouched):
        V[i][j] = F(1)
    for j, i in enumerate(support):
        V[i][len(untouched)+j] = F(1)
        for r, ii in enumerate(untouched):
            V[ii][len(untouched)+j] = -Y[r][j]
    transformed = congruence(A, V)
    expected = [[F(0)]*n for _ in range(n)]
    for i in range(len(untouched)):
        for j in range(len(untouched)):
            expected[i][j] = B[i][j]
    for i in range(len(support)):
        for j in range(len(support)):
            expected[len(untouched)+i][len(untouched)+j] = S[i][j]
    require(transformed == expected, 'ALL Schur congruence positions, including cross zeros')
    return S, B, Y


def cap_energy(q, k, kappa):
    s = 3*q+4
    h = F(1, 3*q+5)
    alpha = F(q*(q+1), 2)+3*(q+1)*h
    energy = F(3*k*q+15*q-k*k+3)+F(4*k, q)
    slope = alpha-2*(k+5)*h
    return energy+kappa*slope


def cap_margin(q, k):
    N, s = parameters(q, k)
    return 6*(N-2*s)-cap_energy(q, k, F(1, 8))


def odd_coefficient(q):
    """Closed original b/c-odd shorted energy, independent of k and kappa."""
    return F(2*(3*q+4)*(3*q*q+3*q-2), 6*q*q+5*q-2)


def automatic_odd_cap_floor(q, k):
    N, s = parameters(q, k)
    return 2*(N-2*s)-F(7, 3)*odd_coefficient(q)


def odd_full_gram(q):
    """Original signed b-c, ab-ac, sum(bx-cx), sum(abx-acx) Gram."""
    s, rr = 3*q+4, F(3*q+2, q)
    return [[2*F(x) for x in row] for row in
            [[s, -2, 0, -q*rr], [-2, s, -q*rr, 0],
             [0, -q*rr, q*s, -q*(s-rr)],
             [-q*rr, 0, -q*(s-rr), q*s]]]


def lower_cone(a, b, t, sigma, strict=True):
    require(a > 0 and b > 0, 'positive shorted lower coefficients')
    left, right = 2*t*t/a-2*t, 2*t-2*t*t/b
    return left < sigma < right if strict else left <= sigma <= right


def margin_polynomial(q=poly.Q, k=poly.K):
    q2, k2 = poly.mul(q, q), poly.mul(k, k)
    bracket = poly.add(poly.scale(q2, 47),
                       poly.scale(poly.mul(poly.add(poly.scale(k, 48), poly.constant(193)), q), -1),
                       poly.scale(k2, 16), poly.scale(k, -96), poly.constant(-48))
    first = poly.mul(poly.mul(q, poly.add(poly.scale(q, 3), poly.constant(5))), bracket)
    return poly.add(first,
                    poly.scale(poly.mul(k, poly.add(poly.scale(q, 3), poly.constant(5))), -64),
                    poly.scale(poly.mul(q, poly.add(poly.scale(q, 3), poly.scale(k, -2), poly.constant(-7))), -2))


def cleared_resolvent_margin(q=poly.Q, k=poly.K):
    """Independent full clearing of 6g-E0-(alpha-2(k+5)h)/8."""
    q2, k2 = poly.mul(q, q), poly.mul(k, k)
    factor = poly.add(poly.scale(q, 3), poly.constant(5))
    integer_part = poly.add(poly.scale(q2, 3),
                            poly.scale(poly.mul(poly.add(poly.scale(k, 3), poly.constant(12)), q), -1),
                            k2, poly.scale(k, -6), poly.constant(-3))
    return poly.add(poly.scale(poly.mul(poly.mul(q, factor), integer_part), 16),
                    poly.scale(poly.mul(k, factor), -64),
                    poly.scale(poly.mul(poly.mul(q2, poly.add(q, poly.constant(1))), factor), -1),
                    poly.scale(poly.mul(q, poly.add(poly.scale(q, 3), poly.scale(k, -2), poly.constant(-7))), -2))


def uniform():
    H = multiply(transpose(ANCHOR), ANCHOR)
    HI = solve(H, [[F(i == j) for j in range(4)] for i in range(4)])
    trace_inverse = sum(HI[i][i] for i in range(4))
    require(schur_psd(H) == 4 and trace_inverse > 0, 'fixed whole kernel anchor positive/injective')
    ordinary = margin_polynomial()
    require(ordinary == cleared_resolvent_margin(),
            'EVERY polynomial coefficient in independent full resolvent-margin clearing')
    shifted = margin_polynomial(poly.add(poly.constant(9), poly.scale(poly.K, 3), poly.Q),
                                poly.add(poly.constant(3), poly.K))
    require(shifted.get((0, 0), F(0)) > 0 and all(v > 0 for v in shifted.values()),
            'ALL cap-margin shifted coefficients positive for k>=3,q>=3k')
    controls = []
    for q, k in [(9, 3), (12, 4), (21, 6), (21, 7), (24, 8), (60, 20), (150, 50)]:
        D = forms(q, k)
        w = [F(key not in T_KEYS) for key in D['keys']]
        for kap in [F(0), F(1, 4096), F(1, 8)]:
            require(pair(D['C0'], w)+kap*pair(D['Delta'], w) == cap_energy(q, k, kap),
                    'complete original counted untouched-constant energy')
        p = poly.evaluate(ordinary, q, k)
        require(p == 16*q*(3*q+5)*cap_margin(q, k) > 0, 'cleared entire cap-margin identity')
        controls.append({'q': q, 'k': k, 'margin': cap_margin(q, k),
                         'cap_floor': cap_margin(q, k)/D['N'],
                         'lower_floor_at_kappa1_4096': F(1, 4096)/(2*(1+4*D['s']*trace_inverse))})
    return {'all_domain': 'ALL integersk>=3,q>=3k; real0<kappa<=1/8',
            'anchor': ANCHOR, 'anchor_gram': H, 'anchor_inverse': HI,
            'trace_anchor_inverse': trace_inverse,
            'lower_floor_formula': 'kappa/[2(1+4s*trace(H_T^-1))]',
            'cap_floor_formula': '[6(N-2s)-E_O(q,k,1/8)]/N',
            'cap_margin_polynomial': [[list(power), value] for power, value in sorted(ordinary.items())],
            'entire_cleared_resolvent_identity_verified': True,
            'shifted_cap_margin_coefficients': [[list(power), value] for power, value in sorted(shifted.items())],
            'shifted_coefficient_count': len(shifted),
            'controls_not_unbounded_proof': controls,
            'ordinary_resolvent_kernel_compression_bridges_unformalized': True,
            'base_spectral_premises_credited8757_9145_9195': True}


def reduced(q, k, kappa, tb=F(0), tc=F(0), sigma=F(0)):
    require(k >= 3 and q >= 3*k and 0 < kappa <= F(1, 8), 'proved coupled reduction domain')
    D = forms(q, k)
    C, U = evaluate(D, kappa, tb, sigma, tc)
    T = [D['keys'].index(key) for key in T_KEYS]
    O = [i for i in range(len(D['keys'])) if i not in T]
    require(len(D['keys']) == 23 and len(O) == 18, 'whole fixed-space dimensions')
    a = vectors(D)['star']
    require(not any(action(C, a)) and a[T[0]] == 1 and D['sizes'][T[0]] == 1,
            'forced-star exact anchor coordinate')
    keep = [i for i in range(23) if i != T[0]]
    reduced_C = submatrix(C, keep)
    lower_support = [keep.index(i) for i in T[1:]]
    lower_O = [keep.index(i) for i in O]
    SL, BL, YL = schur(reduced_C, lower_support, lower_O)
    SU, BU, YU = schur(U, T, O)
    require(schur_psd(BL) == schur_psd(BU) == 18, 'both actual untouched blocks strictly positive')
    weights = [D['sizes'][i] for i in O]
    WT = [[F(weights[i]*int(i == j)) for j in range(18)] for i in range(18)]
    H = multiply(transpose(ANCHOR), ANCHOR)
    HI = solve(H, [[F(i == j) for j in range(4)] for i in range(4)])
    etaL = kappa/(2*(1+4*D['s']*sum(HI[i][i] for i in range(4))))
    etaU = cap_margin(q, k)/D['N']
    require(schur_psd([[BL[i][j]-etaL*WT[i][j] for j in range(18)] for i in range(18)]) == 18 and
            schur_psd([[BU[i][j]-etaU*WT[i][j] for j in range(18)] for i in range(18)]) == 18,
            'both complete actual physical untouched-floor inequalities')
    return D, SL, SU, {'lower_schur': SL, 'cap_schur': SU,
                       'untouched_lower_sha256': exact.digest(encode(BL)),
                       'untouched_cap_sha256': exact.digest(encode(BU)),
                       'lower_solve_sha256': exact.digest(encode(YL)),
                       'cap_solve_sha256': exact.digest(encode(YU)),
                       'lower_floor': etaL, 'cap_floor': etaU,
                       'all_congruence_and_solve_positions_verified': True}


def parity(SL, SU):
    VL = [[F(x) for x in row] for row in [[1, 0, 1, 0], [1, 0, -1, 0],
                                        [0, 1, 0, 1], [0, 1, 0, -1]]]
    VU = [[F(x) for x in row] for row in [[1, 0, 0, 0, 0], [0, 1, 0, 1, 0],
                                        [0, 1, 0, -1, 0], [0, 0, 1, 0, 1],
                                        [0, 0, 1, 0, -1]]]
    lower, cap = congruence(SL, VL), congruence(SU, VU)
    require(all(lower[i][j] == 0 for i in range(2) for j in range(2, 4)) and
            all(cap[i][j] == 0 for i in range(3) for j in range(3, 5)),
            'ALL b/c parity cross energies zero')
    return {'lower_even': submatrix(lower, [0, 1]), 'lower_odd': submatrix(lower, [2, 3]),
            'cap_even': submatrix(cap, [0, 1, 2]), 'cap_odd': submatrix(cap, [3, 4])}
