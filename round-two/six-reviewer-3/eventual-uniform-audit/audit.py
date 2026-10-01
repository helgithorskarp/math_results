#!/usr/bin/env python3
"""Independent all-rank uniform H audit, six-reviewer-3.

No author Python imports. Solve the entire symmetric affine constraint system;
use exact sectors, integer Bareiss, literal matching lifts and three public
hash-pinned comparison receipts. The infinite proof is in REVIEW.md.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb, lcm
from pathlib import Path
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tr(a):
    return list(map(list, zip(*a)))


def psd(a):
    """Symmetric pivoted integer Bareiss after one denominator clearing."""
    if not a:
        return 0
    n = len(a)
    need(all(len(row) == n for row in a), 'square PSD input')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'PSD symmetry')
    den = lcm(*(F(x).denominator for row in a for x in row))
    a = [[int(F(x)*den) for x in row] for row in a]
    previous, rank = 1, 0
    while a:
        n = len(a)
        need(all(a[i][i] >= 0 for i in range(n)), 'negative PSD diagonal')
        k = max(range(n), key=lambda i: a[i][i])
        if not a[k][k]:
            need(all(x == 0 for row in a for x in row), 'illegal singular PSD residual')
            break
        ids = [i for i in range(n) if i != k]
        p = a[k][k]
        out = []
        for i in ids:
            row = []
            for j in ids:
                v = p*a[i][j]-a[i][k]*a[k][j]
                need(v % previous == 0, 'nonintegral Bareiss division')
                row.append(v//previous)
            out.append(row)
        a, previous, rank = out, p, rank+1
    return rank


def solve(a, b):
    """Full rational constraint solve, not the author's triangular formulas."""
    n = len(b)
    need(len(a) == n and all(len(row) == n for row in a), 'square affine system')
    a = [[F(x) for x in row]+[F(v)] for row, v in zip(a, b)]
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        need(pivot is not None, 'nonunique affine system')
        a[k], a[pivot] = a[pivot], a[k]
        d = a[k][k]
        a[k] = [x/d for x in a[k]]
        for i in range(k+1, n):
            d = a[i][k]
            if d:
                a[i] = [x-d*y for x, y in zip(a[i], a[k])]
    x = [F(0)]*n
    for i in reversed(range(n)):
        x[i] = a[i][-1]-sum(a[i][j]*x[j] for j in range(i+1, n))
    return x


def parameters(n, r):
    need(type(n) is int and type(r) is int and r >= 2 and n >= 2*r, 'affine domain')
    N = sum(comb(n, a) for a in range(r+1))
    s = sum(comb(n-1, a) for a in range(r))
    T = N-1-s
    unknowns = [(a, b) for a in range(1, r+1) for b in range(a, r+1) if b >= r-1]
    need(len(unknowns) == 2*r-1, 'variable count')
    a, rhs = [], []
    # All centering rows, and star rows except the last redundant one.
    for star in [False, True]:
        for layer in range(1, r+1-int(star)):
            row = []
            for i, j in unknowns:
                b = j if i == layer else i if j == layer else None
                row.append(0 if b is None else comb(n-layer-int(star), b-int(star)))
            a.append(row)
            rhs.append(s if star else T)
    weights = [[F(0)]*(r+1) for _ in range(r+1)]
    for (i, j), x in zip(unknowns, solve(a, rhs)):
        weights[i][j] = weights[j][i] = x
    for layer in range(1, r+1):
        need(sum(weights[layer][b]*comb(n-layer, b) for b in range(1, r+1)) == T, 'centering row')
        need(sum(weights[layer][b]*comb(n-layer-1, b-1) for b in range(1, r+1)) == s, 'star row')
    epsilon = F(n, 72*(N-1)*(n-1)*(n-2)*(n-3))
    return n, r, N, s, weights, epsilon


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def blocks(P, epsilon=F(0)):
    n, r, N, s, b, _ = P
    output = []
    for j in range(r+1):
        layers = list(range(max(1, j), r+1))
        metric = [comb(n-2*j, a-j) for a in layers]
        K = [[F(s*(a == c)-int(j == 0)*comb(n, c))
              + (-1)**j*(b[a][c]+epsilon*trade(n, a, c))*comb(n-a-j, c-j)
              for c in layers] for a in layers]
        U = [[N*(a == c)-int(j == 0)*comb(n, c)-K[i][k]
              for k, c in enumerate(layers)] for i, a in enumerate(layers)]
        output.append((j, layers, metric, K, U))
    return output


def weighted(K, metric):
    return [[g*x for x in row] for g, row in zip(metric, K)]


def quotient_maps(r):
    p = r-1
    q0 = [[F(int(a == b)+(a-r)*int(b == p)+(p-a)*int(b == r))
           for b in range(1, r+1)] for a in range(1, p)]
    q1 = [[F(int(a == b)-int(b == r)) for b in range(1, r+1)] for a in range(1, r)]
    return q0, q1


def quotients(P, centered):
    q0, q1 = quotient_maps(P[1])
    result = []
    for q, block in zip([q0, q1], centered[:2]):
        K = block[3]
        qk = mm(q, K)
        A = [row[:len(q)] for row in qk]
        need(mm(A, q) == qk, 'quotient intertwining')
        result.append(A)
    return result+[x[3] for x in centered[2:]]


def radius(A, s):
    return max((sum(abs(x-s*(i == j)) for j, x in enumerate(row))/s
                for i, row in enumerate(A)), default=F(0))


def schur(H, low, scale, metric):
    need(len(H)-low <= 2, 'small residual size')
    need(all(H[i][j] == scale*metric[i]*(i == j) for i in range(low) for j in range(low)), 'leading diagonal')
    return [[H[i][j]-sum(H[i][a]*H[a][j]/(scale*metric[a]) for a in range(low))
             for j in range(low, len(H))] for i in range(low, len(H))]


def sharper_bounds(P, radii):
    n, r, N, s, b, _ = P
    need(n >= 8*r*r, 'sharper theorem domain')
    p, B, T = r-1, comb(n, r-2), N-1-s
    Z = sum(comb(n, k) for k in range(r-1))
    weighted_tail = sum((p-a+1)*comb(n, a) for a in range(1, p))
    need(F(r, n-r+1) <= F(1, 15), 'backwards ratio')
    need(Z <= F(9, 8)*B and weighted_tail <= F(9, 4)*B, 'tail bounds')
    need(F(B, s) <= F(8*r, 7*n), 'improved low ratio')
    need(F(s, comb(n, r)) <= F(4*r, 3*n), 'improved top ratio')
    need(s <= F(8, 7)*comb(n, p) and comb(n, p) <= 2*s and T <= 2*comb(n, r), 'top tail bounds')
    for a in range(1, r+1):
        for k in [p, r]:
            need(comb(n-a, k) >= F(6, 7)*comb(n, k), 'displacement')
        need(F(s, comb(n-a, p)) <= F(4, 3), 'denominator')
    U = sum(comb(n-1, k) for k in range(1, r-1))
    D = p*s-(n-r)*U-n
    if r == 2:
        need(D == 0 and b[1][1] == 0 and b[1][2] == b[2][2] == F(n, n-2), 'rank-two boundary')
    else:
        V = sum(comb(n-1, k) for k in range(1, r-2))
        need(D == r*comb(n-1, r-2)-(n-2*r+1)*V+p-n, 'cancellation identity')
        need(F(comb(n-1, r-2), s) <= F(16*r, 15*n), 'near-top tail ratio')
        need(F(V, s) <= F(128*r*r, 105*n*n), 'second tail ratio')
        need(F(n, s) <= F(3, n), 'constant term ratio')
        need(abs(D) <= F(55*r*r, 21*n)*s, 'improved cancellation')
    Lp = sum(b[a][p]*comb(n-p, a) for a in range(1, p))
    Hp = sum(a*b[a][p]*comb(n-p, a) for a in range(1, p))
    X = r*(T-Lp)-((n-p)*s-Hp)
    need(X == D-r*Lp+Hp, 'top cancellation identity')
    need(abs(Lp) <= 3*B, 'Lp control')
    need(abs(r*Lp-Hp) <= 3*r*B, 'direct weighted cancellation')
    need(abs(X) <= F(127*r*r, 21*n)*s, 'top X control')
    for a in range(1, p):
        need(abs(b[a][p]) <= F(4, 3)*(p-a+1) and abs(b[a][r]) <= 3, 'low weights')
    need(abs(b[p][p]) <= F(508*r*r, 63*n), 'top diagonal weight')
    need(abs(b[p][r]) <= 3 and abs(b[r][r]) <= 3, 'top other weights')
    need(max(abs(x) for row in b for x in row) <= 2*r, 'all weights')
    constants = [F(51, 7), F(9, 2)]+[F(18, 7)]*(r-1)
    need(all(value <= c*F(r*r, n) for value, c in zip(radii, constants)), 'sharper quotient radii')
    need(max(radii) <= F(51, 56), 'uniform real spectral window')
    need(s >= n and F(s, 16) >= 2 and N-F(31*s, 16) >= 1, 'quantitative repair hypotheses')
    return {'D': D, 'B_over_s': str(F(B, s)), 's_over_top': str(F(s, comb(n, r))),
            'scalar_margin': s-sum(comb(n, a) for a in range(1, r-1))}


def sector_audit(P, strengthened):
    n, r, N, s, b, eps = P
    centered = blocks(P)
    qs = quotients(P, centered)
    radii = [radius(x, s) for x in qs]
    if strengthened:
        bounds = sharper_bounds(P, radii)
    else:
        bounds = None
    q0, _ = quotient_maps(r)
    if r > 2:
        w = [comb(n, a) for a in range(1, r-1)]
        small = [[F(s*w[i]*(i == j)-w[i]*w[j]) for j in range(len(w))] for i in range(len(w))]
        need(mm(mm(tr(q0), small), q0) == weighted(centered[0][3], centered[0][2]), 'zero congruence')
    original_lower, upper, repaired, residual_count = [], [], [], 0
    full_original, full_repaired, full_upper = 0, 0, 0
    for j, layers, metric, K, U in centered:
        H, HU = weighted(K, metric), weighted(U, metric)
        lower_rank, upper_rank = psd(H), psd(HU)
        need(lower_rank == len(layers)-2*int(j == 0)-int(j == 1), 'centered rank')
        need(upper_rank == len(layers), 'centered cap')
        low = sum(a <= r-2 for a in layers)
        upres = schur(HU, low, N-s, metric)
        need(psd(upres)+low == upper_rank, 'cap residual equivalence')
        residual_count += 1
        if j:
            lowres = schur(H, low, s, metric)
            need(psd(lowres)+low == lower_rank, 'core residual equivalence')
            residual_count += 1
        multiplicity = comb(n, j)-choose(n, j-1)
        full_original += multiplicity*lower_rank
        full_upper += multiplicity*upper_rank
        original_lower.append(lower_rank)
        upper.append(upper_rank)
    for j, layers, metric, K, U in blocks(P, eps):
        rank = psd(weighted(K, metric))
        need(rank == len(layers)-int(j <= 1), 'original repaired rank')
        need(psd(weighted(U, metric)) == len(layers), 'original repaired cap')
        repaired.append(rank)
        full_repaired += (comb(n, j)-choose(n, j-1))*rank
    need((full_original, full_repaired, full_upper) == (N-n-2, N-n-1, N-1), 'all harmonic multiplicities')
    improved = None
    if strengthened:
        endpoint = F(2, (n-2)*(n-3)*(2*n-1))
        ranks = []
        for j, layers, metric, K, U in blocks(P, endpoint):
            rank = psd(weighted(K, metric))
            need(rank == len(layers)-int(j <= 1), 'closed-endpoint repaired rank')
            need(psd(weighted(U, metric)) == len(layers), 'closed-endpoint strict cap')
            ranks.append(rank)
        improved = {'epsilon_endpoint': str(endpoint), 'coefficient_gain': str(endpoint/eps),
                    'repaired_sector_ranks': ranks}
    digest = sha256(json.dumps([[str(x) for x in row] for row in b], separators=(',', ':')).encode()).hexdigest()
    return {'n': n, 'r': r, 'N': N, 's': s, 'weights_sha256': digest,
            'centered_sector_ranks': original_lower, 'repaired_sector_ranks': repaired,
            'upper_sector_ranks': upper, 'lower_full_rank': full_repaired+1, 'upper_full_rank': full_upper,
            'quotient_row_radii': [str(x) for x in radii], 'residual_checks': residual_count,
            'epsilon': str(eps), 'sharper_bounds': bounds, 'closed_repair': improved}


def literal(P):
    n, r, N, s, beta, eps = P
    need(N <= 170, 'literal size guard')
    family = [sum(1 << i for i in a) for k in range(r+1) for a in combinations(range(n), k)]
    positive = family[1:]
    C = [[F(s*(a == b)-1)+(beta[a.bit_count()][b.bit_count()]+eps*trade(n, a.bit_count(), b.bit_count()))*int(not(a & b))
          for b in positive] for a in positive]
    rows = list(map(sum, C))
    L = [[1+sum(rows)]+[1-x for x in rows]]+[[1-rows[i]]+[1+x for x in row] for i, row in enumerate(C)]
    need(all(sum(row) == N for row in L), 'literal row sums')
    need(all(not(a & b) or L[i][j] == s*(i == j) for i, a in enumerate(family) for j, b in enumerate(family)), 'literal support')
    need(psd(L) == N-n, 'literal lower rank')
    need(psd([[N*(i == j)-L[i][j] for j in range(N)] for i in range(N)]) == N-1, 'literal upper rank')
    for point in range(n):
        v = [F(bool(a & (1 << point)))-F(s, N) for a in family]
        need(all(sum(x*y for x, y in zip(row, v)) == 0 for row in L), 'literal centered point star')
    # Independent matching-polynomial lifts on every original vertex.
    checks = 0
    for j in range(r+1):
        def h(a):
            value = 1
            for i in range(j):
                value *= int(bool(a & (1 << (2*i))))-int(bool(a & (1 << (2*i+1))))
            return value
        for a in range(max(1, j), r+1):
            av = [v for v in positive if v.bit_count() == a]
            need(sum(h(v)**2 for v in av) == 2**j*comb(n-2*j, a-j), 'literal lift norm')
            for b in range(max(1, j), r+1):
                bv = [v for v in positive if v.bit_count() == b]
                coefficient = (-1)**j*comb(n-a-j, b-j)
                for v in av:
                    need(sum(h(w) for w in bv if not(v & w)) == coefficient*h(v), 'literal disjoint action')
                    checks += 1
    return {'n': n, 'r': r, 'N': N, 'lower_rank': N-n, 'upper_rank': N-1,
            'literal_L_sha256': sha256(json.dumps([[str(x) for x in row] for row in L], separators=(',', ':')).encode()).hexdigest(),
            'matching_action_checks': checks}


def trade_audit(n, r):
    P = parameters(n, r)
    alpha = F((n-2)*(n-3)*(2*n-1), 2)
    negative = (n-1)*(n-3)
    for j, layers, metric, K, _ in blocks(P):
        D = [[F((-1)**j*trade(n, a, b)*comb(n-a-j, b-j)) for b in layers] for a in layers]
        if j <= 2:
            sign = -1 if j == 1 else 1
            need(psd(weighted([[sign*x for x in row] for row in D], metric)) == 1, 'trade sector sign/rank')
            value = alpha if j == 0 else -negative if j == 1 else F(1)
            need(sum(D[i][i] for i in range(len(D))) == value, 'trade nonzero eigenvalue')
        else:
            need(all(x == 0 for row in D for x in row), 'trade higher-degree zero')
    need(alpha-(n-1)*negative+comb(n, 2)-n == 0, 'trade multiplicity trace')
    return {'n': n, 'r': r, 'positive_degree0': str(alpha), 'negative_degree1': -negative,
            'positive_degree2': 1, 'closed_endpoint': str(1/alpha)}


def projected_gap(H, metric, kernels, gamma):
    """Use a full rational Gram solve for the counting-metric projection."""
    d, k = len(metric), len(kernels)
    if k:
        Gram = [[sum(metric[i]*u[i]*v[i] for i in range(d))
                 for v in kernels] for u in kernels]
        columns = [solve(Gram, [F(a == b) for a in range(k)]) for b in range(k)]
        inverse = tr(columns)
    else:
        inverse = []
    return [[H[i][j]-gamma*metric[i]*(i == j)
             + gamma*metric[i]*metric[j]*sum(kernels[a][i]*inverse[a][b]*kernels[b][j]
                                             for a in range(k) for b in range(k))
             for j in range(d)] for i in range(d)]


def linear_audit(P):
    n, r, N, s, beta, eps = P
    need(n >= 8*r, 'linear theorem domain')
    p, T = r-1, N-1-s
    D = (p-1)+2*sum((p-k)*comb(n-1, k) for k in range(1, p))
    need(D == r*T-(n-p)*s, 'positive telescoping cancellation')
    d, tau, kappa = F(D, s), F(T, s), F(comb(n, p), comb(n, r))
    low = list(range(1, p))
    R = {a: F(comb(n, a), comb(n, p)) for a in low}
    h = {a: max(1, r-a) for a in range(1, r+1)}
    f = {a: d-(p-a) for a in low}
    need(0 <= d <= F(7, 18) < F(2, 5), 'positive tail moment')
    need(all(R[a] <= F(1, 7)**(p-a) for a in low), 'linear tail ratio')
    sumR = sum(R.values())
    W = sum(h[a]*R[a] for a in low)
    F0 = sum(abs(f[a])*R[a] for a in low)
    F1 = sum(h[a]*abs(f[a])*R[a] for a in low)
    need(sumR <= F(1, 6) and W <= F(13, 36) < F(3, 8), 'first weighted tail')
    need(F0 <= F(47, 180) < F(1, 3) and F1 <= F(323, 540) < F(3, 5), 'absolute weighted tails')
    ell = sum(f[a]*R[a] for a in low)
    x = d-sum(h[a]*f[a]*R[a] for a in low)
    y = tau-ell-x
    z = kappa*y
    ellr = kappa*sum((tau-f[a])*R[a] for a in low)
    v = tau-ellr-z
    need(tau <= F(n, r) and kappa <= F(1, 7) and kappa*tau <= F(8, 7), 'linear top ratios')
    need(abs(ell) <= F(1, 3) and abs(x) <= 1 and abs(z) <= F(4, 3) and abs(ellr) <= F(1, 4), 'normalized corners')
    need(kappa*tau*W+kappa*F1 <= F(18, 35), 'reverse weighted tail')
    for a in low:
        for i, j, value in [(a, p, f[a]), (p, a, f[a]*R[a]),
                            (a, r, tau-f[a]), (r, a, kappa*(tau-f[a])*R[a])]:
            need(beta[i][j]*comb(n-i, j) == s*value, 'disjoint denominator cancellation')
    for a, b, value in [(p, p, x), (p, r, y), (r, p, z), (r, r, v)]:
        need(beta[a][b]*comb(n-a, b) == s*value, 'normalized corner identity')
    need(sum(comb(n, a) for a in low) <= F(4, 21)*s, 'degree-zero congruence gap')
    centered = blocks(P)
    Qs = quotients(P, centered)
    weighted_radii, gaps = [], []
    for j, layers, metric, K, U in centered:
        A = Qs[j]
        qlayers = list(range(1, p)) if j == 0 else list(range(1, r)) if j == 1 else layers
        rad = max((sum(abs(value-s*(i == k))*F(h[qlayers[k]], h[qlayers[i]])
                       for k, value in enumerate(row))/s for i, row in enumerate(A)), default=F(0))
        limit = F(39, 35) if j == 0 else F(181, 315) if j == 1 else F(1, 3)
        need(rad <= limit, 'linear scaled sector radius')
        weighted_radii.append(str(rad))
        gamma = (F(17, 21) if j == 0 else F(2, 5) if j == 1 else F(2, 3))*s
        kernels = [[1]*len(layers), layers] if j == 0 else [[1]*len(layers)] if j == 1 else []
        need(psd(projected_gap(weighted(K, metric), metric, kernels, gamma)) == len(layers)-len(kernels), 'projected linear spectral gap')
        need(psd([[F(74, 35)*s*metric[i]*(i == k)-metric[i]*value
                   for k, value in enumerate(row)] for i, row in enumerate(K)]) == len(layers), 'linear upper spectral bound')
        gaps.append(str(gamma))
        if j:
            for a in layers:
                for b in layers:
                    theta = F(comb(n-a-j, b-j), comb(n-a, b))
                    need(theta <= F(1, 6)**j and tau*theta <= F(8, 7)*F(1, 6)**(j-1), 'all falling-factorial bounds')
    need(N >= 8*s+1 and F(2*s, 5) >= 2, 'closed repair hypotheses in linear range')
    endpoint = F(2, (n-2)*(n-3)*(2*n-1))
    alpha = 1/endpoint
    delta = F(n*(n-1)*(n-2)*(n-3), 4)
    gap = F(3, 4)*(1-endpoint)
    need(F(delta, (N-1)*alpha) <= F(1, 16), 'repair eigenvector/constant angle')
    need(N-F(74*s, 35)-1 >= 1-endpoint > 0, 'upper gap away from constants')
    for j, layers, metric, K, U in blocks(P, endpoint):
        need(psd(weighted(K, metric)) == len(layers)-int(j <= 1), 'linear closed endpoint lower rank')
        need(psd(weighted(U, metric)) == len(layers), 'linear closed endpoint strict cap')
        need(psd(weighted([[value-gap*(i == k) for k, value in enumerate(row)]
                           for i, row in enumerate(U)], metric)) == len(layers), 'quantitative closed endpoint upper gap')
    record = sector_audit(P, False)
    record['linear_bounds'] = {'d': str(d), 'weighted_tail': str(W), 'F0': str(F0), 'F1': str(F1),
                               'x': str(x), 'y': str(y), 'z': str(z), 'v': str(v),
                               'weighted_radii': weighted_radii,
                               'verified_sector_lower_gaps': gaps, 'upper_core_bound': str(F(74*s, 35))}
    record['closed_repair'] = {'epsilon_endpoint': str(endpoint), 'coefficient_gain': str(endpoint/eps),
                               'uniform_upper_core_gap': str(gap)}
    return record


def compact(record):
    """Keep a compact reproducible receipt after all entrywise comparisons."""
    record = dict(record)
    radii = record.pop('quotient_row_radii', None)
    if radii is not None:
        record['quotient_row_radii_sha256'] = sha256(json.dumps(radii, separators=(',', ':')).encode()).hexdigest()
    if record.get('linear_bounds'):
        bounds = dict(record['linear_bounds'])
        radii = bounds.pop('weighted_radii')
        bounds['weighted_radii_sha256'] = sha256(json.dumps(radii, separators=(',', ':')).encode()).hexdigest()
        record['linear_bounds'] = bounds
    return record


def reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('malformed control accepted')


def run(author, baseline, linear_author):
    original, new, literal_rows = [], [], []
    for old in author['quantitative_cases']+author['smaller_examples']:
        P = parameters(old['n'], old['r'])
        row = sector_audit(P, old['n'] >= 8*old['r']**2)
        for key in ['N', 's', 'centered_sector_ranks', 'repaired_sector_ranks', 'upper_sector_ranks',
                    'lower_full_rank', 'upper_full_rank', 'quotient_row_radii', 'residual_checks', 'epsilon']:
            need(row[key] == old[key], 'original receipt '+key)
        original.append(row)
    for r in range(2, 17):
        for n in [8*r*r, 8*r*r+1]:
            new.append(sector_audit(parameters(n, r), True))
    for old in author['literal']:
        row = literal(parameters(old['n'], old['r']))
        for k in old:
            need(row[k] == old[k], 'original full matrix '+k)
        literal_rows.append(row)
    for rec in baseline['cases']:
        b = parameters(rec['n'], 5)[4]
        need({key: str(b[int(key[0])][int(key[1])]) for key in rec['beta']} == rec['beta'], 'rank-five input table')
    linear = []
    for old in linear_author['linear_cases']:
        row = linear_audit(parameters(old['n'], old['r']))
        for key in old:
            need(row[key] == old[key], 'linear original receipt '+key)
        linear.append(row)
    linear_literal = []
    for old in linear_author['literal']:
        row = literal(parameters(old['n'], old['r']))
        for key in old:
            need(row[key] == old[key], 'linear literal comparison '+key)
        linear_literal.append(row)
    trades = [trade_audit(n, r) for n, r in [(32, 2), (72, 3), (128, 4), (200, 5), (2048, 16)]]
    P = parameters(20, 10)
    low = sum(comb(20, a) for a in range(1, 9))
    need((P[3], low, low*(P[3]-low)) == (262144, 263949, -476427945), 'stable sparse obstruction')
    centered = blocks(P)
    q0, _ = quotient_maps(10)
    w = [comb(20, a) for a in range(1, 9)]
    small = [[F(P[3]*w[i]*(i == j)-w[i]*w[j]) for j in range(8)] for i in range(8)]
    need(mm(mm(tr(q0), small), q0) == weighted(centered[0][3], centered[0][2]), 'negative boundary congruence')
    reject(lambda: psd(weighted(centered[0][3], centered[0][2])))
    controls = [lambda: parameters(3, 2), lambda: parameters(32.0, 2), lambda: parameters(128, True),
                lambda: psd([[-1]]), lambda: psd([[0, 1], [1, 0]]), lambda: psd([[1, 0], [1, 1]]),
                lambda: solve([[1, 1], [1, 1]], [1, 2]),
                lambda: sharper_bounds(parameters(127, 4), [F(0)]*5)]
    for fn in controls:
        reject(fn)
    damaged = [row[:] for row in centered[1][3]]
    damaged[0][0] += 1
    need(any(sum(row) != 0 for row in damaged), 'kernel mutation detected')
    reject(lambda: need(all(sum(row) == 0 for row in damaged), 'damaged kernel'))
    reject(lambda: linear_audit(parameters(15, 2)))
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'original_receipt_cases': list(map(compact, original)),
            'quadratic_corroboration_cases': list(map(compact, new)), 'literal': literal_rows,
            'linear_receipt_cases': list(map(compact, linear)), 'linear_literal': linear_literal,
            'trade_checks': trades, 'rank_five_tables_matched': 3, 'rejected_controls': len(controls)+3,
            'negative_ansatz_witness': {'n': 20, 'r': 10, 'scalar': -1805, 'full_core_form': -476427945},
            'additional_linear_domain_rejection': True,
            'proof_status': 'Independent ordinary unformalized audit of 8660 and 8722; closed repair interval at n>=8r; quadratic corroboration is superseded; general H/I open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-results', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--linear-results', type=Path, required=True)
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    inputs = []
    for path, digest in [(args.author_results, '5635bf2e94f88b8d6f47e7ff1e1a61b6282ff31a1f07af02d73caf554f79cc88'),
                         (args.baseline, '3bd48141e92a017cb175666bd9783b8d66cd1648fa6e3832367d5f9640665428'),
                         (args.linear_results, 'c4c04361e2831a4ad1c00d36906c04051ae1ba330435aab7a4d7597cfb6a30e9')]:
        raw = path.read_bytes()
        need(sha256(raw).hexdigest() == digest, 'public comparison input SHA256')
        inputs.append(json.loads(raw))
    result = run(*inputs)
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.write:
        args.write.write_bytes(raw)
    if args.check:
        need(result == json.loads(args.check.read_bytes()), 'independent expected receipt')
    print(json.dumps({'ok': True, 'original_cases': len(result['original_receipt_cases']),
                      'quadratic_corroboration_cases': len(result['quadratic_corroboration_cases']),
                      'linear_cases': len(result['linear_receipt_cases']),
                      'literal_orders': [x['N'] for x in result['literal']],
                      'rejected_controls': result['rejected_controls'], 'expected_sha256': sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
