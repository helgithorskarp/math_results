#!/usr/bin/env python3
"""Definition-level transversal and equality-case checker; no producer import."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'hadwiger_nelson_heule517_family_pilot/certificate.json'
INPUT_SHA = 'd9cb7562d20c385d42a789dc052b0bd66c6859077f4d58f96e8e30a51e6a3ca3'


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def check(certificate, raw):
    require(sha256(raw).hexdigest() == certificate['input_sha256'] == INPUT_SHA,
            'fixed input identity')
    rows = json.loads(raw)['rows']
    require(len(rows) == 526, 'cut count')
    cuts = []
    for row in rows:
        d = row['D']
        require(d and all(type(v) is int and 0 <= v < 517 for v in d)
                and len(d) == len(set(d)), 'cut domain')
        cuts.append(frozenset(d))
    singleton_rows = [i for i, d in enumerate(cuts) if len(d) == 1]
    forced = frozenset().union(*(cuts[i] for i in singleton_rows))
    require(len(singleton_rows) == len(forced) == 329, 'distinct singletons')
    optimum = certificate['optimum']
    require(type(optimum) is int and optimum == 339, 'claimed cost')
    packing = singleton_rows + certificate['packing_extra_rows']
    require(len(packing) == len(set(packing)) == optimum, 'packing order')
    used = set()
    for i in packing:
        require(type(i) is int and 0 <= i < len(cuts), 'packing row')
        require(not used.intersection(cuts[i]), 'packing disjointness')
        used.update(cuts[i])
    # Every transversal has >=339 vertices by the disjoint 339 cuts.
    mandatory = set(forced)
    force_checks = []
    for step in certificate['hub_forcing_steps']:
        v = step['vertex']
        require(type(v) is int and 0 <= v < 517 and v not in mandatory,
                'new forced vertex')
        leaves = set()
        for i in step['pair_rows']:
            require(type(i) is int and 0 <= i < len(cuts), 'forcing row')
            d = cuts[i]
            require(len(d) == 2 and v in d, 'forcing pair')
            leaf, = d - {v}
            require(leaf not in leaves and leaf not in mandatory,
                    'distinct unforced leaves')
            leaves.add(leaf)
        require(len(mandatory) + len(leaves) > optimum, 'avoid-hub bound')
        force_checks.append({'vertex': v, 'mandatory_before': len(mandatory),
                             'leaves': len(leaves),
                             'cost_if_absent_at_least': len(mandatory) + len(leaves)})
        mandatory.add(v)
    added = certificate['added_vertices']
    require(added == list(range(510, 517)) and mandatory == forced.union(added),
            'all and only seven new mandatory vertices')
    residual = [i for i, d in enumerate(cuts) if not d.intersection(mandatory)]
    require(residual == certificate['residual_rows'] and len(residual) == 5,
            'complete residual constraints')
    rvertices = sorted(set().union(*(cuts[i] for i in residual)))
    budget = optimum - len(mandatory)
    require(budget == 3 and len(rvertices) == 8, 'residual size')
    # A minimum transversal has no redundant point outside mandatory union R:
    # deleting it would preserve all constraints and contradict the packing bound.
    models = []
    attempted = 0
    for t in combinations(rvertices, budget):
        attempted += 1
        if all(set(t).intersection(cuts[i]) for i in residual):
            models.append(list(t))
    require(models == certificate['optimal_extras'] and len(models) == 4,
            'complete minimum-transversal list')
    for t in models:
        selected = mandatory.union(t)
        require(len(selected) == optimum and all(selected.intersection(d) for d in cuts),
                'full primal witness')
    return {'status': 'EXACT CUT TRANSVERSAL NUMBER 339; FOUR MINIMUM SETS',
            'vertices': 517, 'cuts': 526, 'singleton_cuts': 329,
            'disjoint_packing_rows': len(packing), 'packing_union_vertices': len(used),
            'transversal_number': optimum, 'minimum_transversals': len(models),
            'residual_rows': residual, 'residual_triples_checked': attempted,
            'full_primal_cut_checks': len(models) * len(cuts),
            'hub_forcing': force_checks, 'optimal_extras': models,
            'graph_queries': 0, 'native_solver_used': False,
            'family_closed': False, 'record_improvement': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    answer = check(json.loads(args.certificate.read_text()), INPUT.read_bytes())
    if args.report:
        args.report.write_text(json.dumps(answer, indent=2) + '\n')
    print(json.dumps(answer, sort_keys=True))
