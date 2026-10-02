#!/usr/bin/env python3
"""Reconstruct the full input cover and replay the eleven certified cases."""
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

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA256 = '387cd2081e6e0832024862d0be4c4d4dbc645a59e9404e3e4b896fc77e8fd91f'
ENV = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')


def need(condition,message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command,seconds):
    r = subprocess.run(list(map(str,command)),capture_output=True,text=True,env=ENV,timeout=seconds)
    need(r.returncode==0,'Child failed: '+r.stdout+r.stderr)
    return r.stdout


def pin(path,spec):
    need(sha(path)==spec['sha256'],'Byte-pinned imported source changed')


def sources(work,specs):
    work.mkdir(parents=True,exist_ok=True)
    for name,filename in (('RUP_checker','check_rup_lrat.py'),('drat_converter','drat-trim.c')):
        target=work/filename
        if not target.exists():
            with urllib.request.urlopen(specs[name]['url'],timeout=20) as response:
                target.write_bytes(response.read())
        pin(target,specs[name])
    converter=work/'drat-trim'
    if not converter.exists():
        run(['cc','-O2','-std=c99',work/'drat-trim.c','-o',converter],20)
    return work/'check_rup_lrat.py',converter


def native(cnf):
    # The pinned PySAT/CaDiCaL ASCII-trace interface was used in the author's
    # published five-seed-satellites618/reproduce.py (source13091ffd...).
    # It proposes new proof bytes for these new signed-unit models.
    import pysat
    from pysat.solvers import Solver
    need(pysat.__version__=='1.8.dev24','Use pinned python-sat1.8.dev24')
    rows=[list(map(int,line.split()[:-1])) for line in cnf.read_text().splitlines()[1:]]
    started=time.monotonic()
    with Solver(name='cadical195',bootstrap_with=rows,with_proof=True) as solver:
        solver.conf_budget(100000)
        answer=solver.solve_limited()
        stats=solver.accum_stats()
        if answer is False:
            need(ctypes.CDLL(None).fflush(None)==0,'Native ASCII trace flush failed')
            cnf.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
        if answer is True:
            cnf.with_suffix('.assignment.json').write_text(json.dumps(solver.get_model())+'\n')
    return {'status':{None:'UNKNOWN',False:'UNSAT_PENDING_CHECK',True:'SAT_PENDING_CHECK'}[answer],
            'conflict_budget':100000,'stats':stats,'seconds':time.monotonic()-started,
            'mathematical_exclusion':False}


def main(args):
    started=time.monotonic()
    need(platform.python_version()=='3.11.2','Validated runtime is Python3.11.2')
    work=args.work.resolve()
    work.mkdir(parents=True,exist_ok=True)
    manifest=ROOT/'expected.json'
    need(sha(manifest)==EXPECTED_SHA256,'Frozen expected family altered or narrowed')
    expected=json.loads(manifest.read_text())
    need(expected['proved_case_numbers']==list(range(1,12)),'Checked family changed')
    need(args.only is None or args.only in expected['proved_case_numbers'],'Select a proved case1..11')
    need(sha(ROOT/'cover.json')==expected['cover_sha256'],'Complete cover bytes changed')
    families=[]
    for suffix,flags in (('normal',[]),('optimized',['-O'])):
        directory=work/('audited-'+suffix)
        run([sys.executable,*flags,ROOT/'audit_family.py','--cover',ROOT/'cover.json','--workdir',directory],35)
        family=json.loads((directory/'family-audit.json').read_text())
        need(family['coverage']==expected['input_cover_audit'],'Actual input cover changed')
        for actual,wanted in zip(family['cases'],expected['cases']):
            need({k:v for k,v in actual.items() if k!='path'} ==
                 {k:v for k,v in wanted.items() if k not in ('proof','drat_sha256')},
                 'Frozen signed-unit model/audit changed')
        need(len(family['cases'])==15,'Full model family narrowed')
        families.append(family)
    checker,converter=sources((args.tools or work/'tools').resolve(),expected['sources'])
    altered=dict(expected['sources']['RUP_checker'],sha256='0'*64)
    try:pin(checker,altered)
    except ValueError:pass
    else:raise ValueError('Changed checker pin accepted')
    tiny=[]
    for q,wanted in zip((7,11,13),expected['controls']):
        modes=[]
        for suffix,flags in (('normal',[]),('optimized',['-O'])):
            got=json.loads(run([sys.executable,*flags,ROOT/'controls.py','--q',q,
                                '--workdir',work/('controls-'+str(q)+'-'+suffix)],35))
            need(got==wanted,'Complete small signed-word controls changed')
            modes.append(got)
        need(modes[0]==modes[1],'Small controls differ under-O')
        tiny.append(modes[0])
    profile=[]
    damaged=[]
    for flags in ([],['-O']):
        profile.append(json.loads(run([sys.executable,*flags,ROOT/'profile_check.py','--cover',ROOT/'cover.json',
                                       '--expected',manifest],10)))
        damaged.append(json.loads(run([sys.executable,*flags,ROOT/'source_controls.py','--cover',ROOT/'cover.json',
                                       '--expected',manifest],25)))
    need(profile[0]==profile[1]==expected['restricted_profile_scope'],'Restricted consequence scope changed')
    need(damaged[0]==damaged[1]=={'incomplete_input_cover_rejected':1,'profile_damages_rejected':3,'total_damages_rejected':4},
         'Coverage/consequence damage guards changed')
    completed=[]
    production_controls=[]
    for case in expected['cases']:
        number=case['number']
        if number not in expected['proved_case_numbers'] or (args.only is not None and number!=args.only):
            continue
        shape,opposite=case['case'],case['opposite']
        filename='case-'+str(shape)+'-opposite-'+str(opposite)+'.cnf'
        cnf=work/'audited-normal'/filename
        lrat=cnf.with_suffix('.lrat')
        proposal=None
        if args.resume is not None:
            candidate=args.resume.resolve()/Path(filename).with_suffix('.lrat')
            need(candidate.is_file(),'Missing untrusted cached candidate')
            shutil.copyfile(candidate,lrat)
        else:
            proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],35))
            (cnf.with_suffix('.native.json')).write_text(json.dumps(proposal,indent=2)+'\n')
            need(proposal['status']=='UNSAT_PENDING_CHECK','Incomplete proposal; stop without exclusion or retry')
            need(sha(cnf.with_suffix('.drat'))==case['drat_sha256'],'Fresh candidate DRAT bytes differ')
            output=run([converter,cnf,cnf.with_suffix('.drat'),'-t','25','-L',lrat],30)
            cnf.with_suffix('.conversion.log').write_text(output)
        need(sha(lrat)==case['proof']['proof_sha256'],'Candidate LRAT bytes differ')
        replays=[]
        for suffix,flags in (('normal',[]),('optimized',['-O'])):
            proof=json.loads(run([sys.executable,*flags,checker,cnf,lrat],50))
            cnf.with_suffix('.proof-'+suffix+'.json').write_text(json.dumps(proof,indent=2)+'\n')
            proof.pop('seconds',None)
            need(proof==case['proof'] and proof['mathematical_exclusion'],'Strict positive-RUP refutation failed')
            replays.append(proof)
        need(replays[0]==replays[1],'Strict replay differs under-O')
        if number==1 or args.only is not None:
            modes=[]
            for flags in ([],['-O']):
                got=json.loads(run([sys.executable,*flags,ROOT/'proof_controls.py','--checker',checker,
                                    '--cnf',cnf,'--lrat',lrat],50))
                need(got==expected['proof_controls'],'Strict proof damage guards changed')
                modes.append(got)
            need(modes[0]==modes[1],'Proof damage guards differ under-O')
            production_controls.append(modes[0])
        completed.append({'number':number,'case':shape,'opposite':opposite,'fresh_native_proposal':proposal,
                          'proof':replays[0]})
        print(json.dumps({'number':number,'status':'EXACT_SINGLETON_CLASS_STRICTLY_REFUTED'}),flush=True)
    full=args.only is None
    checked=[c['number'] for c in completed]
    need(checked==(expected['proved_case_numbers'] if full else [args.only]),'Certified case family incomplete')
    totals={'checked_additions_per_mode':sum(c['proof']['checked_additions'] for c in completed),
            'propagation_hints_per_mode':sum(c['proof']['propagation_hints_checked'] for c in completed)}
    if full:
        need(all(totals[k]==expected['totals'][k] for k in totals),'Complete strict proof totals changed')
    result={'agent':'six-vdw-3','role':'researcher','status':'COMPLETE_ELEVEN_CASE_RESTRICTED_DENSITY_CHECKED' if full else 'SELECTED_CASE_REPLAY_NOT_COMPLETE_DENSITY_LEMMA',
            'checked_case_numbers':checked,'complete_declared_eleven_case_negative_coverage':full,
            'four_geometry_density_two_theorem_checked_with_cited_zero_dependency':full,
            'restricted_profile_scope':profile[0] if full else None,
            'imported_zero_case_mathematical_dependency':expected['zero_case_dependency'],
            'uniform_six_geometry_at_least_two_proved':False,'unrestricted_deleted_robustness_proved':False,
            'length3704_coloring_found':False,'W_bound_improved':False,
            'expected_sha256':EXPECTED_SHA256,'full_thirty_input_cover_and_all_fifteen_models_audited':True,
            'common_actual_cyclic_base_pairs_per_mode':1143918,'fixed_word_models_compared_per_mode':15,
            'anchored_small_inputs_per_mode':sum(c['anchored_orientation_inputs'] for c in tiny),
            'positive_small_partial_words_per_mode':sum(c['positive_partial_words'] for c in tiny),
            'model_damages_rejected_per_mode':sum(c['model_damages_rejected'] for c in tiny),
            'complete_q7_pair_inputs_per_mode':tiny[0]['complete_q7_pair_inputs'],
            'q7_consistent_fixed_word_inputs_per_mode':tiny[0]['consistent_q7_fixed_word_inputs'],
            'source_controls_per_mode':damaged[0],'production_proof_controls_per_mode':production_controls,
            'changed_checker_pin_rejected':True,'cached_candidates_untrusted':args.resume is not None,
            'fresh_native_proposals_run':args.resume is None,'first_UNKNOWN_case12_not_retried':True,
            'existing_resource_caps_unchanged':True,'all_threads':1,'max_CPU_intensive_jobs':1,
            'native_external_seconds':35,'native_conflict_budget':100000,'converter_internal_seconds':25,
            'converter_external_seconds':30,'strict_replay_external_seconds':50,
            'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'pipeline_seconds':time.monotonic()-started,**totals}
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='restricted_profile_scope'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path)
    p.add_argument('--resume',type=Path)
    p.add_argument('--tools',type=Path)
    p.add_argument('--only',type=int)
    p.add_argument('--solve',type=Path)
    a=p.parse_args()
    if a.solve:
        print(json.dumps(native(a.solve)))
    else:
        need(a.work is not None,'--work required')
        main(a)
