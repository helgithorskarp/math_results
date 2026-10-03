"""Credited pure literal/MRV/packing helpers; imports no producer. six-code-2, researcher."""
from itertools import combinations
import json
import os
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def literal(ps):
    return sum(1 << p for p in ps)


def point_set(w, k):
    require(type(w) is int and 0 <= w < 1 << 17 and w.bit_count() == k, 'physical old-point word')
    return frozenset(p for p in range(17) if w >> p & 1)


def cap_family(cap, parent, hole_ids, guard):
    rows = {i: tuple(parent[i] - {p} for p in sorted(parent[i] & cap))
            for i in range(68) if i not in hole_ids and len(parent[i] & cap) >= 3}
    require(all(len(t) == 4 and len(t & cap) == 2 for choices in rows.values() for t in choices),
            'nonempty blocking parent has no admissible contained tail')
    keys = set()
    nodes = 0

    def visit(assignment):
        nonlocal nodes
        nodes += 1
        if nodes % 2048 == 0:
            guard('adaptive-carrier')
        if len(assignment) == len(rows):
            keys.add(tuple((i, literal(t)) for i, t in sorted(assignment.items())))
            return
        domains = {i: tuple(t for t in choices if all(len(t & u) <= 1 for u in assignment.values()))
                   for i, choices in rows.items() if i not in assignment}
        row = min(domains, key=lambda i: (len(domains[i]), i))
        for tail in domains[row]:
            visit(assignment | {row: tail})

    visit({})
    return keys, nodes


def check_packing(words, expected_size):
    require(len(words) == len(set(words)) == expected_size, 'positive distinct word count')
    require(all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5 for w in words),
            'positive weight-five domain')
    ps = tuple(frozenset(v for v in range(18) if w >> v & 1) for w in words)
    require(all(len(a & b) <= 2 for a, b in combinations(ps, 2)), 'positive physical collision')
    triples = [t for w in ps for t in combinations(sorted(w), 3)]
    require(len(triples) == len(set(triples)) == 10 * expected_size, 'positive triple ownership')
    return ps


def rejection(label, callback, expected):
    try:
        callback()
    except ValueError as error:
        require(str(error) == expected, 'control rejected for unintended reason: ' + label)
        return label
    raise ValueError('semantic damage accepted: ' + label)


def operations_guard():
    """Optional read-only campaign barrier, never a host mutation."""
    value = os.environ.get('DISCOVERY_OPERATIONS_STATE')
    if value:
        require(not any((Path(value) / name).exists()
                        for name in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                'operations pause/handover barrier')
