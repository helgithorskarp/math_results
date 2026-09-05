#!/usr/bin/env python3
"""One seed and bounded core-guided simultaneous block replacement."""
from hashlib import sha256
import argparse
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
from engine import HERE,build,direct_cnf,check_model,require
WORK=None


def save(name,obj):
    p=WORK/name;t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');t.replace(p)


def main():
    global WORK
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True)
    args=ap.parse_args();WORK=args.work.resolve();WORK.mkdir(parents=True,exist_ok=False)
    require(not (WORK/'pilot.json').exists(),'pilot already exists; no restart')
    resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296));start=time.monotonic()
    data=build();save('preflight.json',data['facts'])
    selected=set(data['vertices'])-{data['omit']};I=set(data['interface']);inverse={v:k for k,v in data['activation'].items()}
    result=dict(status='running',seed_omission=data['omit'],queries=[],selected=sorted(selected));save('pilot.json',result)
    with Solver(name='cadical195',bootstrap_with=data['clauses']) as solver:
        def query(candidate,budget):
            assumptions=[data['activation'][v] for v in sorted(candidate-I)]
            solver.conf_budget(budget);t=time.monotonic();answer=solver.solve_limited(assumptions=assumptions)
            row=dict(query=len(result['queries']),selected_vertices=len(candidate),conflict_budget=budget,
                     answer='UNSAT_UNCERTIFIED' if answer is False else 'SAT_CHECKED' if answer is True else 'UNKNOWN',
                     wall_seconds=time.monotonic()-t)
            if answer is True:row['witness']=check_model(data,candidate,solver.get_model())
            if answer is False:
                core=solver.get_core() or [];require(set(core)<=set(assumptions),'assumption-core labels')
                row['core']=sorted(I|{inverse[v] for v in core})
            result['queries'].append(row);save('pilot.json',result)
            print(json.dumps({k:v for k,v in row.items() if k not in ['witness','core']}|({'core_vertices':len(row['core'])} if 'core' in row else {})),flush=True)
            return answer,row
        answer,row=query(selected,100000)
        if answer is not False:
            result['status']='SEED_SAT' if answer else 'SEED_UNKNOWN';result['wall_seconds']=time.monotonic()-start;save('pilot.json',result);return
        selected=set(row['core']);tested=set()
        while len(result['queries'])<129:
            possible=selected-I-tested
            if not possible:break
            v=min(possible,key=lambda v:(v>=509,-data['degree_new'].get(v,0),v));tested.add(v)
            answer,row=query(selected-{v},25000);row['deleted_trial_vertex']=v
            if answer is False:selected=set(row['core'])
            result['selected']=sorted(selected);save('pilot.json',result)
            if len(selected)<=373:break
    raw,vertices,edges=direct_cnf(data,selected);(WORK/'final.cnf').write_bytes(raw)
    result.update(status='FINAL_SIGNATURE_PROOF_PENDING',selected=vertices,final_vertices=len(vertices),final_edges=len(edges),
                  final_new_vertices=sum(v>=509 for v in vertices),final_original_vertices=sum(v<374 for v in vertices),
                  final_cnf_sha256=sha256(raw).hexdigest(),all_remaining_vertices_tested=not(selected-I-tested));save('pilot.json',result)
    t=time.monotonic()
    with (WORK/'final_solver.log').open('w') as f:r=subprocess.run([str(args.kissat.resolve()),'--time=180',str(WORK/'final.cnf'),str(WORK/'final.drat')],stdout=f,stderr=subprocess.STDOUT)
    result['final_solver']=dict(exit_code=r.returncode,wall_seconds=time.monotonic()-t)
    if r.returncode==20:
        t=time.monotonic()
        with (WORK/'final_checker.log').open('w') as f:c=subprocess.run([str(args.drat_trim.resolve()),str(WORK/'final.cnf'),str(WORK/'final.drat')],stdout=f,stderr=subprocess.STDOUT)
        require(c.returncode==0 and 's VERIFIED' in (WORK/'final_checker.log').read_text(),'complete final proof rejected')
        result.update(status='FINAL_BLOCK_SIGNATURE_VERIFIED',final_checker=dict(exit_code=c.returncode,wall_seconds=time.monotonic()-t),
                      final_proof_bytes=(WORK/'final.drat').stat().st_size,final_proof_sha256=sha256((WORK/'final.drat').read_bytes()).hexdigest())
    else:result['status']='FINAL_SIGNATURE_UNCERTIFIED'
    result['wall_seconds']=time.monotonic()-start;save('pilot.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['queries','selected']}),flush=True)


if __name__=='__main__':main()
