"""Bounded untrusted proposal; literal model checking is a separate child."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import resource
import sys
import time

from pysat.solvers import Solver


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    directory = args.model_dir
    output = directory / 'solver.json'
    require(not output.exists(), 'Existing native query')
    meta = json.loads((directory / 'metadata.json').read_text())
    require(meta['status'] == 'THREE_RUN_CANONICAL_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK', 'Wrong stage')
    for name, key in [('CNF', 'CNF_sha256'), ('base_word', 'base_file_sha256'), ('AP_pool', 'AP_pool_sha256')]:
        require(sha(meta[name]) == meta[key], 'Input changed')
    # Preflight includes every parsed literal, every row, every possible model identifier,
    # and the full reported conflict cap. A separate child checks the returned literal model.
    cases = meta['clauses'] + meta['literals'] + meta['variables'] + 10000 + 100
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'metadata_sha256': sha(directory / 'metadata.json'), 'CNF_sha256': meta['CNF_sha256'],
              'source_sha256': sha(__file__), 'solver': 'CaDiCaL1.9.5', 'python_sat': importlib.metadata.version('python-sat'),
              'conflict_cap_requested': 9500, 'reported_conflict_cap': 10000, 'conservative_combined_cases': cases,
              'proof_checked': False, 'family_exclusion': False, 'new_W_bound': None, 'threads': 1}
    if cases > 200000:
        result['status'] = 'THREE_RUN_SOLVER_PREFLIGHT_OVER_CAP_PAUSED_NO_EXCLUSION'
    else:
        lines = Path(meta['CNF']).read_text().splitlines()
        require(lines[0] == f"p cnf {meta['variables']} {meta['clauses']}", 'Exact CNF header')
        clauses = []
        for line in lines[1:]:
            row = list(map(int, line.split()))
            require(row and row[-1] == 0 and all(0 < abs(x) <= meta['variables'] for x in row[:-1]), 'Literal domain')
            clauses.append(row[:-1])
        require(len(clauses) == meta['clauses'] and sum(map(len, clauses)) == meta['literals'], 'Exact parsing domain')
        native_began = time.monotonic()
        with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
            solver.conf_budget(9500)
            answer = solver.solve_limited()
            stats = solver.accum_stats()
            assignment = solver.get_model() if answer is True else None
            proof = solver.get_proof() if answer is False else None
        result.update(status='SAT_THREE_RUN_WORD_PENDING_INDEPENDENT_CHECKS' if answer is True else
                             'UNSAT_UNCHECKED_PROOF_NO_THREE_RUN_FAMILY_EXCLUSION' if answer is False else
                             'UNKNOWN_THREE_RUN_QUERY_PAUSED_NO_EXCLUSION', stats=stats,
                      solver_seconds=time.monotonic() - native_began,
                      reported_conflict_budget_respected=int(stats.get('conflicts', 0)) <= 10000)
        if assignment is not None:
            require(len(assignment) == meta['variables'] and all(type(x) is int for x in assignment)
                    and {abs(x) for x in assignment} == set(range(1, meta['variables'] + 1)), 'Complete native assignment')
            target = directory / 'assignment.json'
            target.write_text(json.dumps(assignment, separators=(',', ':')) + '\n')
            result.update(assignment=str(target.resolve()), assignment_sha256=sha(target))
        if proof is not None:
            target = directory / 'unchecked-proof.drat'
            target.write_text('\n'.join(proof) + '\n')
            result.update(unchecked_proof=str(target.resolve()), unchecked_proof_sha256=sha(target), proof_lines=len(proof))
        require(result['reported_conflict_budget_respected'], 'Reported conflict cap exceeded')
    result.update(seconds=time.monotonic() - began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(result['seconds'] < 30, 'Unchanged native30-second cap')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
