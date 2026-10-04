"""Generic original-coordinate checks copied from published lemma9766.

The exact excerpt provenance is in PROVENANCE.json. Their copied
symbolic helper is also credited. No parent verifier is imported.
"""
from forms import *
import symbolic

KAPPA = F(1, 4096)

def indicator(D, masks):
    return [F(z+w == 0 and c in masks) for c, z, w in D['keys']]



def lower_dual(D):
    q, m = D['q'], len(D['keys'])
    v, s = vectors(D), D['s']
    u2 = [F(int(bool(c & 2))+int(bool(c & 4))-2*int(c.bit_count() >= 2)) for c, z, w in D['keys']]
    require(not any(action(D['C0'], u2)) and not any(action(D['Delta'], u2)), 'entire even old-kernel actions')
    h, g = v['h'], indicator(D, (3, 5))
    ds = [[u2[i]-h[i]+g[i] for i in range(m)],
          [indicator(D, (1,))[i]+g[i] for i in range(m)],
          indicator(D, (6,)), indicator(D, (7,)), v['y']]
    G = [[pair(D['C0'], a, b) for b in ds] for a in ds]
    cross = [pair(D['C0'], a, h) for a in ds]
    reduced = [[G[i+1][j+1]-G[i+1][0]*G[0][j+1]/G[0][0] for j in range(4)] for i in range(4)]
    cb = [cross[i+1]-G[i+1][0]*cross[0]/G[0][0] for i in range(4)]
    require(G[0][0] == 4*(s-2) and cross[0] == -2*(s-2), 'entire first elimination entries')
    require(reduced == [[F(symbolic.at(p, q)) for p in row] for row in symbolic.M] and
            cb == [F(symbolic.at(p, q)) for p in symbolic.B], 'all original reduced physical entries')
    den = symbolic.at(symbolic.D, q)
    theta = [F(symbolic.at(p, q), den) for p in [symbolic.FIRST]+symbolic.THETA]
    w = [h[i]+sum(t*d[i] for t, d in zip(theta, ds)) for i in range(m)]
    c = F(symbolic.at(symbolic.COST, q), den)
    pairs = {name: pair(D[name], w) for name in ('C0', 'Delta', 'Rb', 'Rc', 'B')}
    require(pairs == {'C0': 2*c, 'Delta': F(0), 'Rb': F(0), 'Rc': F(0), 'B': F(2)},
            'every closed original lower dual pairing')
    return w, c, pairs



def orientation(D):
    q, k = D['q'], D['k']
    v = vectors(D)
    alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
    require(not any(action(D['C0'], v['z'])) and all(not any(action(D[name], v['z']))
             for name in ('Rb', 'Rc', 'B')), 'whole surviving orientation coefficient actions')
    require(pair(D['Delta'], v['z']) == alpha > 0, 'positive orientation for all real kappa')
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    d = alpha-F(2*k, 3*q+5)
    require(pair(D['U0'], v['one']) == e and pair(D['Delta'], v['one']) == d > 0,
            'whole cap-one original scalar identities')
    require(pair(D['C0'], v['h']) == 2*(D['s']-2) and
            pair(D['C0'], v['h'], v['v']) == -2 and
            pair(D['C0'], v['v']) == q*q+6 and pair(D['Delta'], v['v']) == q,
            'whole all-singleton lower compression')
    require(pair(D['Delta'], v['h']) == pair(D['Delta'], v['h'], v['v']) == 0 and
            pair(D['B'], v['h']) == 2 and
            all(pair(D[name], v['h']) == pair(D[name], v['h'], v['v']) ==
                pair(D[name], v['v']) == 0 for name in ('Rb', 'Rc')) and
            pair(D['B'], v['h'], v['v']) == pair(D['B'], v['v']) == 0,
            'every lower compression repair coefficient')
    require(sum(D['sizes'][i]*v['p'][i] for i in range(len(v['p']))) == 0 and
            sum(D['sizes'][i]*v['p'][i]*v['z'][i] for i in range(len(v['p']))) == 0 and
            all(v['z'][D['keys'].index(key)] == 0 for key in ((2, 0, 0), (4, 0, 0), (6, 0, 0))) and
            pair(D['Rb'], v['one']) == pair(D['Rc'], v['one']) == 0 and
            pair(D['B'], v['one']) == 2 and d > F(4*q, (q*q+6)**2),
            'balanced correction isotropy and reciprocal monotonicity')
    return {'alpha': alpha, 'cap_one_base': e, 'cap_one_derivative': d,
            'mean_necessary_polynomial': 2*(e+2*D['s']-4)}



def literal_checks(D, lower=None, cap=None, parameters=None):
    q, k, m = D['q'], D['k'], len(D['keys'])
    X, tab = domain(q, k), table(q)
    require(all(literal.member(q, k, A & ~(1 << i)) for A in X for i in range(q+3) if A & (1 << i)),
            'every immediate original downset deletion')
    ix = {key: i for i, key in enumerate(D['keys'])}
    raw_groups = {}
    for A in X[1:]:
        raw_groups.setdefault(orbit(A, k), []).append(A)
    require(sorted(raw_groups) == D['keys'] and [len(raw_groups[key]) for key in D['keys']] == D['sizes'],
            'complete independent original physical orbit census')
    grams = {name: [[F(0)]*m for _ in range(m)] for name in NAMES}
    lp = {'C0': F(0), 'Delta': F(0), 'Rb': F(0), 'Rc': F(0), 'B': F(0)} if lower is not None else None
    cp = {'U0': F(0), 'Delta': F(0), 'Rb': F(0), 'Rc': F(0), 'B': F(0)} if cap is not None else None
    C = [] if parameters is not None else None
    for A in X[1:]:
        i = ix[orbit(A, k)]
        row = []
        for B in X[1:]:
            j = ix[orbit(B, k)]
            values = list(entry(q, D['s'], tab, A, B))
            values[-1] += D['N']*int(A == B)-1
            for name, value in zip(NAMES, values):
                grams[name][i][j] += value
            if lower is not None:
                energy = lower[i]*lower[j]
                for name, value in zip(NAMES[:5], values[:5]):
                    lp[name] += energy*value
            if cap is not None:
                energy = cap[i]*cap[j]
                for name, value in zip(NAMES, values):
                    if name in cp:
                        cp[name] += energy*value
            if parameters is not None:
                kk, t, sigma = parameters
                row.append(values[0]+kk*values[1]+t*(values[2]+values[3])+sigma*values[4])
        if C is not None:
            C.append(row)
    require(all(grams[name] == D[name] for name in NAMES), 'ALL six original weighted forms equal entire original pair sums')
    if lp is not None:
        require(lp == {name: pair(D[name], lower) for name in lp}, 'entire separately decoded original lower vector energies')
    if cp is not None:
        require(cp == {name: pair(D[name], cap) for name in cp}, 'entire separately decoded original cap vector energies')
    return X, C, {'positions': (len(X)-1)**2, 'weighted_entries': 6*m*m,
                  'forms_sha256': exact.digest(encode(grams)), 'literal_lower_pairings': lp, 'literal_cap_pairings': cp}



def psd_record(A, rank):
    first = schur_psd(A)
    second, characteristic, denominator = polynomial_psd(A)
    require(first == second == rank, 'both exact PSD algorithms and full rank')
    return {'rank': first, 'matrix_sha256': exact.digest(encode(A)),
            'characteristic_sha256': characteristic, 'integer_scaling_denominator': denominator}



def check_lift(D, X, C, L, M, t, sigma):
    N, s, q, k = (D[name] for name in ('N', 's', 'q', 'k'))
    require(len(L) == len(M) == len(X) == N and X[0] == 0, 'actual empty vertex')
    require(all(L[i][j] == L[j][i] and M[i][j] == M[j][i] for i in range(N) for j in range(N)), 'all original symmetry positions')
    require(all(sum(row) == N for row in L) and all(sum(row) == 1 for row in M), 'every original row equation')
    require(all(M[i][j] == 0 for i, A in enumerate(X) for j, B in enumerate(X) if A & B), 'every original intersecting zero')
    star = [F(bool(A & 1)) for A in X[1:]]
    centered = [F(bool(A & 1))-F(s, N) for A in X]
    require(sum(star) == s and not any(action(C, star)) and not any(action(L, centered)), 'entire original star and centered-star actions')
    h = F(1, 3*q+5)
    alpha = F(q*(q+1), 2)+3*(q+1)*h
    require(L[0][0] == 1+k*(s-k)+KAPPA*(alpha-2*k*h)+2*sigma, 'independent actual-empty diagonal formula')
    tab = table(q)
    for j, A in enumerate(X[1:], 1):
        core = (A & 7).bit_count()
        r = F(1) if core == 0 else h if core < 3 else -3*(q+1)*h
        intersects = k if A & 6 else ((A >> 3) & ((1 << k)-1)).bit_count()
        if intersects == k:
            deleted = -k
        else:
            aa, bb = tab[tuple(sorted((typ(A), (2, 1))))]
            deleted = -intersects+(k-intersects)*(aa-1+KAPPA*bb)
        repair = sum(F(edges.get(tuple(sorted((A, B))), 0)) for edges in (RB, RC) for B in range(1, 8))
        expected = 1-(KAPPA*r-deleted+t*repair+sigma*int(A in (2, 4)))
        require(L[0][j] == expected, 'every separate original actual-empty off-diagonal')
