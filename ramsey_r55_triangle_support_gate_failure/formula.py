#!/usr/bin/env python3
"""Literal necessary-extension formula; fixed core and 140 remaining edges."""
from itertools import combinations
from pathlib import Path


def generate():
    raw = (Path(__file__).resolve().parent/'r44_17.g6').read_bytes()
    rows = raw.decode().splitlines()
    if len(rows) != 1:
        raise ValueError('one core record required')
    data = [ord(c)-63 for c in rows[0]]
    if data[0] != 17 or any(not 0 <= x < 64 for x in data):
        raise ValueError('core graph6 format')
    bits = [(v >> k) & 1 for v in data[1:] for k in range(5, -1, -1)]
    fixed = {}
    at = 0
    for v in range(1, 17):
        for u in range(v):
            fixed[u, v] = bits[at]
            at += 1
    if any(bits[at:]):
        raise ValueError('graph6 padding')
    free = {e: i+1 for i, e in enumerate(e for e in combinations(range(24), 2)
                                        if e not in fixed)}
    clauses = []
    for size, color in ((4, 1), (5, 0)):
        for q in combinations(range(24), size):
            clause = []
            for e in combinations(q, 2):
                if e in fixed:
                    if fixed[e] != color:
                        break
                else:
                    clause.append(-free[e] if color else free[e])
            else:
                clauses.append(clause)
    dimacs = f'p cnf {len(free)} {len(clauses)}\n'
    dimacs += ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
    return fixed, free, clauses, dimacs


if __name__ == '__main__':
    print(generate()[3], end='')
