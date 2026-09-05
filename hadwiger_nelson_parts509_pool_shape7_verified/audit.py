#!/usr/bin/env python3
"""Audit generated witnesses with independent integer coordinates and bitsets.

Does not import this contribution's verifier or its exact-geometry module.
The second geometry implementation comes from the committed independent
two-triple-budget review and uses the scale-96 integer Parts table.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def main():
    if not __debug__:raise RuntimeError('Run without Python optimization flags')
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
    facts=json.loads((HERE/'expected.json').read_text());n=facts['killing_clauses']
    source=REPO/'hadwiger_nelson_parts509_two_triple_budgets_review3/independent_check.py'
    spec=importlib.util.spec_from_file_location('independent_geometry',source)
    geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
    denominator,points=geo.read_all_points()
    U=sorted(json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())['W_S'])
    L=list(range(374));vertices=L+U;pos={v:i for i,v in enumerate(U)};ls=set(L)
    assert len(vertices)==len({points[v] for v in vertices})==677
    edges=geo.unit_edges(points,vertices,denominator);assert len(edges)==3400
    adj=[0]*len(U);cross=[[] for _ in U]
    for a,b in edges:
        if a in pos and b in pos:adj[pos[a]]|=1<<pos[b];adj[pos[b]]|=1<<pos[a]
        elif a in ls and b in pos:cross[pos[b]].append(a)
        elif b in ls and a in pos:cross[pos[a]].append(b)
    wl=[r['witness_colouring_L'] for r in json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())['classes']]
    forb=[]
    for w in wl:
        assert len(w)==374 and set(w)<=set('0123')
        assert all(w[a]!=w[b] for a,b in edges if a in ls and b in ls)
        row=[]
        for ns in cross:
            mask=0
            for l in ns:mask|=1<<int(w[l])
            row.append(mask)
        forb.append(row)
    with (HERE/'killing_clauses.cnf').open() as f:
        assert f.readline().split()==['p','cnf','303',str(n)]
        killing=[tuple(map(int,line.split()[:-1])) for line in f]
    assert len(killing)==n and len(set(killing))==n
    hints=json.loads((HERE/'interface_hints.json').read_text());seen=set()
    for line in (args.work/'colourings.jsonl').open():
        r=json.loads(line);i,p,c=r['i'],r['p'],r['c']
        assert type(i) is int and 0<=i<len(killing) and i not in seen;seen.add(i)
        assert type(p) is int and 0<=p<len(wl) and p==hints[i]
        assert len(c)==303 and set(c)<=set('.0123')
        masks=[0,0,0,0];deleted=[]
        for j,ch in enumerate(c):
            if ch=='.':deleted.append(j+1)
            else:masks[int(ch)]|=1<<j
        assert tuple(deleted)==killing[i]
        for j,ch in enumerate(c):
            if ch!='.':assert not(adj[j]&masks[int(ch)]) and not(forb[p][j]&(1<<int(ch)))
    assert seen==set(range(n))
    facts=json.loads((HERE/'expected.json').read_text())
    cnf=args.work/'master.cnf';assert hashlib.sha256(cnf.read_bytes()).hexdigest()==facts['cnf_sha256']
    with cnf.open() as f:
        assert f.readline().split()==['p','cnf',str(facts['variables']),str(facts['clauses'])]
        for c in killing:assert tuple(map(int,f.readline().split()))==c+(0,)
    result=dict(status='independent integer geometry and all positive certificates VERIFIED',
                points=677,unit_edges=3400,denominator=denominator,killing_clauses=len(seen),
                exact_edges_sha256=geo.edge_digest(edges),master_cnf_sha256=facts['cnf_sha256'],
                geometry_checker_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (args.work/'independent_audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
