#!/usr/bin/env python3
"""Independent literal-core, multiset-cover and entire-formula auditor.
No import from the multiplicity or formula producers.
"""
from itertools import combinations,combinations_with_replacement
from pathlib import Path
import argparse
import copy
import json

ROOT=Path(__file__).resolve().parent


def need(ok,why):
    if not ok:raise ValueError(why)


def check_cover(data):
    old=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_anchor_propagation'/'result.json').read_text())
    residual=[r for r in old['cases'] if r['status']=='open']
    need([r['index'] for r in data['cores']]==[r['index'] for r in residual],'complete residual cover')
    raw_total=0;hist={};closed=[];survivors=[]
    for row,saved in zip(data['cores'],residual):
        need(all(row[k]==saved[k] for k in ('index','bits','labeled')),'literal core identity')
        matrix=[[False]*12 for _ in range(12)];offset=0
        for i in range(4):
            for a,b in combinations(range(3*i,3*i+3),2):matrix[a][b]=matrix[b][a]=True
        for i,j in combinations(range(4),2):
            for shift in range(3):
                for s in range(3):
                    a=3*i+s;b=3*j+(s+shift)%3
                    matrix[a][b]=matrix[b][a]=saved['bits'][offset+shift]=='1'
            offset+=3
        need(all(0<sum(matrix[a][b] for a,b in combinations(t,2))<10 for t in combinations(range(12),5)),'literal Ramsey core')
        good=[]
        for omitted in range(4):
            vertices=[v for v in range(12) if v//3!=omitted]
            if all(any(matrix[a][b] for a,b in combinations(t,2)) for t in combinations(vertices,3)):good.append(omitted)
        need(good==row['good']==saved['omitted'],'all blue-free complements')
        need([w['omitted'] for w in row['red_k4_witnesses']]==good,'complete K4 witness set')
        for w in row['red_k4_witnesses']:
            t=w['red_k4'];need(len(set(t))==4 and all(0<=v<12 and v//3!=w['omitted'] for v in t),'K4 vertex support')
            need(all(matrix[a][b] for a,b in combinations(t,2)),'literal red K4 witness')
        g=len(good);hist[str(g)]=hist.get(str(g),0)+1
        singles=[1+int(i in good) for i in range(4)];need(row['singletons']==singles,'forced singleton counts')
        beginning=[1<<i for i in range(4) for _ in range(singles[i])]
        large=[m for m in range(1,16) if m not in (1,2,4,8)];survive=[];raw=0
        for tail in combinations_with_replacement(large,10-len(beginning)):
            raw+=1;masks=beginning+list(tail)
            if any(sum(bool(m&(1<<i)) for m in masks)>4 for i in range(4)):continue
            if any(all(m&(1<<j) for j in range(4) if j!=i) for i in good for m in masks):continue
            if any(masks.count(1<<i)+masks.count((1<<i)|(1<<j))>3 for i,j in ((i,j) for i in range(4) for j in range(4) if i!=j)):continue
            valid=True
            for i in set(range(4))-set(good):
                positions=[j for j in range(4) if j!=i]
                projected=[tuple(int(bool(m&(1<<j))) for j in positions) for m in masks]
                expected=[(0,0,0),(1,0,0),(1,0,0),(0,1,0),(0,1,0),(0,0,1),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
                if sorted(projected)!=sorted(expected):valid=False;break
            if valid:survive.append(sorted(masks))
        survive.sort();need(raw==row['raw_completions'] and survive==row['profiles'],'independent multiset enumeration')
        raw_total+=raw
        if survive:survivors.append(row['index'])
        else:closed.append(row['index'])
    need(hist=={'1':7,'2':18,'4':1} and raw_total==39105==data['raw_completions'],'complete arithmetic domain')
    need(closed==data['arithmetically_closed'] and survivors==[194],'exact arithmetic boundary')
    pairs=[3,5,6,9,10,12]
    expected=sorted(sorted([1,1,2,2,4,4,8,8,a,b]) for a,b in combinations(pairs,2))
    actual=next(r['profiles'] for r in data['cores'] if r['index']==194)
    need(actual==expected,'all fifteen distinct-pair profiles')
    need(len(data['cases'])==15,'complete case count')
    for n,(case,masks) in enumerate(zip(data['cases'],expected)):
        need(case['index']==n and case['core']==194 and case['masks']==masks,'case identity')
        words=sorted([[int(bool(m&(1<<i))) for i in range(4)] for m in masks])
        need(case['prefixes']==words,'lexicographic four-bit order')
    return dict(cores=26,labeled=sum(r['labeled'] for r in residual),raw_completions=raw_total,
        good_count_histogram=hist,arithmetically_closed=closed,surviving_core=194,complete_cases=15)


def primary_links():
    # Recover all primary variable IDs from unordered edge orbits of the actual action.
    def rotate(v):return v if v>=33 else 3*(v//3)+(v%3+1)%3
    left=set(combinations(range(43),2));moving=[];fixed=[];links=[]
    while left:
        e=min(left);orbit={e};f=tuple(sorted(map(rotate,e)))
        while f!=e:orbit.add(f);f=tuple(sorted(map(rotate,f)))
        left-=orbit;a,b=min(orbit)
        if b<33:
            if a//3!=b//3:moving.append((min(orbit),orbit))
        elif a>=33:fixed.append((min(orbit),orbit))
        else:links.append((min(orbit),orbit))
    moving.sort(key=lambda r:(r[0][0]//3,r[0][1]//3,(r[0][1]-r[0][0])%3));fixed.sort();links.sort(key=lambda r:(r[0][1],r[0][0]//3))
    need(len(moving+fixed+links)==320,'primary orbit count')
    return {edge:n for n,(_,orbit) in enumerate(moving+fixed+links,1) for edge in orbit}


def check_formula(base,formula,case):
    ids=primary_links();words=sorted(tuple(bool(m&(1<<i)) for i in range(4)) for m in case['masks'])
    units=[ids[3*i,f]*(1 if bit else -1) for f,word in zip(range(33,43),words) for i,bit in enumerate(word)]
    need(len(units)==40,'forty units')
    with base.open('rb') as f,formula.open('rb') as g:
        need(f.readline()==b'p cnf 34320 616138\n','base header')
        need(g.readline()==b'p cnf 34320 616178\n','formula header')
        for line in f:need(line==g.readline(),'entire strengthened base prefix')
        for unit in units:need(g.readline()==f'{unit} 0\n'.encode(),'literal fixed-signature unit')
        need(not g.read(),'exact EOF')
    return dict(entire_base=True,primary_units=40,new_variables=0,variables=34320,clauses=616178)


def controls(data,base,formula,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    for name in ('missing_core','wrong_good','false_k4','missing_profile','wrong_singletons','wrong_prefix'):
        bad=copy.deepcopy(data)
        if name=='missing_core':bad['cores'].pop(0)
        if name=='wrong_good':bad['cores'][0]['good']=[]
        if name=='false_k4':bad['cores'][0]['red_k4_witnesses'][0]['red_k4']=[0,0,0,0]
        if name=='missing_profile':bad['cases'].pop()
        if name=='wrong_singletons':bad['cores'][0]['singletons'][0]+=1
        if name=='wrong_prefix':bad['cases'][0]['prefixes'][0][0]^=1
        try:check_cover(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    lines=formula.read_bytes().splitlines(keepends=True)
    for name in ('lost_base','lost_unit','flipped_unit','wrong_vertex','wrong_header','extra_empty'):
        bad=lines[:]
        if name=='lost_base':bad.pop(20)
        if name=='lost_unit':bad.pop()
        if name=='flipped_unit':bad[-40]=b'211 0\n'
        if name=='wrong_vertex':bad[-40]=b'-212 0\n'
        if name=='wrong_header':bad[0]=b'p cnf 34320 616177\n'
        if name=='extra_empty':bad.append(b'0\n')
        path=work/'bad.cnf';path.write_bytes(b''.join(bad))
        try:check_formula(base,path,data['cases'][0])
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted '+name)
    (work/'bad.cnf').unlink()
    return dict(rejected=rejected,cover=check_cover(data),formula=check_formula(base,formula,data['cases'][0]))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--classification',type=Path,required=True)
    p.add_argument('--base',type=Path,required=True);p.add_argument('--formula',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    answer=controls(json.loads(a.classification.read_text()),a.base,a.formula,a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS literal cores, independent arithmetic cover and twelve corruptions')
