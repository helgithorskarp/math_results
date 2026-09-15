#!/usr/bin/env python3
"""Check both negative obligations, regenerating proofs unless supplied.

Supply the full generated witness table. Geometry and all positive words are
rechecked before either UNSAT check. Output directories must be outside Git.
"""
import argparse
import json
from pathlib import Path
import subprocess
import time
from geometry import require
from verify import verify, digest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--relation', required=True, type=Path)
    ap.add_argument('--cadical', required=True, type=Path)
    ap.add_argument('--drat-trim', required=True, type=Path)
    ap.add_argument('--solver-seconds', type=int, default=900)
    ap.add_argument('--checker-seconds', type=int, default=600)
    ap.add_argument('--completeness-proof', type=Path)
    ap.add_argument('--parent-proof', type=Path)
    a = ap.parse_args()
    require(min(a.solver_seconds, a.checker_seconds) > 0, 'positive limits')
    verify(a.out, a.relation)
    results = []
    for name in ('completeness', 'parent'):
        start = time.monotonic()
        instance = a.out / (name + '.cnf')
        supplied = getattr(a, name + '_proof')
        proof = supplied or (a.out / (name + '.drat'))
        solve = None
        solver_exit = None
        if supplied is None:
            solve = [str(a.cadical.resolve()), '-t', str(a.solver_seconds),
                     str(instance), str(proof)]
            with (a.out / (name + '.solver.log')).open('w') as log:
                r = subprocess.run(solve, stdout=log, stderr=subprocess.STDOUT,
                                   timeout=a.solver_seconds + 20)
            solver_exit = r.returncode
            require(solver_exit == 20, 'UNSAT required; UNKNOWN is not a proof')
        check = [str(a.drat_trim.resolve()), str(instance), str(proof),
                 '-t', str(a.checker_seconds)]
        logfile = a.out / (name + '.checker.log')
        with logfile.open('w') as log:
            c = subprocess.run(check, stdout=log, stderr=subprocess.STDOUT,
                               timeout=a.checker_seconds + 20)
        require(c.returncode == 0 and 's VERIFIED' in logfile.read_text(),
                'independent DRAT proof check')
        results.append(dict(name=name, cnf_sha256=digest(instance),
                            cnf_bytes=instance.stat().st_size,
                            drat_sha256=digest(proof), drat_bytes=proof.stat().st_size,
                            supplied_proof=supplied is not None, solver_exit=solver_exit,
                            checker_exit=c.returncode, verified=True,
                            seconds=time.monotonic()-start,
                            solver_command=solve, checker_command=check,
                            solver_binary_sha256=digest(a.cadical),
                            checker_binary_sha256=digest(a.drat_trim)))
        (a.out / 'checked_proofs.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(results[-1]), flush=True)


if __name__ == '__main__':
    main()
