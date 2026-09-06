#!/usr/bin/env python3
"""Projected colouring CNF for a fixed boundary-retaining H514 vertex set.

Four Boolean colour indicators per OLD vertex, twelve availability variables,
and no colour indicators for the four new vertices. No SAT call is made.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEIGHBOURS = [[361,417,495,503,509], [418,498,506,508],
              [359,362,502], [358,416,507]]
BOUNDARY = {0} | {v for row in NEIGHBOURS for v in row}


def build(edges, omitted, certificate):
    omitted = set(omitted)
    if not omitted <= set(range(514)) or omitted & BOUNDARY:
        raise ValueError('Requires an H514 vertex set retaining the certified boundary')
    selected = set(range(510)) - omitted
    clauses = [[4*v+c+1 for c in range(4)] for v in sorted(selected)]
    clauses += [[-4*u-c-1, -4*v-c-1] for u,v in edges
                if u in selected and v in selected for c in range(4)]
    clauses.append([1])
    for i, neighbours in enumerate(NEIGHBOURS):
        for c in range(3):
            a = 2041 + 3*i+c
            xs = [4*v+(c+1)+1 for v in neighbours]
            clauses.extend([[-a,-x] for x in xs])
            clauses.append([a]+xs)
    for row in certificate['obstructions']:
        clause = row['clause']
        # An omitted path vertex makes its negative selection literal true.
        if any(510+(-x-1) in omitted for x in clause if x < 0):
            continue
        clauses.append([2041+(x-5) for x in clause if x > 0])
    return 2052, clauses


def dimacs(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n' + ''.join(
        ' '.join(map(str, row))+' 0\n' for row in clauses)).encode('ascii')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--omitted', required=True, help='Comma-separated H514 indices')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('geometry_checker', HERE/'verify.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    edges, _, _ = m.geometry()
    certificate = json.loads((HERE/'certificate.json').read_text())
    n, clauses = build(edges, [int(x) for x in args.omitted.split(',') if x], certificate)
    raw = dimacs(n, clauses); args.out.write_bytes(raw)
    print(json.dumps(dict(variables=n, clauses=len(clauses), bytes=len(raw), sha256=sha256(raw).hexdigest(), solver_called=False)))
