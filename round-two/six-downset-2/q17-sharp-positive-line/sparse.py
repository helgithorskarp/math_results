"""Explicit q17 affine recipe. The lower and tree readers certify its spectra."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

reader = Path(__file__).resolve().parent
from original import audit, build, canonical, member_type, require


def point_at(base, tau, return_matrices=False):
    require(type(tau) is F and 0 <= tau <= F(1, 128), 'selected exact candidate interval')
    members = base['members']; proper = members[1:]; den = base['denominator']
    C = [[F(x, den) for x in row] for row in base['C_num']]
    original = [[F(x, den) for x in row] for row in base['L_num']]
    dYY = F(256509, den); dBCY = F(1324, den); P0 = F(556505, 8192)
    beta = (dBCY+tau)/28
    alpha = (dYY+tau-7*beta)/21
    gamma = (P0+23*tau)/210
    require(alpha > 0 and beta > 0 and gamma > 0, 'three prescribed NN changes')
    NN_counts = {'YY_YY': 0, 'YY_bcY': 0, 'XX_XX': 0}
    P = F(0); decrease = F(0)
    for i, v in enumerate(proper):
        for j, w in enumerate(proper[i+1:], i+1):
            if not set(v).isdisjoint(w):
                continue
            tv, tw = sorted((member_type(v), member_type(w)))
            change = F(0); label = None
            if tv == tw == (0, 0, 2):
                change = -alpha; label = 'YY_YY'
            elif tv == (0, 0, 2) and tw == (6, 0, 1):
                change = -beta; label = 'YY_bcY'
            elif tv == tw == (0, 2, 0):
                change = gamma; label = 'XX_XX'
            if label is not None:
                NN_counts[label] += 1
                C[i][j] += change; C[j][i] += change
                P += max(change, 0); decrease += max(-change, 0)
    require(NN_counts == {'YY_YY': 378, 'YY_bcY': 252, 'XX_XX': 210},
            'all literal unordered orbit occurrences')
    require(P == P0+23*tau, 'actual positive NN mass and necessary strict-slack slope')
    a = proper.index((0,)); abc = proper.index((0, 1, 2))
    # This anchored star trade preserves each nonstar whole-star row sum.
    abc_change = original[0][abc+1]-tau
    xs = [i for i, v in enumerate(proper) if member_type(v) == (0, 1, 0)]
    require(len(xs) == 8, 'every original X singleton')
    for x in xs:
        C[abc][x] += abc_change/8; C[x][abc] += abc_change/8
        C[a][x] -= abc_change/8; C[x][a] -= abc_change/8
    star_trades = []
    for i, v in enumerate(proper):
        if 0 in v and original[0][i+1] < 0:
            require(i != a, 'selected seed anchor has a positive budget')
            targets = [x for x in xs if set(v).isdisjoint(proper[x])]
            require(len(targets) == 8 and member_type(v) == (1, 0, 1),
                    'every NEW q17 bad star incidence; do not copy q18 abc-only trade')
            change = original[0][i+1]-tau
            for x in targets:
                C[i][x] += change/8; C[x][i] += change/8
                C[a][x] -= change/8; C[x][a] -= change/8
            star_trades.append({'member': list(v), 'total_change': str(change)})
    require(len(star_trades) == 9, 'all nine aY bad star incidences')
    row_sums = [sum(row) for row in C]
    L = [[F(0) for _ in members] for _ in members]
    L[0][0] = 1+sum(row_sums)
    for i in range(len(proper)):
        L[0][i+1] = L[i+1][0] = 1-row_sums[i]
        for j in range(len(proper)):
            L[i+1][j+1] = 1+C[i][j]
    negatives = []; minimum = None; allowed = 0
    for i, v in enumerate(members):
        require(sum(L[i]) == 255 and all(L[i][j] == L[j][i] for j in range(255)),
                'every original stochastic row and symmetric position')
        for j, w in enumerate(members):
            M = (L[i][j]-55*int(i == j))/200
            if set(v).isdisjoint(w):
                allowed += 1
                minimum = M if minimum is None else min(minimum, M)
                if M < 0:
                    negatives.append({'i': i, 'j': j, 'v': list(v), 'w': list(w), 'M': str(M)})
            else:
                require(M == 0, 'every actual intersecting/diagonal position')
    bad_rows = [i for i, v in enumerate(proper) if 0 not in v and original[0][i+1] < 0]
    require(len(bad_rows) == 45 and all(L[0][i+1] == tau for i in bad_rows),
            'ALL45 formerly bad nonstar empty positions exactly repaired')
    require(L[0][0]-55 == tau and L[0][abc+1] == tau,
            'actual empty loop and abc empty entry both retained')
    require(all(L[0][i+1] == tau for i, v in enumerate(proper)
                if 0 in v and original[0][i+1] < 0),
            'all NEW bad star-empty positions repaired')
    require(all(sum(C[i][j] for j, v in enumerate(proper) if 0 in v) == 0
                for i in range(len(proper))), 'every original proper centered-star relation')
    record = {'tau': str(tau), 'alpha': str(alpha), 'beta': str(beta), 'gamma': str(gamma),
            'anchored_abc_total_trade': str(abc_change), 'NN_counts': NN_counts,
            'fresh_bad_star_trades': star_trades,
            'P': str(P), 'negative_NN_mass': str(decrease), 'allowed_positions': allowed,
            'minimum_allowed_M': str(minimum), 'negative_allowed_positions': negatives,
            'original_stochastic_support_star_empty_checks': True,
            'T_rational_matrix_sha256': hashlib.sha256(canonical([[str(x) for x in row[1:]]
                for row in C[1:]])).hexdigest(),
            'all_original_L_sha256': hashlib.sha256(canonical([[str(x) for x in row]
                for row in L])).hexdigest(),
            'entry_and_mass_reader_only': True}
    if return_matrices:
        return record, [row[1:] for row in C[1:]], L
    return record


def run():
    base = build(json.loads((reader/'COEFFICIENTS.json').read_bytes())); audit(base)
    return {'agent': 'six-downset-2', 'role': 'researcher', 'carrier': 'q17/k8',
            'reference_source': '65580698bccd45f168ec50272d0ed15e610a3606 / ACTUAL10278',
            'exact_original_entry_candidates': [point_at(base, F(0)), point_at(base, F(1, 128))],
            'lower_and_upper_certificates_in_separate_readers': True,
            'ordinary_bridges_unformalized': True, 'independently_reviewed': False,
            'seed_coefficients_from_published_q17': True,
            'D3_q18_sparse_mechanism_credited_but_no_matrix_or_floor_inherited': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--record', required=True)
    args = p.parse_args(); result = run(); raw = canonical(result)+b'\n'
    Path(args.record).write_bytes(raw)
    print(json.dumps({'whole_record_bytes': len(raw),
                      'whole_record_sha256': hashlib.sha256(raw).hexdigest(), 'result': result}))
