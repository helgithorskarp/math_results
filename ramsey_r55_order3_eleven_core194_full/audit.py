#!/usr/bin/env python3
"""Literal full-base and all-fixed-vertex guarded-bound auditor."""
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import json
import hashlib
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
    bases=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation/result.json').read_text())
    branches=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4/result.json').read_text())
    maximal=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_core194_maximal/result.json').read_text())
    need(len(cases)==1 and cases[0]['index']==194,'only full Core194')
    c=cases[0];base=next(r for r in bases['cases'] if r['index']==194);branch=next(r for r in branches['cases'] if r['index']==194)
    need(all(c[k]==base[k] for k in ('index','bits','labeled','omitted','formula')),'unrestricted base identity')
    need(c['formula']==branch['base'] and c['formula']!=branch['formula'],'reject old maximal child')
    need(all(c['formula']['sha256']!=r['formula']['sha256'] for r in maximal['cases']),'reject local classifier and fixed-neighborhood full model')
    need(c['bits']=='100110110110110100' and c['omitted']==[0,1,2,3] and c['labeled']==81,'literal core194 and four anchors')
    return dict(cores=1,labeled=81,indices=[194],untested=[92,97,118,119,124,155,164,168,180,182,185,186,190,191,192,193])


def expected():
    ids=primary();rows=[]
    for f in range(33,43):
        guard=tuple(ids[3*i,f] for i in range(4));links=[ids[3*j,f] for j in range(4,11)]
        rows.extend(guard+c for c in combinations(links,4))
    return rows


def check(base,full,case):
    h=hashlib.sha256()
    with base.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    need(dict(bytes=base.stat().st_size,sha256=h.hexdigest())==case['formula'],'unrestricted base hash')
    rows=expected();need(len(rows)==350 and all(len(c)==8 for c in rows),'ten exact guarded bounds')
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==b'p cnf 34320 617582\n','base header')
        need(g.readline()==b'p cnf 34320 617932\n','strengthened header')
        for line in f:need(g.readline()==line,'entire unrestricted base')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'literal guarded bound')
        need(not g.read(),'exact EOF')
    return dict(entire_unrestricted_base=True,new_variables=0,fixed_vertices_covered=10,guard_red_core_links=4,
        minimum_red_bluecycle_links_if_empty=4,guarded_clauses=350,added_fixed_edge_units=0,variables=34320,clauses=617932)


def truth_tables():
    rows=expected();ids=primary();accepted=[];total=0
    for f in range(33,43):
        variables=[ids[3*i,f] for i in range(11)];block=rows[35*(f-33):35*(f-32)];count=0
        for bits in product((False,True),repeat=11):
            values=dict(zip(variables,bits));holds=all(any(values[v] for v in c) for c in block)
            need(holds==(any(bits[:4]) or sum(bits[4:])>=4),'guarded truth equivalence')
            count+=holds;total+=1
        need(count==1984,'all nonempty signatures retained');accepted.append(count)
    complementary=0;fixed_assignments=0
    for moving in product((False,True),repeat=7):
        for fixed in product((False,True),repeat=9):
            fixed_assignments+=1;degree=3*sum(moving)+sum(fixed);b=7-sum(moving)
            if 18<=degree<=24:
                need(b<=4,'degree window')
                if b==4:need(sum(fixed)==9,'maximal branch transfer')
                if b<=3:complementary+=1;need(sum(moving)>=4,'complementary incidence retained')
    need(fixed_assignments==65536 and complementary==17728,'exact complementary truth domain')
    need(all(211<=v<=320 for row in rows for v in row),'only fixed-to-moving primary IDs')
    return dict(fixed_vertex_truth_assignments=total,accepted_patterns_per_fixed_vertex=accepted,
        nonempty_signature_patterns_retained_per_vertex=1920,empty_signature_patterns_retained_per_vertex=64,
        empty_moving_fixed_assignments=fixed_assignments,degree_admissible_complementary_assignments=complementary)


def controls(cases,base,full,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    branch=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4/result.json').read_text())
    local=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_core194_maximal/result.json').read_text())
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    for name in ('missing_case','changed_core','changed_base','blue4_child_as_base','classifier_as_base','fixed_neighborhood_as_base','other_core'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='changed_core':bad[0]['bits']='0'*18
        if name=='changed_base':bad[0]['formula']['sha256']='0'*64
        if name=='blue4_child_as_base':bad[0]['formula']=next(r['formula'] for r in branch['cases'] if r['index']==194)
        if name=='classifier_as_base':bad[0]['formula']=local['cases'][0]['formula']
        if name=='fixed_neighborhood_as_base':bad[0]['formula']=local['cases'][1]['formula']
        if name=='other_core':bad[0]['index']=180
        reject(name,lambda:check_cases(bad))
    lines=full.read_bytes().splitlines(keepends=True)
    for name in ('lost_base','lost_guarded_clause','wrong_guard_sign','wrong_cycle','unguarded_nonempty_vertex','fixed_edge_unit','wrong_header','extra_empty'):
        bad=lines[:]
        if name=='lost_base':bad.pop(10)
        if name=='lost_guarded_clause':bad.pop()
        if name=='wrong_guard_sign':bad[-350]=bad[-350].replace(b'211',b'-211')
        if name=='wrong_cycle':bad[-350]=bad[-350].replace(b'215',b'225')
        if name=='unguarded_nonempty_vertex':bad[-315]=b'226 227 228 229 0\n'
        if name=='fixed_edge_unit':bad[-1]=b'166 0\n'
        if name=='wrong_header':bad[0]=b'p cnf 34320 617617\n'
        if name=='extra_empty':bad.append(b'0\n')
        path=work/'bad.cnf';path.write_bytes(b''.join(bad));reject(name,lambda:check(base,path,cases[0]))
    contaminated=work/'bad_base.cnf';contaminated.write_bytes(base.read_bytes()+b'166 0\n')
    reject('contaminated_base',lambda:check(contaminated,full,cases[0]));contaminated.unlink();(work/'bad.cnf').unlink()
    return dict(rejected=rejected,cases=check_cases(cases),truth_tables=truth_tables(),formula=check(base,full,cases[0]))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',type=Path,required=True);p.add_argument('--base',type=Path,required=True)
    p.add_argument('--formula',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    r=controls(json.loads(a.cases.read_text()),a.base,a.formula,a.work)
    a.report.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('PASS Core194,ten guarded bounds and16 corruptions')
