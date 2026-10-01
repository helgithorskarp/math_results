#!/usr/bin/env python3
"""Regenerate, definition-audit, and exactly replay all three distance cuts."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import urllib.request

ROOT=Path(__file__).resolve().parent
EXPECTED=json.loads((ROOT/'expected.json').read_text())
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv,seconds=40):
    p=subprocess.run(list(map(str,argv)),text=True,capture_output=True,env=ENV,timeout=seconds)
    require(p.returncode==0,'Child failed: '+p.stderr+p.stdout)
    return p.stdout


def pinned(info,target):
    data=target.read_bytes() if target.exists() else urllib.request.urlopen(info['url'],timeout=20).read()
    require(hashlib.sha256(data).hexdigest()==info['sha256'],'External source hash mismatch')
    target.write_bytes(data)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def solve(cnf,conflicts):
    import pysat
    from pysat.solvers import Solver
    require(pysat.__version__==EXPECTED['solver']['python_sat_version'],'Solver version differs')
    clauses=[list(map(int,row.split()[:-1])) for row in cnf.read_text().splitlines()[1:]]
    t=time.monotonic()
    with Solver(name='cadical195',bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(conflicts);result=solver.solve_limited();stats=solver.accum_stats()
        if result is False:
            require(ctypes.CDLL(None).fflush(None)==0,'Proof stream flush failed')
            cnf.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
        elif result is True:
            cnf.with_suffix('.assignment.json').write_text(json.dumps(solver.get_model())+'\n')
    if conflicts==1:
        require(result is None,'One-conflict control must remain UNKNOWN')
    else:
        require(result is False,'SAT/UNKNOWN is not a refutation')
    print(json.dumps({'status':'UNKNOWN' if result is None else 'UNSAT_PENDING_CHECK',
                      'conflict_budget':conflicts,'stats':stats,'seconds':time.monotonic()-t,
                      'mathematical_exclusion':False}))


def proof_controls(checker,work,cnf,lrat):
    tiny=work/'control.cnf';proof=work/'control.lrat'
    tiny.write_text('p cnf 2 3\n1 2 0\n-1 0\n-2 0\n');proof.write_text('4 0 2 3 1 0\n')
    require(checker.verify(tiny,proof)['mathematical_exclusion'],'Positive proof control rejected')
    invalid=['4 1 0 3 1 0\n','4 0 -1 2 0\n','4 3 0 1 0\n','4 0 99 0\n',
             '4 0 2 3 1\n','4 0 1 0\n','4 d 2 0\n5 0 2 3 1 0\n','3 0 2 3 1 0\n']
    for body in invalid:
        proof.write_text(body)
        try:checker.verify(tiny,proof)
        except (ValueError,KeyError,IndexError):pass
        else:raise ValueError('Malformed proof control accepted')
    lines=lrat.read_text().splitlines();changed=lines.copy();n=int(cnf.read_text().splitlines()[0].split()[2])
    for i,row in enumerate(changed):
        words=row.split()
        if words[1] not in ('d','0'):
            words[1]=str(n+1);changed[i]=' '.join(words);break
    else:raise ValueError('No nonempty production addition')
    damaged=['\n'.join(changed)+'\n','\n'.join(row for row in lines if row.split()[1]!='0')+'\n']
    for body in damaged:
        proof.write_text(body)
        try:checker.verify(cnf,proof)
        except (ValueError,KeyError,IndexError):pass
        else:raise ValueError('Corrupted production proof accepted')
    tiny.unlink();proof.unlink();return {'generic_bad_proofs_rejected':len(invalid),'production_corruptions_rejected':len(damaged)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir',type=Path,default=ROOT/'build')
    parser.add_argument('--solve',type=Path)
    parser.add_argument('--conflicts',type=int,choices=(1,100000),default=100000)
    args=parser.parse_args()
    if args.solve:
        solve(args.solve,args.conflicts);return
    start=time.monotonic();work=args.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
    paths={'cut_generator':work/'base.py','RUP_checker':work/'check_rup_lrat.py','drat_converter':work/'drat-trim.c'}
    for key,path in paths.items():pinned(EXPECTED['sources'][key],path)
    run(['gcc','-O2','-std=gnu99',paths['drat_converter'],'-o',work/'drat-trim'])
    elementary=[]
    for flags in ([],['-O']):
        result=json.loads(run([sys.executable,*flags,ROOT/'elementary.py']))
        require(result==EXPECTED['elementary'],'Combinatorial checks differ');elementary.append(result['status'])
    small=[]
    for q,d in ((7,2),(7,4),(13,4),(13,6),(13,8)):
        cnf=work/f'small-{q}-{d}.cnf'
        run([sys.executable,ROOT/'generate.py','--q',q,'--distance',d,'--base-source',paths['cut_generator'],'--output',cnf])
        result=json.loads(run([sys.executable,ROOT/'check.py',cnf,'--q',q,'--distance',d,'--small-family']))
        small.append(result)
    require(small==EXPECTED['small_family'],'Complete small controls differ')
    require(sum(x['accepted_orientations'] for x in small)>0,'Missing actual positive cases')
    print('COMBINATORIAL_AND_COMPLETE_SMALL_CONTROLS_PASSED',flush=True)
    checker=module(paths['RUP_checker'],'strict_positive_RUP_checker');cases=[]
    for reference in EXPECTED['cases']:
        d=reference['model']['distance'];cnf=work/f'distance-{d}.cnf'
        generated=json.loads(run([sys.executable,ROOT/'generate.py','--distance',d,'--base-source',paths['cut_generator'],'--output',cnf]))
        require(generated==reference['model'],'Exact generated model differs')
        for flags in ([],['-O']):
            audited=json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--distance',d,'--controls']))
            require(audited==reference['audit'],'Definition-level model audit differs')
        print(f'DISTANCE_{d}_NORMAL_AND_OPTIMIZED_MODEL_AUDITED',flush=True)
        proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],seconds=35))
        lrat=cnf.with_suffix('.lrat');drat=cnf.with_suffix('.drat')
        conversion=run([work/'drat-trim',cnf,drat,'-t','25','-L',lrat],seconds=30)
        cnf.with_suffix('.conversion.log').write_text(conversion)
        require('VERIFIED' in conversion,'Conversion failed; no exclusion')
        replays=[]
        for flags in ([],['-O']):
            checked=json.loads(run([sys.executable,*flags,paths['RUP_checker'],cnf,lrat]))
            checked.pop('seconds',None)
            require(checked['mathematical_exclusion'] and checked['cnf_sha256']==generated['model_sha256'],
                    'Proof does not exactly refute the audited model')
            replays.append(checked)
        require(replays[0]==replays[1],'Normal/optimized replay mismatch')
        bad=proof_controls(checker,work,cnf,lrat)
        unknown=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf,'--conflicts',1]))
        require(unknown['status']=='UNKNOWN','Incomplete proposal control differs')
        cases.append({'model':generated,'proof':replays[0],'proposal':proposal,'controls':bad,
                      'reference_trace_match':sha(drat)==reference['drat_sha256'] and sha(lrat)==reference['proof']['proof_sha256'],
                      'normal_and_optimized_audits_and_replays':True,'one_conflict_UNKNOWN_control':True})
        print(f'DISTANCE_{d}_EXACT_REFUTATION_AND_CORRUPTION_CONTROLS_PASSED',flush=True)
    summary={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_DERIVATIVE_RANGE_32_72_AND_WEIGHT_20_83',
             'cases':cases,'elementary_checks':elementary,'small_family':small,
             'seconds':time.monotonic()-start,
             'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
             'full_separable_family_excluded':False,'length3704_witness_found':False,'new_W_bound':False}
    (work/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('cases','small_family')},sort_keys=True))


if __name__=='__main__':main()
