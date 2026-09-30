"""Replay the compact RUP certificate independently of encoder and solver.

The occurrence-index RUP algorithm is reused, with attribution, from the
published thirteen_endpoint_frontier/check_exclusion.py.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'thirteen_endpoint_frontier'))
from check_exclusion import RUP, clauses, subset_check, self_check


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--full-cnf', type=Path)
    args = p.parse_args()
    m = json.loads((HERE / 'exclusion.json').read_text())
    core, proof = HERE / m['core_file'], HERE / m['proof_file']
    assert hashlib.sha256(core.read_bytes()).hexdigest() == m['core_sha256']
    assert hashlib.sha256(proof.read_bytes()).hexdigest() == m['proof_sha256']
    n, initial = clauses(core)
    assert n == m['full_cnf']['variables'] and len(initial) == m['core_clauses']
    rup = RUP(n, initial)
    assert not rup.entails_by_rup(()), 'Premature empty clause accepted'
    count = 0
    for line in proof.read_text().splitlines():
        values = list(map(int, line.split()))
        assert values[-1] == 0 and all(0 < abs(v) <= n for v in values[:-1])
        clause = tuple(sorted(set(values[:-1])))
        assert rup.entails_by_rup(clause), f'Failed RUP addition{count + 1}'
        rup.add(clause); count += 1
    assert rup.has_empty and count == m['proof_additions']
    checked = subset_check(initial, args.full_cnf, m['full_cnf']) if args.full_cnf else None
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'core_clauses': len(initial), 'RUP_additions': count,
                      'full_formula_clauses_checked': checked,
                      'tiny_truth_controls': self_check(),
                      'premature_empty_clause_rejected': True,
                      'status': 'UNSAT core checked; mathematical reductions and encoding are separate prerequisites.'}))


if __name__ == '__main__':
    main()
