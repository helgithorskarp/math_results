"""Optional witness discovery with python-sat; outputs require check.py validation.

The proof does not require this script or a SAT solver. Different solver
versions and deletion orders can produce different valid witness sets.
"""
import argparse
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import random

from pysat.solvers import Solver


def discover(vertices, seed, budget):
    vertices = sorted(set(vertices))
    index = {v: i for i, v in enumerate(vertices)}
    m = len(vertices)
    def var(v, colour): return 3*index[v]+colour+1
    def selector(v): return 3*m+index[v]+1
    clauses = []
    for v in vertices:
        clauses.append([-selector(v)] + [var(v,c) for c in range(3)])
        for a, b in combinations(range(3), 2):
            clauses.append([-selector(v), -var(v,a), -var(v,b)])
    for x, y in combinations_with_replacement(vertices, 2):
        if x+y not in index:
            continue
        edge = sorted({x,y,x+y})
        for c in range(3):
            clauses.append([-selector(v) for v in edge] + [-var(v,c) for v in edge])
    # Global colour permutation if active; otherwise this variable is irrelevant.
    clauses.append([var(vertices[-1],0)])
    reverse = {selector(v): v for v in vertices}
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        def test(active, limit):
            solver.conf_budget(limit)
            return solver.solve_limited(assumptions=[selector(v) for v in sorted(active)])
        if test(vertices, 1000000) is not False:
            raise RuntimeError('initial instance not proved UNSAT by the discovery solver')
        active = {reverse[s] for s in solver.get_core()}
        order = sorted(active)
        random.Random(seed).shuffle(order)
        for v in order:
            if v in active and test(active-{v}, budget) is False:
                active = {reverse[s] for s in solver.get_core()}
    return sorted(active)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('palette', nargs=3, type=int)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--budget', type=int, default=3000)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    fixtures = json.loads((directory/'fixtures.json').read_text())
    colours = [0]+list(map(int, fixtures[args.input]['colours']))
    palette = sorted(args.palette)
    if len(set(palette)) != 3 or not set(palette) <= set(range(1,7)):
        raise ValueError('palette must have three distinct colours from 1,...,6')
    vertices = [v for v in range(1,len(colours)) if colours[v] in palette]
    if args.input == 'baseline':
        vertices.append(537)
    witness = discover(vertices, args.seed, args.budget)
    row = {'input': args.input, 'palette': palette, 'vertices': witness,
           'root': witness[-1]}
    Path(args.output).write_text(json.dumps(row, indent=2)+'\n')
    print('UNVERIFIED candidate: {} vertices; run exact verification'.format(len(witness)))


if __name__ == '__main__':
    main()
