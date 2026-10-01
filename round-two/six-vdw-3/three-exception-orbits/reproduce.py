#!/usr/bin/env python3
"""Reproduce the complete structural cover, model audits and frozen RUP cuts."""
import argparse
import ctypes
import hashlib
import importlib.metadata
import json
import os
import resource
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def need(condition,message):
    if not condition:raise ValueError(message)

def run(argv,limit):
    result=subprocess.run(list(map(str,argv)),text=True,capture_output=True,env=ENV,timeout=limit)
    need(result.returncode==0,'Child failed: '+result.stderr+result.stdout)
    return result.stdout

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def source(info,path):
    data=path.read_bytes() if path.exists() else urllib.request.urlopen(info['url'],timeout=20).read()
    need(hashlib.sha256(data).hexdigest()==info['sha256'],'External source hash differs')
    path.write_bytes(data)

def solve(cnf,cap):
    import pysat
    from pysat.solvers import Solver
    need(pysat.__version__=='1.8.dev24','Solver version differs')
    clauses=[list(map(int,row.split()[:-1])) for row in cnf.read_text().splitlines()[1:]]
    begin=time.monotonic()
    with Solver(name='cadical195',bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(cap);answer=solver.solve_limited();stats=solver.accum_stats()
        if answer is False:
            need(ctypes.CDLL(None).fflush(None)==0,'Proof stream flush failed')
            cnf.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
        if answer is True:cnf.with_suffix('.assignment.json').write_text(json.dumps(solver.get_model())+'\n')
    print(json.dumps({'status':{None:'UNKNOWN',False:'UNSAT_PENDING_CHECK',True:'SAT_PENDING_CHECK'}[answer],
                      'conflict_budget':cap,'stats':stats,'seconds':time.monotonic()-begin,'mathematical_exclusion':False}))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir',type=Path,default=ROOT/'build')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--solve',type=Path);parser.add_argument('--conflicts',type=int,choices=(1,100000),default=100000)
    parser.add_argument('--only',help='Native/pipeline smoke selection, e.g. same-2; never a full-family certificate')
    args=parser.parse_args()
    if args.solve:solve(args.solve,args.conflicts);return
    expected_path=ROOT/'expected.json'
    need(expected_path.is_file(),'Frozen expected evidence must exist before validation')
    expected_digest=digest(expected_path);expected=json.loads(expected_path.read_text())
    begin=time.monotonic();work=args.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
    checker=work/'check_rup_lrat.py';converter=work/'drat-trim.c'
    source(expected['sources']['RUP_checker'],checker)
    source(expected['sources']['drat_converter'],converter)
    run(['gcc','-O2','-std=gnu99',converter,'-o',work/'drat-trim'],15)
    selected=[row for row in expected['cases'] if args.only is None or row['name']==args.only]
    need(selected,'No matching case')
    full=args.only is None
    if full:
        manifest=work/'cases.json'
        run([sys.executable,ROOT/'normalize.py','--output',manifest],10)
        need(json.loads(manifest.read_text())==expected['manifest'],'Complete representative manifest differs')
        for flags in ([],['-O']):
            receipt=work/('orbits-'+str(bool(flags))+'.json')
            run([sys.executable,*flags,ROOT/'check_orbits.py',manifest,'--output',receipt],60)
            result=json.loads(receipt.read_text())
            result.pop('seconds');result.pop('peak_KiB')
            need(result==expected['orbit_audit'],'Complete orbit replay differs')
        for flags in ([],['-O']):
            controls=json.loads(run([sys.executable,*flags,ROOT/'controls.py','--checker',checker],30))
            need(controls==expected['controls'],'Complete controls differ')
        for ref in expected['small']:
            q,kind,lam=ref['q'],ref['kind'],ref['lambda'];cnf=work/(str(q)+'-'+kind+'-'+str(lam)+'.cnf')
            run([sys.executable,ROOT/'generate.py','--q',q,'--kind',kind,'--lambda',lam,'--output',cnf],10)
            for flags in ([],['-O']):
                result=json.loads(run([sys.executable,*flags,ROOT/'check_model.py',cnf,'--q',q,'--kind',kind,'--lambda',lam,'--small'],50))
                need(result==ref,'Complete small orientation replay differs')
    cases=[]
    for ref in selected:
        name=ref['name'];kind,lam=ref['model']['kind'],ref['model']['lambda']
        cnf=work/(name+'.cnf');drat=cnf.with_suffix('.drat');lrat=cnf.with_suffix('.lrat')
        model=json.loads(run([sys.executable,ROOT/'generate.py','--kind',kind,'--lambda',lam,'--output',cnf],15))
        need(model==ref['model'],'Complete production CNF differs')
        for flags in ([],['-O']):
            audit=json.loads(run([sys.executable,*flags,ROOT/'check_model.py',cnf,'--kind',kind,'--lambda',lam],20))
            audit.pop('seconds');need(audit==ref['audit'],'Literal cyclic production model audit differs')
        density=json.loads(run([sys.executable,ROOT/'density.py','--kind',kind,'--lambda',lam],10))
        need(density==ref['density'] and density['cnf_clauses']==model['clauses'],'Pair/triple interaction formula differs')
        proposal={'status':'RESUMED_PROPOSAL','mathematical_exclusion':False}
        if not(args.resume and drat.exists() and lrat.exists()):
            proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],35))
            need(proposal['status']=='UNSAT_PENDING_CHECK','Incomplete proposal: no exclusion follows')
            conversion=run([work/'drat-trim',cnf,drat,'-t','25','-L',lrat],30)
            cnf.with_suffix('.conversion.log').write_text(conversion)
        need(digest(drat)==ref['drat_sha256'],'Native proof bytes differ from frozen reference')
        for flags in ([],['-O']):
            replay=json.loads(run([sys.executable,*flags,checker,cnf,lrat],50));replay.pop('seconds',None)
            need(replay==ref['proof'],'Strict positive-RUP replay differs')
        cases.append({'name':name,'model_sha256':model['cnf_sha256'],'proof_sha256':ref['proof']['proof_sha256'],
                      'checked_additions':ref['proof']['checked_additions'],'propagation_hints_checked':ref['proof']['propagation_hints_checked'],
                      'normal_and_optimized_model_and_proof_checks':True,'proposal':proposal})
        summary={'agent':'six-vdw-3','role':'researcher','status':'PARTIAL_EXACT_REPLAY_CHECKPOINT',
                 'completed_cases':cases,'full_family_excluded':False,'expected_sha256':expected_digest}
        (work/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps({'stage':'EXACT_CASE_REPLAYED','name':name,'completed':len(cases),'selected':len(selected)}),flush=True)
    need(digest(expected_path)==expected_digest,'Frozen evidence changed during validation')
    if full:
        need(len(cases)==69 and {row['name'] for row in cases}=={row['name'] for row in expected['cases']},'Incomplete cover')
    production_corruptions=0
    for kind in ('same','mixed'):
        example=next((row for row in selected if row['model']['kind']==kind),None)
        if example is None:continue
        cnf=work/(example['name']+'.cnf')
        for flags in ([],['-O']):
            controls=json.loads(run([sys.executable,*flags,ROOT/'controls.py','--checker',checker,
                                    '--production-cnf',cnf,'--production-lrat',cnf.with_suffix('.lrat')],30))
            need(controls['production_damaged_proofs_rejected']==2,'Production corruption controls differ')
            production_corruptions+=2
    # UNKNOWN remains an incomplete control, never a mathematical refutation.
    control=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',work/(selected[0]['name']+'.cnf'),'--conflicts',1],35))
    need(control['status']=='UNKNOWN' and not control['mathematical_exclusion'],'UNKNOWN control misclassified')
    changed=work/'changed_checker.py';changed.write_bytes(checker.read_bytes()+b'\n# changed pin\n')
    try:source(expected['sources']['RUP_checker'],changed)
    except ValueError:pass
    else:raise ValueError('Changed checker pin accepted')
    changed.unlink()
    result={'agent':'six-vdw-3','role':'researcher',
            'status':'VERIFIED_ALL_THREE_EXCEPTION_CUTS' if full else 'VERIFIED_SELECTED_PIPELINE_SMOKE_ONLY',
            'full_family_excluded':full,'cases':cases,'expected_sha256':expected_digest,
            'frozen_expected_existed_before_validation':True,'one_conflict_UNKNOWN_control':True,
            'changed_checker_pin_rejected':True,'seconds':time.monotonic()-begin,
            'production_damaged_proofs_rejected_normal_and_optimized':production_corruptions,
            'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'runtime':{'python':sys.version.split()[0],'python_sat':importlib.metadata.version('python-sat'),'six':importlib.metadata.version('six')},
            'mathematical_inputs_not_recomputed':expected['mathematical_inputs_not_recomputed']}
    (work/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
