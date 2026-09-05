#!/usr/bin/env python3
"""Finite activation controls against direct graph colouring backtracking."""
import itertools
import json
import random
import time
from pysat.solvers import Solver
from activation import encode, decode, load_graph, require


def direct(labels, edges):
    adj = {v: set() for v in labels}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].add(b); adj[b].add(a)
    colours = {}
    def visit():
        if len(colours) == len(labels):
            return True
        v = max((v for v in labels if v not in colours),
                key=lambda v: (len({colours[w] for w in adj[v] if w in colours}), len(adj[v]), v))
        used = {colours[w] for w in adj[v] if w in colours}
        for c in range(4):
            if c not in used:
                colours[v] = c
                if visit():
                    return True
                del colours[v]
        return False
    return visit()


def main():
    start = time.monotonic()
    rng = random.Random(574309)
    fixtures = []
    for n in range(8):
        labels = list(range(n)); pairs = list(itertools.combinations(labels, 2))
        fixtures += [(labels, pairs), (labels, [])]
        for _ in range(4):
            fixtures.append((labels, [e for e in pairs if rng.randrange(4) != 0]))
    checked = sat = unsat = pinned = 0
    for labels, edges in fixtures:
        for pins in [()] + ([(0, 1, 2)] if all(e in edges for e in [(0, 1), (0, 2), (1, 2)]) else []):
            required = set(pins)
            selectable = sorted(set(labels) - required)
            rows, meta = encode(labels, edges, selectable, pins)
            with Solver(name='cadical195', bootstrap_with=rows) as solver:
                for mask in range(1 << len(selectable)):
                    keep = required | {v for i, v in enumerate(selectable) if mask >> i & 1}
                    answer = solver.solve(assumptions=[meta['activation'][v] for v in sorted(keep-required)])
                    require(answer == direct(sorted(keep), edges), 'direct fixture mismatch')
                    if answer:
                        decode(labels, edges, meta, solver.get_model(), keep)
                    checked += 1; sat += answer; unsat += not answer; pinned += bool(pins)
    labels, edges, cert = load_graph()
    # Known positive deletion in X, with all L present; the fixed pins survive.
    omitted = cert['pool_labels'][-1]
    labels = [v for v in labels if v != omitted]
    edges = [e for e in edges if omitted not in e]
    rows, meta = encode(labels, edges, range(374), (384, 386, 388))
    with Solver(name='cadical195', bootstrap_with=rows, use_timer=True) as solver:
        solver.conf_budget(100000)
        answer = solver.solve_limited(assumptions=list(meta['activation'].values()))
        require(answer is True, 'known pool-deletion control must be SAT')
        decode(labels, edges, meta, solver.get_model(), set(labels))
        native = solver.time()
    print(json.dumps(dict(fixtures=len(fixtures), assignments=checked, sat=sat, unsat=unsat,
                          pinned_assignments=pinned, known_deleted_pool_vertex=omitted,
                          actual_positive_control_native_seconds=native,
                          wall_seconds=time.monotonic()-start, status='ALL CONTROLS VERIFIED'), indent=2))


if __name__ == '__main__':
    main()
