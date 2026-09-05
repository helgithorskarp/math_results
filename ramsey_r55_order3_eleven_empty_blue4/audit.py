#!/usr/bin/env python3
"""Independent full-base, literal attachment and maximal-degree-branch audit."""
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
    old=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'/'result.json').read_text())
    boundary=json.loads((ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'/'boundary.json').read_text())
    saved=[c for c in old['cases'] if c['status']=='open']
    need([r['index'] for r in cases]==[r['index'] for r in saved]==boundary['remaining_open'],'complete residual cover')
    for c,s in zip(cases,saved):need(all(c[k]==s[k] for k in ('index','bits','labeled','omitted','formula')),'inherited core/base identity')
    need(len(cases)==25 and sum(c['labeled'] for c in cases)==15957,'complete totals')
    return dict(cores=25,labeled=15957,indices=[c['index'] for c in cases])


def expected():
    ids=primary();moving=[ids[3*j,33] for j in range(4,11)]
    rows=list(combinations(moving,5))
    rows.extend(tuple(-v for v in four) for four in combinations(moving,4))
    rows.extend((ids[33,f],) for f in range(34,43))
    return rows


def check(base,full,case):
    nv=34280+10*len(case['omitted']);nc=617382+50*len(case['omitted']);rows=expected()
    need(len(rows)==65,'complete hypothesis/consequence tail')
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==f'p cnf {nv} {nc}\n'.encode(),'base header')
        need(g.readline()==f'p cnf {nv} {nc+65}\n'.encode(),'child header')
        for line in f:need(g.readline()==line,'entire inherited base')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'literal branch clause')
        need(not g.read(),'exact EOF')
    return dict(entire_base=True,new_variables=0,exact_red_moving_links=3,
        lower_clauses=21,upper_clauses=35,red_fixed_units=9,variables=nv,clauses=nc+65)


def truth_tables():
    cards=0;accepted=[];degrees=0;extremal=0
    for moving in product((False,True),repeat=7):
        holds=all(any(moving[i] for i in five) for five in combinations(range(7),5)) and all(not all(moving[i] for i in four) for four in combinations(range(7),4))
        need(holds==(sum(moving)==3),'cardinality truth table')
        cards+=1
        if holds:accepted.append([i for i,x in enumerate(moving) if not x])
        for fixed in product((False,True),repeat=9):
            red_degree=3*sum(moving)+sum(fixed);blue_degree=42-red_degree;blue_cycles=7-sum(moving)
            if 18<=red_degree<=24:
                need(blue_cycles<=4,'blue moving-cycle upper bound')
                if blue_cycles==4:
                    need(all(fixed) and red_degree==18 and blue_degree==24,'maximal branch saturation')
                    extremal+=1
            degrees+=1
    need(cards==128 and degrees==65536 and extremal==35,'complete arithmetic domain')
    need(sorted(accepted)==list(map(list,combinations(range(7),4))),'all35 labeled blue-four choices')
    return dict(cardinality_assignments=cards,degree_assignments=degrees,admissible_blue_four_patterns=35)


def controls(cases,base,full,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    for name in ('missing_case','changed_core','changed_base'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='changed_core':bad[0]['bits']=str(1-int(bad[0]['bits'][0]))+bad[0]['bits'][1:]
        if name=='changed_base':bad[0]['formula']['sha256']='0'*64
        try:check_cases(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    lines=full.read_bytes().splitlines(keepends=True)
    for name in ('lost_base','lost_lower','wrong_lower_sign','lost_upper','wrong_moving_triangle','lost_fixed','wrong_fixed_edge','wrong_header','extra_empty'):
        bad=lines[:]
        if name=='lost_base':bad.pop(10)
        if name=='lost_lower':bad.pop(-65)
        if name=='wrong_lower_sign':bad[-65]=bad[-65].replace(b'215',b'-215')
        if name=='lost_upper':bad.pop(-44)
        if name=='wrong_moving_triangle':bad[-65]=bad[-65].replace(b'215',b'214')
        if name=='lost_fixed':bad.pop()
        if name=='wrong_fixed_edge':bad[-9]=b'175 0\n'
        if name=='wrong_header':bad[0]=b'p cnf 34300 617546\n'
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
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS all25 cases,35 labeled choices,65536 degree assignments and12 corruptions')
