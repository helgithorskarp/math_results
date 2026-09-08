"""Regenerate complete tail decisions and independently check every certificate."""
import argparse
import concurrent.futures
import ctypes
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time
import audit
import encode
import verify

def decide(job):
    from pysat.solvers import Solver
    i, line, expected, scratch, checker = job
    directory = Path(scratch) / f'canonical-{i:04d}'
    directory.mkdir()
    core = encode.decode(line)
    raw = encode.dimacs(core)
    audit.require(hashlib.sha256(raw).hexdigest() == expected['cnf_sha256'], 'Formula identity')
    (directory / 'tail.cnf').write_bytes(raw)
    clauses = encode.formula(core)
    t = time.monotonic()
    with Solver(name='cadical300', bootstrap_with=clauses, with_proof=True) as solver:
        status = solver.solve()
        audit.require(status is True or status is False, 'UNKNOWN is not a decision')
        record = {'index': i, 'core': line, 'status': 'SAT' if status else 'UNSAT_CHECKED',
                  'solver_seconds': time.monotonic() - t, 'cnf_sha256': expected['cnf_sha256']}
        if status:
            values = {abs(x): int(x > 0) for x in solver.get_model()}
            audit.require(set(range(1, 280)) <= set(values) and audit.holds(clauses, values), 'Invalid SAT assignment')
            word = ''.join(str(values[i]) for i in range(1, 137))
            audit.witness(line, word)
            record['free_edges'] = word
        else:
            # PySAT's C FILE needs flushing; its binary-to-text helper is not used.
            audit.require(ctypes.CDLL(None).fflush(None) == 0, 'C proof flush failed')
            solver.solver.prfile.seek(0)
            proof = solver.solver.prfile.read() + b'a\x00'
            # Appending the empty clause is sound only when the independent checker accepts it.
            path = directory / 'tail.drat.bin'
            path.write_bytes(proof)
            record['proof_file'] = path.name
            record['proof_sha256'] = hashlib.sha256(proof).hexdigest()
            record['checker_output_sha256'] = verify.check_proof(checker, directory / 'tail.cnf', path)
    audit.require(('SAT' if status else 'UNSAT') == expected['tail_status'], 'Decision differs from published table')
    (directory / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    return {'index': i, 'status': record['status'], 'solver_seconds': record['solver_seconds']}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--catalog', required=True)
    p.add_argument('--scratch', required=True)
    p.add_argument('--drat-trim', required=True)
    p.add_argument('--jobs', type=int, default=1)
    p.add_argument('--case', type=int)
    a = p.parse_args()
    audit.require(1 <= a.jobs <= 4, 'Use one through four worker processes')
    audit.require(importlib.metadata.version('python-sat') == '1.9.dev15', 'Expected python-sat 1.9.dev15')
    scratch = Path(a.scratch).resolve()
    scratch.mkdir(exist_ok=False)
    checker = Path(a.drat_trim).resolve()
    audit.require(checker.is_file(), 'Missing drat-trim executable')
    lines = encode.catalog(a.catalog)
    rows = json.loads((Path(__file__).resolve().parent / 'RESULTS.json').read_text())
    indices = list(range(640)) if a.case is None else [a.case]
    audit.require(all(0 <= i < 640 for i in indices), 'Case index')
    jobs = [(i, lines[i], rows[i], str(scratch), str(checker)) for i in indices]
    t = time.monotonic()
    if a.jobs == 1:
        results = [decide(job) for job in jobs]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=a.jobs) as pool:
            results = list(pool.map(decide, jobs))
    status = 'REPRODUCED_ALL_640_TAIL_DECISIONS' if len(results) == 640 else 'REPRODUCED_ONE_TAIL_CONTROL'
    report = {'status': status, 'cases': len(results), 'seconds': time.monotonic() - t,
              'sat': sum(r['status'] == 'SAT' for r in results), 'unsat': sum(r['status'] != 'SAT' for r in results),
              'python': sys.version, 'python_sat': importlib.metadata.version('python-sat'),
              'checker_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(), 'good43': False}
    (scratch / 'REPLAY.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))

if __name__ == '__main__':
    main()
