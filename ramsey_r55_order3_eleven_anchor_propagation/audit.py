#!/usr/bin/env python3
"""Independent literal application and complete formula auditor; no producer import."""
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import json


def need(ok, why):
    if not ok:raise ValueError(why)


def application(case):
    bits=case['bits'];need(len(bits)==18 and set(bits)<={'0','1'},'18 binary bits')
    pairs=list(combinations(range(4),2));red=set()
    for a,b in combinations(range(12),2):
        i,s=divmod(a,3);j,t=divmod(b,3)
        if i==j or bits[3*pairs.index((i,j))+(t-s)%3]=='1':red.add((a,b))
    for five in combinations(range(12),5):
        colors={e in red for e in combinations(five,2)}
        need(len(colors)==2,'locally invalid core')
    omitted=[]
    for i in range(4):
        vertices=[a for a in range(12) if a//3!=i]
        if not any(all(e not in red for e in combinations(three,2)) for three in combinations(vertices,3)):omitted.append(i)
    need(case['omitted']==omitted and bool(omitted),'all and only blue-free complementary triples')
    return omitted


def check_cases(cases):
    root=Path(__file__).resolve().parent.parent
    anchors=json.loads((root/'ramsey_r55_order3_eleven_anchor_equality'/'anchors.json').read_text())
    bases={r['index']:r for r in json.loads((root/'ramsey_r55_order3_eleven_residual_sweep'/'result.json').read_text())['cases']}
    need([r['index'] for r in cases]==[r['index'] for r in anchors['residual']],'complete entrywise case order')
    counts={};applications=0
    for row,old in zip(cases,anchors['residual']):
        need(row['bits']==old['bits'] and row['labeled']==old['labeled'],'inherited core identity')
        need(row['base']==bases[row['index']]['formula'] and row['bits']==bases[row['index']]['bits'],'inherited base identity')
        g=len(application(row));applications+=g;counts[str(g)]=counts.get(str(g),0)+1
    need(len(cases)==34 and applications==56 and sum(r['labeled'] for r in cases)==24057,'residual totals')
    return dict(cases=34,labeled=24057,applications=applications,application_histogram=counts)


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


def check_base(parent, base, case):
    ids=primary();units=[]
    for q,(i,j) in enumerate(combinations(range(4),2)):
        for d in range(3):units.append(ids[3*i,3*j+d]*(1 if case['bits'][3*q+d]=='1' else -1))
    with parent.open('rb') as f,base.open('rb') as g:
        need(f.readline()==b'p cnf 34280 615920\n','parent header')
        need(g.readline()==b'p cnf 34280 615938\n','base header')
        for line in f:need(g.readline()==line,'entire parent prefix')
        for unit in units:need(g.readline()==f'{unit} 0\n'.encode(),'literal core unit')
        need(not g.read(),'base EOF')
    return dict(entire_parent=True,core_units=18,variables=34280,clauses=615938)


def check(base, full, case):
    omitted=application(case);ids=primary();expected=[];fresh=34280
    for i in omitted:
        indicators=[]
        for f in range(33,43):
            fresh+=1;indicators.append(fresh)
            target=[ids[3*j,f] for j in range(4) if j!=i]
            for v in target:expected.append((-fresh,-v))
            expected.append(tuple([fresh]+target))
        expected.extend(combinations(indicators,9))
        # Producer orders nine-subsets by their omitted member, not lex order.
        expected[-10:]=list(reversed(expected[-10:]))
    need(fresh==34280+10*len(omitted) and len(expected)==50*len(omitted),'fresh auxiliary range')
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==b'p cnf 34280 615938\n','base header')
        need(g.readline()==f'p cnf {fresh} {615938+len(expected)}\n'.encode(),'full header')
        for line in f:need(g.readline()==line,'entire base prefix')
        for row in expected:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'intrinsic gate/cardinality clause')
        need(not g.read(),'full EOF')
    return dict(entire_base=True,applications=omitted,new_variables=10*len(omitted),new_clauses=len(expected),variables=fresh,clauses=615938+len(expected))


def truth_tables():
    for assignment in product((False,True),repeat=4):
        u,*links=assignment
        holds=all(not u or not x for x in links) and (u or any(links))
        need(holds==(u==not_any(links)),'indicator truth table')
    cards=list(combinations(range(10),9))
    for bits in product((False,True),repeat=10):
        holds=all(any(bits[j] for j in row) for row in cards)
        need(holds==(sum(bits)>=2),'at-least-two truth table')
    return dict(indicator_assignments=16,cardinality_assignments=1024)


def not_any(values):return not any(values)


def controls(parent, base, full, cases, work):
    work.mkdir(parents=True,exist_ok=True);case=cases[0];need(case['index']==88,'control core88')
    rejected=[]
    for name in ('missing_case','missing_anchor','false_anchor','wrong_core'):
        bad=copy.deepcopy(cases)
        if name=='missing_case':bad.pop()
        if name=='missing_anchor':bad[0]['omitted']=[]
        if name=='false_anchor':bad[0]['omitted']=[1]
        if name=='wrong_core':bad[0]['bits']='1'+bad[0]['bits'][1:]
        try:check_cases(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed cases '+name)
    lines=full.read_text().splitlines(keepends=True)
    for name in ('lost_gate','wrong_gate_sign','wrong_triple','lost_count_clause','aux_overlap','lost_base','extra_empty','wrong_header'):
        bad=lines[:]
        if name=='lost_gate':bad.pop(-50)
        if name=='wrong_gate_sign':bad[-50]=bad[-50].replace('-34281','34281')
        if name=='wrong_triple':bad[-50]=bad[-50].replace('-212','-211')
        if name=='lost_count_clause':bad.pop()
        if name=='aux_overlap':bad[-50]=bad[-50].replace('34281','34280')
        if name=='lost_base':bad.pop(10)
        if name=='extra_empty':bad.append('0\n')
        if name=='wrong_header':bad[0]='p cnf 34280 615988\n'
        path=work/'bad.cnf';path.write_text(''.join(bad))
        try:check(base,path,case)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed formula '+name)
    (work/'bad.cnf').unlink()
    return dict(rejected=rejected,cases=check_cases(cases),truth_tables=truth_tables(),
                base=check_base(parent,base,case),formula=check(base,full,case))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True)
    p.add_argument('--base',type=Path,required=True);p.add_argument('--formula',type=Path,required=True)
    p.add_argument('--cases',type=Path,required=True);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    answer=controls(a.parent,a.base,a.formula,json.loads(a.cases.read_text()),a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    print('PASS all34 cases, intrinsic gate/count truth tables and12 corruptions')
