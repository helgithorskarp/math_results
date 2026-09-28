"""Exact shifted cyclic fibre criterion; full-family target status is UNKNOWN."""
import argparse
import itertools
import json
from pathlib import Path

def variable_maps(a, p=7):
    if a < 3 or a % 2 != 1 or p not in (5, 7):
        raise ValueError('need odd a>=3 and p=5 or7')
    t, h = ((p - 1) // 2, (a - 1) // 2)
    common = tuple(range(t, 6))
    labels = (0, *common)
    top = 0
    E, Q = ({}, {})
    for u in range(1, h + 1):
        for c in range(6):
            top += 1
            E[u, c] = top
    for q in range(a):
        for c in labels:
            top += 1
            Q[q, c] = top
    return dict(a=a, p=p, t=t, h=h, common=common, labels=labels, E=E, Q=Q, variables=top)


def decode(m, truth):
    axis = {u: next((c for c in range(6) if m['E'][u, c] in truth)) for u in range(1, m['h'] + 1)}
    fibre = {q: next((c for c in m['labels'] if m['Q'][q, c] in truth)) for q in range(m['a'])}
    word = []
    for x in range(1, m['a'] * m['p']):
        q, b = divmod(x, m['p'])
        if b == 0:
            colour = axis[min(q, m['a'] - q)]
        else:
            state = fibre[q if b <= m['t'] else m['a'] - 1 - q]
            colour = state if state else min(b, m['p'] - b) - 1
        word.append(colour)
    return word


def encoding(a, p=7, symmetry=True):
    m = variable_maps(a, p)
    E, Q = (m['E'], m['Q'])
    cnf = []
    for row in [[E[u, c] for c in range(6)] for u in range(1, m['h'] + 1)] + [[Q[q, c] for c in m['labels']] for q in range(a)]:
        cnf.append(row)
        cnf.extend([[-v, -w] for v, w in itertools.combinations(row, 2)])
    cnf.append([Q[0, 0]])
    clauses = set()
    for x in range(1, a):
        for y in range(x, a):
            z = (x + y) % a
            if z:
                edge = {min(u, a - u) for u in (x, y, z)}
                for c in range(6):
                    clauses.add(tuple(sorted((-E[u, c] for u in edge))))
    for x in range(a):
        for y in range(x, a):
            z = (x + y) % a
            w = (-1 - x - y) % a
            for c in m['common']:
                clauses.add(tuple(sorted({-Q[u, c] for u in (x, y, z)})))
                clauses.add(tuple(sorted({-Q[u, c] for u in (x, y, w)})))
    for x, y in itertools.combinations(range(a), 2):
        d = min(y - x, a - y + x)
        for c in range(m['t']):
            clauses.add(tuple(sorted((-Q[x, 0], -Q[y, 0], -E[d, c]))))
        for c in m['common']:
            clauses.add(tuple(sorted((-Q[x, c], -Q[y, c], -E[d, c]))))
    cnf.extend(map(list, sorted(clauses, key=lambda row: (len(row), row))))
    if symmetry:
        seen = {c: [] for c in m['common']}
        for table, u in [(Q, q) for q in range(a)] + [(E, u) for u in range(1, m['h'] + 1)]:
            for c in m['common'][1:]:
                cnf.append([-table[u, c], *seen[c - 1]])
            for c in m['common']:
                seen[c].append(table[u, c])
        for u in range(1, m['h'] + 1):
            for c in range(1, m['t']):
                cnf.append([-E[u, c], *[E[v, c - 1] for v in range(1, u)]])
    m['criterion_clauses'] = clauses
    return (m, cnf)


def dimacs(a=109,p=5):
    m,clauses=encoding(a,p)
    text=f"p cnf {m['variables']} {len(clauses)}\n"
    text+=''.join(' '.join(map(str,row))+' 0\n' for row in clauses)
    return text.encode('ascii')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    parser.add_argument('--axis-factor',type=int,default=109)
    parser.add_argument('--short-factor',type=int,default=5)
    args=parser.parse_args()
    args.output.write_bytes(dimacs(args.axis_factor,args.short_factor))
