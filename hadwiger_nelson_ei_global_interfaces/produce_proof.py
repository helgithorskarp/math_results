"""Regenerate the omitted proof files; the solver and trimmer are untrusted."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from pysat.solvers import Cadical195
import geometry as G
import lrat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--drat-trim', required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    G.require(not output.is_relative_to(G.REPO.resolve()), 'proof output must be outside the repository')
    output.mkdir(parents=True, exist_ok=True)
    points, _, pins = G.half_layer()
    cert = G.read(G.ROOT / 'certificate.json')
    clauses = G.cnf(len(points), G.edges(points), cert['selected_triangles'], pins)
    (output / 'half.cnf').write_text(G.dimacs(len(points), clauses))
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        G.require(solver.solve() is False, 'the forcing formula is not UNSAT')
        proof = solver.get_proof()
        stats = solver.accum_stats()
    (output / 'half.drat').write_text('\n'.join(proof) + '\n')
    result = subprocess.run([args.drat_trim, str(output/'half.cnf'), str(output/'half.drat'),
                             '-L', str(output/'half.lrat')], capture_output=True, text=True, check=True)
    (output / 'drat_trim.txt').write_text(result.stdout + result.stderr)
    verified = lrat.verify(clauses, 4*len(points), output / 'half.lrat')
    manifest = G.read(G.ROOT / 'proof_manifest.json')
    files = {name: {'sha256': hashlib.sha256((output/name).read_bytes()).hexdigest(),
                    'bytes': (output/name).stat().st_size} for name in manifest['files']}
    G.require(files == manifest['files'], 'pinned proof bytes differ; check versions and independently verify')
    print(json.dumps({'verified': verified, 'solver_stats': stats, 'files': files}, sort_keys=True))


if __name__ == '__main__':
    main()
