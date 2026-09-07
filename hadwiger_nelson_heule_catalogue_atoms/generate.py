#!/usr/bin/env python3
"""Optional SAT discovery; only its positive models enter the final proof."""
import argparse
import json
import time
from pathlib import Path
from pysat.solvers import Solver
from native import build, require


def maximal_masks(weights, limit):
    orders = [0] * (1 << len(weights))
    maximal, admissible = [], 0
    for mask in range(len(orders)):
        if mask:
            low = mask & -mask
            orders[mask] = orders[mask ^ low] + weights[low.bit_length() - 1]
        if orders[mask] <= limit:
            admissible += 1
            if all(mask >> i & 1 or orders[mask] + w > limit for i, w in enumerate(weights)):
                maximal.append(mask)
    maximal.sort(key=lambda m: (-orders[m], m))
    return orders, maximal, admissible


class Oracle:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph['points'])
        self.k = len(graph['atoms'])
        self.av = {v: i for i, a in enumerate(graph['atoms']) for v in a['vertices']}
        clauses = []
        for v in range(self.n):
            atom = 4*self.n + self.av[v] + 1
            clauses.append([-atom] + [4*v+c+1 for c in range(4)])
            clauses.extend([[-4*v-c-1, atom] for c in range(4)])
        for u, v in graph['edges']:
            clauses.extend([[-4*u-c-1, -4*v-c-1] for c in range(4)])
        self.solver = Solver(name='cadical195', bootstrap_with=clauses)

    def check(self, mask, word):
        require(len(word) == self.n, 'model length')
        require(all(word[v] in ('0123' if mask >> self.av[v] & 1 else '-')
                    for v in range(self.n)), 'model support')
        require(all(word[u] == '-' or word[v] == '-' or word[u] != word[v]
                    for u, v in self.graph['edges']), 'model edge')

    def solve(self, mask, budget):
        assumptions = [(4*self.n+i+1)*(1 if mask >> i & 1 else -1) for i in range(self.k)]
        aset = {v for v in range(self.n) if mask >> self.av[v] & 1}
        adj = {v: set() for v in aset}
        for u, v in self.graph['edges']:
            if u in aset and v in aset:
                adj[u].add(v)
                adj[v].add(u)
        triangle = None
        for u in sorted(aset):
            for v in sorted(adj[u]):
                if u < v and adj[u] & adj[v]:
                    triangle = (u, v, min(adj[u] & adj[v]))
                    break
            if triangle:
                break
        if triangle:
            assumptions.extend(4*v+c+1 for c, v in enumerate(triangle))
        self.solver.conf_budget(budget)
        result = self.solver.solve_limited(assumptions=assumptions)
        word = None
        if result:
            model = set(self.solver.get_model())
            word = ''.join(str(next(c for c in range(4) if 4*v+c+1 in model))
                           if v in aset else '-' for v in range(self.n))
            self.check(mask, word)
        return result, word


def crossover(graph):
    # Fixed-under-sqrt5 vertices of H510 plus nonfixed vertices of H553.
    mask = sum(1 << i for i, a in enumerate(graph['atoms'])
               if (a['side'] == 0 and a['membership'] & 1)
               or (a['side'] == 1 and a['membership'] & 8))
    vertices = sorted(v for i, a in enumerate(graph['atoms']) if mask >> i & 1 for v in a['vertices'])
    require(len(vertices) == 508, 'crossover order')
    labels = {v: i for i, v in enumerate(vertices)}
    edges = [(labels[u], labels[v]) for u, v in graph['edges'] if u in labels and v in labels]
    clauses = [[4*v+c+1 for c in range(4)] for v in range(len(vertices))]
    for u, v in edges:
        clauses.extend([[-4*u-c-1, -4*v-c-1] for c in range(4)])
    with Solver(name='cadical195', bootstrap_with=clauses) as s:
        s.conf_budget(100000)
        require(s.solve_limited() is True, 'crossover not positively solved')
        model = set(s.get_model())
    word = ['-'] * len(graph['points'])
    for i, v in enumerate(vertices):
        word[v] = str(next(c for c in range(4) if 4*i+c+1 in model))
    return dict(mask=mask, word=''.join(word))


def generate(inputs, out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    graph = build(inputs)
    weights = [len(a['vertices']) for a in graph['atoms']]
    orders, maximal, admissible = maximal_masks(weights, 508)
    oracle = Oracle(graph)
    first = crossover(graph)
    oracle.check(first['mask'], first['word'])
    covers, unknown, queries = [first], [], []
    remaining = [m for m in maximal if m & ~first['mask']]
    while remaining:
        mask = remaining[0]
        result, word = oracle.solve(mask, 200000)
        queries.append(['primary', mask, orders[mask], result])
        if result is None:
            unknown.append(mask)
            remaining.pop(0)
            continue
        require(result is True, f'non-four-colourable candidate {mask}; independently certify it')
        grown = mask
        for i in sorted(range(len(weights)), key=lambda i: (-weights[i], i)):
            if grown >> i & 1:
                continue
            trial = grown | (1 << i)
            yes, new_word = oracle.solve(trial, 2000)
            queries.append(['growth', trial, orders[trial], yes])
            if yes:
                grown, word = trial, new_word
        oracle.check(grown, word)
        covers.append(dict(mask=grown, word=word))
        remaining = [m for m in remaining if m & ~grown]
        unknown = [m for m in unknown if m & ~grown]
    oracle.solver.delete()
    report = dict(admissible=admissible, maximal=len(maximal), covers=len(covers),
                  unknown=unknown, queries=queries, seconds=time.monotonic()-start)
    (out/'search.json').write_text(json.dumps(report, indent=2)+'\n')
    require(not unknown, 'unresolved masks; no family theorem')
    certificate = dict(version='heule-catalogue-atoms-v1', target=508, covers=covers)
    (out/'certificate.json').write_text(json.dumps(certificate, separators=(',', ':'))+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'queries'}, sort_keys=True))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    generate(args.inputs, args.out)
