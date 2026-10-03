"""Exact controls for the uniform coupled-cone reduction.

Finite controls validate the decoder, metric, repairs, shorting, and
boundary interpretation. Infinite/complement/symmetry proofs are written.
"""
from pathlib import Path
import argparse
import json
from math import comb

import reduce as r
from reduce import F, require
import original_checks as credited
import symbolic as univariate


def psd(A, rank):
    require(r.schur_psd(A) == rank, 'exact Schur PSD/rank')
    rr, digest, scale = r.polynomial_psd(A)
    require(rr == rank, 'separate exact characteristic PSD/rank')
    return {'matrix_sha256': r.exact.digest(r.encode(A)), 'rank': rank,
            'characteristic_sha256': digest, 'scaling_denominator': scale}


def partitions(D):
    T = [D['keys'].index(key) for key in r.T_KEYS]
    O = [i for i in range(23) if i not in T]
    keep = [i for i in range(23) if i != T[0]]
    return T, O, keep


def kernel_congruence(D, C):
    T, O, keep = partitions(D)
    star = r.vectors(D)['star']
    V = [[star[i]]+[F(i == j) for j in keep] for i in range(23)]
    expected = [[F(0)]*23 for _ in range(23)]
    for ii, i in enumerate(keep, 1):
        for jj, j in enumerate(keep, 1):
            expected[ii][jj] = C[i][j]
    require(r.congruence(C, V) == expected, 'ALL forced-kernel congruence positions')
    return r.exact.digest(r.encode(expected))


def odd_frame(D):
    cols = [[], [], [], []]
    for c, z, w in D['keys']:
        cols[0].append(F((c == 2)-(c == 4)) if z+w == 0 else F(0))
        cols[1].append(F((c == 3)-(c == 5)) if z+w == 0 else F(0))
        cols[2].append(F((c == 2)-(c == 4)) if z+w == 1 else F(0))
        cols[3].append(F((c == 3)-(c == 5)) if z+w == 1 else F(0))
    require(all(not any(r.action(D['Delta'], v)) for v in cols), 'EVERY original odd derivative action zero')
    actual = [[r.pair(D['C0'], x, y) for y in cols] for x in cols]
    require(actual == r.odd_full_gram(D['q']), 'all original four-vector odd Gram positions')
    S, B, Y = r.schur(actual, [0, 1], [2, 3])
    b = r.odd_coefficient(D['q'])
    require(S == [[b, -b], [-b, b]], 'complete original closed odd shorting identity')
    return {'original_gram': actual, 'untouched': psd(B, 2), 'shorted_coefficient': b,
            'shorted': psd(S, 1), 'original_delta_actions_zero': True}


def uniform():
    result = r.uniform()
    s, rr = [4, 3], [2, 3]  # s and q*r0
    q = [0, 1]
    den = univariate.add(univariate.scale(univariate.mul(q, s), 2), univariate.scale(rr, -1))
    top = univariate.add(univariate.scale(univariate.mul(q, s), 2),
                         univariate.scale(univariate.mul([1, 1], rr), -1))
    num = univariate.scale(univariate.mul(s, top), 2)
    require(den == [-2, 5, 6] and
            num == univariate.scale(univariate.mul([4, 3], [-2, 3, 3]), 2),
            'entire closed odd coefficient numerator/denominator identities')
    difference = univariate.add(univariate.D,
                                univariate.scale(univariate.mul([2, 3], den), -1))
    require(difference == [-8, 8, 30, 18], 'entire old-2c versus odd-b identity')
    half_difference = univariate.add(univariate.D,
                                     univariate.scale(univariate.mul([2, 3], den), -2))
    require(half_difference == [-4, 4, 3], 'entire stronger old-2c versus half-b identity')
    shifted = [univariate.shift4(p) for p in (den, num, difference, half_difference)]
    require(all(v[0] > 0 and all(x >= 0 for x in v) for v in shifted),
            'ALL odd positivity and comparison coefficients on whole q>=4 half-line')
    result['odd_closed_identity'] = {'denominator': den, 'numerator': num,
                                   'comparison_difference': difference,
                                   'half_comparison_difference': half_difference,
                                   'whole_shifted_positive_coefficients': shifted}
    automatic = univariate.add(univariate.mul([0, 1, 3], den), univariate.scale(num, -7))
    require(automatic == [112, -86, -295, -105, 18], 'entire automatic odd-cap floor numerator identity')
    at9 = [sum(automatic[j]*comb(j, i)*9**(j-i) for j in range(i, len(automatic)))
           for i in range(len(automatic))]
    require(at9 == [16996, 21577, 5618, 543, 18] and all(x > 0 for x in at9),
            'ALL automatic odd-cap floor coefficients positive on whole q>=9')
    result['automatic_odd_cap'] = {'lower_feasible_repairs_only': True,
                                 'whole_floor_formula': '2(N-2s)-7b(q)/3',
                                 'uniform_minimum_cleared_numerator': automatic,
                                 'whole_positive_coefficients_at_q9_plus_u': at9,
                                 'proof_uses_a_le_2c_lt_b_over_2': True}
    result['credited_lower_dual_complete_identity'] = univariate.check()
    return result


def original(q, k):
    D, positions = r.original_forms(q, k)
    T, O, keep = partitions(D)
    require(all(not any(D[name][i][j] for i in O for j in range(23))
                for name in ('Rb', 'Rc', 'B')), 'EVERY repair untouched row/column zero')
    zero = r.submatrix(D['C0'], O)
    require(r.schur_psd(zero) == 17, 'actual zero-kappa untouched kernel rank')
    zeta = [F(1-int(bool(c & 1))-int(bool(c & 2))-int(bool(c & 4))+int(c.bit_count() >= 2))
            for c, z, w in D['keys']]
    require(not any(r.action(D['C0'], zeta)) and all(zeta[i] == 0 for i in T) and
            all(not any(r.action(D[name], zeta)) for name in ('Rb', 'Rc', 'B')),
            'complete actual extra zero-kappa kernel and repair actions')
    out = {'q': q, 'k': k, 'original_positions': positions,
           'all_six_literal_original_grams_sha256': r.exact.digest(r.encode({n: D[n] for n in r.NAMES})),
           'zero_kappa_untouched_rank': 17, 'odd': odd_frame(D)}
    C, U = r.evaluate(D, F(1, 4096), F(2), F(-4), F(3))
    out['unequal_trade_full_kernel_congruence_sha256'] = kernel_congruence(D, C)
    return out


def lower_shape(D, SL, SU):
    parts = r.parity(SL, SU)
    a, b = parts['lower_even'][0][0], parts['lower_odd'][0][0]
    require(parts['lower_even'] == [[a, a], [a, a]] and
            parts['lower_odd'] == [[b, -b], [-b, b]] and b == r.odd_coefficient(D['q']) and
            a > 0 and b > 0, 'ENTIRE bare lower rank-one parity forms and closed b')
    low, cost, pairs = credited.lower_dual(D)
    star = r.vectors(D)['star']
    T, O, keep = partitions(D)
    low = [x-low[T[0]]*v for x, v in zip(low, star)]
    require([low[i] for i in T] == [0, 1, 1, 0, 0], 'actual credited dual projected support')
    require(a <= 2*cost < b/2, 'exact shorted old-dual bound and uniform closed half-b comparison control')
    return a, b, cost, parts


def coupled(q, k):
    kap = F(1, 4096)
    D, SL, SU, rec = r.reduced(q, k, kap)
    a, b, cost, parts = lower_shape(D, SL, SU)
    T, O, keep = partitions(D)
    lower_support = [keep.index(i) for i in T[1:]]
    C, U = r.evaluate(D, kap, F(0), F(0), F(0))
    out = {'q': q, 'k': k, 'kappa': kap, 'reduction': rec,
           'a': a, 'b': b, 'old_c': cost,
           'bare_lower_congruence': kernel_congruence(D, C),
           'bare_lower_physical': psd(C, 20),
           'bare_lower_even': psd(parts['lower_even'], 1),
           'bare_lower_odd': psd(parts['lower_odd'], 1)}
    # Both independent trades enter with their actual original coefficients.
    tb, tc, sigma = F(2), F(3), F(-4)
    CC, UU = r.evaluate(D, kap, tb, sigma, tc)
    mixedL, _, _ = r.schur(r.submatrix(CC, keep), lower_support, [keep.index(i) for i in O])
    mixedU, _, _ = r.schur(UU, T, O)
    repairs = [(tb, D['Rb']), (tc, D['Rc']), (sigma, D['B'])]
    expectedL = [[SL[i][j]+sum(p*R[T[i+1]][T[j+1]] for p, R in repairs)
                  for j in range(4)] for i in range(4)]
    expectedU = [[SU[i][j]-sum(p*R[T[i]][T[j]] for p, R in repairs)
                  for j in range(5)] for i in range(5)]
    require(mixedL == expectedL and mixedU == expectedU, 'ALL independently-traded affine Schur positions/signs')
    swap = lambda c: (c & 1) | ((c & 2) << 1) | ((c & 4) >> 1)
    p = [D['keys'].index((swap(c), z, w)) for c, z, w in D['keys']]
    Cavg, Uavg = r.evaluate(D, kap, (tb+tc)/2, sigma)
    require(all((CC[i][j]+CC[p[i]][p[j]])/2 == Cavg[i][j] and
                (UU[i][j]+UU[p[i]][p[j]])/2 == Uavg[i][j]
                for i in range(23) for j in range(23)), 'ALL original convex b/c averaging positions')
    t, sig = a/2, -a/2
    require(r.lower_cone(a, b, t, sig, strict=False) and not r.lower_cone(a, b, t, sig),
            'sharp lower PSD boundary versus strict condition')
    equalL = [[SL[i][j]+t*(D['Rb'][T[i+1]][T[j+1]]+D['Rc'][T[i+1]][T[j+1]])+
               sig*D['B'][T[i+1]][T[j+1]] for j in range(4)] for i in range(4)]
    equalU = [[SU[i][j]-t*(D['Rb'][T[i]][T[j]]+D['Rc'][T[i]][T[j]])-
               sig*D['B'][T[i]][T[j]] for j in range(5)] for i in range(5)]
    endpoint = r.parity(equalL, equalU)
    require(endpoint['lower_even'] == [[F(0), F(0)], [F(0), a]] and
            endpoint['lower_odd'] == [[b+a, -b+a], [-b+a, b]], 'sharp attainable lower boundary matrices')
    out['sharp_boundary_lower_even'] = psd(endpoint['lower_even'], 1)
    out['sharp_boundary_lower_odd'] = psd(endpoint['lower_odd'], 2)
    sig += a/16
    equalL = [[SL[i][j]+t*(D['Rb'][T[i+1]][T[j+1]]+D['Rc'][T[i+1]][T[j+1]])+
               sig*D['B'][T[i+1]][T[j+1]] for j in range(4)] for i in range(4)]
    require(r.lower_cone(a, b, t, sig), 'strict lower recovery interval')
    out['strict_lower_only_recovery'] = {'t': t, 'sigma': sig, 'lower_schur': psd(equalL, 4),
                                        'cap_not_claimed_for_this_repair': True}
    eta = r.automatic_odd_cap_floor(q, k)
    require(eta > 0, 'strict automatic odd-cap floor')
    boundary_t = 2*a*b/(a+b)
    repairs = [(F(0), F(0)), (a/2, -a/2),
               (boundary_t, 2*boundary_t**2/a-2*boundary_t)]
    controls = []
    for tt, ss in repairs:
        require(r.lower_cone(a, b, tt, ss, strict=False), 'actual weak-lower boundary repair')
        curU = [[SU[i][j]-tt*(D['Rb'][T[i]][T[j]]+D['Rc'][T[i]][T[j]])-
                  ss*D['B'][T[i]][T[j]] for j in range(5)] for i in range(5)]
        odd = r.parity(SL, curU)['cap_odd']
        floor = [[odd[i][j]-eta*int(i == j) for j in range(2)] for i in range(2)]
        controls.append({'t': tt, 'sigma': ss, 'actual_odd_cap': psd(odd, 2),
                         'actual_odd_cap_minus_uniform_floor': psd(floor, 2)})
    out['automatic_odd_cap'] = {'uniform_floor': eta, 'boundary_controls_not_infinite_proof': controls,
                                'only_even3x3_cap_remains_after_lower_interval': True}
    out['independent_trade_and_averaging_all_positions'] = True
    return out


def positive(q):
    D, SL, SU, rec = r.reduced(q, 6, F(1, 4096), F(8), F(8), F(-10))
    C, U = r.evaluate(D, F(1, 4096), F(8), F(-10))
    parts = r.parity(SL, SU)
    return {'q': q, 'k': 6, 'reduction': rec,
            'four_parity_blocks': {name: psd(A, len(A)) for name, A in parts.items()},
            'full_physical_lower': psd(C, 22), 'full_physical_cap': psd(U, 23),
            'scope': 'reproduction of published9826, not a new positive theorem'}


def joint():
    data = json.loads((r.PARENT/'JOINT-CERTIFICATE-21-6.json').read_text())
    weights = [F(x) for x in data['dual']['weights']]
    kap = F(1, 4096)
    D, SL, SU, rec = r.reduced(21, 6, kap)
    T, O, keep = partitions(D)
    C, U = r.evaluate(D, kap, F(0), F(0))
    rows, all_coefficients = [], []
    for plane in data['planes']:
        w = [F(x) for x in plane['vector']]
        lower = plane['endpoint'] == 'lower'
        sign = 1 if lower else -1
        coeffs = [r.pair(D['C0'] if lower else D['U0'], w)] + [sign*r.pair(D[name], w)
                                                   for name in ('Delta', 'Rb', 'Rc', 'B')]
        old = [F(x) for x in plane['coefficients_constant_kappa_trade_sigma']]
        require([coeffs[0], coeffs[1], coeffs[2]+coeffs[3], coeffs[4]] == old and
                coeffs[2] == coeffs[3], 'every original independent-trade joint-plane coefficient')
        original_energy = coeffs[0]+kap*coeffs[1]
        if lower:
            star = r.vectors(D)['star']
            w = [x-w[T[0]]*v for x, v in zip(w, star)]
            require(r.pair(C, w) == original_energy, 'lower dual kernel projection preserves actual energy')
        support = T[1:] if lower else T
        x, y = [w[i] for i in support], [w[i] for i in O]
        A = C if lower else U
        B = r.submatrix(A, O)
        cross = r.submatrix(A, O, support)
        minimizer = [-z[0] for z in r.solve(B, r.multiply(cross, [[v] for v in x]))]
        residual = [yy-mm for yy, mm in zip(y, minimizer)]
        shorted = r.pair(SL if lower else SU, x)
        gap = r.pair(B, residual)
        require(gap >= 0 and original_energy == shorted+gap, 'ALL actual shorted-dual residual-square identities')
        rows.append({'endpoint': plane['endpoint'], 'original_coefficients': coeffs,
                     'original_energy': original_energy, 'shorted_energy': shorted,
                     'nonnegative_discarded_residual': gap})
        all_coefficients.append(coeffs)
    total = [sum(w*row[j] for w, row in zip(weights, all_coefficients)) for j in range(5)]
    old_total = [F(x) for x in data['dual']['total']]
    require([total[0], total[1], total[2]+total[3], total[4]] == old_total and
            total[2:] == [0, 0, 0], 'complete original weighted cancellation of both trades and sigma')
    whole = sum(w*row['original_energy'] for w, row in zip(weights, rows))
    shorted = sum(w*row['shorted_energy'] for w, row in zip(weights, rows))
    require(shorted <= whole < 0, 'strict inherited joint obstruction survives exact shorting')
    return {'q': 21, 'k': 6, 'kappa_control_only': kap, 'rows': rows, 'weights': weights,
            'whole_dual_energy': whole, 'shorted_dual_energy': shorted,
            'scope': 'validation of credited9826 obstruction, not new infeasibility'}


def damage():
    rejected = []
    def reject(name, f):
        try:
            f()
        except ValueError as e:
            rejected.append({'name': name, 'rejection': str(e)})
        else:
            raise ValueError('Accepted damaged claim: '+name)
    reject('zero_kappa_wrong_reduction_domain', lambda: r.reduced(9, 3, F(0)))
    reject('kappa_beyond_ancestral_floor_range', lambda: r.reduced(9, 3, F(1, 4)))
    reject('k2_q6_negative_sufficient_margin_not_a_reduction', lambda: r.reduced(6, 2, F(1, 4096)))
    A = r.odd_full_gram(9)
    S, _, _ = r.schur(A, [0, 1], [2, 3])
    reject('false_odd_closed_coefficient', lambda: require(S[0][0] == r.odd_coefficient(9)+F(1, 9), 'changed exact odd energy'))
    reject('strict_claim_at_singular_sharp_boundary', lambda: require(r.lower_cone(F(2), F(5), F(1), F(-1)), 'singular lower boundary is not strict'))
    reject('missing_anchor_injection', lambda: r.solve([[F(1), F(0)], [F(0), F(0)]], [[F(1)], [F(0)]]))
    D, SL, SU, rec = r.reduced(9, 3, F(1, 4096))
    T, O, keep = partitions(D)
    expected = [[SL[i][j]+F(2)*D['Rb'][T[i+1]][T[j+1]]+F(3)*D['Rc'][T[i+1]][T[j+1]]
                 for j in range(4)] for i in range(4)]
    reject('silently_equal_independent_trades', lambda: require(expected == [[SL[i][j]+F(2)*(D['Rb'][T[i+1]][T[j+1]]+D['Rc'][T[i+1]][T[j+1]])
                             for j in range(4)] for i in range(4)], 'independent trade coefficient lost'))
    reject('wrong_cap_repair_sign', lambda: require([[SU[i][j]+D['B'][T[i]][T[j]] for j in range(5)] for i in range(5)] ==
                    [[SU[i][j]-D['B'][T[i]][T[j]] for j in range(5)] for i in range(5)], 'cap repair sign changed'))
    shifted = r.margin_polynomial(r.poly.add(r.poly.constant(9), r.poly.scale(r.poly.K, 3), r.poly.Q),
                                  r.poly.add(r.poly.constant(3), r.poly.K))
    shifted[(0, 0)] = F(-1)
    reject('lost_uniform_cap_margin', lambda: require(all(x > 0 for x in shifted.values()), 'negative shifted cap margin coefficient'))
    require(len(rejected) == 9, 'complete semantic boundary/damage controls')
    return {'rejected': rejected, 'all_controls_are_exact': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=('uniform', 'original9', 'original12', 'original21',
                                        'coupled9', 'coupled21', 'positive22', 'positive23', 'joint', 'damage'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    f = {'uniform': uniform, 'original9': lambda: original(9, 3),
         'original12': lambda: original(12, 4), 'original21': lambda: original(21, 7),
         'coupled9': lambda: coupled(9, 3), 'coupled21': lambda: coupled(21, 7),
         'positive22': lambda: positive(22), 'positive23': lambda: positive(23),
         'joint': joint, 'damage': damage}[args.phase]
    args.out.write_text(json.dumps(r.encode(f()), indent=2, sort_keys=True)+'\n')
    print(args.phase+' completed exactly')
