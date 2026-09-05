#!/usr/bin/env python3
"""Literal independent anchor census and complete formula comparison; no producer import."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def need(ok, why):
    if not ok: raise ValueError(why)


def graph(bits, k):
    pairs=list(combinations(range(k),2)); red=set()
    for a,b in combinations(range(3*k),2):
        i,s=divmod(a,3);j,t=divmod(b,3)
        if i==j or bits[3*pairs.index((i,j))+(t-s)%3]=='1':red.add((a,b))
    return red


def validate(data):
    free={}; families={11:(1,2,2),13:(2,2,2)}
    for value in range(512):
        bits=f'{value:09b}'
        if any(bits[q:q+3]=='111' for q in (0,3,6)):continue
        red=graph(bits,3)
        if any(all(e not in red for e in combinations(t,2)) for t in combinations(range(9),3)):continue
        need(not any(all(e in red for e in combinations(f,2)) for f in combinations(range(9),5)),'red K5')
        weights=tuple(sorted(sum(int(x) for x in bits[q:q+3]) for q in (0,3,6)))
        hits=[i for i,w in families.items() if w==weights]
        need(len(hits)==1,'weight classification');free[bits]=hits[0]
    need({r['bits']:r['type'] for r in data['blue_free']}==free,'entrywise free census')
    reps={11:graph('100110110',3),13:graph('110110101',3)}
    checked=0
    for row in data['blue_free']:
        old=graph(row['bits'],3)
        vertex=[3*row['perm'][i]+(row['sign']*s+row['shift'][i])%3 for i in range(3) for s in range(3)]
        actual={(a,b) for a,b in combinations(range(9),2) if tuple(sorted((vertex[a],vertex[b]))) in old}
        need(actual==reps[row['type']],'free anchor permutation witness');checked+=1
    root=Path(__file__).resolve().parent.parent
    boundary=json.loads((root/'ramsey_r55_order3_eleven_four_empty_split'/'boundary.json').read_text())
    prior=json.loads((root/'ramsey_r55_order3_eleven_empty_signature'/'classification.json').read_text())
    original={r['index']:r for r in prior['rows']}
    need([r['index'] for r in data['residual']]==boundary['remaining_open'],'full residual list')
    for row in data['residual']:
        need(row['bits']==original[row['index']]['bits'] and row['labeled']==original[row['index']]['labeled'],'input row')
        old=graph(row['bits'],4)
        missing=[]
        for omitted in range(4):
            vertices=[v for v in range(12) if v//3!=omitted]
            if not any(all(e not in old for e in combinations(t,2)) for t in combinations(vertices,3)):missing.append(omitted)
        need([a['omitted'] for a in row['anchors']]==missing and bool(missing),'all blue-free complements')
        for a in row['anchors']:
            need(sorted(a['perm'])==list(range(4)) and a['perm'][3]==a['omitted'] and a['sign'] in (1,-1),'four-cycle permutation')
            vertex=[3*a['perm'][i]+(a['sign']*s+a['shift'][i])%3 for i in range(4) for s in range(3)]
            actual={(i,j) for i,j in combinations(range(9),2) if tuple(sorted((vertex[i],vertex[j]))) in old}
            need(actual==reps[a['type']],'residual anchor witness');checked+=1
    need(data['remaining_classes']==34 and data['remaining_labeled']==sum(r['labeled'] for r in data['residual'])==24057,'residual totals')
    need(data['type_counts']=={str(i):list(free.values()).count(i) for i in families},'type counts')
    # Generate equality from its extremal multiplicities, independently of mask list.
    eq=sorted([(0,0,0)]+[t for t in product((0,1),repeat=3) if sum(t)==1 for _ in range(2)]+[t for t in product((0,1),repeat=3) if sum(t)==2])
    need(len(eq)==10 and all(sum(t[i] for t in eq)==4 for i in range(3)),'equality multiplicities')
    full=sorted(product((0,1),repeat=11))
    need([x[:3] for x in full]==sorted(x[:3] for x in full),'full prefix order')
    return dict(blue_free=len(free),type_counts=data['type_counts'],literal_witnesses=checked,
                residual_classes=34,residual_labeled=24057,full_fixed_rows_checked=len(full),equality_prefixes=eq)


def check(parent, cnf, anchor_type):
    # Literal pair-orbit reconstruction on all43 vertices recovers the primary meaning.
    def image(v):return v if v>=33 else 3*(v//3)+(v%3+1)%3
    unseen=set(combinations(range(43),2));orbits=[]
    while unseen:
        e=min(unseen);orb={e};f=tuple(sorted(map(image,e)))
        while f!=e:orb.add(f);f=tuple(sorted(map(image,f)))
        unseen-=orb;orbits.append(sorted(orb))
    moving=[];fixed=[];links=[]
    for orb in orbits:
        a,b=orb[0]
        if a<33 and b<33:
            if a//3!=b//3:moving.append(orb)
        elif a>=33:fixed.append(orb)
        else:links.append(orb)
    moving.sort(key=lambda o:(o[0][0]//3,o[0][1]//3,(o[0][1]-o[0][0])%3))
    fixed.sort();links.sort(key=lambda o:(o[0][1],o[0][0]//3))
    ids={e:q for q,orb in enumerate(moving+fixed+links,1) for e in orb}
    need(len(moving+fixed+links)==320,'primary orbit count')
    rep='100110110' if anchor_type==11 else '110110101'
    need(anchor_type in (11,13),'anchor type')
    units=[]
    for q,(i,j) in enumerate(combinations(range(3),2)):
        for d in range(3):
            v=ids[3*i,3*j+d];units.append(v if rep[3*q+d]=='1' else -v)
    eq=sorted([(0,0,0)]+[t for t in product((0,1),repeat=3) if sum(t)==1 for _ in range(2)]+[t for t in product((0,1),repeat=3) if sum(t)==2])
    for f,prefix in zip(range(33,43),eq):
        for i,b in enumerate(prefix):units.append(ids[3*i,f] if b else -ids[3*i,f])
    # Drop only the adjacent red-cycle ordering C2 <= C3 at anchor C0.
    skip={(-ids[0,6+d],ids[0,9+d]) for d in range(3)}
    need(skip=={(-4,7),(-5,8),(-6,9)},'three weakened normalizers')
    count=0;removed=set()
    with parent.open() as f,cnf.open() as g:
        need(f.readline()=='p cnf 34280 615920\n','parent header')
        need(g.readline()=='p cnf 34280 615956\n','child header')
        for line in f:
            cl=tuple(map(int,line.split()[:-1]))
            if cl in skip:removed.add(cl);continue
            need(g.readline()==line,'retained full parent mismatch');count+=1
        for unit in units:need(g.readline()==f'{unit} 0\n','derived equality/core unit');count+=1
        need(not g.read(),'EOF')
    need(removed==skip and count==615956,'counts')
    return dict(primary_orbits=320,removed_ordering_clauses=3,retained_parent_clauses=615917,
                anchor_units=9,equality_units=30,clauses=count,variables=34280)


def controls(parent, cnf, data, work):
    import copy
    work.mkdir(parents=True,exist_ok=True)
    rejected=[]
    for name in ('lost_anchor','false_type','lost_residual'):
        bad=copy.deepcopy(data)
        if name=='lost_anchor':bad['blue_free'].pop()
        if name=='false_type':bad['blue_free'][0]['type']=13 if bad['blue_free'][0]['type']==11 else 11
        if name=='lost_residual':bad['residual'].pop()
        try:validate(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed classification '+name)
    lines=cnf.read_text().splitlines(keepends=True)
    for name in ('extra_empty','wrong_prefix','lost_unit','lost_parent','wrong_type','numeric_order','restore_sort'):
        bad=lines[:]
        if name=='extra_empty':bad.append('0\n')
        if name=='wrong_prefix':bad[-1]=str(-int(bad[-1].split()[0]))+' 0\n'
        if name=='lost_unit':bad.pop()
        if name=='lost_parent':bad.pop(10)
        if name=='wrong_type':bad[-39]='-1 0\n'
        if name=='numeric_order':bad[-27:-24]=['222 0\n','-223 0\n','-224 0\n']
        if name=='restore_sort':bad.insert(-39,'-4 7 0\n')
        path=work/'bad.cnf';path.write_text(''.join(bad))
        try:check(parent,path,11)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted malformed formula '+name)
    (work/'bad.cnf').unlink()
    return dict(rejected=rejected,classification=validate(data),formula=check(parent,cnf,11))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True)
    p.add_argument('--formula',type=Path,required=True);p.add_argument('--classification',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();answer=controls(a.parent,a.formula,json.loads(a.classification.read_text()),a.work)
    a.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    print('PASS literal classification, primary meanings and ten corruption controls')
