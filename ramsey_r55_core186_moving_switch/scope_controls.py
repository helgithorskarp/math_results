#!/usr/bin/env python3
"""Exhaustive small controls for preservation of an odd-order action."""
import argparse
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    cases = valid = graphs = 0
    for g in ([1, 2, 0], [1, 2, 0, 3], [1, 2, 0, 3, 4], [1, 2, 0, 4, 5, 3]):
        n = len(g)
        pairs = list(combinations(range(n), 2))
        todo, orbits = set(pairs), []
        while todo:
            u, v = min(todo)
            orbit = {tuple(sorted((u, v))), tuple(sorted((g[u], g[v]))),
                     tuple(sorted((g[g[u]], g[g[v]])))}
            require(orbit <= todo, 'complete pair orbit')
            todo -= orbit
            orbits.append(orbit)
        for mask in range(1 << len(orbits)):
            red = set().union(*(o for j, o in enumerate(orbits) if mask & (1 << j)))
            graphs += 1
            for spins in range(1 << n):
                changed = {e for e in pairs
                           if int(e in red) ^ ((spins >> e[0]) & 1) ^ ((spins >> e[1]) & 1)}
                invariant = all((e in changed) == (tuple(sorted((g[e[0]], g[e[1]]))) in changed)
                                for e in pairs)
                constant = all(((spins >> v) & 1) == ((spins >> g[v]) & 1) for v in range(n))
                require(invariant == constant, 'action-preserving switches')
                valid += invariant
                cases += 1
    return {'status': 'PASS', 'invariant_graphs': graphs,
            'all_switch_cases': cases, 'action_preserving_cases': valid}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
