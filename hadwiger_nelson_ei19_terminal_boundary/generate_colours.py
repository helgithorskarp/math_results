"""Optional discovery replay. SAT supplies positive witnesses only."""
from itertools import combinations
from pathlib import Path
import argparse
import json
from pysat.solvers import Solver

from verify import TERMINALS, INTERIOR, edges, patterns, verify_completions


def generate():
    es = set(edges())
    clauses = [[4*v+c+1 for c in range(4)] for v in range(19)]
    clauses += [[-4*v-c-1, -4*v-d-1] for v in range(19)
                for c, d in combinations(range(4), 2)]
    clauses += [[-4*a-c-1, -4*b-c-1] for a, b in sorted(es) for c in range(4)]
    rows = []
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        for pattern in patterns(es):
            assumptions = [4*v+c+1 for v, c in zip(TERMINALS, pattern)]
            if not solver.solve(assumptions=assumptions):
                raise RuntimeError('unexpected nonextendible terminal pattern')
            model = set(solver.get_model())
            word = []
            for v in range(19):
                colours = [c for c in range(4) if 4*v+c+1 in model]
                if len(colours) != 1:
                    raise RuntimeError('invalid one-hot model')
                word.append(colours[0])
            if (any(word[a] == word[b] for a, b in es)
                    or any(word[v] != c for v, c in zip(TERMINALS, pattern))):
                raise RuntimeError('decoded model violates the original problem')
            rows.append(''.join(str(word[v]) for v in INTERIOR))
    text = '\n'.join(rows) + '\n'
    print(json.dumps(verify_completions(text, es), indent=2))
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path, help='write outside the contribution')
    args = parser.parse_args()
    args.output.write_text(generate())
