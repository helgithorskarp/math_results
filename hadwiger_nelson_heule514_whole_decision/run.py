#!/usr/bin/env python3
"""One bounded traversal of the complete frozen H514 residual family."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
GRAPH_SHA='ec389ca801d42ff3c7661c8df5eb2a017e44b139a979d4545b9e2dc458e50177'


def load(p):return json.loads(p.read_text())
def save(p,x):
    temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(x,indent=2)+'\n');os.replace(temp,p)
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def run(frontier,graph,out):
    for name,digest in load(HERE/'manifest.json').items():
        if sha256((REPO/name).read_bytes()).hexdigest()!=digest:raise ValueError(('input hash',name))
    plan=load(HERE/'plan.json');raw=frontier.read_bytes()
    if sha256(raw).hexdigest()!=plan['frontier']['sha256']:raise ValueError('frozen input hash')
    candidates=[tuple(map(int,l.split(','))) for l in raw.decode('ascii').splitlines()]
    if len(candidates)!=8974 or candidates!=sorted(set(candidates),key=lambda O:(len(O),O)):raise ValueError('input family')
    if sha256(graph.read_bytes()).hexdigest()!=GRAPH_SHA:raise ValueError('exact graph packet')
    edges=[tuple(map(int,l.split())) for l in graph.read_text().splitlines()[1:]]
    if len(edges)!=2526:raise ValueError('graph edge count')
    P=module('prior_positive_decoder',REPO/'hadwiger_nelson_heule514_profile_pilot/pilot.py')
    C=module('verified_path_compiler',REPO/'hadwiger_nelson_heule514_path_projection/compile.py')
    R=module('verified_path_dp',REPO/'hadwiger_nelson_heule514_path_projection/relation.py')
    kernel=load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')
    worker_plan=load(REPO/'hadwiger_nelson_heule514_profile_pilot/plan.json')
    for k in ['conflicts_per_candidate','worker_address_space_bytes']:
        if worker_plan['bounds'][k]!=plan['bounds'][k]:raise ValueError('worker limit mismatch')
    adj=[set() for _ in range(514)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    witnesses=[dict(id=i,kind='inherited',source_index=r['index'],D=r['D'],colouring=r['colouring'])
               for i,r in enumerate(load(REPO/'hadwiger_nelson_heule514_profile_pilot/certificate.json'))]
    for r in witnesses:
        if P.check(r['colouring'],edges)!=r['D']:raise ValueError('inherited positive witness')
    for O in candidates:
        if len(O) not in (6,7) or list(O)!=sorted(set(O)) or set(O)&C.BOUNDARY:raise ValueError('candidate domain')
        if any(set(r['D'])<=set(O) for r in witnesses):raise ValueError('input already covered')
    out.mkdir(exist_ok=False);start=time.monotonic();statuses=Counter();native=[];queries=0;halt=None
    with (out/'records.jsonl').open('w') as journal:
        for i,O in enumerate(candidates):
            Oset=set(O);record=dict(index=i)
            cover=next((r['id'] for r in witnesses if set(r['D'])<=Oset),None)
            remaining=plan['bounds']['total_run_wall_seconds']-(time.monotonic()-start)
            if cover is not None:
                record.update(status='COVERED',witness=cover)
            elif halt is not None or remaining<=0:
                record.update(status='UNQUERIED',reason=halt or 'total_wall_limit')
            else:
                n,clauses=C.build(edges,Oset,kernel);raw_cnf=C.dimacs(n,clauses)
                cnf=out/f'{i:04d}.cnf';cnf.write_bytes(raw_cnf);answer_file=out/f'{i:04d}.model.json'
                row=dict(index=i,omitted=list(O),variables=n,clauses=len(clauses),cnf_sha256=sha256(raw_cnf).hexdigest(),cnf_bytes=len(raw_cnf))
                before=time.monotonic();queries+=1
                if queries>plan['bounds']['target_queries_max']:raise ValueError('query bound')
                with (out/f'{i:04d}.log').open('w') as log:
                    try:
                        process=subprocess.run([sys.executable,'-B',str(REPO/'hadwiger_nelson_heule514_profile_pilot/pilot.py'),'--worker',str(cnf),'--answer',str(answer_file)],stdout=log,stderr=subprocess.STDOUT,
                                               timeout=min(remaining,plan['bounds']['worker_wall_seconds']))
                        if process.returncode:
                            row.update(status='UNKNOWN',reason='worker_error',returncode=process.returncode)
                        else:
                            answer=load(answer_file);row.update({k:v for k,v in answer.items() if k!='model'})
                            row['model_file_sha256']=sha256(answer_file.read_bytes()).hexdigest()
                    except subprocess.TimeoutExpired:row.update(status='UNKNOWN',reason='wall_limit')
                row['worker_wall_seconds']=time.monotonic()-before
                if row['status']=='SAT':
                    truth={x for x in answer['model'] if x>0}
                    if not all(any(x in truth if x>0 else -x not in truth for x in clause) for clause in clauses):raise ValueError('native model clause')
                    c=['.']*514
                    for v in range(510):
                        if v not in Oset:c[v]=str(min(k for k in range(4) if 4*v+k+1 in truth))
                    lists=[sum(1<<k for k in range(3) if all(c[v]!=str(k+1) for v in nb)) for nb in C.NEIGHBOURS]
                    mask=sum(1<<j for j in range(4) if 510+j not in Oset)
                    tail=R.extension(mask,lists)
                    if tail is None:raise ValueError('path extension')
                    for j,k in enumerate(tail):
                        if k>=0:c[510+j]=str(k+1)
                    if P.check(c,edges)!=list(O):raise ValueError('candidate colouring')
                    candidate=''.join(c);fills=[]
                    while True:
                        changed=False
                        for v in O:
                            if c[v]!='.':continue
                            allowed=[str(k) for k in range(4) if all(c[u]!=str(k) for u in adj[v])]
                            if allowed:c[v]=allowed[0];fills.append([v,c[v]]);changed=True
                        if not changed:break
                    D=P.check(c,edges);wid=len(witnesses)
                    witnesses.append(dict(id=wid,kind='native',source_index=i,D=D,colouring=''.join(c),candidate_colouring=candidate,fills=fills))
                    row.update(witness=wid,final_omissions=D);record.update(status='SAT',witness=wid)
                else:
                    record.update(status=row['status'])
                    if row['status']=='UNSAT':halt='native_UNSAT_needs_proof'
                native.append(row);save(out/'native.json',native);save(out/'raw_witnesses.json',witnesses)
                print(json.dumps(dict(index=i,query=queries,status=row['status'],D=row.get('final_omissions'),seconds=row['worker_wall_seconds'])),flush=True)
            statuses[record['status']]+=1;journal.write(json.dumps(record,separators=(',',':'))+'\n')
            if i%100==0 or record['status']=='SAT':
                journal.flush();save(out/'progress.json',dict(processed=i+1,total=8974,native_queries=queries,status_counts=dict(statuses),seconds=time.monotonic()-start))
    save(out/'raw_witnesses.json',witnesses);save(out/'native.json',native)
    # Final minimization and complete fresh cover; previous UNKNOWN can be covered.
    new=[r for r in witnesses if r['kind']=='native'];by_cut={tuple(r['D']):r for r in new}
    keys=sorted(by_cut,key=lambda D:(len(D),D));minimal=[]
    for D in keys:
        if not any(set(E)<=set(D) for E in minimal):minimal.append(D)
    cert=[dict(index=j,source_index=by_cut[D]['source_index'],D=list(D),colouring=by_cut[D]['colouring']) for j,D in enumerate(minimal)]
    tags=[];uncovered=[];hist=Counter()
    for i,O in enumerate(candidates):
        tag=next((j for j,D in enumerate(minimal) if set(D)<=set(O)),None);tags.append(-1 if tag is None else tag)
        if tag is None:uncovered.append(O)
        else:hist[tag]+=1
    tag_raw=''.join(str(t)+'\n' for t in tags).encode('ascii');(out/'coverage.txt').write_bytes(tag_raw)
    survivor_raw=''.join(','.join(map(str,O))+'\n' for O in uncovered).encode('ascii');(out/'survivors.txt').write_bytes(survivor_raw)
    save(out/'certificate.json',cert)
    result=dict(input_rows=8974,covered=8974-len(uncovered),unresolved=len(uncovered),family_closed=not uncovered,
                native_queries=queries,status_counts=dict(statuses),native_status_counts=dict(Counter(r['status'] for r in native)),
                new_positive_witnesses=len(new),minimal_positive_witnesses=len(cert),cut_size_histogram={str(k):v for k,v in sorted(Counter(map(len,minimal)).items())},
                first_cover_histogram={str(k):v for k,v in sorted(hist.items())},coverage_bytes=len(tag_raw),coverage_sha256=sha256(tag_raw).hexdigest(),
                survivor_bytes=len(survivor_raw),survivor_sha256=sha256(survivor_raw).hexdigest(),frontier_sha256=plan['frontier']['sha256'],
                total_wall_seconds=time.monotonic()-start,record_improvement=False,halt_reason=halt)
    save(out/'result.json',result);print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True);p.add_argument('--graph',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.frontier,a.graph,a.out)
