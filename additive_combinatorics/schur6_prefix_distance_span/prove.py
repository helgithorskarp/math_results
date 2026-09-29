"""Regenerate and independently check the 83-point UNSAT certificate.

Large generated files stay in the explicit output directory, outside the
published source. The solver's return value alone never certifies the bound.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from pysat.solvers import Solver
from encode import clauses, dimacs


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--drat-trim', required=True)
    p.add_argument('--out-dir', required=True)
    args = p.parse_args()
    here = Path(__file__).resolve().parent
    data = json.loads((here/'data.json').read_text())
    prefix = list(map(int, data['prefix']))
    k, length = data['palette_size'], data['upper_length']
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cnf, proof = out/'span83.cnf', out/'span83.drup'
    cnf.write_text(dimacs(prefix, length, k))
    semantic = subprocess.run([sys.executable, '-B', str(here/'audit.py'), '--cnf', str(cnf)],
                              capture_output=True, text=True, check=True)
    audit = json.loads(semantic.stdout)
    start = time.monotonic()
    with Solver(name='glucose3', bootstrap_with=clauses(prefix, length, k), with_proof=True) as solver:
        assert solver.solve() is False
        proof.write_text('\n'.join(solver.get_proof())+'\n')
        statistics = solver.accum_stats()
    generated_seconds = time.monotonic()-start
    start = time.monotonic()
    checked = subprocess.run([args.drat_trim, str(cnf), str(proof)],
                             capture_output=True, text=True, check=True)
    (out/'drat-trim.log').write_text(checked.stdout+checked.stderr)
    if 's VERIFIED' not in checked.stdout:
        raise RuntimeError('proof checker did not certify UNSAT')
    result = {'upper_length': length, 'SAT_witness_length': data['span'],
              'literal_audit': audit, 'solver_statistics': statistics,
              'proof_bytes': proof.stat().st_size,
              'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
              'proof_checker': 'drat-trim', 'proof_checked': True,
              'generate_seconds': generated_seconds, 'check_seconds': time.monotonic()-start}
    (out/'verified.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
