#!/usr/bin/env python3
"""Standalone local proof/witness check and independent complete-formula auditor."""
from itertools import combinations,product
from pathlib import Path
import argparse
import copy
import hashlib
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




def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def red_core():
    ids=primary();core_ids=list(range(1,10))+list(range(31,37))+list(range(58,61))
    colors=dict(zip(core_ids,map(int,'100110110110110100')))
    return {e for e in combinations(range(12),2) if e[0]//3==e[1]//3 or colors[ids[e]]==1}


def proof(cert):
    need(cert['index']==194 and cert['bits']=='100110110110110100','literal core194')
    need(cert['empty_pair']==[12,13] and cert['third_fixed']==14,'literal local fixed vertices')
    rows=cert['forbidden_common_blue_signatures'];need([r['mask'] for r in rows]==list(range(16)),'all sixteen signatures')
    core=red_core();blue=0;red=0
    for r in rows:
        mask=r['mask'];edges=core | {(a,14) for a in range(12) if mask&(1<<(a//3))}
        q=r['vertices'];need(len(q)==len(set(q))==5 and all(0<=a<15 for a in q),'five distinct local vertices')
        need(r['color'] in ('red','blue'),'witness color')
        wanted=r['color']=='red'
        need(all((tuple(sorted(e)) in edges)==wanted for e in combinations(q,2)),'literal monochromatic K5 witness')
        need(wanted==(mask.bit_count()>=3),'red or blue signature obstruction')
        if wanted:need(14 in q and all(a<12 or a==14 for a in q),'red-neighborhood K4 plus third vertex');red+=1
        else:need({12,13,14}<=set(q),'blue empty pair and common fixed neighbor');blue+=1
    need(red==5 and blue==11,'all high and low signature cases')
    return dict(signature_masks=16,red_obstructions=red,blue_obstructions=blue,literal_witness_pairs=160)


def fixture(path,n,pair_red):
    lines=path.read_text().splitlines();need(lines and lines[0]==str(n),'fixture order')
    edges=[tuple(map(int,line.split())) for line in lines[1:]]
    need(len(edges)==len(set(edges)) and all(len(e)==2 and 0<=e[0]<e[1]<n for e in edges),'literal edge list')
    red=set(edges);need({e for e in red if e[1]<12}==red_core(),'fixture exact core')
    need(all((a,f) not in red for a in range(12) for f in range(12,n)),'empty signatures')
    need(((12,13) in red)==pair_red,'fixture pair color')
    count=0
    for q in combinations(range(n),5):
        count+=1;need(len({e in red for e in combinations(q,2)})==2,'fixture monochromatic K5')
    def rotate(v):return v if v>=12 else 3*(v//3)+(v%3+1)%3
    for a,b in combinations(range(n),2):
        need(((a,b) in red)==(tuple(sorted((rotate(a),rotate(b)))) in red),'fixture order-three action')
    common=[f for f in range(14,n) if (12,f) not in red and (13,f) not in red]
    need(common==([] if n==14 else [14]),'exact common blue fixed neighbors')
    need(len(red)==(42 if n==14 else 43),'red edge count')
    return dict(vertices=n,red_edges=len(red),five_sets_checked=count,pair_red=pair_red,common_blue_fixed=common)


def local(cert,fixtures):
    return dict(proof=proof(cert),blue_pair=fixture(fixtures/'blue_pair14.edges',14,False),red_pair_counterexample=fixture(fixtures/'red_pair15.edges',15,True))


def check_cases(cases):
    need(cases==[dict(id='blue',index=194,pair_red=False),dict(id='red',index=194,pair_red=True)],'complete two-color partition')
    need(primary()[33,34]==166,'literal first empty edge')
    return dict(cases=2,whole_cores=1,labeled=81,first_empty_edge=[33,34],primary=166)


def expected(case):
    ids=primary();need(case['id'] in ('blue','red') and case['pair_red']==(case['id']=='red'),'color label')
    if case['pair_red']:return [(ids[33,34],)]
    return [(-ids[33,34],)]+[(ids[33,f],ids[34,f]) for f in range(35,43)]


def check(base,full,case):
    need(sha(base)==dict(bytes=24968424,sha256='214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4'),'entire multiple-empty base identity')
    ids=primary();inherited={(' '.join(map(str,(ids[33,34],ids[3*i,33],ids[3*i,34])))+' 0\n').encode() for i in range(4,11)}
    need(len(inherited)==7,'seven inherited moving-cycle prohibitions');found=set();tail=expected(case)
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==b'p cnf 34320 617936\n','base header')
        need(g.readline()==('p cnf 34320 '+str(617936+len(tail))+'\n').encode(),'child header')
        for line in f:
            need(g.readline()==line,'entire multiple base retained')
            if line in inherited:found.add(line)
        for row in tail:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'exact new full clause')
        need(not g.read(),'exact EOF')
    need(found==inherited,'all seven moving-cycle clauses already in base')
    return dict(entire_multiple_base=True,variables=34320,clauses=617936+len(tail),new_pair_units=1,new_common_fixed_clauses=len(tail)-1,inherited_blue_cycle_clauses=7,new_variables=0,new_normalizers=0)


def truth():
    blue=0;red=0;total=0
    for p in (False,True):
        for contacts in product((False,True),repeat=16):
            total+=1
            implication=p or all(contacts[2*k] or contacts[2*k+1] for k in range(8))
            holds_blue=(not p) and all(contacts[2*k] or contacts[2*k+1] for k in range(8))
            holds_red=p
            need((holds_blue or holds_red)==implication and not(holds_blue and holds_red),'guarded full incidence partition')
            blue+=holds_blue;red+=holds_red
    need(total==131072 and blue==6561 and red==65536,'complete incidence truth table')
    return dict(pair_fixed_incidence_assignments=total,accepted_blue=blue,accepted_red=red)


def controls(cert,cases,base,fixtures,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    for name in ('missing_signature','bad_witness','wrong_color','wrong_core','wrong_pair'):
        bad=copy.deepcopy(cert)
        if name=='missing_signature':bad['forbidden_common_blue_signatures'].pop()
        if name=='bad_witness':bad['forbidden_common_blue_signatures'][0]['vertices']=[0,1,2,12,13]
        if name=='wrong_color':bad['forbidden_common_blue_signatures'][0]['color']='red'
        if name=='wrong_core':bad['bits']='0'*18
        if name=='wrong_pair':bad['empty_pair']=[12,14]
        reject(name,lambda:proof(bad))
    bad=cases[:1];reject('missing_red_case',lambda:check_cases(bad))
    for name in ('bad_order','duplicate_edge','red_in_empty_signature','wrong_pair_color'):
        lines=(fixtures/'red_pair15.edges').read_text().splitlines()
        if name=='bad_order':lines[0]='14'
        if name=='duplicate_edge':lines.append(lines[1])
        if name=='red_in_empty_signature':lines.append('0 14')
        if name=='wrong_pair_color':lines.remove('12 13')
        path=work/'bad.edges';path.write_text('\n'.join(lines)+'\n');reject(name,lambda:fixture(path,15,True))
    for case in cases:
        lines=(work.parent/(case['id']+'.cnf')).read_bytes().splitlines(keepends=True)
        for name in ('lost_base','lost_clause','wrong_sign','wrong_edge','extra_empty','wrong_header'):
            bad=lines[:]
            if name=='lost_base':bad.pop(10)
            if name=='lost_clause':bad.pop()
            if name=='wrong_sign':bad[-1]=b'-'+bad[-1]
            if name=='wrong_edge':bad[-1]=b'167 0\n'
            if name=='extra_empty':bad.append(b'0\n')
            if name=='wrong_header':bad[0]=b'p cnf 34320 617936\n'
            path=work/'bad.cnf';path.write_bytes(b''.join(bad));reject(case['id']+'_'+name,lambda:check(base,path,case))
    for name in ('bad.cnf','bad.edges'):(work/name).unlink()
    need(len(rejected)==22,'all corruption controls')
    return dict(local=local(cert,fixtures),coverage=check_cases(cases),truth_table=truth(),rejected=rejected)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--fixtures',type=Path,required=True)
    p.add_argument('--local',action='store_true');p.add_argument('--cases',type=Path);p.add_argument('--base',type=Path);p.add_argument('--work',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    cert=json.loads(a.certificate.read_text())
    if a.local:answer=local(cert,a.fixtures)
    else:
        need(a.cases and a.base and a.work,'full control arguments');answer=controls(cert,json.loads(a.cases.read_text()),a.base,a.fixtures,a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS literal empty-pair proof and requested checks')
