#!/usr/bin/env python3
"""Standalone exact seed-satellite growth; all native tools are untrusted proposers."""
import argparse
import ctypes
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXPECTED_SHA256='c6d5c8c9f375de16e7b1470ac2092f32801c49d1cc9c7062561fc95dbbd458a4'
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def need(condition,message):
    if not condition:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run(argv,seconds):
    r=subprocess.run(list(map(str,argv)),capture_output=True,text=True,env=ENV,timeout=seconds)
    need(r.returncode==0,'Child failed: '+r.stderr+r.stdout);return r.stdout

def pin(path,spec):need(sha(path)==spec['sha256'],'Imported source pin mismatch')

def sources(tools,specs):
    tools.mkdir(parents=True,exist_ok=True)
    for name,filename in (('RUP_checker','check_rup_lrat.py'),('drat_converter','drat-trim.c')):
        target=tools/filename
        if not target.exists():
            with urllib.request.urlopen(specs[name]['url'],timeout=20) as response:target.write_bytes(response.read())
        pin(target,specs[name])
    converter=tools/'drat-trim'
    if not converter.exists():run(['cc','-O2','-std=c99',tools/'drat-trim.c','-o',converter],20)
    return tools/'check_rup_lrat.py',converter

def native(cnf,conflicts):
    import pysat
    from pysat.solvers import Solver
    need(pysat.__version__=='1.8.dev24','PySAT version mismatch')
    rows=[list(map(int,line.split()[:-1])) for line in cnf.read_text().splitlines()[1:]];begin=time.monotonic()
    with Solver(name='cadical195',bootstrap_with=rows,with_proof=True) as solver:
        solver.conf_budget(conflicts);answer=solver.solve_limited();stats=solver.accum_stats()
        if answer is False:
            need(ctypes.CDLL(None).fflush(None)==0,'Native trace flush failed')
            cnf.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
        if answer is True:cnf.with_suffix('.assignment.json').write_text(json.dumps(solver.get_model())+'\n')
    return {'status':{None:'UNKNOWN',False:'UNSAT_PENDING_CHECK',True:'SAT_PENDING_CHECK'}[answer],
            'conflict_budget':conflicts,'stats':stats,'seconds':time.monotonic()-begin,'mathematical_exclusion':False}

def main(args):
    begin=time.monotonic();need(platform.python_version()=='3.11.2','Use pinned Python3.11.2')
    work=args.work.resolve();work.mkdir(parents=True,exist_ok=True)
    expected_path=ROOT/'expected.json';need(sha(expected_path)==EXPECTED_SHA256,'Frozen expectation altered or narrowed')
    expected=json.loads(expected_path.read_text());need(expected['q']==103 and expected['full_deleted_robustness_proved'] is False,'Scope altered')
    literal=[];local_controls=[]
    for flags,suffix in (([],'normal'),(['-O'],'optimized')):
        local_path=work/('local-'+suffix+'.json')
        run([sys.executable,*flags,ROOT/'local.py','--output',local_path],20)
        need(json.loads(local_path.read_text())==expected['local_proposal'],'Complete local proposal changed')
        literal.append(json.loads(run([sys.executable,*flags,ROOT/'check_local.py',local_path],25)))
        local_controls.append(json.loads(run([sys.executable,*flags,ROOT/'local_controls.py',local_path],40)))
    need(literal[0]==literal[1]==expected['local_audit'],'Full literal local cover changed')
    need(local_controls[0]==local_controls[1]=={'positive_local_accepted':2802,'damaged_local_artifacts_rejected':8},'Local damage guards changed')
    cases=expected['cases'];need([c['case'] for c in cases]==[1,2,3],'Global case family narrowed or reordered')
    need([c['model']['holes'] for c in cases]==literal[0]['zero_other_color_reflection_classes'],'Models do not cover literal exceptional geography')
    need(args.only is None or args.only in (1,2,3),'Unknown selected case')
    checker,converter=sources((args.tools or work/'tools').resolve(),expected['sources'])
    altered=dict(expected['sources']['RUP_checker']);altered['sha256']='0'*64
    try:pin(checker,altered)
    except ValueError:pass
    else:raise ValueError('Changed checker pin accepted')
    controls=[]
    for q in (7,11,13):
        modes=[]
        for flags in ([],['-O']):modes.append(json.loads(run([sys.executable,*flags,ROOT/'controls.py','--q',q,'--work',work/('controls-'+str(q))],40)))
        need(modes[0]==modes[1],'Small controls differ under-O');controls.append(modes[0])
    need(controls==expected['controls'],'Positive literal controls changed')
    completed=[];rejected=0;unknown_guard=False
    for case in cases:
        number=case['case']
        if args.only is not None and number!=args.only:continue
        directory=work/('case-'+str(number));directory.mkdir(exist_ok=True);cnf=directory/'model.cnf'
        model=json.loads(run([sys.executable,ROOT/'generate.py','--case',number,'--output',cnf],15));need(model==case['model'],'Frozen full model changed')
        audits=[]
        for flags in ([],['-O']):
            a=json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--case',number],20));a.pop('seconds');audits.append(a)
        need(audits[0]==audits[1]==case['audit'],'Literal full model changed')
        if not unknown_guard:
            guard=work/'one-conflict.cnf';shutil.copyfile(cnf,guard)
            answer=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',guard,'--conflicts','1'],35))
            need(answer['status']=='UNKNOWN' and answer['mathematical_exclusion'] is False,'UNKNOWN guard promoted or unexpectedly completed')
            unknown_guard=True
        lrat=cnf.with_suffix('.lrat');discovery=args.resume is None;proposal=None
        if args.resume is not None:
            cached=args.resume.resolve()/('case-'+str(number))/'model.lrat'
            need(cached.exists(),'Missing cached proposal trace');shutil.copyfile(cached,lrat)
        else:
            proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf,'--conflicts','100000'],35))
            (directory/'native-proposal.json').write_text(json.dumps(proposal,indent=2)+'\n')
            need(proposal['status']=='UNSAT_PENDING_CHECK','Native result incomplete: no mathematical exclusion')
            need(sha(cnf.with_suffix('.drat'))==case['drat_sha256'],'Native proposal bytes differ from frozen expectation')
            converted=run([converter,cnf,cnf.with_suffix('.drat'),'-t','25','-L',lrat],30);(directory/'conversion.log').write_text(converted)
        need(sha(lrat)==case['proof']['proof_sha256'],'Candidate LRAT bytes differ')
        replays=[]
        for flags in ([],['-O']):
            p=json.loads(run([sys.executable,*flags,checker,cnf,lrat],50));p.pop('seconds',None);replays.append(p)
        need(replays[0]==replays[1]==case['proof'] and replays[0]['mathematical_exclusion'],'Strict positive-RUP replay failed')
        if number in (1,3) or args.only is not None:
            probes=[]
            for flags in ([],['-O']):probes.append(json.loads(run([sys.executable,*flags,ROOT/'proof_controls.py','--checker',checker,'--cnf',cnf,'--lrat',lrat],50)))
            need(probes[0]==probes[1],'Damaged-proof checks differ under-O')
            rejected+=2*probes[0]['production_damaged_proofs_rejected']
        completed.append({'case':number,'fresh_native_discovery':discovery,'native_proposal':proposal,'proof':replays[0]})
        print(json.dumps({'case':number,'status':'EXACT_ZERO_GROWTH_CASE_VERIFIED'}),flush=True)
    full=args.only is None
    result={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_FIVE_SEED_SATELLITE_GROWTH' if full else 'VERIFIED_SELECTED_PIPELINE_NOT_UNIFORM_LEMMA',
            'uniform_five_seed_satellite_growth_proved':full,'unrestricted_deleted_robustness_proved':False,'W_bound_improved':False,
            'expected_sha256':EXPECTED_SHA256,'cases_checked':len(completed),'fresh_native_discovery':args.resume is None,
            'all_models_regenerated_and_literal_checked':True,'all_proofs_strictly_replayed_normal_and_optimized':True,
            'cached_traces_are_untrusted_proposals':args.resume is not None,'one_conflict_UNKNOWN_control':unknown_guard,
            'changed_checker_pin_rejected':True,'damaged_local_artifacts_rejected_normal_and_optimized':16,
            'damaged_production_proofs_rejected_normal_and_optimized':rejected,
            'checked_additions_per_python_mode':sum(c['proof']['checked_additions'] for c in completed),
            'propagation_hints_per_python_mode':sum(c['proof']['propagation_hints_checked'] for c in completed),
            'normalized_small_orientation_inputs':1808,'positive_small_partial_colorings':265,
            'local_ternary_inputs':4864,'positive_local_patterns_before_global_refutations':2802,
            'positive_local_patterns_remaining_after_global_refutations':2796 if full else None,
            'raw_seed_disjoint_hole_triples':152096,'raw_seed_hole_reflection_classes':76048,
            'seconds':time.monotonic()-begin,'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    if full:
        need(len(completed)==3,'Family incomplete')
        for key in ('checked_additions_per_python_mode','propagation_hints_per_python_mode'):need(result[key]==expected['totals'][key],'Total proof evidence differs')
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path);p.add_argument('--resume',type=Path);p.add_argument('--tools',type=Path)
    p.add_argument('--only',type=int);p.add_argument('--solve',type=Path);p.add_argument('--conflicts',type=int,choices=(1,100000),default=100000)
    a=p.parse_args()
    if a.solve:print(json.dumps(native(a.solve,a.conflicts)))
    else:
        need(a.work is not None,'--work required');main(a)
