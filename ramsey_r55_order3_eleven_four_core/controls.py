#!/usr/bin/env python3
"""Malformed compact covers and direct local graph controls, active under Python -O."""
from pathlib import Path
from copy import deepcopy
import argparse
import json
import check_cover


def run(cover):
    check_cover.preflight(cover)
    mutants = {}
    x = deepcopy(cover)
    x['cases'].pop()
    mutants['missing_class'] = x
    x = deepcopy(cover)
    x['cases'][-1] = dict(x['cases'][0], index=196)
    mutants['duplicate_class'] = x
    x = deepcopy(cover)
    x['cases'][0]['units'][0] *= -1
    mutants['wrong_primary_polarity'] = x
    x = deepcopy(cover)
    x['cases'][0]['code'] ^= 1
    mutants['wrong_representative_encoding'] = x
    rejected = []
    for name, mutant in mutants.items():
        try:
            check_cover.preflight(mutant)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed cover accepted')
    ids, _ = check_cover.core_positions()
    empty = check_cover.graph(0, ids)
    complete = check_cover.graph((1 << 18)-1, ids)
    check_cover.require(not check_cover.clique(empty, 4095, 5) and check_cover.clique(complete, 4095, 5), 'known cores')
    pattern = cover['forbidden_patterns'][0]
    check_cover.require(all(pattern >> (3*i) & 7 != 7 for i in range(6)), 'noncomplete obstruction')
    check_cover.require(check_cover.clique(check_cover.graph(pattern, ids), 4095, 5), 'planted noncomplete K5')
    return dict(rejected=sorted(rejected), empty_cross_core_valid=True,
                complete_red_core_rejected=True, noncomplete_planted_red_five_rejected=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    result = run(json.loads(a.cover.read_text()))
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
