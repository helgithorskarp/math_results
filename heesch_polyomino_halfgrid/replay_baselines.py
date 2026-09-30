"""Fresh coarse-grid obstructions for the three explicit motion separations.

These certificates, together with the separately published finite-upper
bridge, exclude plane tiling even though first relaxed coronas exist.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

from halfgrid import load_dependencies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    parser.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    parser.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    parser.add_argument('--examples', type=Path, default=Path(__file__).parent/'fractional_examples.json')
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    if work.is_relative_to(Path(__file__).resolve().parent):
        raise ValueError('generated output must stay outside the public source directory')
    cover, _ = load_dependencies(args.prior_dir, args.motion_dir)
    from pysat.solvers import Solver
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    results = []
    for example in json.loads(args.examples.read_text())['cases']:
        destination = work/str(example['i'])
        destination.mkdir(parents=True, exist_ok=True)
        circuit, _, _ = cover.build_cover(example['cells'], 1)
        formula, trace = destination/'coarse.cnf', destination/'coarse.drat'
        circuit.write_dimacs(formula)
        cnf_hash = hashlib.sha256(formula.read_bytes()).hexdigest()
        if cnf_hash != example['coarse_grid_cnf_sha256']:
            raise RuntimeError('pinned coarse instance changed')
        with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
            solver.conf_budget(10000)
            decision = solver.solve_limited()
            if decision is not False:
                raise RuntimeError('coarse obstruction incomplete or contradicted; no negative claim')
            proof = solver.get_proof() or ['0']
        trace.write_text('\n'.join(proof)+'\n')
        run = subprocess.run([str(args.checker.resolve()), str(formula), str(trace)],
                             capture_output=True, text=True, timeout=30, env=env)
        log = run.stdout.replace('\r', '\n')
        (destination/'checker.log').write_text(log+run.stderr)
        if run.returncode not in (0, 1) or 's VERIFIED' not in log.splitlines():
            raise RuntimeError('coarse negative certificate not verified')
        results.append({'i': example['i'], 'coarse_cnf_sha256': cnf_hash,
                        'coarse_unsat_verified': True,
                        'proof_sha256': hashlib.sha256(trace.read_bytes()).hexdigest(),
                        'conditional_all_motion_upper': example['conditional_unrestricted_upper']})
    print(json.dumps({'agent': 'six-heesch-1', 'role': 'researcher', 'cases': results},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
