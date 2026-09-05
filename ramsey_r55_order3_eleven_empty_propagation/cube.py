#!/usr/bin/env python3
"""Complete residual formulas with an empty prefix and sharp pair-signature cuts."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_anchor_propagation'
NOEMPTY=ROOT.parent/'ramsey_r55_order3_eleven_noempty_rigidity'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PINS={PREVIOUS/'result.json':'efb670ac77e1ff9e3d3b8b22040942e64a27164bd83b45db95f388209bcbb801',
      NOEMPTY/'boundary.json':'a4dce0f8cde0da8db257447c1b0dd1b6d9d25b957c906405966bde209a5dac0a',
      NOEMPTY/'classification.json':'644ff84bafe212eee0b1230be546528b4972c52d1765010cfc34e8efa8e754a7',
      NOEMPTY/'PROOF.md':'dba2b97656ea00c3b54dc77e07ab2b8453b63e6c372b0f1b43382b826fadd594',
      NOEMPTY/'local_obstructions.json':'e4de90166f85c56472196da820a7d9da39b268d5ff083856b48462486ac69092'}


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for path,pin in PINS.items():require(info(path)['sha256']==pin,'pinned '+path.name)
    old=json.loads((PREVIOUS/'result.json').read_text());boundary=json.loads((NOEMPTY/'boundary.json').read_text())
    require(old['complete'] and not old['target_graph'],'complete inherited boundary')
    rows=[{k:c[k] for k in ('index','bits','labeled','omitted','formula')} for c in old['cases'] if c['status']=='open']
    require([c['index'] for c in rows]==boundary['remaining_full_cores']==boundary['forced_empty_cores'],'all residual cores force empty')
    require(len(rows)==26 and sum(c['labeled'] for c in rows)==16605,'complete current boundary')
    return rows


def clauses():
    rows=[(-211-i,) for i in range(4)]
    for fixed in combinations(range(10),3):
        for i in range(4):
            for j in range(4):
                if i==j:continue
                row=[]
                for f in fixed:
                    row.append(-(211+11*f+i))
                    row.extend(211+11*f+k for k in range(4) if k not in (i,j))
                rows.append(tuple(row))
    require(len(rows)==1444 and len(set(rows))==1444,'four units and1440 unique cuts')
    return rows


def make(base,output,case):
    require(info(base)==case['formula'],'complete inherited strengthened base')
    nv=34280+10*len(case['omitted']);nc=615938+50*len(case['omitted']);rows=clauses()
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'base header')
        g.write(f'p cnf {nv} {nc+1444}\n'.encode());shutil.copyfileobj(f,g)
        for row in rows:g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
