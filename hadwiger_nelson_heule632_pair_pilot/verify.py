#!/usr/bin/env python3
"""Independently verify the exact seed, positive colours and a DRAT proof.

No producing graph/CNF/runner module is imported. A proof can be supplied,
read from the original run, or regenerated with the provided solver.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
import independent as I

HERE=Path(__file__).resolve().parent


def limit_child():
    p=json.loads((HERE/'plan.json').read_text())['limits']
    resource.setrlimit(resource.RLIMIT_AS,(p['address_space_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(p['proof_file_bytes'],)*2)


def call(command,log,seconds):
    start=time.monotonic()
    with log.open('wb') as f:
        p=subprocess.run(list(map(str,command)),stdout=f,stderr=subprocess.STDOUT,timeout=seconds,preexec_fn=limit_child)
    return p.returncode,time.monotonic()-start


def check_model(log,clauses,vertices,k,expected):
    literals=[int(x) for line in log.splitlines() if line.startswith('v ') for x in line.split()[1:] if x!='0']
    truth={abs(x):x>0 for x in literals}
    I.check(len(truth)==len(literals)==k*len(vertices) and set(truth)==set(range(1,k*len(vertices)+1)),'complete signed model')
    for clause in clauses:I.check(any(truth[abs(x)]==(x>0) for x in clause),'every native model clause')
    result=['.']*632
    for i,v in enumerate(vertices):
        colours=[c for c in range(k) if truth[k*i+c+1]];I.check(len(colours)==1,'one-hot model');result[v]=str(colours[0])
    I.check(''.join(result)==expected,'independent native model decode')
    return len(clauses)


def verify(out,drat,proof=None,archive=None,kissat=None):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((HERE/'plan.json').read_text());prep=json.loads((HERE/'preparation.json').read_text())
    I.check(sha256((HERE/'preparation.json').read_bytes()).hexdigest()==plan['preparation_sha256'],'frozen preparation bytes')
    points,edges,large=I.geometry();I.check(I.selection(edges,large)==prep,'independent pair ranking and24 frozen formulas')
    cert=json.loads((HERE/'certificate.json').read_text());cases=json.loads((HERE/'cases.json').read_text());result=json.loads((HERE/'result.json').read_text())
    idx=cert['winner_index'];row=prep['selected'][idx];omitted=cert['omitted'];I.check(omitted==row['omitted']==[399,462] and idx==5,'fixed winning support')
    vertices=sorted(set(range(632))-set(omitted));es=[(u,v) for u,v in edges if u in vertices and v in vertices]
    I.check((len(vertices),len(es))==(630,3098),'exact seed size')
    clauses,raw,vs,tri=I.formula(vertices,edges,4);(out/'four.cnf').write_bytes(raw)
    I.check(sha256(raw).hexdigest()==row['cnf_sha256']==cert['four_cnf_sha256'],'independent winning CNF')
    I.check(len(clauses)==16805 and len(vs)*4==2520 and tri==[0,143,146],'winning encoding domain')
    five_checks=I.colouring(cert['five_colouring'],omitted,edges,5)
    prefix_checks=0
    I.check([r['index'] for r in cert['four_colourings']]==list(range(idx)),'complete positive prefix')
    for positive in cert['four_colourings']:
        p=prep['selected'][positive['index']]
        I.check(positive['omitted']==p['omitted'],'prefix omission identity')
        prefix_checks+=I.colouring(positive['colouring'],positive['omitted'],edges,4)
    I.check([r['index'] for r in cases]==list(range(idx+1)) and [r['status'] for r in cases]==['SAT']*idx+['UNSAT_VERIFIED'],'exact stopped prefix')
    for record,p in zip(cases,prep['selected']):
        for key,value in p.items():I.check(record[key]==value,('frozen case',key))
    I.check(result['attempted']==6 and result['unattempted']==18 and result['outcomes']=={'SAT':5,'UNSAT_VERIFIED':1} and result['winner']==5 and result['five_colour_certificate'],'public pilot boundary')
    model_clauses=0
    if archive is not None:
        I.check(json.loads((archive/'records.json').read_text())==cases,'original execution records')
        for record in cases:
            i=record['index'];cs,data,sel,_=I.formula(set(range(632))-set(record['omitted']),edges,4)
            I.check(data==(archive/f'{i:02d}.cnf').read_bytes(),'independent native formula bytes')
            if record['status']=='SAT':model_clauses+=check_model((archive/f'{i:02d}.log').read_text(),cs,sel,4,cert['four_colourings'][i]['colouring'])
        cs,data,sel,_=I.formula(vertices,edges,5);I.check(data==(archive/'five.cnf').read_bytes(),'independent five-colour formula')
        model_clauses+=check_model((archive/'five.log').read_text(),cs,sel,5,cert['five_colouring'])
        proof=archive/f'{idx:02d}.drat'
        I.check(sha256(proof.read_bytes()).hexdigest()==cert['original_proof_sha256'],'original proof identity')
    regenerated=False;solver_seconds=None
    if kissat is not None:
        I.check(proof is None,'choose one proof source');proof=out/'regenerated.drat'
        code,solver_seconds=call([kissat,*plan['solver']['options'],out/'four.cnf',proof],out/'regenerate.log',plan['limits']['solver_outer_wall_seconds'])
        I.check(code==20 and 's UNSATISFIABLE' in (out/'regenerate.log').read_text().splitlines(),'regenerated refutation verdict');regenerated=True
    I.check(proof is not None and proof.is_file(),'a real proof is required for the lower bound')
    code,checker_seconds=call([drat,out/'four.cnf',proof,*plan['proof_checker']['options']],out/'drat.log',plan['limits']['checker_outer_wall_seconds'])
    I.check(code==0 and 's VERIFIED' in (out/'drat.log').read_text().splitlines(),'independent DRAT verification')
    rejected=0
    bads=[cert['five_colouring'][:-1],cert['five_colouring'].replace('.', '0',1)]
    bad=list(cert['five_colouring']);u,v=es[0];bad[v]=bad[u];bads.append(''.join(bad))
    for bad in bads:
        try:I.colouring(bad,omitted,edges,5)
        except ValueError:rejected+=1
        else:raise ValueError('malformed positive certificate accepted')
    report={'status':'EXACT630-VERTEX FIVE-CHROMATIC UNIT-DISTANCE GRAPH VERIFIED','vertices':630,'unit_edges':3098,'omitted_old_vertices':omitted,'chromatic_number':5,
            'exact_coordinate_pairs':199396,'full_host_edge_sha256':prep['edge_sha256'],'frozen_pair_formulas_rebuilt':24,
            'four_cnf_variables':2520,'four_cnf_clauses':16805,'four_cnf_sha256':sha256(raw).hexdigest(),
            'five_colouring_edge_checks':five_checks,'prefix_four_colouring_edge_checks':prefix_checks,'native_model_clauses_checked':model_clauses,
            'proof_sha256':sha256(proof.read_bytes()).hexdigest(),'proof_bytes':proof.stat().st_size,'proof_regenerated':regenerated,'solver_seconds':solver_seconds,'proof_checker_seconds':checker_seconds,
            'malformed_colourings_rejected':rejected,'original_archive_audited':archive is not None,'record_improvement':False,'minimality_claimed':False,
            'independent_author_review_claimed':False,'seconds':time.monotonic()-start}
    (out/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True)
    g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--proof',type=Path);g.add_argument('--archive',type=Path);g.add_argument('--regenerate-with',type=Path,metavar='KISSAT')
    a=ap.parse_args();verify(a.out,a.drat_trim,a.proof,a.archive,a.regenerate_with)
