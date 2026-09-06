#!/usr/bin/env python3
"""Exact positive-colouring and exhaustive nine-omission cover checker.

No new producer, selector solver or negative proof is needed for the theorem.
Uses the previous independent monomial geometry routine, hash-pinned here.
"""
import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(ok,why):
    if not ok:raise ValueError(why)


def threshold(n,k):
    # Independently enumerate prefix symbols, then write the backward implications.
    names=[(i,j) for i in range(1,n+1) for j in range(1,min(i,k)+1)]
    z={a:n+t+1 for t,a in enumerate(names)};clauses=[]
    for i,j in names:
        first=[-z[i,j]]
        if (i-1,j) in z:first.append(z[i-1,j])
        clauses.append(first+[i])
        if j>1:
            second=[-z[i,j]]
            if (i-1,j) in z:second.append(z[i-1,j])
            clauses.append(second+[z[i-1,j-1]])
    if k:clauses.append([z[n,k]])
    return n+len(names),clauses


def raw(n,cs):
    return (f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode()


def cover(cuts,small):
    singleton=[next(iter(d)) for d in cuts if len(d)==1]
    require(len(singleton)==len(set(singleton)), 'distinct singleton cuts')
    forced=set(singleton);free=sorted(set(small)-forced);pos={v:i for i,v in enumerate(free)}
    residual=[d for d in cuts if not d&forced]
    masks=[sum(1<<pos[v] for v in d) for d in residual]
    require(all(masks), 'nonempty residual cuts')
    count=0
    for c in combinations(range(len(free)),9):
        omitted=sum(1<<i for i in c)
        require(any(omitted&m==m for m in masks), ('uncovered nine-omission set',[free[i] for i in c]))
        count+=1
    return {'forced':sorted(forced),'free':free,'residual_cuts':len(residual),'nine_sets_checked':count}


def verify(work=None):
    start=time.monotonic()
    for name,digest in json.loads((HERE/'manifest.json').read_text()).items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    path=REPO/'hadwiger_nelson_heule517_joint_interface/verify.py'
    spec=importlib.util.spec_from_file_location('independent_graph',path);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
    points,edges=G.graph()
    L=sorted(v for v,p in enumerate(points) if all(p[a][k]==0 for a in (0,1) for k in [2,3,6,7]));S=sorted(set(range(517))-set(L));ss=set(S)
    require(len(L)==375 and len(S)==142 and len(edges)==2555,'exact support')
    sep=json.loads((REPO/'hadwiger_nelson_heule517_joint_interface/separator.json').read_text())
    require(sep['large']==L and sep['small']==S,'block indexing')
    I=sorted({v for u,w in edges if (u in ss)!=(w in ss) for v in (u,w) if v not in ss})
    require(I==sep['boundary'],'boundary indexing')
    profiles=json.loads((REPO/'hadwiger_nelson_heule517_joint_interface/certificate.json').read_text())['rows']
    prior=json.loads((REPO/'hadwiger_nelson_heule517_family_pilot/certificate.json').read_text())['rows']
    union=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels=[v for v in range(553) if '510' in union['provenance'][v]]
    def seed(row):
        r=prior[row['row']]
        if r['source']=='native':c=r['colouring']
        else:
            if r['source']=='forced':D=[r['index']];text=union['forced_witness'][str(r['index'])]
            else:
                require(r['source']=='family','inherited witness kind');old=union['family'][r['index']];D=old['D'];text=old['witness']
            surviving=sorted(set(range(553))-set(D));require(len(text)==len(surviving),'old colouring length');m=dict(zip(surviving,text));c=''.join(m.get(v,'.') for v in labels)+r['extra']
        require(row['D']==r['D'],'inherited omitted set');return c
    def decode(row):
        if row['kind']=='seed':return seed(row)
        require(row['kind']=='case' and type(row['case']) is int and 0<=row['case']<20,'case identity')
        p=profiles[row['case']];require(len(p['colouring'])==375 and len(row['colouring'])==142,'block witness length')
        out=['.']*517
        for v,c in zip(L,p['colouring']):out[v]=c
        for v,c in zip(S,row['colouring']):out[v]=c
        return ''.join(out)
    def check_row(row):
        c=decode(row);require(len(c)==517 and set(c)<=set('.0123'),'colouring domain')
        D=[v for v,x in enumerate(c) if x=='.'];require(D==row['D'] and set(D)<=ss,'exact small omission set')
        require(all(c[u]=='.' or c[v]=='.' or c[u]!=c[v] for u,v in edges),'proper full union colouring')
        return sum(c[u]!='.' and c[v]!='.' for u,v in edges)
    rows=json.loads((HERE/'certificate.json').read_text())['rows']
    require(len(rows)==206,'final cut count');edge_checks=sum(check_row(r) for r in rows)
    inherited=[{'kind':'seed','row':i,'D':r['D']} for i,r in enumerate(prior) if set(r['D'])<=ss]
    require(len(inherited)==148,'exact initial cut family')
    for row in inherited:check_row(row)
    cuts=[set(r['D']) for r in rows]
    require(all(not a<=b for i,a in enumerate(cuts) for j,b in enumerate(cuts) if i!=j),'cut antichain')
    t=time.monotonic();coverage=cover(cuts,S);cover_seconds=time.monotonic()-t
    require(len(coverage['forced'])==119 and len(coverage['free'])==23 and coverage['nine_sets_checked']==817190,'complete omission cover')
    n,cs=threshold(142,9);spos={v:i for i,v in enumerate(S)}
    cs += [[-spos[v]-1 for v in r['D']] for r in rows];master=raw(n,cs)
    native_checks=0;activation_compared=False
    if work:
        require((work/'master_final.cnf').read_bytes()==master and (work/'master_residual.cnf').read_bytes()==master,'actual final CNF')
        require(json.loads((work/'certificate.json').read_text())=={'rows':rows},'actual final certificate')
        native=json.loads((work/'native_witnesses.json').read_text());require(len(native)==222,'native witness count')
        native_checks=sum(check_row(r) for r in native)
        small_edges=[e for e in edges if set(e)<=ss];cross=[e for e in edges if (e[0] in ss)!=(e[1] in ss)]
        for k,p in enumerate(profiles):
            fixed=dict(zip(I,map(int,p['pattern'])))
            ac=[[-569-i]+[4*i+c+1 for c in range(4)] for i in range(142)]
            for u,v in small_edges:
                for c in range(4):ac.append([-4*spos[u]-c-1,-4*spos[v]-c-1])
            for u,v in cross:
                if u in fixed:ac.append([-4*spos[v]-fixed[u]-1])
                else:ac.append([-4*spos[u]-fixed[v]-1])
            require((work/f'activation_{k:02d}.cnf').read_bytes()==raw(710,ac),'actual case activation formula')
        activation_compared=True
    return {'status':'ALL SUBGRAPHS WITH AT MOST133 SMALL VERTICES ARE FOUR-COLOURABLE',
            'full_H517_family_closed':False,'fixed_L_at_most508_family_closed':True,
            'small_vertices_needed_by_any_nonfour_subgraph_at_least':134,
            'record_improvement':False,'vertices':517,'large_vertices':375,'small_vertices':142,
            'unit_edges':2555,'exact_pair_checks':133386,'final_cuts':len(rows),
            'final_witness_edge_checks':edge_checks,'inherited_rows_checked':len(inherited),
            'native_witnesses_checked':222 if work else 0,'native_witness_edge_checks':native_checks,
            'activation_formulas_compared':20 if activation_compared else 0,
            'master_variables':n,'master_clauses':len(cs),'master_sha256':sha256(master).hexdigest(),
            'coverage':coverage,'cover_seconds':cover_seconds,'seconds':time.monotonic()-start,
            'negative_solver_proof_required':False,'native_solver_used_by_checker':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path);ap.add_argument('--report',type=Path);args=ap.parse_args()
    result=verify(args.work)
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
