"""One bounded constructive SAT query, preserving assignment or an unchecked proof."""
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
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    directory, output = args.model_dir, args.model_dir / 'solver.json'
    require(not output.exists(), 'Existing solver query')
    metadata = json.loads((directory / 'metadata.json').read_text())
    require(metadata['status'] == 'TWO_RUN_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK', 'Not ready')
    for name, digest in [('CNF', 'CNF_sha256'), ('AP_pool', 'AP_pool_sha256'), ('base_word', 'base_file_sha256')]:
        require(sha(metadata[name]) == metadata[digest], 'Model input changed')
    lines = Path(metadata['CNF']).read_text().splitlines()
    require(lines[0] == f"p cnf {metadata['variables']} {metadata['clauses']}", 'CNF header')
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        require(values[-1] == 0 and all(0 < abs(lit) <= metadata['variables'] for lit in values[:-1]), 'CNF row')
        clauses.append(values[:-1])
    require(len(clauses) == metadata['clauses'] and sum(map(len, clauses)) == metadata['literals'], 'Complete CNF')
    # Includes row reads, complete SAT-model literal checks, decoding and conflict cap.
    preflight = 2 * len(clauses) + metadata['literals'] + 2 * metadata['variables'] + 10000 + 100
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'metadata_sha256': sha(directory / 'metadata.json'), 'CNF_sha256': metadata['CNF_sha256'],
              'AP_pool_sha256': metadata['AP_pool_sha256'], 'solver': 'CaDiCaL1.9.5 via python-sat',
              'python_sat': importlib.metadata.version('python-sat'), 'variables': metadata['variables'],
              'clauses': metadata['clauses'], 'APs': metadata['APs'], 'length': metadata['length'],
              'max_disagreement_runs': 2, 'source_sha256': sha(__file__),
              'conservative_combined_cases': preflight, 'conflict_cap_requested': 9500,
              'reported_conflict_cap': 10000, 'threads': 1, 'proof_checked': False,
              'family_exclusion': False, 'new_W_bound': None}
    if preflight > 200000:
        result.update(status='TWO_RUN_SOLVER_PREFLIGHT_OVER_CAP_PAUSED_NO_EXCLUSION',
                      seconds=time.monotonic() - began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    else:
        solver_began = time.monotonic()
        with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
            solver.conf_budget(9500)
            answer = solver.solve_limited()
            stats = solver.accum_stats()
            assignment = solver.get_model() if answer is True else None
            proof = solver.get_proof() if answer is False else None
        result.update(status='SAT_TWO_RUN_WORD_PENDING_INDEPENDENT_DIRECT_CHECK' if answer is True else
                             'UNSAT_UNCHECKED_PROOF_NO_FAMILY_EXCLUSION' if answer is False else
                             'UNKNOWN_TWO_RUN_QUERY_PAUSED_NO_EXCLUSION', stats=stats,
                      solver_seconds=time.monotonic() - solver_began,
                      reported_conflict_budget_respected=int(stats.get('conflicts', 0)) <= 10000)
        if assignment is not None:
            truth = {abs(lit): lit > 0 for lit in assignment}
            require(set(truth) == set(range(1, metadata['variables'] + 1)), 'Incomplete assignment')
            require(all(any(truth[abs(lit)] == (lit > 0) for lit in row) for row in clauses), 'SAT assignment fails CNF')
            target = directory / 'assignment.json'
            target.write_text(json.dumps(assignment, separators=(',', ':')) + '\n')
            result.update(assignment=str(target.resolve()), assignment_sha256=sha(target))
        if proof is not None:
            target = directory / 'unchecked-proof.drat'
            target.write_text('\n'.join(proof) + '\n')
            result.update(unchecked_proof=str(target.resolve()), unchecked_proof_sha256=sha(target), proof_lines=len(proof))
        result.update(seconds=time.monotonic() - began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        require(result['reported_conflict_budget_respected'] and result['seconds'] < 30, 'Native query exceeded existing cap')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
