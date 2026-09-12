"""Actual certificate admission across original strata, including mixed q8,r8.

This receiver never accepts status-only receipts. UNKNOWN/missing proofs leave
parents UNKNOWN. No transaction or historical queue is modified.
"""
from pathlib import Path
import argparse,importlib.util,json,subprocess,sys
from common import HERE,Q8,ROOT,LOCAL,need,dependencies,core_guards,assumptions,sha
from registry import ranges
sys.path.insert(0,str(Q8))
import worker

def root_checker():
    spec=importlib.util.spec_from_file_location('cross_join_root_checker',ROOT/'independent_check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def exact_job(cert,r,guard):
    need(cert.get('r')==r and type(cert.get('r')) is int,'wrong proof base')
    need(cert.get('core_assumptions')==assumptions(guard),'proof is not for the complete specified cohort')
    need(cert.get('edge_cube')==([119] if r==8 else []),'missing positive edge or unresolved physical child')

def drat_job(queue,r,guard,cnf,proof,checker):
    """Check actual whole-worker DIMACS and DRAT; no metadata-only admission."""
    need(checker is not None,'DRAT checker executable required')
    meta,raw=worker.base_bytes(queue,r);base_header,body=raw.split(b'\n',1)
    need(base_header==f"p cnf {meta['variables']} {meta['clauses']}".encode(),'full base header')
    units=assumptions(guard)+([119] if r==8 else [])
    expected=f"p cnf {meta['variables']} {meta['clauses']+len(units)}\n".encode()+body+''.join(f'{x} 0\n' for x in units).encode()
    need(Path(cnf).read_bytes()==expected,'DRAT input is not the complete exact cohort formula')
    input_sha,proof_sha=sha(cnf),sha(proof)
    result=subprocess.run([str(checker),str(cnf),str(proof)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    need(result.returncode==0 and b's VERIFIED' in result.stdout,'actual whole-cohort DRAT check failed or incomplete')
    need(sha(cnf)==input_sha and sha(proof)==proof_sha,'proof/input changed while checking')
    return {'input_sha256':input_sha,'proof_sha256':proof_sha,'checker_sha256':sha(checker),'format':'CHECKED_DRAT_WHOLE_PHYSICAL_COHORT'}

def local19(catalog,proofs,checker):
    # Recheck every trace against an independently grounded original formula.
    command=[sys.executable,'-O','-B',str(LOCAL/'audit_saved.py'),str(Path(catalog)/'r44_15.g6'),str(proofs),str(checker),'--workers','2']
    proc=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    need(proc.returncode==0,'local 19 proof audit failed: '+proc.stderr[-1000:]);result=json.loads(proc.stdout)
    need(result['status']=='ALL_640_SAVED_PROOFS_RECHECKED' and result['proofs_verified']==640,'complete local proof corpus required')
    return result

def receive(queue,proof_directory,catalog=None,local_proofs=None,checker=None):
    dependencies();guards=core_guards(queue);proof_directory=Path(proof_directory);rows=[];closed={r:0 for r in range(5,9)}
    # This is a mixed-premise certificate, never passed to the LRAT importer.
    neg=json.loads((ROOT/'branch-certificate.json').read_text());negative=root_checker().check(queue,neg)
    for r in range(5,9):
        for leaf,guard in enumerate(guards):
            path=proof_directory/f'r{r}-cohort{leaf:03d}.json'
            row={'r':r,'cohort':leaf,'core_assumptions':assumptions(guard),'edge_cube':[119] if r==8 else [],'status':'UNKNOWN'}
            if path.exists():
                need(not path.with_suffix('.cnf').exists() and not path.with_suffix('.drat').exists(),'ambiguous dual proof formats')
                cert=json.loads(path.read_text());exact_job(cert,r,guard)
                worker.verify(queue,cert)  # Reads the pinned full base and checks every actual hinted RUP step.
                row.update(status='CERTIFIED_COHORT_UNSAT_WITH_IMPORTED_RAMSEY_THEOREM' if r==8 else 'CERTIFIED_COHORT_UNSAT',proof_sha256=sha(path))
                closed[r]+=1
            else:
                cnf,proof=path.with_suffix('.cnf'),path.with_suffix('.drat')
                if cnf.exists() and proof.exists():
                    receipt=drat_job(queue,r,guard,cnf,proof,checker)
                    row.update(receipt,status='CERTIFIED_COHORT_UNSAT_WITH_IMPORTED_RAMSEY_THEOREM' if r==8 else 'CERTIFIED_COHORT_UNSAT');closed[r]+=1
                elif cnf.exists() or proof.exists():row['status']='INCOMPLETE_PROOF_INPUT_PARENT_UNKNOWN'
            rows.append(row)
    local_receipt=None
    if any(closed[r]==239 for r in (5,6)):
        need(all(x is not None for x in [catalog,local_proofs,checker]),'all 640 local proofs required before q7 original admission')
        local_receipt=local19(catalog,local_proofs,checker)
        from local_pullback import run as pullback
        mapped=pullback(catalog,local_proofs)
        local_receipt['original_branch_pullback_status']=mapped['status']
        local_receipt['original_branches']=mapped['original_task_branches']
    admitted=[x for x in ranges() if x['route']=='Q8_PHYSICAL' and closed[x['r']]==239]
    total=sum(x['count'] for x in admitted);old_overlap=518 if closed[5]==239 else 0
    return {'status':'ALL_Q8_MACRO_FAMILIES_CERTIFIED_UNSAT' if all(n==239 for n in closed.values()) else 'COMPLETE_JOIN_PENDING',
            'physical_units':rows,'complete_r_counts':{str(r):n for r,n in closed.items()},
            'original_ranges_certified_unsat':admitted,'original_ids_certified_by_this_join':total,
            'overlap_with_518_inherited_exclusions':old_overlap,'new_original_exclusions':total-old_overlap,
            'local19_receiving_audit':local_receipt,'negative_r8_receiving_audit':negative,
            'remaining_original_parent_ranges':[x for x in ranges() if x['route']=='ORIGINAL_PARENT'],
            'ramsey_number_decided':False,'notes':['The 1010 original-parent complement is not admitted by this join.',
            'For r8 a checked positive proof joins the separately checked negative certificate with its explicit R(4,5)<=25 premise.',
            'Existing 518 original exclusions remain separate; any overlap must be deduplicated by exact ID.']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('queue');p.add_argument('proof_directory');p.add_argument('--catalog');p.add_argument('--local-proofs');p.add_argument('--checker');s=p.parse_args()
    print(json.dumps(receive(s.queue,s.proof_directory,s.catalog,s.local_proofs,s.checker),indent=2,sort_keys=True))
