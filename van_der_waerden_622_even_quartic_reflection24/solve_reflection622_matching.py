"""One bounded matching SAT query; only a directly checked witness proves anything."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps'))
from pysat.solvers import Solver


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    directory = args.model_dir
    output = directory / 'solver.json'
    require(not output.exists(), 'Do not repeat an existing query')
    metadata = json.loads((directory / 'metadata.json').read_text())
    require(metadata['status'] == 'MATCHING_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK', 'Model not ready')
    cnf_path, hg_path = Path(metadata['CNF']), Path(metadata['hypergraph'])
    require(sha(cnf_path) == metadata['CNF_sha256'] and sha(hg_path) == metadata['hypergraph_sha256'], 'Model changed')
    hypergraph = json.loads(hg_path.read_text())
    lines = cnf_path.read_text().splitlines()
    require(lines[0] == f"p cnf {metadata['variables']} {metadata['clauses']}", 'CNF header')
    clauses = []
    for line in lines[1:]:
        ints = list(map(int, line.split()))
        require(ints[-1] == 0 and all(0 < abs(x) <= metadata['variables'] for x in ints[:-1]), 'CNF row')
        clauses.append(ints[:-1])
    require(len(clauses) == metadata['clauses'], 'Complete CNF rows')
    preflight = 2 * len(clauses) + 7 * len(hypergraph['edges']) + 10000 + 200
    result = {'agent': 'six-vdw-1', 'role': 'researcher',
              'checked_at': datetime.now(timezone.utc).isoformat(), 'index': hypergraph['index'],
              'metadata_sha256': sha(directory / 'metadata.json'),
              'CNF_sha256': metadata['CNF_sha256'], 'hypergraph_sha256': metadata['hypergraph_sha256'],
              'solver': 'CaDiCaL1.9.5 via python-sat', 'python_sat': importlib.metadata.version('python-sat'),
              'variables': metadata['variables'], 'clauses': len(clauses),
              'target_matching_size': 12, 'conservative_preflight_cases': preflight,
              'conflict_cap_requested': 9500, 'reported_conflict_cap': 10000,
              'source_sha256': sha(Path(__file__)), 'threads': 1, 'proof_checked': False,
              'mathematical_exclusion': False, 'new_W_bound': None}
    if preflight > 200000:
        result.update(status='MATCHING_SOLVER_PREFLIGHT_OVER_CAP_PAUSED_NO_EXCLUSION',
                      seconds_total=time.monotonic() - began)
        output.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result), flush=True)
        return
    solver_began = time.monotonic()
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        solver.conf_budget(9500)
        answer = solver.solve_limited()
        stats = solver.accum_stats()
        assignment = solver.get_model() if answer is True else None
    result.update(status='SAT_MATCHING_PENDING_ACTUAL_TERM_CHECK' if answer is True else
                         'UNSAT_NOT_INDEPENDENTLY_PROVED_NO_EXCLUSION' if answer is False else
                         'UNKNOWN_MATCHING_QUERY_PAUSED_NO_EXCLUSION',
                  stats=stats, solver_seconds=time.monotonic() - solver_began,
                  seconds_total=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  reported_conflict_budget_respected=int(stats.get('conflicts', 0)) <= 10000)
    if assignment is not None:
        values = {abs(lit): lit > 0 for lit in assignment}
        require(all(any(values[abs(lit)] == (lit > 0) for lit in row) for row in clauses), 'Invalid solver model')
        ids = [i for i in range(1, len(hypergraph['edges']) + 1) if values[i]]
        require(len(ids) >= 12, 'Decoded matching below target')
        chosen = ids[:12]
        used = set()
        for i in chosen:
            support = set(hypergraph['edges'][i - 1]['orbits'])
            require(len(support) == 7 and not support.intersection(used), 'Decoded orbit matching invalid')
            used.update(support)
        witness = {'modulus': 311, 'pairs_per_case': 12,
                   'cases': [{'index': hypergraph['index'], 'coefficients': hypergraph['coefficients'],
                              'pairs': [hypergraph['edges'][i - 1]['pair'] for i in chosen]}]}
        witness_path = directory / 'witness.json'
        assignment_path = directory / 'assignment.json'
        require(not witness_path.exists() and not assignment_path.exists(), 'Existing witness/assignment')
        witness_path.write_text(json.dumps(witness, separators=(',', ':')) + '\n')
        assignment_path.write_text(json.dumps(assignment, separators=(',', ':')) + '\n')
        result.update(witness=str(witness_path.resolve()), witness_sha256=sha(witness_path),
                      assignment=str(assignment_path.resolve()), assignment_sha256=sha(assignment_path),
                      selected_edge_ids=chosen, total_selected_edges=len(ids))
    require(result['seconds_total'] < 30 and result['reported_conflict_budget_respected'], 'Matching child resource guard')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
