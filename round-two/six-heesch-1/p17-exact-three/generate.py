"""Optional bounded Glucose4 regeneration; no solver verdict is a certificate."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from build import (HERE, ROOT, Tile, require, third_formula, compile_subset,
                   RupChecker, dimacs)


def proof(cnf, nv):
    from pysat.solvers import Glucose4
    with Glucose4(bootstrap_with=cnf, with_proof=True) as solver:
        solver.conf_budget(200000)
        status = solver.solve_limited()
        require(status is False, 'SAT or UNKNOWN: no negative certificate')
        lines = [p for p in solver.get_proof() if not p.startswith('d ')]
    trace = '\n'.join(lines)+'\n' if lines else '0\n'
    require(len(trace.encode()) <= 250000, 'retained proof guard: incomplete')
    trimmed = RupChecker(cnf, nv).verify(trace, capture=True)['trimmed']
    require(len(trimmed.encode()) <= 100000, 'compact proof guard: incomplete')
    RupChecker(cnf, nv).verify(trimmed)
    return trimmed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dependency-root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path, default=HERE)
    args = parser.parse_args()
    start = time.monotonic()
    data = json.loads((HERE/'input.json').read_text())
    tile = Tile(data['cells'])
    pairs = json.loads((args.dependency_root/
             'heesch_polyomino_corner_obstruction/pairs.json').read_text())
    fixed, pool, cnf, nv, metadata = third_formula(tile, data, pairs, args.dependency_root)
    third_trace = proof(cnf, nv)
    mp, mc, mn = compile_subset(tile, list(map(tuple, data['forbidden_three_copy_support'])),
                                 2, data['half_grid_target'])
    require(len(mp) <= 2000 and len(mc) <= 250000, 'motif formula guard: incomplete')
    motif_trace = proof(mc, mn)
    cert = {'third': {'metadata': metadata,
                     'cnf_sha256': hashlib.sha256(dimacs(cnf, nv)).hexdigest(),
                     'proof_sha256': hashlib.sha256(third_trace.encode()).hexdigest()},
            'motif': {'candidates': len(mp), 'clauses': len(mc), 'variables': mn,
                     'cnf_sha256': hashlib.sha256(dimacs(mc, mn)).hexdigest(),
                     'proof_sha256': hashlib.sha256(motif_trace.encode()).hexdigest()}}
    args.output_dir.mkdir(exist_ok=True, parents=True)
    (args.output_dir/'third-cover.rup').write_text(third_trace)
    (args.output_dir/'three-copy.rup').write_text(motif_trace)
    (args.output_dir/'certificate.json').write_text(json.dumps(cert, indent=2)+'\n')
    print(dict(third_proof_bytes=len(third_trace.encode()),
               motif_proof_bytes=len(motif_trace.encode()), seconds=time.monotonic()-start,
               maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
