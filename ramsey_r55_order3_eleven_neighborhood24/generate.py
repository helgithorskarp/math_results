#!/usr/bin/env python3
"""Exact order-three Ramsey(5,4;24) neighborhood formulas, with fixed red cores."""
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'ramsey_r55_order3_eleven_empty_blue4'
PINS = {'result.json': '2954c6534946f23a8d58c6a532c956fc875342c7a4bb3a02ac205471346dbe17',
        'boundary.json': '1e958b64e2211d188cf2b1b0de8f81c2d4c08747285e917e0b0231856b1daaa9'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def info(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(1 << 20): digest.update(chunk)
    return dict(bytes=path.stat().st_size, sha256=digest.hexdigest())


def cases():
    for name, digest in PINS.items():
        need(info(OLD / name)['sha256'] == digest, 'pinned boundary')
    old = json.loads((OLD / 'result.json').read_text())
    boundary = json.loads((OLD / 'boundary.json').read_text())
    rows = [{k: c[k] for k in ('index', 'bits', 'labeled', 'omitted')}
            for c in old['cases'] if c['status'] == 'open']
    need([c['index'] for c in rows] == boundary['blue4_open'] == [124,155,159,168,180,194], 'six residual branches')
    need(sum(c['labeled'] for c in rows) == 2349, 'label total')
    return rows


def model(triangles=8, red_triangles=4):
    ids = {(i,j,d): v for v,(i,j,d) in enumerate(
        ((i,j,d) for i,j in combinations(range(triangles),2) for d in range(3)),1)}
    def edge(a,b):
        a,b = sorted((a,b));i,s = divmod(a,3);j,t = divmod(b,3)
        return i < red_triangles if i == j else ids[i,j,(t-s)%3]
    return ids, edge


def ramsey_clauses(triangles=8, red_triangles=4):
    _, edge = model(triangles, red_triangles);rows = set()
    for order, color in ((5,True),(4,False)):
        for vertices in combinations(range(3*triangles),order):
            literals = set()
            for a,b in combinations(vertices,2):
                e = edge(a,b)
                if type(e) is bool:
                    if e != color:
                        break
                else:
                    literals.add(-e if color else e)
            else:
                rows.add(tuple(sorted(literals)))
    return sorted(rows)


def core_units(case):
    ids,_ = model()
    variables = [ids[i,j,d] for i,j in combinations(range(4),2) for d in range(3)]
    need(len(case['bits']) == 18 and set(case['bits']) <= {'0','1'}, '18-bit core')
    return [(v if bit == '1' else -v,) for v,bit in zip(variables,case['bits'])]


def write(path, case):
    rows = ramsey_clauses() + core_units(case)
    path.write_text(f'p cnf 84 {len(rows)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in rows))
    return dict(**info(path), variables=84, clauses=len(rows), ramsey_clauses=len(rows)-18, core_units=18)


def decode(log, path):
    values = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for v in map(int,line.split()[1:]):
                if v:
                    need(abs(v) not in values or values[abs(v)] == (v > 0), 'conflicting SAT model')
                    values[abs(v)] = v > 0
    need(set(range(1,85)) <= values.keys(), 'complete primary model')
    _,edge = model();red = []
    for a,b in combinations(range(24),2):
        e = edge(a,b)
        color = e if type(e) is bool else values[e]
        if color:
            red.append((a,b))
    path.write_text(f'24 {len(red)}\n' + ''.join(f'{a} {b}\n' for a,b in red))
    return info(path)
