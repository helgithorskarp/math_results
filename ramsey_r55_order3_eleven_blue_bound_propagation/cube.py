#!/usr/bin/env python3
"""Propagate b<=3 into 19 unrestricted full bases after certified b=4 closure."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4'
BASE_SOURCE=ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PINS={'result.json':'2954c6534946f23a8d58c6a532c956fc875342c7a4bb3a02ac205471346dbe17',
      'verification.json':'8c0d7bc28b6c86b0b360b031a25f45e7a8e40b79b8215877c103a9eef93592b1',
      'boundary.json':'1e958b64e2211d188cf2b1b0de8f81c2d4c08747285e917e0b0231856b1daaa9'}


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned '+name)
    old=json.loads((PREVIOUS/'result.json').read_text())
    verified=json.loads((PREVIOUS/'verification.json').read_text())
    boundary=json.loads((PREVIOUS/'boundary.json').read_text())
    bases=json.loads((BASE_SOURCE/'result.json').read_text())
    require(old['complete'] and verified['verified'] and not old['target_graph'],'complete imported branch verdict')
    selected=[r for r in old['cases'] if r['status']=='excluded']
    require([r['index'] for r in selected]==old['excluded']==verified['excluded']==boundary['blue4_excluded'],'exact selected cover')
    base_map={r['index']:r for r in bases['cases'] if r['status']=='open'}
    verify_map={r['index']:r for r in verified['cases']}
    rows=[]
    for r in selected:
        v=verify_map[r['index']];base=base_map[r['index']]
        require(r['replay']['verified'] and v['replay']['verified'] and r['solver_code']==20,'two imported full DRAT replays')
        require(all(r[k]==base[k] for k in ('index','bits','labeled','omitted')),'base identity')
        require(r['base']==base['formula'] and r['base']!=r['formula'],'unrestricted base, never blue4 child')
        rows.append({k:base[k] for k in ('index','bits','labeled','omitted','formula')})
    require(len(rows)==19 and sum(c['labeled'] for c in rows)==13608,'complete selected totals')
    return rows


def clauses():
    # Every four blue-moving links contain a red link: at most three blue.
    rows=list(combinations(range(215,222),4))
    require(len(rows)==35 and len(set(rows))==35,'complete positive four-subset cover')
    return rows


def make(base,output,case):
    require(info(base)==case['formula'],'complete unrestricted base identity')
    nv=34280+10*len(case['omitted']);nc=617382+50*len(case['omitted'])
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'unrestricted base header')
        g.write(f'p cnf {nv} {nc+35}\n'.encode());shutil.copyfileobj(f,g)
        for row in clauses():g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
