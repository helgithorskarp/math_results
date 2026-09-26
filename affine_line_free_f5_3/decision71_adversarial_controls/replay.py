"""Prove each single omission UNSAT; reject its proof on a one-clause weaker SAT input."""
import argparse
import ctypes
import json
from pathlib import Path
import subprocess
import time

from verify import (check_fixture, digest, dimacs, falsified, formula, load_fixtures,
                    positive70, require)

OFFICIAL_SOURCE_SHA256 = 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'


def checked_run(checker, cnf, proof, log, expected):
    result = subprocess.run([str(checker), str(cnf), str(proof)], capture_output=True,
                            text=True, timeout=60)
    log.write_text(result.stdout+result.stderr)
    accepted = result.returncode == 0 and 's VERIFIED' in result.stdout.splitlines()
    if expected:
        require(accepted, 'UNSAT certificate failed native checking')
    else:
        require(result.returncode >= 0 and not accepted
                and 's NOT VERIFIED' in result.stdout.splitlines(),
                'satisfiable input was accepted, crashed, or did not reject normally')
    return result.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--checker-source', type=Path, required=True)
    parser.add_argument('--conflicts', type=int, default=500000)
    args = parser.parse_args()
    require(args.conflicts > 0, 'invalid conflict budget')
    require(digest(args.checker_source.read_bytes()) == OFFICIAL_SOURCE_SHA256,
            'incorrect stock checker source')
    checker = args.checker.resolve()
    checker_hash = digest(checker.read_bytes())
    # Generated proofs and logs stay in a new directory, never beside source artifacts.
    require(not args.out.exists(), 'output must be a new directory')
    args.out.mkdir(parents=True)
    import pysat
    from pysat.solvers import Solver
    libc = ctypes.CDLL(None)
    libc.fflush.argtypes = [ctypes.c_void_p]
    libc.fflush.restype = ctypes.c_int
    fixtures, seeds = load_fixtures()
    records = []
    begun = time.monotonic()
    for r in fixtures:
        check_fixture(r, seeds)
        original = formula(r['weights'])
        removed = r['removed_clause_indices']
        sat_clauses = [c for i, c in enumerate(original) if i not in removed]
        sat_path = args.out/f"case_{r['index']}_omit_both.cnf"
        sat_path.write_bytes(dimacs(sat_clauses))
        require(not falsified(sat_clauses, r['points']), 'invalid explicit SAT certificate')
        # A search-level positive check, in addition to the explicit model verification.
        with Solver(name='cadical195', bootstrap_with=sat_clauses) as solver:
            solver.conf_budget(args.conflicts)
            require(solver.solve_limited() is True, 'weakened SAT positive control failed')
            model = [v-1 for v in solver.get_model() if 0 < v <= 125]
            require(len(model) == 71 and not falsified(sat_clauses, model), 'bad SAT decoder')
        word70, points70 = positive70(r)
        require(not falsified(formula(word70), points70), '70-point control failed')
        for omission in removed:
            clauses = [c for i, c in enumerate(original) if i != omission]
            prefix = args.out/f"case_{r['index']}_omit_{omission}"
            cnf, proof = prefix.with_suffix('.cnf'), prefix.with_suffix('.drat')
            cnf.write_bytes(dimacs(clauses))
            with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
                solver.conf_budget(args.conflicts)
                answer = solver.solve_limited()
                require(answer is False, f'single-omission formula was SAT or UNKNOWN: {prefix.name}')
                stats = solver.accum_stats()
                require(libc.fflush(None) == 0, 'native proof flush failed')
                solver.solver.prfile.seek(0)
                proof.write_bytes(solver.solver.prfile.read())
            proof_hash = digest(proof.read_bytes())
            good = checked_run(checker, cnf, proof, prefix.with_suffix('.valid.log'), True)
            # The second formula differs by exactly one removed original line clause.
            bad = checked_run(checker, sat_path, proof, prefix.with_suffix('.invalid.log'), False)
            require(digest(proof.read_bytes()) == proof_hash, 'proof changed during checking')
            require(cnf.read_bytes() == dimacs(clauses) and sat_path.read_bytes() == dimacs(sat_clauses),
                    'input changed during checking')
            record = {'index': r['index'], 'omitted_clause': omission,
                      'single_omission_cnf_sha256': digest(cnf.read_bytes()),
                      'double_omission_cnf_sha256': digest(sat_path.read_bytes()),
                      'proof_sha256': proof_hash, 'proof_bytes': proof.stat().st_size,
                      'status': 'UNSAT_DRAT_VERIFIED', 'wrong_input_status': 'SAT_PROOF_REJECTED',
                      'valid_checker_returncode': good, 'invalid_checker_returncode': bad,
                      'stats': stats}
            prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
            records.append(record)
            print(json.dumps({'case': r['index'], 'omission': omission, 'checked': True}), flush=True)
    require(len(records) == 8 and digest(checker.read_bytes()) == checker_hash,
            'incomplete run or checker changed')
    summary = {'status': 'FOUR_MINIMAL_TWO_CLAUSE_WEAKENINGS_VERIFIED',
               'single_omission_unsat_proofs': 8, 'one_clause_wrong_input_rejections': 8,
               'explicit71_sat_controls': 4, 'solver71_sat_controls': 4,
               'explicit70_sat_controls': 4, 'records': records,
               'checker_sha256': checker_hash, 'checker_source_sha256': OFFICIAL_SOURCE_SHA256,
               'python_sat_version': pysat.__version__, 'conflict_budget': args.conflicts,
               'seconds': time.monotonic()-begun, 'global_exact_proof_accepted': False}
    (args.out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'records'}, indent=2))


if __name__ == '__main__':
    main()
