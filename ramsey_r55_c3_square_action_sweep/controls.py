#!/usr/bin/env python3
"""Definition-level small controls and malformed full-CNF rejection."""
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import subprocess
import tempfile
import model
import inspect_graph


def small(work):
    # First seven vertices are one fixed point and two quotient orbits.
    vertices = range(7)
    ids = model.edge_orbits(model.cases()[0])
    chosen = {e: ids[e] for e in combinations(vertices, 2)}
    names = {v: i+1 for i, v in enumerate(sorted(set(chosen.values())))}
    chosen = {e: names[v] for e, v in chosen.items()}
    clauses = model.ramsey_clauses(chosen, vertices)
    nv = len(names)
    checked = good = complement_normal = 0
    with tempfile.TemporaryDirectory(prefix='small-', dir=work) as directory:
        path = Path(directory) / 'control.edges'
        for values in product((False, True), repeat=nv):
            assignment = {i+1: x for i, x in enumerate(values)}
            encoded = all(any(assignment[abs(lit)] == (lit > 0) for lit in c) for c in clauses)
            edges = {e for e, v in chosen.items() if assignment[v]}
            literal = all(0 < sum(e in edges for e in combinations(five, 2)) < 10
                          for five in combinations(vertices, 5))
            model.require(encoded == literal, 'small formula semantics')
            path.write_text(f'7 {len(edges)}\n'+''.join(f'{a} {b}\n' for a, b in sorted(edges)))
            model.require(inspect_graph.inspect(path)['ramsey'] == literal, 'literal verifier mismatch')
            if literal:
                good += 1
                complement_normal += assignment[1]
            checked += 1
    model.require(checked == 128 and good > 0 and 2*complement_normal == good, 'positive/complement control')
    return {'assignments_checked': checked, 'variables': nv, 'ramsey_assignments': good,
            'normalized_ramsey_assignments': complement_normal}


def corruptions(work, cnf, checker):
    case = model.cases()[0]
    prefix = [str(checker.resolve()), *map(str, [case['a'], *case['b'], case['c']])]
    baseline = subprocess.run(prefix+[str(cnf.resolve())], capture_output=True, text=True)
    model.require(baseline.returncode == 0 and ' PASS' in baseline.stdout, 'positive full formula check')
    lines = cnf.read_text().splitlines()
    altered = list(lines)
    literal = altered[1].split()
    literal[0] = str(-int(literal[0]))
    altered[1] = ' '.join(literal)
    mutations = {'first_clause_polarity': altered, 'missing_last_clause': lines[:-1],
                 'wrong_header': ['p cnf 1 1']+lines[1:]}
    rejected = {}
    with tempfile.TemporaryDirectory(prefix='cnf-', dir=work) as directory:
        bad = Path(directory) / 'bad.cnf'
        for name, rows in mutations.items():
            bad.write_text('\n'.join(rows)+'\n')
            result = subprocess.run(prefix+[str(bad)], capture_output=True, text=True)
            model.require(result.returncode != 0, 'accepted malformed full formula')
            rejected[name] = result.stderr.strip()
    return rejected


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--cnf', required=True, type=Path)
    parser.add_argument('--checker', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    model.require(not args.work.resolve().is_relative_to(model.ROOT.parent), 'generated controls outside Git')
    args.work.mkdir(parents=True, exist_ok=True)
    report = {'small': small(args.work), 'rejected': corruptions(args.work, args.cnf, args.checker)}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))
