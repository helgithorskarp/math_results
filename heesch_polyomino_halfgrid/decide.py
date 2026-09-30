"""Complete unrestricted first-Hh-corona decision via a doubled-grid cover.

UNSAT is an exclusion only after the native proof passes a separate checker.
Generated CNFs, traces, witnesses and logs belong in private workspace scratch.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

from halfgrid import decode_cover, double_cells, encode_poses, load_dependencies


def decision(tile, prior, motion_directory, work, checker=None, conflicts=10000):
    if type(conflicts) is not int or conflicts < 1:
        raise ValueError('positive conflict budget required')
    cover, motion = load_dependencies(prior, motion_directory)
    from pysat.solvers import Solver
    from pysat import __version__
    work = Path(work).resolve()
    if work.is_relative_to(Path(__file__).resolve().parent):
        raise ValueError('large generated output must be outside the source directory')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    enlarged = double_cells(tile)
    circuit, candidates, statistics = cover.build_cover(enlarged, 1)
    formula = work/'case.cnf'
    trace = work/'case.drat'
    circuit.write_dimacs(formula)
    statistics.update({'agent': 'six-heesch-1', 'role': 'researcher',
                       'original_cells': len(enlarged)//4,
                       'doubled_cells': len(enlarged),
                       'cnf_sha256': hashlib.sha256(formula.read_bytes()).hexdigest(),
                       'python_sat': __version__, 'solver': 'glucose4',
                       'conflict_budget': conflicts,
                       'build_seconds': round(time.monotonic()-start, 3)})
    with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=True) as solver:
        solver.conf_budget(conflicts)
        start = time.monotonic()
        sat = solver.solve_limited()
        statistics['solve_seconds'] = round(time.monotonic()-start, 3)
        statistics['solver_statistics'] = solver.accum_stats()
        if sat is None:
            statistics['result'] = 'UNKNOWN; no exclusion'
        elif sat:
            selected = {x for x in solver.get_model() if x > 0}
            patch = [enlarged] + [q['cells'] for q in candidates if q['variable'] in selected]
            cover.check_cover(enlarged, 1, patch)
            poses, prefixes = decode_cover(tile, patch, motion)
            certificate = {'cells': motion.normalize(tile), 'depth': 1,
                           'last_prefix_relaxed': True, 'placements': encode_poses(poses)}
            witness = work/'witness.json'
            witness.write_text(json.dumps(certificate, indent=2, sort_keys=True)+'\n')
            statistics.update({'result': 'SAT; first relaxed corona directly checked',
                               'copies': len(poses), 'prefixes': prefixes,
                               'fractional_copies': sum(bool(p.tx % 1 or p.ty % 1) for p in poses),
                               'witness_sha256': hashlib.sha256(witness.read_bytes()).hexdigest()})
        else:
            lines = solver.get_proof() or ['0']
            trace.write_text('\n'.join(lines)+'\n')
            statistics.update({'result': 'UNSAT; proof not yet checked',
                               'proof_bytes': trace.stat().st_size,
                               'proof_sha256': hashlib.sha256(trace.read_bytes()).hexdigest()})
    # The native solver is closed before a checker process starts.
    if sat is False and checker is not None:
        start = time.monotonic()
        command = [str(Path(checker).resolve()), str(formula), str(trace)]
        env = os.environ.copy()
        for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[name] = '1'
        run = subprocess.run(command, capture_output=True, text=True, timeout=30, env=env)
        log = run.stdout.replace('\r', '\n')
        (work/'checker.log').write_text(log+run.stderr)
        if run.returncode not in (0, 1) or 's VERIFIED' not in log.splitlines():
            raise RuntimeError('negative certificate not verified: '+log[-1500:]+run.stderr[-500:])
        statistics.update({'result': 'UNSAT VERIFIED; unrestricted Hc=Hh=0',
                           'checker': 'DRAT-trim',
                           'check_seconds': round(time.monotonic()-start, 3)})
    statistics['peak_self_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (work/'result.json').write_text(json.dumps(statistics, sort_keys=True, indent=2)+'\n')
    return statistics


def main():
    p = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent.parent
    p.add_argument('tile', type=Path, help='JSON with an explicit cells list')
    p.add_argument('--prior-dir', type=Path, default=root/'heesch_polyomino_euler_cnf')
    p.add_argument('--motion-dir', type=Path, default=root/'heesch_polyomino_motion_bridge')
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--checker', type=Path)
    p.add_argument('--conflicts', type=int, default=10000)
    args = p.parse_args()
    result = decision(json.loads(args.tile.read_text())['cells'], args.prior_dir,
                      args.motion_dir, args.output_dir, args.checker, args.conflicts)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
