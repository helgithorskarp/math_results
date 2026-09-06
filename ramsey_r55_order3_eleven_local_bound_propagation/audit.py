#!/usr/bin/env python3
"""Independent full-base, literal attachment and necessary-bound audit."""
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
    bases=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'/'result.json').read_text())
    branches=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4'/'result.json').read_text())
    local=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24'/'result.json').read_text())
    expected_indices=[124,155,159,168,180]
    need([r['index'] for r in cases]==expected_indices==local['local_excluded'],'exact five-case cover')
    saved={c['index']:c for c in bases['cases'] if c['status']=='open'}
    branch_map={c['index']:c for c in branches['cases']};local_map={c['index']:c for c in local['cases']}
    for c in cases:
        s=saved[c['index']];b=branch_map[c['index']];h=local_map[c['index']]
        need(all(c[k]==s[k] for k in ('index','bits','labeled','omitted','formula')),'unrestricted full-base identity')
        need(all(c[k]==h[k] for k in ('index','bits','labeled','omitted')),'local obstruction is for this core')
        need(c['formula']==b['base'] and c['formula']!=b['formula'],'reject maximal-branch child')
        need(c['formula']['sha256']!=h['formula']['sha256'],'reject local24 formula')
    need(len(cases)==5 and sum(c['labeled'] for c in cases)==2268,'complete selected totals')
    return dict(cores=5,labeled=2268,indices=expected_indices,untested=[92,97,118,119,164,182,185,186,190,191,192,193,194])


def expected():
    ids=primary()
    return list(combinations([ids[3*j,33] for j in range(4,11)],4))


def check(base,full,case):
    # Independently reject a blue4 branch even when full preserves that bad prefix.
    h=hashlib.sha256()
    with base.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    need(dict(bytes=base.stat().st_size,sha256=h.hexdigest())==case['formula'],'unrestricted base hash')
    nv=34280+10*len(case['omitted']);nc=617382+50*len(case['omitted']);rows=expected()
    need(len(rows)==35,'all positive four-subsets')
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'base header')
        need(g.readline()==f'p cnf {nv} {nc+35}\n'.encode(),'child header')
        for line in f:need(g.readline()==line,'entire unrestricted base')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'literal bound clause')
        need(not g.read(),'exact EOF')
    return dict(entire_unrestricted_base=True,new_variables=0,minimum_red_moving_links=4,
        positive_four_subset_clauses=35,added_fixed_edge_units=0,variables=nv,clauses=nc+35)


def truth_tables():
    rows=expected();cards=0;accepted=0;fixed_assignments=0;admissible=0
    for moving in product((False,True),repeat=7):
        assignment=dict(zip(range(215,222),moving))
        holds=all(any(assignment[v] for v in row) for row in rows)
        need(holds==(7-sum(moving)<=3),'at most three blue, every assignment')
        cards+=1;accepted+=holds
        for fixed in product((False,True),repeat=9):
            fixed_assignments+=1
            need(all(v not in range(166,175) for row in rows for v in row),'fixed edges absent from new tail')
            red_degree=3*sum(moving)+sum(fixed)
            if 18<=red_degree<=24:
                b=7-sum(moving)
                need(b<=4,'inherited degree upper bound')
                if b==4:need(sum(fixed)==9,'imported maximal branch is exhaustive')
                if b<=3:admissible+=1;need(holds,'no legal complementary incidence lost')
    need(cards==128 and accepted==64 and fixed_assignments==65536,'complete truth domain')
    return dict(moving_assignments=cards,bound_satisfying_patterns=accepted,moving_fixed_assignments=fixed_assignments,
        degree_admissible_complementary_assignments=admissible)


def controls(cases,base,full,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    branches=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_blue4'/'result.json').read_text())
    local=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24'/'result.json').read_text())
    for name in ('missing_case','changed_core','changed_base','blue4_child_as_base','local24_as_base','unproved_case'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='changed_core':bad[0]['bits']=str(1-int(bad[0]['bits'][0]))+bad[0]['bits'][1:]
        if name=='changed_base':bad[0]['formula']['sha256']='0'*64
        if name=='blue4_child_as_base':bad[0]['formula']=next(r['formula'] for r in branches['cases'] if r['index']==cases[0]['index'])
        if name=='local24_as_base':bad[0]['formula']=next(r['formula'] for r in local['cases'] if r['index']==cases[0]['index'])
        if name=='unproved_case':bad[0]['index']=194
        try:check_cases(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    lines=full.read_bytes().splitlines(keepends=True)
    for name in ('lost_base','lost_bound','wrong_sign','wrong_moving_triangle','fixed_edge_unit','wrong_header','extra_empty'):
        bad=lines[:]
        if name=='lost_base':bad.pop(10)
        if name=='lost_bound':bad.pop()
        if name=='wrong_sign':bad[-35]=bad[-35].replace(b'215',b'-215')
        if name=='wrong_moving_triangle':bad[-35]=bad[-35].replace(b'215',b'214')
        if name=='fixed_edge_unit':bad[-1]=b'166 0\n'
        if name=='wrong_header':bad[0]=b'p cnf 34300 617516\n'
        if name=='extra_empty':bad.append(b'0\n')
        path=work/'bad.cnf';path.write_bytes(b''.join(bad))
        try:check(base,path,cases[0])
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    # A complete but branch-restricted base, even preserved literally, must fail.
    b=base.read_bytes().splitlines(keepends=True);header=b[0].split()
    b[0]=f'p cnf {int(header[2])} {int(header[3])+1}\n'.encode();b.append(b'166 0\n')
    wrongbase=work/'wrongbase.cnf';wrongbase.write_bytes(b''.join(b))
    try:check(wrongbase,full,cases[0])
    except ValueError:rejected.append('contaminated_base')
    else:raise ValueError('accepted contaminated base')
    wrongbase.unlink();(work/'bad.cnf').unlink()
    return dict(rejected=rejected,cases=check_cases(cases),truth_tables=truth_tables(),formula=check(base,full,cases[0]))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',type=Path,required=True);p.add_argument('--base',type=Path,required=True)
    p.add_argument('--formula',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    answer=controls(json.loads(a.cases.read_text()),a.base,a.formula,a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS5 full cases,128 moving and65536 moving/fixed assignments,14 corruptions')
