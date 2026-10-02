"""Sharp core-edge cutoff k5, literal duals and full positive certificates.

Standard library only, with both credited executable inputs byte-pinned
before import. Infinite bridges are ordinary proofs in PROOF.md, not
extrapolations from fixtures. Two algorithms do not constitute peer review.
"""
from forms import *
import symbolic
import argparse
import json
import time

KAPPA = F(1, 4096)
LOWER_FLOOR, CAP_FLOOR = F(1, 65536), F(1, 4096)


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


def cap_dual(D):
    v = vectors(D)
    basis = (v['one'], v['y'], v['trade_iso'])
    moment = [[pair(D['U0'], a, b) for b in basis] for a in basis]
    e, A, B0 = moment[0]
    T, B, V = moment[1][1], moment[1][2], moment[2][2]
    determinant = T*V-B*B
    require(T > 0 and determinant > 0, 'complete cap residual homogeneous block positive')
    aa, bb = (V*A-B*B0)/determinant, (T*B0-B*A)/determinant
    w = [basis[0][i]-aa*basis[1][i]-bb*basis[2][i] for i in range(len(D['keys']))]
    pairs = {name: pair(D[name], w) for name in ('U0', 'Delta', 'Rb', 'Rc', 'B')}
    require(pairs['U0'] == e-aa*A-bb*B0 and pairs['Rb'] == pairs['Rc'] == 0 and
            pairs['B'] == 2*(1-bb)**2, 'every original cap residual pairing')
    return w, [aa, bb], pairs, moment


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


def positive(q, trade, sigma):
    D = forms(q, 5)
    G, H = evaluate(D, KAPPA, F(trade), F(sigma))
    m, s, N = len(D['keys']), D['s'], D['N']
    a = vectors(D)['star']
    sizes, weighted = D['sizes'], [x*y for x, y in zip(D['sizes'], a)]
    W = [[F(sizes[i]*int(i == j)) for j in range(m)] for i in range(m)]
    P = [[W[i][j]-F(weighted[i]*weighted[j], s) for j in range(m)] for i in range(m)]
    require(sum(weighted) == s and not any(action(G, a)), 'entire weighted forced-star metric')
    checks = {name: psd_record(matrix, rank) for name, matrix, rank in (
        ('lower', G, m-1), ('cap', H, m),
        ('lower_floor', [[G[i][j]-LOWER_FLOOR*P[i][j] for j in range(m)] for i in range(m)], m-1),
        ('cap_floor', [[H[i][j]-CAP_FLOOR*W[i][j] for j in range(m)] for i in range(m)], m))}
    X, C, literal_record = literal_checks(D, parameters=(KAPPA, F(trade), F(sigma)))
    L = exact.lift(C)
    M = [[(L[i][j]-s*int(i == j))/F(N-s) for j in range(N)] for i in range(N)]
    check_lift(D, X, C, L, M, F(trade), F(sigma))
    stars = [sum(bool(A & (1 << i)) for A in X) for i in range(q+3)]
    require(stars == [s, s-5, s-5]+[q+5]*5+[q+6]*(q-5), 'all original labelled star sizes')
    U = [[F(N*int(i == j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    rows = [sum(row) for row in U]
    EUET = [[sum(rows)]+[-x for x in rows]]+[
        [-rows[i]]+U[i] for i in range(N-1)]
    require(all(F(N*int(i == j))-L[i][j] == EUET[i][j] for i in range(N) for j in range(N)), 'ALL original physical cap-lift positions')
    require(0 < KAPPA <= F(1, 8) and N-2*s > 0 and LOWER_FLOOR <= KAPPA/2 and CAP_FLOOR <= N-2*s,
            'credited complete nonfixed lower and cap margins apply')
    return D, G, H, X, C, L, M, {'q': q, 'k': 5, 'N': N, 's': s,
        'parameters': {'kappa': KAPPA, 't_b': F(trade), 't_c': F(trade), 'sigma': F(sigma)},
        'fixed_checks': checks, 'literal': literal_record, 'stars': stars,
        'whole_positions': N*N, 'complement_dimension': N-1-m,
        'complete_nonfixed_lower_floor': KAPPA/2, 'complete_nonfixed_cap_floor': N-2*s,
        'nonempty_lower_floor': LOWER_FLOOR, 'nonempty_cap_floor': CAP_FLOOR,
        'whole_endpoint_ranks': [N-1, N-1], 'lambda': -F(s, N-s),
        'whole_projected_unit_gap': CAP_FLOOR/(N-s)}


def reject(call, label):
    try:
        call()
    except ValueError:
        return label
    raise ValueError('Semantic damage accepted: '+label)


def run():
    symbolic_record = symbolic.check()
    negative = []
    for q in range(5, 16):
        D = forms(q, 5)
        ori = orientation(D)
        low, c, lp = lower_dual(D)
        cap, coefficients, cp, moment = cap_dual(D)
        require(cp['Delta'] > 0 and cp['B'] > 0 and cp['U0']+c*cp['B'] < 0,
                'all-real original core-only face contradiction')
        _, _, original = literal_checks(D, low, cap)
        negative.append({'q': q, 'k': 5, 'orbit_count': len(D['keys']), 'N': D['N'],
                         'orientation': ori, 'lower_cost': c, 'lower_pairings': lp,
                         'cap_coefficients': coefficients, 'cap_pairings': cp,
                         'combined_margin': cp['U0']+c*cp['B'], 'literal': original})
    positives = [positive(16, 12, -12), positive(17, 4, -6)]
    validations = []
    for q, k in ((4, 0), (5, 5), (6, 5), (7, 5), (18, 5), (30, 0), (30, 29), (30, 30)):
        D = forms(q, k)
        _, c, pairs = lower_dual(D)
        validations.append({'q': q, 'k': k, 'orbit_count': len(D['keys']), 'closed_cost': c,
                            'all_lower_pairs': pairs, 'orientation': orientation(D)})
    base = forms(18, 5)
    _, _, cp, _ = cap_dual(base)
    require(cp['U0'] == F(-784601496, 1274780111), 'exact credited exceptional scalar reproduction')
    damage = []
    D, G, H, X, C, L, M, rec = positives[0]
    damage.append(reject(lambda: schur_psd([[H[i][j]-12*D['B'][i][j] for j in range(23)] for i in range(23)]), 'missing BC correction fails q16 cap'))
    D17 = positives[1][0]
    bad, _ = evaluate(D17, KAPPA, F(4), F(-8))
    damage.append(reject(lambda: schur_psd(bad), 'too negative BC fails q17 lower'))
    badL = [row[:] for row in L]; badL[0][0] += 1
    damage.append(reject(lambda: check_lift(D, X, C, badL, M, F(12), F(-12)), 'altered actual-empty diagonal rejected'))
    badL = [row[:] for row in L]; badL[0][1] += 1
    damage.append(reject(lambda: check_lift(D, X, C, badL, M, F(12), F(-12)), 'altered actual-empty off-diagonal rejected'))
    damage.append(reject(lambda: schur_psd([[G[i][j]-LOWER_FLOOR*D['sizes'][i]*int(i == j) for j in range(23)] for i in range(23)]), 'identity lower floor violates forced star'))
    low, _, _ = lower_dual(D)
    low = low[:]; low[D['keys'].index((1, 0, 0))] += F(1, 128)
    damage.append(reject(lambda: require(pair(D['Rb'], low) == 0, 'bad trade'), 'broken lower dual trade annihilation rejected'))
    den = symbolic.D[:]; symbolic.D[0] += 1
    try:
        damage.append(reject(symbolic.check, 'changed closed rational denominator rejected'))
    finally:
        symbolic.D[:] = den
    wrong = forms(16, 5); wrong['sizes'][0] += 1
    damage.append(reject(lambda: literal_checks(wrong), 'changed physical orbit weight rejected'))
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'exact author certificate plus ordinary infinite bridges, independently unreviewed and unformalized',
              'claim': 'For integer q>=5,k5 and every Z, rational greatest-rank capped H in the core-only face exists iff q>=16; all-real core-only face is empty at q5..15.',
              'negative_beyond_face': False, 'balanced_p_u_cutoff_classified': False,
              'closed_symbolic_certificate': symbolic_record, 'negative_cases': negative,
              'new_positive_cases': [x[-1] for x in positives], 'uniform_lower_controls': validations,
              'credited_q18_residual_scalar': cp['U0'],
              'positive_tail': 'q18 credited9735; every integer q>=19 credited9703. Neither tail is inferred from finite controls.',
              'semantic_damages_rejected': damage}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = encode(run())
    target = Path(__file__).with_name('RESULT.json')
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        require(json.loads(target.read_text()) == result, 'entire frozen exact mathematical payload')
    if args.record:
        args.record.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'record_sha256': exact.digest(result), 'negative_orders': len(result['negative_cases']),
                      'new_positive_orders': [x['q'] for x in result['new_positive_cases']],
                      'whole_projected_unit_gaps': [x['whole_projected_unit_gap'] for x in result['new_positive_cases']],
                      'semantic_damages': len(result['semantic_damages_rejected']), 'seconds': time.monotonic()-start}))
