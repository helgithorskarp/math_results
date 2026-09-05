#!/usr/bin/env python3
"""Independent literal cuts, complete base-prefix and coverage audit."""
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import json

ROOT=Path(__file__).resolve().parent


def need(ok,why):
    if not ok:raise ValueError(why)


def primary():
    # Recover variable meaning from literal edge orbits under the 43-vertex action.
    def rotation(v):return v if v>=33 else 3*(v//3)+(v%3+1)%3
    left=set(combinations(range(43),2));moving=[];fixed=[];links=[]
    while left:
        e=min(left);orbit={e};f=tuple(sorted(map(rotation,e)))
        while f!=e:orbit.add(f);f=tuple(sorted(map(rotation,f)))
        left-=orbit;rep=min(orbit);a,b=rep
        if a<33 and b<33:
            if a//3!=b//3:moving.append((rep,orbit))
        elif a>=33:fixed.append((rep,orbit))
        else:links.append((rep,orbit))
    moving.sort(key=lambda x:(x[0][0]//3,x[0][1]//3,(x[0][1]-x[0][0])%3))
    fixed.sort();links.sort(key=lambda x:(x[0][1],x[0][0]//3))
    need(len(moving+fixed+links)==320,'primary count')
    return {e:n for n,(_,orbit) in enumerate(moving+fixed+links,1) for e in orbit}



def check_cases(cases):
    old=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_anchor_propagation'/'result.json').read_text())
    boundary=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_noempty_rigidity'/'boundary.json').read_text())
    saved=[c for c in old['cases'] if c['status']=='open']
    need([r['index'] for r in cases]==[r['index'] for r in saved]==boundary['forced_empty_cores'],'complete forced-empty cover')
    witnesses=[]
    for c,s in zip(cases,saved):
        need(all(c[k]==s[k] for k in ('index','bits','labeled','omitted','formula')),'inherited identity')
        red=set();pairs=list(combinations(range(4),2))
        for a,b in combinations(range(12),2):
            i,p=divmod(a,3);j,q=divmod(b,3)
            if i==j or c['bits'][3*pairs.index((i,j))+(q-p)%3]=='1':red.add((a,b))
        need(all(0<sum(e in red for e in combinations(five,2))<10 for five in combinations(range(12),5)),'literal Ramsey core')
        for i in range(4):
            for j in range(4):
                if i==j:continue
                k,l=sorted(set(range(4))-{i,j})
                edge=next(((a,b) for a in range(3*k,3*k+3) for b in range(3*l,3*l+3) if (a,b) not in red),None)
                need(edge is not None,'blue cross-edge supporting pair cut')
                witnesses.append([c['index'],i,j,*edge])
    need(len(cases)==26 and len(witnesses)==312,'complete cut applications')
    return dict(cores=26,labeled=sum(c['labeled'] for c in cases),literal_blue_cross_edges=witnesses)


def expected():
    ids=primary();rows=[(-ids[3*i,33],) for i in range(4)]
    for fixed in combinations(range(33,43),3):
        for red_i in range(4):
            for free_j in range(4):
                if red_i==free_j:continue
                blue=[k for k in range(4) if k not in (red_i,free_j)]
                rows.append(tuple(v for f in fixed for v in (-ids[3*red_i,f],ids[3*blue[0],f],ids[3*blue[1],f])))
    return rows


def check(base,full,case):
    nv=34280+10*len(case['omitted']);nc=615938+50*len(case['omitted']);rows=expected()
    need(len(rows)==1444,'complete consequence tail')
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'base header')
        need(g.readline()==f'p cnf {nv} {nc+1444}\n'.encode(),'full header')
        for line in f:need(g.readline()==line,'entire strengthened base')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'literal consequence clause')
        need(not g.read(),'exact EOF')
    return dict(entire_base=True,new_variables=0,empty_units=4,pair_cuts=1440,variables=nv,clauses=nc+1444)


def truth_tables():
    checked=0
    for i in range(4):
        for j in range(4):
            if i==j:continue
            other=sorted(set(range(4))-{i,j})
            for masks in product(range(16),repeat=3):
                holds=any(not(m&(1<<i)) or m&(1<<other[0]) or m&(1<<other[1]) for m in masks)
                forbidden=all(m in (1<<i,(1<<i)|(1<<j)) for m in masks)
                need(bool(holds)==(not forbidden),'cut truth table including free coordinate')
                checked+=1
    need(checked==49152,'complete truth table')
    return dict(ordered_signature_assignments=checked)


def controls(cases,base,full,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    for name in ('missing_case','wrong_core','false_anchor','changed_base'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='wrong_core':bad[0]['bits']=str(1-int(bad[0]['bits'][0]))+bad[0]['bits'][1:]
        if name=='false_anchor':bad[0]['omitted']=[]
        if name=='changed_base':bad[0]['formula']['sha256']='0'*64
        try:check_cases(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    lines=full.read_bytes().splitlines(keepends=True)
    for name in ('lost_base','lost_empty','wrong_empty','lost_cut','flipped_cut','constrained_free_bit','wrong_header','extra_empty'):
        bad=lines[:]
        if name=='lost_base':bad.pop(10)
        if name=='lost_empty':bad.pop(-1444)
        if name=='wrong_empty':bad[-1444]=b'211 0\n'
        if name=='lost_cut':bad.pop()
        if name=='flipped_cut':bad[-1440]=bad[-1440].replace(b'-211',b'211')
        if name=='constrained_free_bit':bad[-1440]=bad[-1440].replace(b'213',b'212')
        if name=='wrong_header':bad[0]=b'p cnf 34300 617481\n'
        if name=='extra_empty':bad.append(b'0\n')
        path=work/'bad.cnf';path.write_bytes(b''.join(bad))
        try:check(base,path,cases[0])
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    (work/'bad.cnf').unlink()
    return dict(rejected=rejected,cases=check_cases(cases),truth_tables=truth_tables(),formula=check(base,full,cases[0]))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',type=Path,required=True);p.add_argument('--base',type=Path,required=True)
    p.add_argument('--formula',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    answer=controls(json.loads(a.cases.read_text()),a.base,a.formula,a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS complete cover,312 blue edges,49152 assignments and12 corruptions')
