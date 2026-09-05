#!/usr/bin/env python3
"""Bounded discovery of the degree-exact mixed-clique realization.

The positive theorem is checked directly from GRAPH.json by verify.py;
no SAT verdict or cardinality encoding is trusted for that theorem.
"""
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time

HERE = Path(__file__).resolve().parent
TEMPLATE = {'core_order': 3, 'core_mask': 7,
            'cells': [[1,8],[2,8],[3,6],[4,10],[5,4],[6,4]]}
ENCODER_SHA = '436487456b86473d45c49091082b626a73e444c49a63812623348be266a062ed'


class CounterEncoder:
    """s[i,j] iff at least j of the first i literals are true."""
    def __init__(self, variables, clauses):
        self.variables = variables
        self.clauses = list(clauses)

    @staticmethod
    def neg(literal):
        return not literal if type(literal) is bool else -literal

    def add(self, *literals):
        if any(lit is True for lit in literals):
            return
        self.clauses.append(tuple(lit for lit in literals if lit is not False))

    def interval(self, literals, lower, upper):
        n = len(literals)
        lower, upper = max(lower, 0), min(upper, n)
        if lower > upper:
            self.add()
            return
        previous = [True]+[False]*(upper+1)
        for i, literal in enumerate(literals, 1):
            current = [True]
            for j in range(1, upper+2):
                if j > i:
                    current.append(False)
                    continue
                self.variables += 1
                s, a, b = self.variables, previous[j], previous[j-1]
                # s <=> a OR (literal AND b).
                self.add(self.neg(a), s)
                self.add(self.neg(literal), self.neg(b), s)
                self.add(-s, a, literal)
                self.add(-s, a, b)
                current.append(s)
            previous = current
        if lower:
            self.add(previous[lower])
        self.add(self.neg(previous[upper+1]))


def build(full_neighborhoods=False):
    path = HERE.parent/'ramsey_r55_m216_signature_obstruction/model.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != ENCODER_SHA:
        raise ValueError('inherited generic template encoder changed')
    spec = importlib.util.spec_from_file_location('template_encoder', path)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    edges, base = model.formula(TEMPLATE)
    E, C, fixed, _ = model.layout(TEMPLATE)
    index = {edge: i+1 for i, edge in enumerate(edges)}
    encoder = CounterEncoder(len(edges), base)
    if full_neighborhoods:
        extra = set()
        for five in combinations(C, 5):
            if any(all(fixed[u,v] for v in five) for u in E):
                extra.add(tuple(index[e] for e in combinations(five, 2)))
            if any(all(not fixed[u,v] for v in five) for u in E):
                extra.add(tuple(-index[e] for e in combinations(five, 2)))
        encoder.clauses.extend(sorted(extra, key=lambda c:(len(c),c)))
    for vertex in C:
        known = sum(fixed[u,vertex] for u in E)
        encoder.interval([index[e] for e in edges if vertex in e], 21-known, 21-known)
    for u in E:
        neighbors = [v for v in E+C if v != u and fixed[tuple(sorted((u,v)))]]
        free = [index[e] for e in combinations(neighbors, 2) if e in index]
        constant = sum(fixed[e] for e in combinations(neighbors, 2) if e in fixed)
        core_degree = sum(fixed[tuple(sorted((u,v)))] for v in E if v != u)
        encoder.interval(free, 94-core_degree-constant, 93-constant)
    return edges, fixed, encoder


def decode(logfile, edges, fixed):
    assignment = {}
    for line in logfile.read_text().splitlines():
        if line.startswith('v '):
            for text in line[2:].split():
                literal = int(text)
                if literal:
                    assignment[abs(literal)] = literal > 0
    if not set(range(1, len(edges)+1)) <= set(assignment):
        raise ValueError('incomplete primary assignment')
    colors = dict(fixed)
    colors.update({edge: assignment[i+1] for i, edge in enumerate(edges)})
    rows = [0]*43
    for (u,v), red in colors.items():
        if red:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return {'format': 'r55-triple-degree-exact-mixed-graph-v1',
            'red_adjacency_hex': [format(row, 'x') for row in rows]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path)
    parser.add_argument('--seconds', type=int, default=60)
    parser.add_argument('--graph-output', type=Path)
    parser.add_argument('--full-neighborhoods', action='store_true')
    parser.add_argument('--emit-only', action='store_true')
    args = parser.parse_args()
    if args.work.exists():
        raise ValueError('use a fresh work directory')
    if args.seconds <= 0:
        raise ValueError('positive solver bound required')
    args.work.mkdir(parents=True)
    started = time.monotonic()
    edges, fixed, encoder = build(args.full_neighborhoods)
    cnf = args.work/'case.cnf'
    cnf.write_text(f'p cnf {encoder.variables} {len(encoder.clauses)}\n' + ''.join(
        ' '.join(map(str, clause))+' 0\n' for clause in encoder.clauses))
    summary = {'full_neighborhoods': args.full_neighborhoods,
               'primary_variables': len(edges), 'variables': encoder.variables,
               'clauses': len(encoder.clauses),
               'formula_sha256': hashlib.sha256(cnf.read_bytes()).hexdigest(),
               'solver_limit_seconds': args.seconds, 'status': 'NOT_RUN'}
    print(json.dumps(summary, sort_keys=True), flush=True)
    if not args.emit_only:
        if args.kissat is None:
            raise ValueError('--kissat required for a solve')
        logfile = args.work/'solver.log'
        with logfile.open('w') as log:
            try:
                result = subprocess.run([str(args.kissat), f'--time={args.seconds}', str(cnf)],
                                        stdout=log, stderr=subprocess.STDOUT, timeout=args.seconds+30)
                summary['solver_exit'] = result.returncode
            except subprocess.TimeoutExpired:
                summary['solver_exit'] = None
        code = summary['solver_exit']
        summary['status'] = 'SAT_UNCHECKED' if code == 10 else 'UNSAT_UNCHECKED' if code == 20 else 'UNKNOWN'
        if code == 10:
            document = decode(logfile, edges, fixed)
            output = args.graph_output or args.work/'graph.json'
            output.write_text(json.dumps(document, indent=2)+'\n')
            summary['graph_sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
        summary['kissat_binary_sha256'] = hashlib.sha256(args.kissat.read_bytes()).hexdigest()
    summary['elapsed_seconds'] = round(time.monotonic()-started, 6)
    summary['largest_child_peak_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    (args.work/'result.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
