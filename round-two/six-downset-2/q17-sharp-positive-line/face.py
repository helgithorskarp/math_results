"""Exact slack identity for the necessary NN mass cut; no PSD verdict."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

reader = Path(__file__).resolve().parent
from original import audit, build, canonical, require


def slack_identity(ell, ell0, changes):
    require(all(type(x) in (int, F) for x in [*ell, ell0, *changes.values()]),
            'exact rational inputs only')
    bad = {i for i, x in enumerate(ell) if x < 0}
    incident = [F(0) for _ in ell]
    P = F(0); bb = F(0); bg = F(0); gg = F(0)
    for (i, j), delta in changes.items():
        require(0 <= i < j < len(ell), 'each edge once, unordered')
        incident[i] += delta; incident[j] += delta
        P += max(delta, 0)
        marked = int(i in bad) + int(j in bad)
        if marked == 2:
            bb += 2 * max(delta, 0)
        elif marked == 1:
            bg += abs(delta)
        else:
            gg += 2 * max(-delta, 0)
    E = [F(x) - incident[i] for i, x in enumerate(ell)]
    loop = F(ell0) + 2 * sum(changes.values())
    D = -sum(ell[i] for i in bad)
    minimum = F(D - ell0) / 2
    row_slack = sum(E[i] for i in bad)
    left = 2 * (P - minimum)
    right = row_slack + loop + bb + bg + gg
    require(left == right, 'entire exact necessary-mass slack identity')
    feasible = min(E, default=0) >= 0 and loop >= 0
    if feasible:
        require(P >= minimum, 'row/loop feasible controls obey the mass cut')
        require((P == minimum) == (row_slack == loop == bb == bg == gg == 0),
                'necessary equality face, every nonnegative slack vanishes')
    return {'P': P, 'minimum': minimum, 'row_slack': row_slack, 'loop': loop,
            'bad_bad_increase_penalty': bb, 'bad_good_absolute_penalty': bg,
            'good_good_decrease_penalty': gg, 'identity_left': left,
            'identity_right': right, 'row_loop_feasible': feasible}


def controls():
    ell = [F(-1), F(-1), F(3), F(3)]
    edges = list(combinations(range(4), 2))
    sharp = slack_identity(ell, F(0), {(0, 1): F(-1), (2, 3): F(1)})
    require(sharp['P'] == sharp['minimum'] == 1 and sharp['row_loop_feasible'],
            'hand-computed sharp row/loop control; PSD not asserted')
    lines = []
    for tau in (F(0), F(1, 128), F(1, 4)):
        x = slack_identity(ell, F(0), {(0, 1): -1-tau, (2, 3): 1+3*tau/2})
        require(x['row_loop_feasible'] and x['P'] == 1+3*tau/2 and
                x['row_slack'] == 2*tau and x['loop'] == tau,
                'hand-computed strict-row/loop slope')
        require(3-1-tau >= 0 and -1+1+3*tau/2 >= 0,
                'toy proper-edge capacities; these controls do not assert H')
        lines.append({'tau': str(tau), 'P': str(x['P']), 'slack': str(x['identity_left'])})
    # Every sign on each edge class must pay its distinct, hand-computed cost.
    for e, penalty in [((0, 1), 'bad_bad_increase_penalty'),
                       ((0, 2), 'bad_good_absolute_penalty'),
                       ((2, 3), 'good_good_decrease_penalty')]:
        for delta in (F(-1), F(1)):
            x = slack_identity(ell, F(0), {e: delta})
            expected = (2*max(delta, 0) if e == (0, 1) else
                        abs(delta) if e == (0, 2) else 2*max(-delta, 0))
            require(x[penalty] == expected, 'both signs of all three edge classes')
    feasible = 0
    for values in product((F(-1), F(0), F(1)), repeat=6):
        x = slack_identity(ell, F(0), dict(zip(edges, values)))
        feasible += x['row_loop_feasible']
    require(feasible > 0, 'finite regression grid includes feasible controls')
    try:
        slack_identity(ell, F(0), {(0, 1): .5})
    except ValueError:
        pass
    else:
        raise RuntimeError('float control was not rejected')
    return {'hand_exact_strict_line': lines, 'signed_edge_classes': 6,
            'finite_regression_vectors': 729, 'row_loop_feasible_vectors': feasible,
            'float_input_rejected': True, 'no_toy_PSD_or_H_assertion': True}


def run():
    point = build(json.loads((reader / 'COEFFICIENTS.json').read_bytes()))
    audit(point)
    proper = point['members'][1:]; C = point['C_num']; den = point['denominator']
    B = [i for i, v in enumerate(proper) if 0 not in v]
    ell = [F(den-sum(C[i][j] for j in B), den) for i in B]
    ell0 = F(sum(C[i][j] for i in B for j in B)-54*den, den)
    edges = [(a, b) for a, i in enumerate(B) for b, j in enumerate(B)
             if a < b and set(proper[i]).isdisjoint(proper[j])]
    bad = {a for a, x in enumerate(ell) if x < 0}
    require(len(B) == 199 and len(bad) == 45 and len(edges) == 15930,
            'complete q17 nonstar incidence and every free edge')
    counts = [sum((int(i in bad)+int(j in bad)) == n for i, j in edges) for n in (2, 1, 0)]
    records = []
    for name in ('zero', 'all_three_classes_both_signs'):
        delta = {e: F(0) if name == 'zero' else F((i % 3)-1, 8)
                 for i, e in enumerate(edges)}
        x = slack_identity(ell, ell0, delta)
        records.append({'name': name, **{k: str(v) if isinstance(v, F) else v for k, v in x.items()}})
    require(records[0]['minimum'] == '556505/8192', 'actual q17 necessary mass budget')
    return {'agent': 'six-downset-2', 'role': 'researcher', 'carrier': 'q17/k8',
            'source_reference': '65580698bccd45f168ec50272d0ed15e610a3606 / ACTUAL10278',
            'all_original_nonstar_rows': 199, 'bad_rows': 45, 'all_unordered_free_edges': 15930,
            'edge_class_counts_bad_bad_bad_good_good_good': counts,
            'whole_original_slack_records': records, 'controls': controls(),
            'strict_actual_empty_entry_floor_epsilon_forces_P_at_least':
                '556505/8192 + 4600*epsilon',
            'ordinary_generic_identity_and_H_bridges_unformalized': True,
            'independently_reviewed': False, 'this_reader_checks_algebra_only_other_readers_certify_attainment': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--record', required=True)
    args = parser.parse_args(); result = run(); raw = canonical(result)+b'\n'
    Path(args.record).write_bytes(raw)
    print(json.dumps({'whole_record_bytes': len(raw),
                      'whole_record_sha256': hashlib.sha256(raw).hexdigest(), 'result': result}))
