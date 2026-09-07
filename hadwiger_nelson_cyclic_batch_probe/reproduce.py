#!/usr/bin/env python3
"""Rebuild a cyclic-augmentation candidate; optionally regenerate both certificates."""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SEED = HERE.parent / 'hadwiger_nelson_neutral_mutation_candidate'
sys.path.insert(0, str(SEED))
import geometry as g
import verify as seed_check


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def construct(spec):
    data = (SEED / 'certificate.json').read_bytes()
    require(sha(data) == spec['seed_certificate_sha256'], 'seed certificate hash')
    cert = json.loads(data)
    _, rows, _ = seed_check.construct(cert, seed_check.load_inputs(cert))
    seed = [(tuple(Fraction(a, 96) for a in row[:8]),
             tuple(Fraction(a, 96) for a in row[8:])) for row in rows]
    deleted = spec['delete_seed_vertices']
    require(len(set(deleted)) == len(deleted) == 6 and all(v in range(509) for v in deleted),
            'invalid seed deletions')
    points = [p for v, p in enumerate(seed) if v not in deleted]
    require(len(spec['circle_templates']) == 40, 'wrong insertion count')
    for a, b, branch in spec['circle_templates']:
        require(a in range(509) and b in range(509) and a < b, 'invalid circle centres')
        roots = g.intersections(seed[a], seed[b])
        require(type(branch) is int and 0 <= branch < len(roots), 'invalid intersection branch')
        points.append(roots[branch])
    require(len(points) == len(set(points)) == 543, 'coincident candidate vertices')
    scale = lcm(*(c.denominator for p in points for axis in p for c in axis))
    rows = [tuple(int(scale * c) for axis in p for c in axis) for p in points]
    require(scale == 288 and sha(json.dumps(rows, separators=(',', ':')).encode()) ==
            spec['coordinate_sha256'], 'candidate coordinate mismatch')
    return rows, scale


def strict_edges(rows, scale):
    edges = []
    for i, j in combinations(range(len(rows)), 2):
        d = [a - b for a, b in zip(rows[i], rows[j])]
        norm = [a + b for a, b in zip(seed_check.square(d[:8]), seed_check.square(d[8:]))]
        if norm == [scale * scale] + [0] * 7:
            edges.append((i, j))
    return edges


def cnf(n, edges):
    clauses = []
    for v in range(n):
        clauses.append([4 * v + c + 1 for c in range(4)])
        clauses.extend([-(4 * v + a + 1), -(4 * v + b + 1)]
                       for a, b in combinations(range(4), 2))
    neighbours = [set() for _ in range(n)]
    for a, b in edges:
        clauses.extend([-(4 * a + c + 1), -(4 * b + c + 1)] for c in range(4))
        neighbours[a].add(b)
        neighbours[b].add(a)
    triangle = next((a, b, c) for a, b in edges
                    for c in sorted(neighbours[a] & neighbours[b]) if b < c)
    clauses.extend([[4 * v + c + 1] for c, v in enumerate(triangle)])
    data = (f'p cnf {4*n} {len(clauses)}\n' +
            ''.join(' '.join(map(str, row)) + ' 0\n' for row in clauses)).encode()
    return data, triangle


def check_deletions(data, n, edges):
    row_bytes = (n - 1 + 3) // 4
    require(len(data) == n * row_bytes, 'incomplete deletion certificate')
    for d in range(n):
        row = data[d * row_bytes:(d + 1) * row_bytes]
        values = [(b >> shift) & 3 for b in row for shift in (0, 2, 4, 6)]
        require(all(c == 0 for c in values[n-1:]), 'nonzero padding')
        word = values[:d] + [-1] + values[d:n-1]
        require(all(word[a] != word[b] for a, b in edges if d not in (a, b)),
                'monochromatic edge in deletion certificate')
    return n


def generate_deletions(n, edges, triangle, budget):
    from pysat.solvers import Cadical195
    packed = bytearray()
    with Cadical195() as solver:
        for v in range(n):
            solver.add_clause([4 * v + c + 1 for c in range(4)])
            for a, b in combinations(range(4), 2):
                solver.add_clause([-(4 * v + a + 1), -(4 * v + b + 1)])
        for a, b in edges:
            for c in range(4):
                solver.add_clause([-(4*n+a+1), -(4*n+b+1),
                                   -(4*a+c+1), -(4*b+c+1)])
        # Retained pinned vertices form a clique, so a palette permutation
        # realizes the pins even when one of the three is absent.
        for c, v in enumerate(triangle):
            solver.add_clause([4*v+c+1])
        for d in range(n):
            solver.conf_budget(budget)
            result = solver.solve_limited(assumptions=[(4*n+v+1) * (-1 if v == d else 1)
                                                       for v in range(n)])
            require(result is True, f'deletion {d} unresolved or non-SAT; no criticality claim')
            model = set(solver.get_model())
            word = [next(c for c in range(4) if 4*v+c+1 in model) for v in range(n)]
            require(all(word[a] != word[b] for a, b in edges if d not in (a, b)), 'invalid SAT word')
            values = [c for v, c in enumerate(word) if v != d]
            values += [0] * (-len(values) % 4)
            packed.extend(sum(values[k+j] << (2*j) for j in range(4))
                          for k in range(0, len(values), 4))
    return bytes(packed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--proof', type=Path)
    parser.add_argument('--kissat')
    parser.add_argument('--drat-trim')
    parser.add_argument('--deletions', type=Path)
    parser.add_argument('--generate-deletions', action='store_true')
    parser.add_argument('--conflicts', type=int, default=2000000)
    args = parser.parse_args()
    require(not (args.proof and args.kissat), 'choose one proof source')
    require(bool(args.drat_trim) == bool(args.proof or args.kissat), 'proof/checker mismatch')
    require(not (args.deletions and args.generate_deletions), 'choose one deletion source')
    spec = json.loads((HERE / 'construction.json').read_text())
    rows, scale = construct(spec)
    n = len(rows)
    edges = strict_edges(rows, scale)
    require(len(edges) == 2587, 'edge count')
    five = list(map(int, spec['five_colouring']))
    require(len(five) == n and all(c in range(5) for c in five) and
            all(five[a] != five[b] for a, b in edges), 'invalid five-colouring')
    formula, triangle = cnf(n, edges)
    require(sha(formula) == spec['cnf_sha256'], 'CNF hash')
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'graph.json').write_text(json.dumps({'scale': scale, 'coordinates': rows,
        'edges': edges}, separators=(',', ':')) + '\n')
    formula_path = args.output / 'graph.cnf'
    formula_path.write_bytes(formula)
    result = {'vertices': n, 'edges': len(edges), 'scale': scale, 'pair_checks': n*(n-1)//2,
              'cnf_sha256': sha(formula), 'five_colouring_checked': True,
              'DRAT_verified': False, 'deletion_words_checked': 0}
    if args.proof or args.kissat:
        proof = args.proof or (args.output / 'graph.drat')
        if args.kissat:
            run = subprocess.run([args.kissat, '--quiet', str(formula_path), str(proof)],
                                 capture_output=True, text=True)
            (args.output / 'kissat.log').write_text(run.stdout + run.stderr)
            require(run.returncode == 20, 'UNSAT proof generation failed')
        run = subprocess.run([args.drat_trim, str(formula_path), str(proof)],
                             capture_output=True, text=True)
        (args.output / 'drat-trim.log').write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and 's VERIFIED' in run.stdout, 'proof verification failed')
        result.update(DRAT_verified=True, proof_sha256=sha(proof.read_bytes()))
    if args.generate_deletions or args.deletions:
        data = generate_deletions(n, edges, triangle, args.conflicts) if args.generate_deletions else args.deletions.read_bytes()
        result['deletion_words_checked'] = check_deletions(data, n, edges)
        result['deletion_words_sha256'] = sha(data)
        (args.output / 'deletion_words.bin').write_bytes(data)
    (args.output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
