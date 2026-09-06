#!/usr/bin/env python3
"""Exact final geometry, positive certificates and a mandatory checked refutation.

The exploratory selector solver and its negative verdicts are not imported.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def save(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')


def run_native(command,log,seconds,limits):
    def bounded():
        resource.setrlimit(resource.RLIMIT_AS,(limits['address_space_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_FSIZE,(limits['output_file_bytes'],)*2)
    start=time.monotonic()
    with log.open('wb') as stream:
        try:r=subprocess.run(list(map(str,command)),stdout=stream,stderr=subprocess.STDOUT,timeout=seconds,preexec_fn=bounded);code=r.returncode
        except subprocess.TimeoutExpired:code=None
    return code,time.monotonic()-start


def check_positive(text,domain,edges,k):
    return I.colouring(text,sorted(set(range(632))-set(domain)),edges,k)


def verify(out,archive,solver,checker,proof):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=False)
    plan=json.loads((HERE/'plan.json').read_text())
    for rel,digest in plan['input_files'].items():I.check(sha256((HERE.parent/rel).read_bytes()).hexdigest()==digest,'pinned input')
    points,edges,_=I.geometry();initial=set(range(632))-{399,462}
    if archive is not None:data=json.loads((archive/'search_result.json').read_text())
    else:data=json.loads((HERE/'certificate.json').read_text())
    vertices=data['retained'];active=set(vertices);I.check(vertices==sorted(active) and active<=initial,'exact retained seed subset')
    omitted=sorted(set(range(632))-active);es=[(u,v) for u,v in edges if u in active and v in active]
    I.check(data['vertices']==len(active) and data['unit_edges']==len(es),'exact counts')
    checks5=check_positive(data['five_colouring'],active,edges,5)
    clauses,raw,_,triangle=I.formula(vertices,edges,4);cnf=out/'four.cnf';cnf.write_bytes(raw);digest=sha256(raw).hexdigest()
    archive_report=None
    if archive is not None:
        rows=json.loads((archive/'final_deletions.json').read_text());checks=0
        for label,row in rows.items():
            v=int(label);I.check(v in active,'deletion vertex retained');checks+=check_positive(row['colouring'],active-{v},edges,4)
        I.check(len(rows)==data['singleton_witnesses'] and sorted(active-set(map(int,rows)))==data['unresolved_singletons'],'exact singleton coverage')
        initial_rows=json.loads((HERE/'initial_positive.json').read_text());library={r['source']:r['colouring'] for r in initial_rows}
        initial_checks=0
        for text in library.values():initial_checks+=check_positive(text,{v for v,c in enumerate(text) if c!='.'},edges,4)
        positive_rows=[json.loads(line) for line in (archive/'positive.jsonl').read_text().splitlines()];positives={r['source']:r for r in positive_rows}
        neighbours={v:set() for v in range(632)}
        for u,v in edges:neighbours[u].add(v);neighbours[v].add(u)
        state=set(initial);nquery=0;nchecked=0;event_list=json.loads((archive/'events.json').read_text());previous=-1
        for event in event_list:
            v=event['vertex'];index=event['index'];status=event['status'];I.check(index>=previous and v in state,'ordered retained event');previous=index
            if status=='DEGREE_REMOVED':
                low=[u for u in sorted(state) if len(neighbours[u]&state)<=3]
                I.check(low and low[0]==v,'smallest low-degree vertex');state.remove(v)
            else:
                I.check(plan['order'][index]==v,'frozen ordered query')
                if status=='POSITIVE_COVER':
                    text=library[event['source']];I.check(state-{u for u,c in enumerate(text) if c!='.'}=={v},'valid positive inclusion')
                else:
                    tag='query:'+str(nquery);nquery+=1
                    if status=='SAT_VERIFIED':
                        row=positives[tag];I.check(row['vertex']==v,'positive query vertex');nchecked+=check_positive(row['colouring'],state-{v},edges,4);library[tag]=row['colouring']
                    elif status=='UNSAT_PROVISIONAL':state.remove(v)
                    else:I.check(status=='UNKNOWN','known search event')
            I.check(event['vertices_after']==len(state),'event support size')
        I.check(state==active and nquery==data['native_queries'],'final search replay')
        archive_report={'event_count':len(event_list),'native_queries':nquery,'initial_positive_edge_checks':initial_checks,'native_positive_edge_checks':nchecked,'final_singleton_edge_checks':checks,'singleton_witnesses':len(rows),'unresolved_singletons':sorted(active-set(map(int,rows))),'raw_final_deletions_sha256':sha256((archive/'final_deletions.json').read_bytes()).hexdigest()}
    else:
        I.check(digest==data['four_cnf_sha256'] and len(clauses)==data['four_cnf_clauses'],'public direct formula identity')
    solver_seconds=None
    if solver is not None:
        proof=out/'four.drat';code,solver_seconds=run_native([solver,*plan['final_solver']['options'],cnf,proof],out/'solver.log',plan['final_solver']['outer_seconds'],plan['limits'])
        I.check(code==20 and 's UNSATISFIABLE' in (out/'solver.log').read_text().splitlines(),'fresh direct refutation; otherwise no lower-bound claim')
    I.check(proof is not None and proof.is_file(),'real proof required')
    code,checker_seconds=run_native([checker,cnf,proof,*plan['proof_checker']['options']],out/'drat.log',plan['proof_checker']['outer_seconds'],plan['limits'])
    I.check(code==0 and 's VERIFIED' in (out/'drat.log').read_text().splitlines(),'DRAT checker acceptance')
    bad=list(data['five_colouring']);u,v=es[0];bad[v]=bad[u]
    try:check_positive(''.join(bad),active,edges,5)
    except ValueError:pass
    else:raise ValueError('improper positive accepted')
    certificate={'status':'EXACT FIVE-CHROMATIC SEED VERIFIED','vertices':len(active),'unit_edges':len(es),'chromatic_number':5,'retained':vertices,'omitted':omitted,'five_colouring':data['five_colouring'],'four_cnf_variables':4*len(active),'four_cnf_clauses':len(clauses),'four_cnf_sha256':digest,'triangle':triangle,'original_proof_sha256':sha256(proof.read_bytes()).hexdigest(),'original_proof_bytes':proof.stat().st_size,'record_improvement':len(active)<=508,'minimality_claimed':False}
    save(out/'certificate.json',certificate)
    report={'status':certificate['status'],'vertices':len(active),'unit_edges':len(es),'exact_host_pairs':199396,'five_colour_edge_checks':checks5,'four_cnf_sha256':digest,'proof_sha256':certificate['original_proof_sha256'],'proof_bytes':proof.stat().st_size,'proof_regenerated':solver is not None,'solver_seconds':solver_seconds,'checker_seconds':checker_seconds,'archive_audit':archive_report,'seconds':time.monotonic()-start,'record_improvement':certificate['record_improvement'],'minimality_claimed':False,'independent_author_review_claimed':False}
    save(out/'verification.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--archive',type=Path);ap.add_argument('--drat-trim',type=Path,required=True)
    g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--regenerate-with',type=Path);g.add_argument('--proof',type=Path)
    a=ap.parse_args();verify(a.out,a.archive,a.regenerate_with,a.drat_trim,a.proof)
