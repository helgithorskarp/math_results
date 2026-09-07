#!/usr/bin/env python3
"""One frozen odd-cycle hypergraph proof gate; no geometric graph search."""
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path
import resource
import sys
import time
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    raise SystemExit('Usage: reconstruct_frozen.py /scratch/empty-output-directory')
HERE = Path(sys.argv[1]).resolve()
if HERE.is_relative_to(ROOT):
    raise SystemExit('Generated files must be outside the repository')
HERE.mkdir(parents=True, exist_ok=True)
if any(HERE.iterdir()):
    raise SystemExit('Output directory must be empty')
SOURCE = ROOT / 'hadwiger_nelson_haugland2131_exact_reproduction/graph.json'
EXPECTED_SOURCE = '201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d'
DISCOVERY_CONFLICTS = 400000
REPLAY_CONFLICTS = 100000
ROUNDS = 512


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        if not 0 <= a < b < n:
            raise ValueError('bad edge')
        adj[a].add(b)
        adj[b].add(a)
    return [sorted(ns) for ns in adj]


def canonical_cycle(cycle):
    k = cycle.index(min(cycle))
    a = tuple(cycle[k:] + cycle[:k])
    b = (a[0],) + a[:0:-1]
    return min(a, b)


def odd_cycles(adj, side):
    """Return fundamental odd cycles, or a proper two-colouring of each side."""
    n = len(adj)
    parity = [-1] * n
    parent = [-1] * n
    depth = [0] * n
    cycles = {}
    for root in range(n):
        if parity[root] >= 0:
            continue
        parity[root] = 0
        todo = deque([root])
        while todo:
            u = todo.popleft()
            for v in adj[u]:
                if side[u] != side[v]:
                    continue
                if parity[v] < 0:
                    parity[v] = 1 - parity[u]
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    todo.append(v)
                elif u < v and parity[u] == parity[v]:
                    a, b = u, v
                    left, right = [a], [b]
                    while depth[a] > depth[b]:
                        a = parent[a]
                        left.append(a)
                    while depth[b] > depth[a]:
                        b = parent[b]
                        right.append(b)
                    while a != b:
                        a, b = parent[a], parent[b]
                        left.append(a)
                        right.append(b)
                    walk = canonical_cycle(left + list(reversed(right[:-1])))
                    check_cycle(walk, adj)
                    if len({side[x] for x in walk}) != 1:
                        raise ValueError('nonmonochromatic obstruction')
                    key = tuple(sorted(walk))
                    cycles[key] = min(walk, cycles.get(key, walk))
    return cycles, parity


def check_cycle(walk, adj):
    if len(walk) < 3 or len(walk) % 2 != 1 or len(set(walk)) != len(walk):
        raise ValueError('not a simple odd cycle')
    if any(walk[(i + 1) % len(walk)] not in adj[u] for i, u in enumerate(walk)):
        raise ValueError('cycle has a missing edge')


def cycle_clauses(key):
    return [[v + 1 for v in key], [-v - 1 for v in key]]


def controls():
    # All 1,024 labelled five-vertex simple graphs and all 32 Boolean cuts.
    # Compare the BFS cycle criterion with explicit second-cut enumeration.
    n = 5
    pairs = list(itertools.combinations(range(n), 2))
    partitions = list(itertools.product(range(2), repeat=n))
    checks = 0
    for mask in range(1 << len(pairs)):
        edges = [e for i, e in enumerate(pairs) if mask >> i & 1]
        adj = adjacency(n, edges)
        for x in partitions:
            found, y = odd_cycles(adj, x)
            exists = any(all(x[u] != x[v] or z[u] != z[v] for u, v in edges)
                         for z in partitions)
            if bool(found) == exists:
                raise ValueError('two-cut equivalence control failed')
            if not found and not all(x[u] != x[v] or y[u] != y[v] for u, v in edges):
                raise ValueError('bad decoded second cut')
            checks += 1
    return {'labelled_graphs': 1024, 'partition_checks': checks,
            'explicit_second_cut_enumeration': True}


def main():
    started = time.monotonic()
    test = controls()
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SOURCE:
        raise ValueError('source changed')
    data = json.loads(raw)
    original_edges = [tuple(e) for e in data['G1_edges']]
    if len(original_edges) != 3985 or data['G1_endpoints'] != [0, 5]:
        raise ValueError('wrong source')
    labels = [v for v in range(740) if v != 5]
    mapping = {v: i for i, v in enumerate(labels)}
    mapping[5] = mapping[0]
    edges = sorted({tuple(sorted((mapping[u], mapping[v]))) for u, v in original_edges})
    adj = adjacency(len(labels), edges)
    # A four-colouring may be renamed so the anchor triangle is 00,01,10.
    anchor = [mapping[v] for v in (0, 13, 42)]
    if any(b not in adj[a] for a, b in itertools.combinations(anchor, 2)):
        raise ValueError('anchor is not a triangle')
    pins = [[-anchor[0] - 1], [-anchor[1] - 1], [anchor[2] + 1]]
    cycles = {}
    for u in range(len(adj)):
        for v in adj[u]:
            if u < v:
                for w in sorted(set(adj[u]).intersection(adj[v])):
                    if v < w:
                        cycles[(u, v, w)] = (u, v, w)
    initial_triangles = len(cycles)
    clauses = list(pins)
    for key in sorted(cycles):
        clauses.extend(cycle_clauses(key))
    history = []
    outcome = 'UNKNOWN'
    colouring = None
    with Solver(name='cadical195', bootstrap_with=clauses, use_timer=True) as solver:
        for turn in range(ROUNDS):
            before = solver.accum_stats()['conflicts']
            remaining = DISCOVERY_CONFLICTS - before
            if remaining <= 0:
                break
            solver.conf_budget(remaining)
            result = solver.solve_limited()
            stats = solver.accum_stats()
            row = {'round': turn, 'sat': result, 'conflicts': stats['conflicts'],
                   'elapsed_seconds': time.monotonic() - started, 'cycles_before': len(cycles)}
            if result is None:
                history.append(row)
                break
            if result is False:
                outcome = 'UNSAT_UNCHECKED'
                history.append(row)
                break
            model = set(solver.get_model())
            side = [int(v + 1 in model) for v in range(len(labels))]
            bad, parity = odd_cycles(adj, side)
            if not bad:
                colouring = [2 * side[mapping[v]] + parity[mapping[v]] for v in range(740)]
                if colouring[0] != colouring[5] or any(colouring[u] == colouring[v] for u, v in original_edges):
                    raise ValueError('bad four-colouring')
                outcome = 'ENDPOINT_EQUAL_FOUR_COLOURING'
                row['new_cycles'] = 0
                history.append(row)
                break
            new = {k: w for k, w in bad.items() if k not in cycles}
            if not new:
                raise ValueError('SAT assignment violated existing cycle clause')
            for key in sorted(new):
                cs = cycle_clauses(key)
                solver.append_formula(cs)
                clauses.extend(cs)
                cycles[key] = new[key]
            row['new_cycles'] = len(new)
            history.append(row)
            (HERE / 'progress.json').write_text(json.dumps(row, indent=2) + '\n')
            if turn < 5 or turn % 25 == 0:
                print(json.dumps(row), flush=True)
        discovery_stats = solver.accum_stats()
    for walk in cycles.values():
        check_cycle(walk, adj)
    cnf = f'p cnf {len(labels)} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    (HERE / 'odd_cycles.cnf').write_text(cnf)
    (HERE / 'cycles.json').write_text(json.dumps({'walks': [cycles[k] for k in sorted(cycles)],
                                                'pins': pins, 'quotient_labels': labels}, separators=(',', ':')) + '\n')
    (HERE / 'history.json').write_text(json.dumps(history, indent=2) + '\n')
    expected_cnf = '57058179a7ca8dd5d74c9711f202a53378b1adba9001786687dd92e82d3cf038'
    expected_cycles = 'bac6fe6962012d4ae5c79e65e9ad5dc39383bfd5c40d651f9cff877ac61b5a63'
    if outcome != 'UNKNOWN' or len(history) != 512:
        raise ValueError('Frozen run was not reproduced; do not substitute another family')
    if hashlib.sha256((HERE / 'odd_cycles.cnf').read_bytes()).hexdigest() != expected_cnf:
        raise ValueError('Frozen CNF identity differs')
    if hashlib.sha256((HERE / 'cycles.json').read_bytes()).hexdigest() != expected_cycles:
        raise ValueError('Frozen cycle archive identity differs')
    print(json.dumps({'frozen_run_reproduced': True, 'refinements': 512,
                      'cycles': len(cycles), 'cnf_sha256': expected_cnf,
                      'cycles_sha256': expected_cycles}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
