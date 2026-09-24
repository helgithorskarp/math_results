"""Regenerate one CNF and require a separately checked DRAT proof.

Generated CNFs, traces, and logs belong in a scratch directory, not Git.
A SAT/UNKNOWN result or failed checker always exits unsuccessfully.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import time

from pysat.solvers import Solver
from generate_cnf import CASES, case_formula


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1048576), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('work', type=Path)
    parser.add_argument('--drat-trim', type=Path, required=True)
    parser.add_argument('--conflicts', type=int, default=2000000)
    args = parser.parse_args()
    if args.conflicts <= 0:
        parser.error('--conflicts must be positive')
    args.work.mkdir(parents=True, exist_ok=True)
    cnf_path = args.work / (args.case + '.cnf')
    trace_path = args.work / (args.case + '.drat')
    check_path = args.work / (args.case + '.check.log')
    receipt_path = args.work / (args.case + '.receipt.json')
    receipt_path.unlink(missing_ok=True)
    cnf, pool = case_formula(args.case)
    cnf.to_file(str(cnf_path))
    started = time.monotonic()
    with Solver(name='cadical195', bootstrap_with=cnf.clauses,
                with_proof=True) as solver:
        solver.conf_budget(args.conflicts)
        result = solver.solve_limited()
        if result is not False:
            raise RuntimeError(f'No UNSAT certificate: solver returned {result!r}')
        # PySAT 1.9.dev15 does not flush CaDiCaL's C FILE buffer before
        # reading its temporary proof file. Python file.flush() is not enough.
        libc = ctypes.CDLL(None)
        libc.fflush.argtypes = [ctypes.c_void_p]
        libc.fflush.restype = ctypes.c_int
        if libc.fflush(None) != 0:
            raise OSError('C proof-buffer flush failed')
        proof = solver.get_proof()
        if not proof:
            raise RuntimeError('Empty proof export')
        trace_path.write_text('\n'.join(proof) + '\n')
        stats = solver.accum_stats()
    solve_seconds = time.monotonic() - started
    checked = time.monotonic()
    with check_path.open('w') as log:
        run = subprocess.run([str(args.drat_trim.resolve()), str(cnf_path),
                              str(trace_path)], stdout=log,
                             stderr=subprocess.STDOUT, check=False)
    if run.returncode != 0 or 's VERIFIED' not in check_path.read_text():
        raise RuntimeError(f'Independent DRAT check failed; see {check_path}')
    receipt = {
        'case': args.case, 'status': 'UNSAT', 'proof_verified': True,
        'variables': pool.top, 'clauses': len(cnf.clauses),
        'cnf_sha256': sha256(cnf_path), 'drat_sha256': sha256(trace_path),
        'drat_bytes': trace_path.stat().st_size,
        'conflict_budget': args.conflicts, 'solver_stats': stats,
        'solve_seconds': solve_seconds,
        'check_seconds': time.monotonic() - checked,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
