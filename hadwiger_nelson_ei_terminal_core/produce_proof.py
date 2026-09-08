"""Regenerate the unit-only terminal refutation outside the repository."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from pysat.solvers import Glucose3
import geometry as G
from verify import proof_checker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--drat-trim', required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    G.require(not output.is_relative_to(G.ROOT.parent.resolve()), 'proof output must be outside repository')
    output.mkdir(parents=True, exist_ok=True)
    rows = G.rows()
    pins = G.read('certificate.json')['pins']
    clauses = G.cnf(len(rows), G.half_edges(rows), pins)
    (output/'reduced.cnf').write_text(G.dimacs(len(rows), clauses))
    with Glucose3(bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(200000)
        G.require(solver.solve_limited() is False, 'proof generation unresolved')
        raw = '\n'.join(solver.get_proof())+'\n'
        stats = solver.accum_stats()
    (output/'reduced.drat').write_text(raw)
    run = subprocess.run([args.drat_trim, str(output/'reduced.cnf'), str(output/'reduced.drat'),
                          '-L', str(output/'reduced.lrat')], capture_output=True, text=True, check=True)
    (output/'drat_trim.txt').write_text(run.stdout+run.stderr)
    proof = proof_checker().verify(clauses, 4*len(rows), output/'reduced.lrat')
    files = {name: {'sha256': hashlib.sha256((output/name).read_bytes()).hexdigest(),
                    'bytes': (output/name).stat().st_size} for name in G.read('proof_manifest.json')['files']}
    G.require(files == G.read('proof_manifest.json')['files'], 'pinned proof bytes differ')
    print(json.dumps({'verified': proof, 'solver_stats': stats, 'files': files}, sort_keys=True))


if __name__ == '__main__':
    main()
