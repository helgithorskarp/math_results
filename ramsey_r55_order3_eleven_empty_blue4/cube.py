#!/usr/bin/env python3
"""Complete first-empty-vertex blue-four branch on all25 current core bases."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PINS={'result.json':'536397d3b24e5d14a5144108be91933e72c85248dc5b4d0ab6231b16f37fcf44',
      'boundary.json':'3f5c0c88b63a40243d00df1c13878d73032457b5a39874f58b1ed98ba17845fe',
      'verification.json':'50efb091a807f15f10a0a6330f33c6da5b49b52af97f9113bec4bd8ac2c3842d'}


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned '+name)
    old=json.loads((PREVIOUS/'result.json').read_text());boundary=json.loads((PREVIOUS/'boundary.json').read_text())
    require(old['complete'] and not old['target_graph'],'complete inherited boundary')
    rows=[{k:c[k] for k in ('index','bits','labeled','omitted','formula')} for c in old['cases'] if c['status']=='open']
    require([c['index'] for c in rows]==boundary['remaining_open'],'complete25-case cover')
    require(len(rows)==25 and sum(c['labeled'] for c in rows)==15957,'current totals')
    return rows


def clauses():
    # e=33: at least/exactly three red links to the seven blue moving triangles.
    links=list(range(215,222));rows=list(combinations(links,5))
    rows += [tuple(-v for v in four) for four in combinations(links,4)]
    rows += [(v,) for v in range(166,175)]
    require(len(rows)==65 and len(set(rows))==65,'21 lower,35 upper and9 fixed-edge units')
    return rows


def make(base,output,case):
    require(info(base)==case['formula'],'complete inherited strengthened base')
    nv=34280+10*len(case['omitted']);nc=617382+50*len(case['omitted']);rows=clauses()
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'base header')
        g.write(f'p cnf {nv} {nc+65}\n'.encode());shutil.copyfileobj(f,g)
        for row in rows:g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
