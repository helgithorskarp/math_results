#!/usr/bin/env python3
"""Execute the frozen covering-graph/conditional-target protocol."""
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
import build as B
import independent as I


def save(p,x):
    q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');q.replace(p)


def native(command,log,seconds,plan):
    def bounds():
        p=plan['limits'];resource.setrlimit(resource.RLIMIT_AS,(p['address_space_bytes'],)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(p['output_file_bytes'],)*2)
    start=time.monotonic()
    with log.open('wb') as f:
        try:r=subprocess.run(list(map(str,command)),stdout=f,stderr=subprocess.STDOUT,timeout=seconds,preexec_fn=bounds);code=r.returncode
        except subprocess.TimeoutExpired:code=None
    return code,time.monotonic()-start


def run(out,kissat,checker):
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text())
    for p,h in plan['input_files'].items():I.check(sha256((HERE.parent/p).read_bytes()).hexdigest()==h,'pinned input')
    for p,k in ((kissat,'solver'),(checker,'checker')):I.check(sha256(p.read_bytes()).hexdigest()==plan[k]['sha256'],'frozen executable')
    _,edges,_=B.geometry();_,other,_=I.geometry();I.check(edges==other,'independent full exact geometry')
    for row in plan['cases']:
        _,raw,_,_=B.formula(row['retained'],edges,4);I.check(raw==I.formula(row['retained'],edges,4)[1] and sha256(raw).hexdigest()==row['cnf_sha256'],'both frozen direct CNFs')
    inherited=json.loads((HERE.parent/'hadwiger_nelson_heule632_minimize/certificate.json').read_text())['five_colouring']
    out.mkdir(parents=True,exist_ok=False);records=[]
    for row in plan['cases']:
        name=row['name'];vs=row['retained'];clauses,raw,_,_=B.formula(vs,edges,4);cnf=out/(name+'.cnf');proof=out/(name+'.drat');log=out/(name+'.log');cnf.write_bytes(raw)
        save(out/'checkpoint.json',{'phase':'COLOUR QUERY IN FLIGHT','name':name,'completed':records})
        code,seconds=native([kissat,*plan['solver']['options'],cnf,proof],log,plan['solver']['outer_seconds'],plan);text=log.read_text();status='SAT' if code==10 and 's SATISFIABLE' in text.splitlines() else 'UNSAT' if code==20 and 's UNSATISFIABLE' in text.splitlines() else 'UNKNOWN'
        record={'name':name,'status':status,'vertices':len(vs),'edges':row['edges'],'cnf_sha256':sha256(raw).hexdigest(),'solver_seconds':seconds,'solver_exit_code':code}
        if status=='SAT':
            colours=B.decode(text,vs,4,clauses);checks=B.check_colouring(colours,vs,edges,4);col=''.join(str(colours[v]) if v in colours else '.' for v in range(632));I.check(I.colouring(col,sorted(set(range(632))-set(vs)),other,4)==checks,'independent positive check');record.update(colouring=col,edge_checks=checks)
        elif status=='UNSAT':
            save(out/'checkpoint.json',{'phase':'PROOF CHECK IN FLIGHT','name':name,'completed':records})
            code,elapsed=native([checker,cnf,proof,*plan['checker']['options']],out/(name+'.check.log'),plan['checker']['outer_seconds'],plan)
            I.check(code==0 and 's VERIFIED' in (out/(name+'.check.log')).read_text().splitlines(),'real proof required')
            col=''.join(c if v in vs else '.' for v,c in enumerate(inherited));checks=I.colouring(col,sorted(set(range(632))-set(vs)),other,5)
            record.update(status='UNSAT_VERIFIED',chromatic_number=5,five_colouring=col,edge_checks=checks,proof_bytes=proof.stat().st_size,proof_sha256=sha256(proof.read_bytes()).hexdigest(),checker_seconds=elapsed)
        records.append(record);save(out/'records.json',records);print(json.dumps({k:v for k,v in record.items() if 'colouring' not in k}),flush=True)
        if name=='free50' and status!='UNSAT':break
    report={'status':'BOUNDED DEGREE-FAMILY PROTOCOL COMPLETE','records':records,'target16_queried':len(records)==2,'free50_subfamily_closed':records[0]['status']=='SAT','degree_screen_excludes_no_cardinality_0_through16':True,'whole560_family_closed':False,'record_improvement':any(r['vertices']<=508 and r['status']=='UNSAT_VERIFIED' for r in records),'seconds':time.monotonic()-start}
    save(out/'result.json',report);save(out/'checkpoint.json',{'phase':'COMPLETE','result':report});print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True)
    a=ap.parse_args();run(a.out,a.kissat,a.drat_trim)
