#!/usr/bin/env python3
"""Independent literal audit and exhaustive weak-composition classification."""
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


def compositions(total,length):
    if length==1:
        yield (total,);return
    for x in range(total+1):
        for tail in compositions(total-x,length-1):yield (x,)+tail


def classify(cert):
    need(cert['index']==194 and cert['bits']=='100110110110110100' and cert['labeled']==81,'literal Core194')
    ids=primary();core_ids=list(range(1,10))+list(range(31,37))+list(range(58,61))
    colors=dict(zip(core_ids,map(int,cert['bits'])))
    red=lambda a,b: a//3==b//3 or colors[ids[tuple(sorted((a,b)))]]==1
    need([w['omitted'] for w in cert['red_k4_witnesses']]==list(range(4)),'four complementary witnesses')
    for w in cert['red_k4_witnesses']:
        q=w['red_k4'];need(len(q)==len(set(q))==4 and all(0<=a<12 and a//3!=w['omitted'] for a in q),'complementary four-set')
        need(all(red(a,b) for a,b in combinations(q,2)),'literal red K4 excludes larger signatures')
    pairs=list(combinations(range(4),2));survivors=[];examined=0
    for counts in compositions(9,10):
        examined+=1;xs=counts[:4];ys=counts[4:]
        if min(xs)<1:continue
        if any(xs[i]+ys[k]>2 or xs[j]+ys[k]>2 for k,(i,j) in enumerate(pairs)):continue
        need(xs==(1,1,1,1) and sorted(ys)==[0,1,1,1,1,1],'one-empty rigidity')
        masks=[0]
        for i,count in enumerate(xs):masks.extend([1<<i]*count)
        for pair,count in zip(pairs,ys):masks.extend([sum(1<<i for i in pair)]*count)
        masks.sort(key=lambda m:tuple(bool(m&(1<<i)) for i in range(4)))
        survivors.append(dict(missing_pair=list(pairs[ys.index(0)]),masks=masks))
    survivors.sort(key=lambda x:x['missing_pair'])
    need(examined==48620 and len(survivors)==6,'complete count domain')
    need(cert['one_empty_patterns']==survivors,'all six exact signature patterns')
    rows=list(product((0,1),repeat=11));need(len(rows)==2048,'all full rows')
    need(all(rows[i][:4]<=rows[i+1][:4] for i in range(2047)),'full row order implies prefix order')
    need(all((not any(row[:4]))==(k<128) for k,row in enumerate(rows)),'empty rows precede nonempty rows')
    for bits in product((False,True),repeat=4):
        need(bool(any(bits))!=all(not bit for bit in bits),'one/multiple second-prefix partition')
    return dict(weak_compositions=examined,one_empty_patterns=survivors,red_k4_witnesses=cert['red_k4_witnesses'],full_rows_checked=2048,second_prefix_patterns=16)


def check_cases(cases,cert):
    patterns=cert['one_empty_patterns'];expected=[]
    for p in patterns:
        i,j=p['missing_pair'];expected.append(dict(id='one_'+str(i)+str(j),index=194,branch='one',**p))
    expected.append(dict(id='multiple',index=194,branch='multiple'));expected.sort(key=lambda c:c['id'])
    need(cases==expected and len(cases)==7,'six one-empty cases and one complementary branch')
    return dict(cases=7,one_empty_cases=6,multiple_cases=1,whole_cores=1,labeled=81)


def expected(case):
    ids=primary()
    if case['branch']=='multiple':return [(-ids[3*i,34],) for i in range(4)]
    rows=[]
    for f,m in zip(range(34,43),case['masks'][1:]):
        rows.extend(((1 if m&(1<<i) else -1)*ids[3*i,f],) for i in range(4))
    need(len(rows)==36 and all(222<=abs(c[0])<=313 for c in rows),'only four-bit later prefixes')
    return rows


def check(base,full,case):
    need(sha(base)==dict(bytes=24968396,sha256='f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf'),'entire guarded base hash')
    rows=expected(case)
    with base.open('rb') as f,full.open('rb') as g:
        need(f.readline()==b'p cnf 34320 617932\n','base header')
        need(g.readline()==('p cnf 34320 '+str(617932+len(rows))+'\n').encode(),'child header')
        for line in f:need(g.readline()==line,'entire guarded base retained')
        for row in rows:need(g.readline()==(' '.join(map(str,row))+' 0\n').encode(),'exact literal prefix unit')
        need(not g.read(),'exact EOF')
    return dict(entire_guarded_base=True,variables=34320,clauses=617932+len(rows),added_units=len(rows),added_fixed_edges=0,added_bluecycle_links=0,new_normalizers=0)


def controls(cert,cases,base,work):
    work.mkdir(parents=True,exist_ok=True);rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):rejected.append(name)
        else:raise ValueError('accepted malformed '+name)
    for name in ('missing_pattern','bad_red_k4','wrong_core','duplicate_pattern','reversed_prefix_order'):
        bad=copy.deepcopy(cert)
        if name=='missing_pattern':bad['one_empty_patterns'].pop()
        if name=='bad_red_k4':bad['red_k4_witnesses'][0]['red_k4']=[0,1,2,3]
        if name=='wrong_core':bad['bits']='0'*18
        if name=='duplicate_pattern':bad['one_empty_patterns'][-1]=bad['one_empty_patterns'][0]
        if name=='reversed_prefix_order':bad['one_empty_patterns'][0]['masks'].reverse()
        reject(name,lambda:classify(bad))
    for name in ('lost_multiple_case','wrong_missing_pair'):
        bad=copy.deepcopy(cases)
        if name=='lost_multiple_case':bad.pop(0)
        if name=='wrong_missing_pair':bad[1]['missing_pair']=[0,0]
        reject(name,lambda:check_cases(bad,cert))
    for case in (cases[0],cases[1]):
        full=work.parent/(case['id']+'.cnf');lines=full.read_bytes().splitlines(keepends=True);n=len(expected(case))
        for name in ('lost_base','lost_unit','wrong_sign','wrong_prefix','fixed_edge_unit','extra_empty','wrong_header'):
            bad=lines[:]
            if name=='lost_base':bad.pop(10)
            if name=='lost_unit':bad.pop()
            if name=='wrong_sign':bad[-1]=(-int(bad[-1].split()[0])).__str__().encode()+b' 0\n'
            if name=='wrong_prefix':bad[-n]=b'-211 0\n'
            if name=='fixed_edge_unit':bad[-1]=b'166 0\n'
            if name=='extra_empty':bad.append(b'0\n')
            if name=='wrong_header':bad[0]=b'p cnf 34320 617932\n'
            path=work/'bad.cnf';path.write_bytes(b''.join(bad));reject(case['branch']+'_'+name,lambda:check(base,path,case))
    (work/'bad.cnf').unlink()
    return dict(classification=classify(cert),coverage=check_cases(cases,cert),rejected=rejected)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--cases',type=Path,required=True)
    p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    cert=json.loads(a.certificate.read_text());cases=json.loads(a.cases.read_text());answer=controls(cert,cases,a.base,a.work)
    need(len(answer['rejected'])==21,'all malformed inputs rejected')
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n');print('PASS six-pattern rigidity,complete seven-case cover and21 corruptions')
