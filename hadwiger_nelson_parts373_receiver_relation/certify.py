#!/usr/bin/env python3
"""Generate and independently check DRAT proofs; write bulky outputs outside Git."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from verify import verify, digest
from receiver import require


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--cadical', required=True, type=Path)
    ap.add_argument('--drat-trim', required=True, type=Path)
    ap.add_argument('--seconds', type=int, default=180)
    a = ap.parse_args()
    require(a.seconds > 0, 'positive time limit')
    verify(a.out)
    results = []
    for name in ('completeness', 'parent'):
        start = time.monotonic()
        instance = a.out / (name + '.cnf')
        proof = a.out / (name + '.drat')
        solve = [str(a.cadical.resolve()), '-t', str(a.seconds), str(instance), str(proof)]
        check = [str(a.drat_trim.resolve()), str(instance), str(proof), '-t', str(a.seconds)]
        with (a.out / (name + '.solver.log')).open('w') as log:
            r = subprocess.run(solve, stdout=log, stderr=subprocess.STDOUT,
                               timeout=a.seconds + 10)
        require(r.returncode == 20, 'UNSAT required; UNKNOWN is not a certificate')
        with (a.out / (name + '.checker.log')).open('w') as log:
            c = subprocess.run(check, stdout=log, stderr=subprocess.STDOUT,
                               timeout=a.seconds + 10)
        require(c.returncode == 0 and
                's VERIFIED' in (a.out / (name + '.checker.log')).read_text(),
                'independent DRAT verification required')
        results.append({
            'name': name, 'cnf_sha256': digest(instance), 'cnf_bytes': instance.stat().st_size,
            'drat_sha256': digest(proof), 'drat_bytes': proof.stat().st_size,
            'solver_exit': r.returncode, 'checker_exit': c.returncode, 'verified': True,
            'seconds': time.monotonic() - start,
            'solver_command': solve, 'checker_command': check,
            'solver_binary_sha256': digest(a.cadical),
            'checker_binary_sha256': digest(a.drat_trim),
        })
        (a.out / 'checked_proofs.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(results[-1]), flush=True)


if __name__ == '__main__':
    main()
