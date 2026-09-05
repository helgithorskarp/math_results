#!/usr/bin/env python3
"""Fixed-selection colourability with positive vertex activation assumptions."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'hadwiger_nelson_parts509_quantified_dual'))
import encode_dual as prior


def encode(source):
    n = source['n']
    colours = [[n + 4*v + c + 1 for c in range(4)] for v in range(n)]
    patterns = list(range(5*n + 1, 5*n + len(source['patterns']) + 1))
    rows = [patterns]
    rows += [[-v-1] + colours[v] for v in range(n)]
    rows += [[-colours[a][c], -colours[b][c]]
             for a,b in source['edges'] for c in range(4)]
    rows += [[-patterns[j], -colours[v][pattern[a]]]
             for a,v in source['cross'] for j,pattern in enumerate(source['patterns'])]
    return rows, dict(variables=5*n+len(patterns), clauses=len(rows),
                     colours=colours, patterns=patterns)


def decode(source, meta, model, selected):
    positive = {v for v in model if v > 0}
    j = next(j for j,v in enumerate(meta['patterns']) if v in positive)
    c = {v:next(k for k,lit in enumerate(meta['colours'][v]) if lit in positive)
         for v in selected}
    assert all(c[a] != c[b] for a,b in source['edges'] if a in selected and b in selected)
    assert all(c[v] != source['patterns'][j][a] for a,v in source['cross'] if v in selected)
    return dict(pattern=j, colours=''.join(str(c[v]) if v in c else '.' for v in range(source['n'])))


def input_data():
    return prior.original().pool_input()


def dimacs(rows, nv):
    return (f'p cnf {nv} {len(rows)}\n' +
            ''.join(' '.join(map(str,row))+' 0\n' for row in rows)).encode()
