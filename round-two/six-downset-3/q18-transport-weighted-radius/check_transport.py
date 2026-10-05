"""Literal certificate check: no import or execution of typed-flow producer.

Canonical DATA decoder is openly shared with this author's new census.
Separate mathematical mechanism: iterate ALL58x81 original coordinates,
checking support/floors/radius, ALL58 targets, and ALL81 column equations.
This is not independent peer review or a full Hoffman feasibility proof.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode():
    p = Path(__file__).with_name('census.py')
    spec = importlib.util.spec_from_file_location('literal_transport_decoder', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.original()


def check(path):
    raw = Path(path).read_bytes(); certificate = json.loads(raw)
    endpoints = certificate['endpoint_certificates']
    require(len(endpoints) == 2 and [F(x['e']) for x in endpoints] == [F(1, 363), F(1, 362)]
            and all(F(x['tau']) == F(1, 256) for x in endpoints),
            'designated exact endpoint/floor domain')
    S, B, label, A, nums, P, N, D = decode()
    v = [F(x, D) for x in nums]; abc = S.index(7); J = [i for i in P if i != abc]
    V = sum(v[i] for i in P); alpha = v[abc]
    original_cells = {(label[s], label[bad]) for s in S for bad in B if not s & bad}
    require(len(original_cells) == 23, 'whole literal allowed typed domain')
    receipts = []
    for record in endpoints:
        e, tau = F(record['e']), F(record['tau'])
        recipe = record['recipe_all23_types']
        table = {(tuple(x['star_type']), tuple(x['bad_type'])): F(x['C_change']) for x in recipe}
        require(len(recipe) == len(table) == 23 and set(table) == original_cells,
                'whole exactly23 original transport recipe types')
        q = list(map(F, record['q']))
        a = alpha-15840*e; b = V-alpha-269280*e; t = a+b
        target = [a if i == abc else b/19 if i in J else -t/38 for i in range(58)]
        require(len(q) == 58 and q == target and sum(q) == 0,
                'whole58 original subset-primal targets')
        delta = []; counts = {key: 0 for key in table}
        minimum_floor_slack = None; minimum_radius_slack = None
        for i, s in enumerate(S):
            row = []
            for j, bad in enumerate(B):
                if s & bad:
                    require(A[i][j] == -D, 'ALL792 original intersecting entries fixed minus1')
                    change = F(0)
                else:
                    key = label[s], label[bad]; counts[key] += 1; change = table[key]
                    radius_slack = 220*e-abs(change)
                    floor_slack = F(A[i][j], D)+change-(tau-1)
                    require(radius_slack >= 0, 'ALL3906 original entry displacement bounds')
                    require(floor_slack >= 0, 'ALL3906 original entry floor bounds')
                    minimum_radius_slack = radius_slack if minimum_radius_slack is None else min(minimum_radius_slack, radius_slack)
                    minimum_floor_slack = floor_slack if minimum_floor_slack is None else min(minimum_floor_slack, floor_slack)
                row.append(change)
            require(v[i]+sum(row) == q[i], 'ALL58 original transported row equations')
            delta.append(row)
        require(sum(counts.values()) == 3906 and all(counts[(tuple(x['star_type']),tuple(x['bad_type']))] == x['original_allowed_positions'] for x in recipe),
                'whole original3906 recipe position multiplicities')
        require(all(sum(delta[i][j] for i in range(58)) == 0 for j in range(81)),
                'ALL81 original individual transported column equations')
        energy = sum(x*x for x in q)
        require(energy == F(record['exact_energy']) == a*a+b*b/19+t*t/38,
                'whole original58 transported energy')
        receipts.append({'e': str(e), 'tau': str(tau), 'literal_total_entry_checks': 4698,
                         'allowed_radius_checks': 3906, 'allowed_floor_checks': 3906,
                         'intersecting_fixed_checks': 792, 'row_equations': 58,
                         'column_equations': 81, 'all23_original_type_counts': [
                             {'star_type': list(r), 'bad_type': list(c), 'count': count}
                             for (r, c), count in sorted(counts.items())],
                         'minimum_original_radius_slack': str(minimum_radius_slack),
                         'minimum_original_floor_slack': str(minimum_floor_slack),
                         'energy': str(energy)})
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE literal exact endpoint transport certificate checked',
            'certificate_bytes': len(raw), 'certificate_SHA256': hashlib.sha256(raw).hexdigest(),
            'endpoint_checks': receipts, 'flow_algorithm_executed': False,
            'ancestor_program_PSD_factor_or_peer_input_imported': False,
            'ordinary_convex_all_real_bridge_or_full_radius_classification_claimed_by_code_alone': False,
            'original_global_stochastic_PSD_matrix_or_best_distance_claimed': False,
            'independent_mathematical_review_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('TRANSPORT.json'))
    print(json.dumps(check(parser.parse_args().certificate), indent=2))
