#!/usr/bin/env python3
"""Independent incidence encoding; optionally regenerate and check a DRAT proof.

The mathematical CNF generator uses only the standard library. Solving
requires python-sat==1.9.dev15. Proof checking requires drat-trim.
Large generated files go in an explicitly supplied work directory.
"""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

from cnf import Cnf
from completion import validate_completion, validate_through
from local import require

ROOT = Path(__file__).resolve().parent


def generate(rows):
    validate_through(rows)
    formula = Cnf()
    incidence = [[formula.var() for _ in range(12)] for _ in range(10)]
    for row in incidence:
        formula.exactly(row, 6)
    for point in range(12):
        formula.exactly([row[point] for row in incidence], 5)
    for left, right in zip(incidence, incidence[1:]):
        formula.lex_le(left[::-1], right[::-1], strict=True)
    missed = [triple for triple in combinations(range(12), 3)
              if not any(all(row >> point & 1 for point in triple) for row in rows)]
    for triple in missed:
        formula.clauses.append([formula.and_var([row[p] for p in triple]) for row in incidence])
    for u, v in combinations(range(12), 2):
        pair = (1 << u) | (1 << v)
        through = [row for row in rows if row & pair == pair]
        both = [formula.and_var([row[u], row[v]]) for row in incidence]
        states = formula.count_states(both, 2)
        if len(through) == 1:
            formula.clauses.append([states[2]])
        else:
            forced = (4095 ^ (through[0] | through[1])) | pair
            matches = [formula.and_var([lit if forced >> p & 1 else -lit
                                        for p, lit in enumerate(row)]) for row in incidence]
            formula.clauses.append([states[2]] + matches)
    return formula, incidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', type=int, choices=range(6))
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path)
    parser.add_argument('--generate-only', action='store_true')
    parser.add_argument('--pin-witness', action='store_true', help='positive control for cases 0..3')
    args = parser.parse_args()
    record = json.loads((ROOT / 'families.json').read_text())['classes'][args.case]
    formula, incidence = generate(record['rows'])
    if args.pin_witness:
        require(len(record['completion']) == 10, 'the selected upper witness has eleven blocks')
        for row, mask in zip(incidence, sorted(record['completion'])):
            formula.clauses.extend([[lit if mask >> p & 1 else -lit]
                                    for p, lit in enumerate(row)])
    args.work_dir.mkdir(parents=True, exist_ok=True)
    stem = f'case{args.case}' + ('_pin' if args.pin_witness else '')
    cnf = args.work_dir / (stem + '.cnf')
    cnf.write_text(f'p cnf {formula.nvars} {len(formula.clauses)}\n'
                   + ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in formula.clauses))
    summary = dict(case=args.case, variables=formula.nvars, clauses=len(formula.clauses),
                   cnf_sha256=sha256(cnf.read_bytes()).hexdigest())
    if args.generate_only:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name='glucose4', bootstrap_with=formula.clauses, with_proof=True) as solver:
        solver.conf_budget(3000000)
        result = solver.solve_limited()
        summary.update(solver_result=result, solve_seconds=time.monotonic() - started,
                       solver_statistics=solver.accum_stats())
        require(result is not None, 'UNKNOWN: conflict budget exhausted; no exclusion is established')
        if result:
            model = set(solver.get_model())
            blocks = [sum(1 << p for p, lit in enumerate(row) if lit in model) for row in incidence]
            validate_completion(record['rows'], blocks)
            summary.update(status='VERIFIED_SAT_WITNESS', completion=blocks)
        else:
            proof = args.work_dir / (stem + '.drat')
            proof.write_text('\n'.join(solver.get_proof()) + '\n')
            summary.update(proof_sha256=sha256(proof.read_bytes()).hexdigest(),
                           proof_bytes=proof.stat().st_size)
            require(args.drat_trim is not None, 'UNSAT remains unchecked: supply --drat-trim')
            log = args.work_dir / (stem + '_drat.log')
            with log.open('w') as output:
                check = subprocess.run([str(args.drat_trim.resolve()), str(cnf.resolve()),
                                        str(proof.resolve())], stdout=output,
                                       stderr=subprocess.STDOUT, check=False)
            require(check.returncode == 0 and 's VERIFIED' in log.read_text(), 'DRAT check failed')
            summary['status'] = 'INDEPENDENTLY_CHECKED_UNSAT'
    (args.work_dir / (stem + '_summary.json')).write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
