"""Exact six-deletion cutoff and uniform necessary cap bound.

The complete complement/rank/gap inference is an ordinary written
bridge. Passing finite controls does not prove the uniform criterion.
These are author checks; independent review and formalization are pending.
"""
from forms import *
import sys
import argparse
import json
import time
import polycap

import original_checks as parent
KAPPA, LOWER_FLOOR, CAP_FLOOR = F(1, 4096), F(1, 65536), F(1, 65536)


def negative_mean(q):
    D = forms(q, 6)
    low, cost, lp = parent.lower_dual(D)
    v = vectors(D)
    orientation = parent.orientation(D)
    cap = {name: pair(D[name], v['one']) for name in ('U0', 'Delta', 'Rb', 'Rc', 'B')}
    require(cap['Rb'] == cap['Rc'] == 0 and cap['B'] == 2 and cap['Delta'] > 0,
            'all original mean cap omitted-parameter energies')
    margin = cap['U0']+2*cost
    require(margin < 0, 'strict mean exclusion using the uniform credited lower dual')
    _, _, literal = parent.literal_checks(D, low, v['one'])
    return {'q': q, 'k': 6, 'N': D['N'], 'sigma_lower_cost': cost,
            'margin': margin, 'orientation': orientation, 'lower_pairings': lp, 'cap_pairings': cap,
            'literal': literal, 'method': 'mean plus published9766 BC lower bound',
            'all_real_core_face_excluded': True}


def negative_residual(q):
    D = forms(q, 6)
    low, cost, lp = parent.lower_dual(D)
    values = polycap.scalars(q, 6)
    v = vectors(D)
    cap = [v['one'][i]-values['a']*v['y'][i]-values['b']*v['trade_iso'][i] for i in range(len(D['keys']))]
    cp = {name: pair(D[name], cap) for name in ('U0', 'Delta', 'Rb', 'Rc', 'B')}
    moment = [[pair(D['U0'], a, b) for b in (v['one'], v['y'], v['trade_iso'])]
              for a in (v['one'], v['y'], v['trade_iso'])]
    require(moment == values['moment'] and cp['Rb'] == cp['Rc'] == 0 and
            cp['B'] == 2*(1-values['b'])**2 and cp['Delta'] == values['Delta_pairing'] > 0 and
            cp['U0']+cost*cp['B'] == values['adjusted_cap_minimum'] < 0,
            'complete adjusted original cap pairings and strict obstruction')
    parent.orientation(D)
    _, _, literal = parent.literal_checks(D, low, cap)
    return {'q': q, 'k': 6, 'N': D['N'], 'values': values,
            'lower_pairings': lp, 'cap_pairings': cp, 'literal': literal,
            'method': 'new BC-adjusted original residual', 'all_real_core_face_excluded': True}


def negative_joint():
    data = json.loads(Path(__file__).with_name('JOINT-CERTIFICATE-21-6.json').read_text())
    require(data['q'] == 21 and data['k'] == 6 and len(data['planes']) == 3, 'exact three-plane frontier input')
    D = forms(21, 6)
    weights = [F(x) for x in data['dual']['weights']]
    require(all(x > 0 for x in weights) and sum(weights) == 1, 'every rational dual weight strictly positive')
    decoded = [[F(x) for x in p['vector']] for p in data['planes']]
    require(all(len(w) == len(D['keys']) for w in decoded), 'every exact original orbit value present')
    require(all((4096*x).denominator == 1 for w in decoded for x in w), 'every displayed integer dual coordinate is exact')
    swap = lambda c: (c & 1) | ((c & 2) << 1) | ((c & 4) >> 1)
    swap_indices = [D['keys'].index((swap(c), z, w)) for c, z, w in D['keys']]
    require(all(w == [F(x) for x in p['partner']] == [w[i] for i in swap_indices]
                for p, w in zip(data['planes'], decoded)), 'all three original vectors explicitly b/c invariant')
    original, positions = original_forms(21, 6)
    require(original == D, 'all six coefficient forms decoded over ALL original pairs')
    X, tab = domain(21, 6), table(21)
    index = {key: i for i, key in enumerate(D['keys'])}
    literal_pairings = [{name: F(0) for name in NAMES} for p in data['planes']]
    for A in X[1:]:
        i = index[orbit(A, 6)]
        for B in X[1:]:
            j = index[orbit(B, 6)]
            entries = list(entry(21, D['s'], tab, A, B))
            entries[-1] += D['N']*int(A == B)-1
            for w, pairings in zip(decoded, literal_pairings):
                product = w[i]*w[j]
                for name, value in zip(NAMES, entries):
                    pairings[name] += product*value
    rows = []
    for p, w, pairings in zip(data['planes'], decoded, literal_pairings):
        require(pairings == {name: pair(D[name], w) for name in NAMES}, 'each entire separately decoded original dual energy')
        require(pairings['Rb'] == pairings['Rc'], 'both original trade coefficients explicitly equal')
        if p['endpoint'] == 'lower':
            row = [pairings['C0'], pairings['Delta'], pairings['Rb'], pairings['Rc'], pairings['B']]
        else:
            require(p['endpoint'] == 'cap', 'unsupported dual endpoint')
            row = [pairings['U0'], -pairings['Delta'], -pairings['Rb'], -pairings['Rc'], -pairings['B']]
        expected = [F(x) for x in p['coefficients_constant_kappa_trade_sigma']]
        require([row[0], row[1], row[2]+row[3], row[4]] == expected, 'every regenerated exact affine row')
        rows.append(row)
    total = dual_total(weights, rows, data['dual']['total'])
    orientation = parent.orientation(D)
    return {'q': 21, 'k': 6, 'N': D['N'], 'keys': D['keys'], 'sizes': D['sizes'],
            'weights': weights, 'vectors_times4096': [[int(4096*x) for x in w] for w in decoded],
            'literal_pairings': literal_pairings, 'rows_constant_kappa_tb_tc_sigma': rows,
            'total': total, 'orientation': orientation, 'original_ordered_positions': positions,
            'method': 'three original positive-weight PSD planes; no finite-grid premise',
            'all_real_independent_trade_core_face_excluded': True, 'balanced_p_u_extension_excluded': False}


def positive(q=22, trade=F(8), sigma=F(-10)):
    k = 6
    D = forms(q, k)
    G, H = evaluate(D, KAPPA, trade, sigma)
    m, s, N = len(D['keys']), D['s'], D['N']
    a = vectors(D)['star']
    sizes, weighted = D['sizes'], [x*y for x, y in zip(D['sizes'], a)]
    W = [[F(sizes[i]*int(i == j)) for j in range(m)] for i in range(m)]
    P = [[W[i][j]-F(weighted[i]*weighted[j], s) for j in range(m)] for i in range(m)]
    require(sum(weighted) == s and not any(action(G, a)), 'complete weighted forced-star action')
    checks = {name: parent.psd_record(A, rank) for name, A, rank in (
        ('lower', G, m-1), ('cap', H, m),
        ('lower_floor', [[G[i][j]-LOWER_FLOOR*P[i][j] for j in range(m)] for i in range(m)], m-1),
        ('cap_floor', [[H[i][j]-CAP_FLOOR*W[i][j] for j in range(m)] for i in range(m)], m))}
    X, C, literal_record = parent.literal_checks(D, parameters=(KAPPA, trade, sigma))
    L = exact.lift(C)
    M = [[(L[i][j]-s*int(i == j))/F(N-s) for j in range(N)] for i in range(N)]
    parent.check_lift(D, X, C, L, M, trade, sigma)
    stars = [sum(bool(A & (1 << i)) for A in X) for i in range(q+3)]
    require(stars == [s, s-k, s-k]+[q+5]*k+[q+6]*(q-k), 'all original labelled stars including outside classes')
    U = [[F(N*int(i == j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    rows = [sum(row) for row in U]
    EUET = [[sum(rows)]+[-x for x in rows]]+[[-rows[i]]+U[i] for i in range(N-1)]
    require(all(F(N*int(i == j))-L[i][j] == EUET[i][j] for i in range(N) for j in range(N)), 'ALL physical cap-lift positions')
    require(0 < KAPPA <= F(1, 8) and N-2*s > 0 and LOWER_FLOOR <= KAPPA/2 and CAP_FLOOR <= N-2*s,
            'complete credited nonfixed lower and cap margins apply')
    return {'q': q, 'k': k, 'N': N, 's': s, 'parameters': [KAPPA, trade, trade, sigma],
            'fixed_checks': checks, 'literal': literal_record, 'stars': stars,
            'whole_positions': N*N, 'whole_endpoint_ranks': [N-1, N-1],
            'complement_dimension': N-1-m, 'complete_nonfixed_lower_floor': KAPPA/2,
            'complete_nonfixed_cap_floor': N-2*s, 'nonempty_lower_floor': LOWER_FLOOR,
            'nonempty_cap_floor': CAP_FLOOR, 'lambda': -F(s, N-s),
            'whole_projected_unit_gap': CAP_FLOOR/(N-s),
            'whole_inference_is_credited_ordinary_bridge_not_sampled_complement': True}


def dual_total(weights, rows, expected):
    require(len(weights) == len(rows) == 3 and all(len(row) == 5 for row in rows),
            'complete independent-parameter dual rows')
    require(all(x > 0 for x in weights) and sum(weights) == 1,
            'every dual weight strictly positive and normalized')
    total = [sum(weight*row[j] for weight, row in zip(weights, rows)) for j in range(5)]
    require(total[2:] == [F(0)]*3 and total[0] < -F(1, 256) and total[1] < 0,
            'strict dual cancels BOTH independent trades and BC')
    require([total[0], total[1], F(0), F(0)] == [F(x) for x in expected],
            'entire retained exact dual total')
    return total


def reject(call, label):
    try:
        call()
    except ValueError:
        return label
    raise ValueError('Semantic damage accepted: '+label)


def damages():
    from copy import deepcopy
    frozen = json.loads(Path(__file__).with_name('RESULT.json').read_text())
    joint = frozen['joint']
    weights = [F(x) for x in joint['weights']]
    rows = [[F(x) for x in row] for row in joint['rows_constant_kappa_tb_tc_sigma']]
    data = json.loads(Path(__file__).with_name('JOINT-CERTIFICATE-21-6.json').read_text())
    expected = data['dual']['total']
    dual_total(weights, rows, expected)
    rejected = []
    bad = list(weights)
    bad[1] += bad[0]
    bad[0] = F(0)
    rejected.append(reject(lambda: dual_total(bad, rows, expected), 'zero-positive-dual-weight'))
    badrows = deepcopy(rows)
    badrows[0][2] += F(1, 4096)
    badrows[0][3] -= F(1, 4096)
    require(badrows[0][2]+badrows[0][3] == rows[0][2]+rows[0][3],
            'equal-trade decoy preserves the combined coefficient')
    rejected.append(reject(lambda: dual_total(weights, badrows, expected),
                           'independent-trade-decoy-with-unchanged-sum'))
    badrows = deepcopy(rows)
    badrows[0][4] += F(1, 4096)
    rejected.append(reject(lambda: dual_total(weights, badrows, expected), 'uncancelled-BC-coefficient'))
    badrows = deepcopy(rows)
    for row in badrows:
        row[0] = F(1)
    rejected.append(reject(lambda: dual_total(weights, badrows, expected), 'lost-negative-dual-margin'))
    badrows = deepcopy(rows)
    for row in badrows:
        row[1] = F(1)
    rejected.append(reject(lambda: dual_total(weights, badrows, expected), 'wrong-kappa-orientation'))
    D = forms(21, 6)
    w = [F(x) for x in data['planes'][0]['vector']]
    w[0] += F(1, 4096)
    changed = [pair(D['U0'], w), -pair(D['Delta'], w),
               -pair(D['Rb'], w), -pair(D['Rc'], w), -pair(D['B'], w)]
    rejected.append(reject(lambda: require(changed == rows[0], 'damaged original dual vector energy'),
                           'changed-integer-original-dual-coordinate'))
    ordinary = polycap.coefficients()
    bad_den = polycap.add(polycap.mul(polycap.Q, ordinary['cost_denominator']), polycap.constant(1))
    rejected.append(reject(lambda: polycap.divide(ordinary['residual_numerator'], bad_den),
                           'wrong-entire-residual-division-denominator'))
    shifted = polycap.coefficients(polycap.add(polycap.constant(6), polycap.scale(polycap.K, 3), polycap.Q),
                                   polycap.add(polycap.constant(2), polycap.K))
    bad_poly = dict(shifted['Delta_numerator'])
    bad_poly[(0, 0)] *= -1
    rejected.append(reject(lambda: polycap.positive_coefficients(bad_poly, 'damaged Delta'),
                           'negative-unbounded-shifted-slope-coefficient'))
    rejected.append(reject(lambda: polycap.scalars(17, 6), 'unproved-quadrant-control'))
    D = forms(6, 6)
    D['sizes'][0] += 1
    rejected.append(reject(lambda: parent.literal_checks(D), 'wrong-original-physical-orbit-size'))
    D = forms(6, 6)
    D['Delta'][0][1] += F(1, 4096)
    D['Delta'][1][0] += F(1, 4096)
    rejected.append(reject(lambda: parent.literal_checks(D), 'changed-original-operator-entry'))
    D = forms(22, 6)
    _, U = evaluate(D, KAPPA, F(8), F(-10))
    m = len(D['keys'])
    # This exact stronger sufficient floor actually fails. Its rejection
    # is not a proof of H infeasibility.
    stronger = [[U[i][j]-F(D['sizes'][i]*int(i == j), 4096) for j in range(m)] for i in range(m)]
    rejected.append(reject(lambda: parent.psd_record(stronger, m), 'false-stronger-physical-cap-floor'))
    rejected.append(reject(lambda: parent.psd_record(U, m-1), 'wrong-full-cap-rank'))
    return {'semantic_damages_rejected': rejected,
            'false_stronger_floor_is_not_H_infeasibility': True,
            'damages_are_controls_not_mathematical_premises': True}


PHASES = ('mean', 'residual', 'joint', 'positive', 'positive23', 'uniform', 'damage')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=PHASES, required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    if args.record.exists():
        raise ValueError('Refusing to overwrite a mathematical record')
    start = time.monotonic()
    if args.phase == 'mean':
        record = [negative_mean(q) for q in range(6, 19)]
    elif args.phase == 'residual':
        record = [negative_residual(q) for q in (19, 20)]
    elif args.phase == 'joint':
        record = negative_joint()
    elif args.phase == 'positive':
        record = positive()
    elif args.phase == 'positive23':
        record = positive(23)
    elif args.phase == 'uniform':
        record = polycap.check()
    else:
        record = damages()
    record = encode(record)
    args.record.write_text(json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps({'phase': args.phase, 'record_sha256': exact.digest(record),
                      'seconds': time.monotonic()-start, 'literal_complete': args.phase != 'damage'}), flush=True)


if __name__ == '__main__':
    run()
