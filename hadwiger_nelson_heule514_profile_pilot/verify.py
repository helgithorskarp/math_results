#!/usr/bin/env python3
"""Solver-free certificate audit, with optional independent raw-model audit.

Coverage uses tuple-subset enumeration rather than producer bitmask testing.
Imports no pilot, cover routine, path compiler, relation DP or SAT package.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def need(ok,why):
    if not ok: raise ValueError(why)


def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')


def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def colour_check(c,edges,missing=None):
    need(len(c)==514 and set(c)<=set('.0123'),'colour domain')
    D=[v for v,x in enumerate(c) if x=='.']
    if missing is not None:need(D==list(missing),'colour omission set')
    checks=0
    for u,v in edges:
        if c[u]!='.' and c[v]!='.':
            need(c[u]!=c[v],'unit edge colouring');checks+=1
    return checks


def formula(edges,O,kernel):
    """Independent serialization of the archived projected encoding."""
    chosen=[v for v in range(510) if v not in O]
    clauses=[list(range(4*v+1,4*v+5)) for v in chosen]
    for u,v in edges:
        if v<510 and u not in O and v not in O:
            for c in range(4):clauses.append([-4*u-c-1,-4*v-c-1])
    clauses.append([1])
    nb=[[u for u,v in edges if v==510+i and 0<u<510] for i in range(4)]
    need(not O.intersection({0}|{v for row in nb for v in row}),'projection boundary')
    for i in range(4):
        for c in range(1,4):
            a=2040+3*i+c; xs=[4*v+c+1 for v in nb[i]]
            clauses += [[-a,-x] for x in xs]+[[a]+xs]
    for obstruction in kernel['obstructions']:
        selected=[-x-1 for x in obstruction['clause'] if x<0]
        if all(510+i not in O for i in selected):
            clauses.append([x+2036 for x in obstruction['clause'] if x>0])
    raw=(f'p cnf 2052 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
    return clauses,raw,nb


def raw_audit(pilot,candidates,edges):
    kernel=load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')
    transcript=load(pilot/'transcript.json');certificates=load(pilot/'certificate.json')
    need(len(transcript)==len(candidates)==len(certificates)==77,'complete all-SAT pilot')
    fields=['index','profile','status','clauses','cnf_sha256','final_omissions']
    need([{k:r[k] for k in fields} for r in load(HERE/'cases.json')]==
         [{k:r[k] for k in fields} for r in transcript],'public case mathematical transcript')
    for row in load(HERE/'certificate.json'):
        source=certificates[row['source_candidate']]
        need(source['D']==row['D'] and source['colouring']==row['colouring'],'compact certificate native provenance')
    model_checks=0;edge_checks=0;restoration_steps=0;clause_counts=[]
    for i,(spec,tr,cert) in enumerate(zip(candidates,transcript,certificates)):
        need(spec['index']==tr['index']==cert['index']==i and tr['status']=='SAT','pilot row identity')
        O=set(spec['omitted']);need(tr['omitted']==spec['omitted'],'candidate identity')
        clauses,raw,nb=formula(edges,O,kernel)
        need(raw==(pilot/f'{i:02d}.cnf').read_bytes(),'independent formula bytes')
        need(sha256(raw).hexdigest()==tr['cnf_sha256'] and len(clauses)==tr['clauses'],'formula metadata')
        answer_raw=(pilot/f'{i:02d}.model.json').read_bytes()
        need(sha256(answer_raw).hexdigest()==tr['model_file_sha256'],'model packet hash')
        answer=json.loads(answer_raw);m=answer['model']
        need(answer['status']=='SAT' and len(m)==2052 and {abs(x) for x in m}==set(range(1,2053)),'Boolean model domain')
        truth={x for x in m if x>0}
        for clause in clauses:
            need(any((x in truth) if x>0 else (-x not in truth) for x in clause),'Boolean clause');model_checks+=1
        c=['.']*514
        for v in range(510):
            if v not in O:c[v]=str(next(k for k in range(4) if 4*v+k+1 in truth))
        selected=[j for j in range(4) if 510+j not in O]
        # Enumerate every possible retained path assignment independently of DP.
        extension=None
        for values in product('123',repeat=len(selected)):
            trial=c.copy()
            for j,x in zip(selected,values):trial[510+j]=x
            if all(trial[u]=='.' or trial[v]=='.' or trial[u]!=trial[v] for u,v in edges if v>=510):
                extension=trial;break
        need(extension is not None,'path extension')
        need(''.join(extension)==cert['candidate_colouring'],'independent candidate reconstruction')
        edge_checks+=colour_check(extension,edges,sorted(O))
        current=extension.copy()
        for v,x in cert['fills']:
            need(v in O and current[v]=='.' and x in '0123','restoration step domain')
            current[v]=x;restoration_steps+=1
            need(all(current[u]=='.' or current[t]=='.' or current[u]!=current[t] for u,t in edges if v in (u,t)),'restoration edges')
        need(''.join(current)==cert['colouring'],'restored witness bytes')
        edge_checks+=colour_check(current,edges,cert['D'])
        need(tr['final_omissions']==cert['D'],'transcript final cut')
        clause_counts.append(len(clauses))
    return dict(target_models=77,independently_rebuilt_formulas=77,Boolean_clause_checks=model_checks,
                candidate_and_restored_edge_checks=edge_checks,restoration_steps=restoration_steps,
                clause_count_range=[min(clause_counts),max(clause_counts)],negative_certificates=0,
                public_case_rows_compared=77,compact_certificate_source_rows_compared=15)


def verify(frontier,work,pilot=None):
    start=time.monotonic()
    for filename,digest in load(HERE/'manifest.json').items():
        need(sha256((REPO/filename).read_bytes()).hexdigest()==digest,('input hash',filename))
    G=module('independent_exact_geometry',REPO/'hadwiger_nelson_heule514_path_projection/verify.py')
    edges,boundary_checks,boundary=G.geometry()
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    large={i for i,v in enumerate(labels) if all(G.scale(old['coordinates'][str(v)])[a][k]==0 for a in range(2) for k in (2,3,6,7))}
    need(len(large)==375,'large block definition')
    plan=load(HERE/'plan.json');candidate_raw=(HERE/'candidates.json').read_bytes()
    need(sha256(candidate_raw).hexdigest()==plan['candidate_sha256'],'frozen candidate file')
    candidates=json.loads(candidate_raw);parent=load(REPO/'hadwiger_nelson_heule514_core_propagation/core_census.json')
    expected=[dict(index=i,profile=[r['core_order'],r['large_omissions'],r['new_omission_mask']],profile_count=r['count'],first_input_row=r['first_input_row'],omitted=r['representative_core_omissions']) for i,r in enumerate(parent['profiles'])]
    need(candidates==expected and len(candidates)==77,'exact prespecified profile representatives')
    cert=load(HERE/'certificate.json');cuts=[tuple(r['D']) for r in cert]
    need(cuts==sorted(set(cuts),key=lambda D:(len(D),D)),'canonical cut antichain')
    positive_checks=0
    for i,r in enumerate(cert):
        D=tuple(r['D']);need(r['index']==i and D==tuple(sorted(set(D))) and set(D)<=set(range(514)),'cut schema')
        positive_checks+=colour_check(r['colouring'],edges,D)
        need(set(D)<=set(candidates[r['source_candidate']]['omitted']),'source candidate restriction')
        need(not any(set(E)<set(D) for E in cuts),'minimal cuts')
    previous_free=set(load(REPO/'hadwiger_nelson_heule514_interface/verification.json')['free_vertices'])
    new_forced={D[0] for D in cuts if len(D)==1}
    need(len(previous_free)==30 and new_forced<=previous_free,'additional singleton forcings')
    remaining_free=sorted(previous_free-new_forced)
    # Check representative colourings by restriction of positive certificates.
    candidate_indices=[];representative_checks=0
    for c in candidates:
        O=set(c['omitted']);need(not O.intersection(boundary),'retained required boundary')
        index=next((i for i,D in enumerate(cuts) if set(D)<=O),None)
        need(index is not None,'every representative has a positive witness')
        colour=''.join('.' if v in O else x for v,x in enumerate(cert[index]['colouring']))
        representative_checks+=colour_check(colour,edges,c['omitted']);candidate_indices.append(index)
    # Complete family coverage by enumerating tuple subsets, not bitmask tests.
    raw=frontier.read_bytes();need(sha256(raw).hexdigest()==parent['core_frontier_sha256'],'frozen full core stream')
    lookup={D:i for i,D in enumerate(cuts)};sizes=sorted({len(D) for D in cuts})
    profile=Counter();remaining=Counter();hist=Counter();survivors=[];tags=bytearray();previous=None
    for line in raw.decode('ascii').splitlines():
        O=tuple(map(int,line.split(',')));key=(len(O),O)
        need(tuple(sorted(set(O)))==O and (previous is None or previous<key),'frontier canonical order');previous=key
        matches=[lookup[D] for size in sizes for D in combinations(O,size) if D in lookup]
        index=min(matches) if matches else None;tags.append(255 if index is None else index)
        pr=(514-len(O),sum(v in large for v in O),sum(1<<(v-510) for v in O if v>=510))
        profile[pr]+=1
        if index is None:remaining[pr]+=1;survivors.append(line)
        else:hist[index]+=1
    need(sum(profile.values())==190536,'all input cores')
    need(profile==Counter({(r['core_order'],r['large_omissions'],r['new_omission_mask']):r['count'] for r in parent['profiles']}),'complete original profile census')
    survivor_raw=''.join(line+'\n' for line in survivors).encode('ascii')
    result=load(HERE/'coverage.json')
    need(result['input_cores']==190536 and result['covered']==sum(hist.values()) and result['survivors']==len(survivors),'whole family totals')
    need(result['candidate_cover_indices']==candidate_indices,'representative coverage')
    need(result['coverage_sha256']==sha256(tags).hexdigest() and result['coverage_bytes']==len(tags),'complete first-cover tags')
    need(result['survivor_sha256']==sha256(survivor_raw).hexdigest() and result['survivor_bytes']==len(survivor_raw),'exact survivor bytes')
    need(result['first_cover_histogram']=={str(k):v for k,v in sorted(hist.items())},'certificate use counts')
    need(result['profile_rows']==[dict(profile=list(pr),input=profile[pr],covered=profile[pr]-remaining[pr],remaining=remaining[pr]) for pr in sorted(profile)],'all profile outcomes')
    need(result['cut_size_histogram']=={str(k):v for k,v in sorted(Counter(map(len,cuts)).items())},'positive cut size counts')
    need(result['surviving_core_orders']=={str(n):sum(v for (order,l,m),v in remaining.items() if order==n) for n in [507,508]},'surviving core orders')
    need(result['covered_profiles']==sum(remaining[p]==0 for p in profile) and result['remaining_profiles']==sum(remaining[p]>0 for p in profile),'profile closure counts')
    work.mkdir(exist_ok=True);(work/'survivors.txt').write_bytes(survivor_raw);(work/'coverage.bin').write_bytes(tags)
    controls=0
    for c in [cert[0]['colouring'][:-1], 'x'+cert[0]['colouring'][1:]]:
        try:colour_check(c,edges)
        except ValueError:controls+=1
        else:raise ValueError('malformed colouring accepted')
    bad=list(cert[0]['colouring']);u,v=next((u,v) for u,v in edges if bad[u]!='.' and bad[v]!='.');bad[v]=bad[u]
    try:colour_check(bad,edges)
    except ValueError:controls+=1
    else:raise ValueError('monochromatic edge accepted')
    report=dict(status='COMPLETE POSITIVE CERTIFICATES AND WHOLE CORE COVER VERIFIED',record_improvement=False,family_closed=False,
                exact_vertices=514,unit_edges=len(edges),exact_coordinate_pairs=131841,boundary_witness_edge_checks=boundary_checks,
                positive_certificates=len(cert),positive_certificate_edge_checks=positive_checks,representatives_checked=77,
                additional_forced_vertices=sorted(new_forced),total_forced_vertices=514-len(remaining_free),remaining_free_vertices=remaining_free,
                representative_edge_checks=representative_checks,core_rows_checked=190536,covered=sum(hist.values()),survivors=len(survivors),
                survivor_sha256=sha256(survivor_raw).hexdigest(),coverage_sha256=sha256(tags).hexdigest(),
                malformed_colourings_rejected=controls,solver_used=False,seconds=time.monotonic()-start)
    if pilot is not None:
        report['raw_native_audit']=raw_audit(pilot,candidates,edges)
        report['seconds_with_raw_audit']=time.monotonic()-start
        need((pilot/'coverage.bin').read_bytes()==bytes(tags) and (pilot/'survivors.txt').read_bytes()==survivor_raw,'independent producer/checker output equality')
    save(work/'verification.json',report);print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--pilot',type=Path);a=p.parse_args();verify(a.frontier,a.work,a.pilot)
