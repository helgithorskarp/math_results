#!/usr/bin/env python3
"""Independent exact degree classification and positive covering certificate."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations,product
import json
from math import comb
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def controls():
    possible=list(combinations(range(4),2));count=0;free_count=0
    for bits in range(64):
        edges=[e for i,e in enumerate(possible) if bits>>i&1]
        for word in product(range(4),repeat=4):
            m={v for v,k in enumerate(word) if k==1};u={v for v,k in enumerate(word) if k in (2,3)};t={v for v,k in enumerate(word) if k==3};selected=m|t
            for threshold in range(5):
                direct=all(sum(v in e and set(e)<=selected for e in edges)>=threshold for v in selected)
                reduced=True
                for v in m|u:
                    base=sum(v in e and len(set(e)&m-{v})==1 for e in edges)
                    extra=sum(v in e and len(set(e)&t-{v})==1 for e in edges)
                    if v in selected and extra<max(0,threshold-base):reduced=False
                I.check(direct==reduced,'degree selector equivalence');count+=1
                if all(sum(v in e and len(set(e)&m-{v})==1 for e in edges)>=threshold for v in m):
                    safe={v for v in u if sum(v in e and len(set(e)&m)==1 for e in edges)>=threshold}
                    if t<=safe:I.check(direct,'free optional subcube');free_count+=1
    return {'degree_assignments':count,'free_subcube_controls':free_count}


def verify(out,archive):
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text());cert=json.loads((HERE/'certificate.json').read_text())
    for rel,h in plan['input_files'].items():I.check(sha256((HERE.parent/rel).read_bytes()).hexdigest()==h,'input identity')
    _,edges,_=I.geometry();m=set(plan['mandatory_vertices']);u=set(plan['optional_vertices']);active=m|u
    I.check(len(m)==492 and len(u)==68 and not m&u,'fixed partition')
    neighbours={v:set() for v in active}
    for a,b in edges:
        if a in active and b in active:neighbours[a].add(b);neighbours[b].add(a)
    rows=[{'vertex':v,'mandatory_degree':len(neighbours[v]&m),'optional_neighbours':sorted(neighbours[v]&u),'required_optional_neighbours':max(0,4-len(neighbours[v]&m))} for v in sorted(u)]
    free=sorted(v for v in u if len(neighbours[v]&m)>=4);dependent=sorted(u-set(free))
    I.check(all(len(neighbours[v]&m)>=4 for v in m),'mandatory graph minimum degree')
    I.check(free==plan['free_vertices'] and dependent==plan['dependent_vertices'] and (len(free),len(dependent))==(50,18),'exact free/dependent partition')
    I.check(rows==cert['optional_degree_rows'],'entrywise degree certificate')
    I.check(all(v>=510 for v in dependent),'dependent vertices all fresh')
    chosen=set();trace=[]
    for step in range(16):
        values=[(len(neighbours[v]&(m|chosen)),-v,v) for v in free if v not in chosen];gain,_,v=max(values);trace.append({'vertex':v,'added_edges':gain});chosen.add(v)
    I.check(trace==plan['selection_trace'],'frozen target selection')
    for row,vs in zip(plan['cases'],[m|set(free),m|chosen]):
        I.check(row['retained']==sorted(vs),'frozen exact support');clauses,raw,_,triangle=I.formula(vs,edges,4)
        I.check(sha256(raw).hexdigest()==row['cnf_sha256'] and len(clauses)==row['clauses'] and triangle==row['triangle'],'independent frozen CNF')
    domain=m|set(free);text=cert['cover_colouring'];checks=I.colouring(text,sorted(set(range(632))-domain),edges,4)
    I.check(checks==2672 and len(domain)==542,'cover graph size')
    target=m|chosen;restricted=''.join(c if v in target else '.' for v,c in enumerate(text));target_checks=I.colouring(restricted,sorted(set(range(632))-target),edges,4);I.check(target_checks==2500,'target restriction edges')
    mandatory_text=''.join(c if v in m else '.' for v,c in enumerate(text));m_checks=I.colouring(mandatory_text,sorted(set(range(632))-m),edges,4)
    I.check(comb(50,16)==plan['free16_support_count'] and sum(comb(50,k) for k in range(17))==plan['free_at_most16_support_count'],'exact subset counts')
    archived_clauses=0
    if archive is not None:
        records=json.loads((archive/'records.json').read_text());I.check(len(records)==1 and records[0]['name']=='free50' and records[0]['status']=='SAT' and records[0]['colouring']==text,'stopped after covering positive')
        cls,raw,vs,_=I.formula(domain,edges,4);I.check(raw==(archive/'free50.cnf').read_bytes(),'native formula bytes')
        literals=[int(x) for line in (archive/'free50.log').read_text().splitlines() if line.startswith('v ') for x in line.split()[1:] if x!='0'];truth={abs(x):x>0 for x in literals}
        I.check(len(truth)==len(literals)==4*len(vs) and set(truth)==set(range(1,4*len(vs)+1)),'complete native model')
        I.check(all(any(truth[abs(x)]==(x>0) for x in c) for c in cls),'every native model clause');archived_clauses=len(cls)
        for i,v in enumerate(vs):I.check([c for c in range(4) if truth[4*i+c+1]]==[int(text[v])],'independent decode')
    rejected=0;bad=list(text);a,b=next((a,b) for a,b in edges if a in domain and b in domain);bad[b]=bad[a]
    for word in (text[:-1],text.replace('.', '0',1),''.join(bad)):
        try:I.colouring(word,sorted(set(range(632))-domain),edges,4)
        except ValueError:rejected+=1
        else:raise ValueError('malformed covering certificate accepted')
    control=controls();out.mkdir(parents=True,exist_ok=False)
    report={'status':'FREE50 OPTIONAL SUBFAMILY FOUR-COLOURABLE; DEGREE SCREEN FEASIBLE','host_exact_pairs':199396,'cover_vertices':542,'cover_edges':checks,'target_vertices':508,'target_restriction_edge_checks':target_checks,'mandatory_vertices':492,'mandatory_edge_checks':m_checks,'free_optional_vertices':50,'dependent_optional_vertices':18,'dependent_all_fresh':True,'dependent_required_neighbours':dict(sorted(Counter(r['required_optional_neighbours'] for r in rows if r['required_optional_neighbours']).items())),'covered_optional_subsets':2**50,'covered_size508_supports':comb(50,16),'covered_size_at_most508_supports_with_M':sum(comb(50,k) for k in range(17)),'native_model_clauses_checked':archived_clauses,'malformed_positives_rejected':rejected,'controls':control,'whole560_family_closed':False,'record_improvement':False,'seconds':time.monotonic()-start}
    (out/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--archive',type=Path);a=ap.parse_args();verify(a.out,a.archive)
