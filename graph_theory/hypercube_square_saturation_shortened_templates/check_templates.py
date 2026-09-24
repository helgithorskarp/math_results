#!/usr/bin/env python3
"""Check the finite hypotheses of the replication lemma, using integers only."""
from __future__ import annotations
import copy
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def check(t: dict) -> dict:
    k = t['k']; q = 1 << k
    C, D, T = map(set, (t['C'], t['D'], t['T']))
    A = C | D
    require(C and D and not C & D, 'classes must be nonempty and disjoint')
    require(all(0 <= x < q for x in A | T), 'out-of-range label')
    require(0 in T, 'zero residue is required')
    require(len(C) == len(t['C']) and len(D) == len(t['D']) and
            len(T) == len(t['T']), 'duplicate label')
    span = {0}
    for v in T:
        span |= {x ^ v for x in span}
    require(len(span) == q, 'T does not span the core')
    core = {tuple(e) for e in t['core_edges']}
    require(len(core) == len(t['core_edges']), 'duplicate core edge')
    for a, b in core:
        require(0 <= a < b < q and (a ^ b) in T, 'invalid core edge')
        require(a in A or b in A, 'core vertex cover failed')
        require(not ({a, b} <= C or {a, b} <= D), 'core independence failed')
    rows = list(map(set, t['outside_neighbors']))
    require(len(rows) == q, 'wrong number of outside rows')
    for x, row in enumerate(rows):
        require(len(row) == len(t['outside_neighbors'][x]), 'duplicate neighbor')
        require(row <= A and row & C and row & D, 'outside domination failed')
        require(all((x ^ a) in T for a in row), 'invalid outside incidence')
    def edge(a: int, b: int) -> bool:
        return tuple(sorted((a, b))) in core
    for cls in (C, D):
        for x in range(q):
            require(x in cls or any(edge(x, a) for a in cls), 'core domination failed')
    core_squares = 0
    for a, b, c in itertools.combinations(range(q), 3):
        d = a ^ b ^ c
        if d <= c:
            continue
        for v, w, x in ((b, c, d), (b, d, c), (c, b, d)):
            core_squares += 1
            require(not (edge(a, v) and edge(v, w) and edge(w, x) and edge(x, a)),
                    'core affine square')
    core_boundary = 0
    for a, b in itertools.combinations(range(q), 2):
        if not ({a, b} & A) or (a ^ b) not in T or edge(a, b):
            continue
        core_boundary += 1
        require(any(w not in (a, b) and edge(a, w) and edge(w, a ^ b ^ w)
                    and edge(a ^ b ^ w, b) for w in range(q)), 'core boundary not saturated')
    outside_squares = 0
    for a, b in itertools.combinations(A, 2):
        for x in range(q):
            outside_squares += 1
            require(not ({a, b} <= rows[x] and {a, b} <= rows[x ^ a ^ b]),
                    'outside affine square')
    outside_boundary = 0
    for x in range(q):
        for a in A:
            if (x ^ a) not in T or a in rows[x]:
                continue
            outside_boundary += 1
            require(any({a, b} <= rows[x ^ a ^ b] for b in rows[x]),
                    'outside boundary not saturated')
    r0, r1 = len(core), sum(map(len, rows))
    require(r0 <= r1, 'coarse edge bound requires r0 <= r1')
    return {'name':t['name'], 'core_order':q, 'class_sizes':[len(C), len(D)],
            'allowed_residues':len(T), 'core_edges':r0, 'outside_edges':r1,
            'core_affine_cycles_tested':core_squares,
            'outside_rectangle_tests':outside_squares,
            'missing_core_boundary_edges':core_boundary,
            'missing_outside_incidences':outside_boundary}


def main() -> None:
    templates = json.loads((ROOT / 'templates.json').read_text())
    records = [check(t) for t in templates]
    rejected = []
    bad = copy.deepcopy(templates[0]); bad['outside_neighbors'][0] = [0]
    rejected.append(('lost_domination', bad))
    bad = copy.deepcopy(templates[1]); bad['core_edges'].append([0, 2])
    rejected.append(('added_affine_square', bad))
    bad = copy.deepcopy(templates[2]); bad['T'].remove(0)
    rejected.append(('lost_zero_residue', bad))
    names = []
    for name, bad in rejected:
        try:
            check(bad)
        except ValueError:
            names.append(name)
        else:
            raise RuntimeError('negative control accepted: ' + name)
    print(json.dumps({'templates':records, 'negative_controls_rejected':names}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
