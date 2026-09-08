"""Optional deterministic discovery pass; final verification trusts no search."""
import argparse
import json
from pathlib import Path
from pysat.solvers import Cadical195
import geometry as G


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    G.require(not args.output.resolve().is_relative_to(G.REPO.resolve()), 'search output must be outside repository')
    points, triangles, pins = G.half_layer()
    n = len(points)
    edges = G.edges(points)
    solver = Cadical195(bootstrap_with=G.cnf(n, edges, [], pins))
    selectors = [4*n+k+1 for k in range(len(triangles))]
    for k, t in enumerate(triangles):
        for c in range(4):
            solver.add_clause([-(4*v+c+1) for v in t] + [-selectors[k]])
    solver.conf_budget(100000)
    G.require(solver.solve_limited(assumptions=selectors) is False, 'initial forcing gate unresolved')
    core = sorted(v-4*n-1 for v in solver.get_core())
    spent = queries = 0
    words = {}
    for k in reversed(core.copy()):
        if k not in core:
            continue
        G.require(spent < 1000000, 'bounded pass exhausted')
        trial = [v for v in core if v != k]
        before = solver.accum_stats()['conflicts']
        solver.conf_budget(min(20000, 1000000-spent))
        answer = solver.solve_limited(assumptions=[selectors[v] for v in trial])
        spent += solver.accum_stats()['conflicts'] - before
        queries += 1
        G.require(answer is not None, 'query unresolved at its cap')
        if answer is False:
            core = sorted(v-4*n-1 for v in solver.get_core())
        else:
            model = {v for v in solver.get_model() if v > 0}
            words[k] = ''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(n))
    cert = {'mask': 1682, 'vertices': n, 'edges': len(edges), 'available_triangles': len(triangles),
            'pins': pins, 'selected_triangles': [list(triangles[k]) for k in core],
            'deletion_colourings': [words[k] for k in core]}
    G.require(cert == G.read(G.ROOT / 'certificate.json'), 'discovery certificate differs')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2) + '\n')
    print(json.dumps({'queries': queries, 'deletion_conflicts': spent, 'retained_triangles': len(core),
                      'certificate_reproduced': True}, sort_keys=True))


if __name__ == '__main__':
    main()
