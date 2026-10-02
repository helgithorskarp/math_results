#!/usr/bin/env python3
"""Reconstruct coverage/models, propose one fresh trace, and strictly replay it."""
import argparse
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
EXPECTED_SHA256='0b383fa618819184ed9e6cf75d8f4d91afb6b6341d7608a6c83615c2726094fc'
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
         BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')


def need(condition,message):
    if not condition:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command,seconds):
    r=subprocess.run(list(map(str,command)),capture_output=True,text=True,env=ENV,timeout=seconds)
    need(r.returncode==0,'Child failed: '+r.stdout+r.stderr)
    return r.stdout


def pin(path,spec):
    need(sha(path)==spec['sha256'],'Byte-pinned imported source changed')


def sources(work,specs):
    work.mkdir(parents=True,exist_ok=True)
    paths={}
    for name,spec in specs.items():
        path=work/spec['filename']
        if not path.exists():
            with urllib.request.urlopen(spec['url'],timeout=20) as response:
                path.write_bytes(response.read())
        pin(path,spec)
        paths[name]=path
    converter=work/'drat-trim'
    if not converter.exists():
        run(['cc','-O2','-std=c99',paths['drat_converter'],'-o',converter],20)
    paths['converter_executable']=converter
    return paths


def main(args):
    started=time.monotonic()
    need(platform.python_version()=='3.11.2','Validated runtime is Python3.11.2')
    manifest=ROOT/'expected.json'
    need(sha(manifest)==EXPECTED_SHA256,'Frozen model/coverage/proof expectations changed')
    expected=json.loads(manifest.read_text())
    work=args.work.resolve()
    work.mkdir(parents=True,exist_ok=True)
    paths=sources((args.tools or work/'tools').resolve(),expected['sources'])
    common=paths['common_checker']
    checker=paths['RUP_checker']
    changed=dict(expected['sources']['RUP_checker'],sha256='0'*64)
    try:pin(checker,changed)
    except ValueError:pass
    else:raise ValueError('Changed RUP checker pin accepted')
    models=[]
    audits=[]
    controls=[]
    covers=[]
    source_guards=[]
    for name,flags in (('normal',[]),('optimized',['-O'])):
        cnf=work/('sparse-'+name+'.cnf')
        model=json.loads(run([sys.executable,*flags,ROOT/'generate.py','--output',cnf],35))
        need(model==expected['model'],'Frozen field/signed-word model changed')
        audit=json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--helper',common],35))
        audit.pop('seconds',None)
        need(audit==expected['actual_cyclic_audit'],'Actual-cyclic domain or fixed word changed')
        tiny=json.loads(run([sys.executable,*flags,ROOT/'controls.py','--helper',common,
                             '--work',work/('controls-'+name)],35))
        need(tiny==expected['controls'],'Complete multi-positive small controls changed')
        cover=json.loads(run([sys.executable,*flags,ROOT/'cover_check.py','--expected',manifest],15))
        need(cover==expected['cover'],'Complete sparse counterexample coverage changed')
        guards=json.loads(run([sys.executable,*flags,ROOT/'source_controls.py','--expected',manifest],25))
        need(guards==expected['source_controls'],'Coverage/scope damage guards changed')
        for kind,record in (('model',model),('audit',audit),('controls',tiny),('cover',cover),('source-controls',guards)):
            (work/(kind+'-'+name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        models.append(model);audits.append(audit);controls.append(tiny);covers.append(cover);source_guards.append(guards)
        print(json.dumps({'stage':name+'_source_models_cover_and_controls_checked'}),flush=True)
    need(models[0]==models[1] and audits[0]==audits[1] and controls[0]==controls[1] and
         covers[0]==covers[1] and source_guards[0]==source_guards[1],'Source differs under -O')
    need((work/'sparse-normal.cnf').read_bytes()==(work/'sparse-optimized.cnf').read_bytes(),
         'CNF bytes differ under -O')
    cnf=work/'sparse-normal.cnf'
    lrat=cnf.with_suffix('.lrat')
    native=None
    if args.resume:
        need(args.resume.is_file(),'Missing untrusted cached LRAT candidate')
        shutil.copyfile(args.resume,lrat)
    else:
        native=json.loads(run([sys.executable,paths['native_driver'],'--solve',cnf],35))
        (work/'native.json').write_text(json.dumps(native,indent=2)+'\n')
        need(native['status']=='UNSAT_PENDING_CHECK','Incomplete native proposal: stop, no exclusion or retry')
        need(sha(cnf.with_suffix('.drat'))==expected['drat_sha256'],'Fresh proposed DRAT bytes differ')
        output=run([paths['converter_executable'],cnf,cnf.with_suffix('.drat'),'-t','25','-L',lrat],30)
        (work/'conversion.log').write_text(output)
    need(sha(lrat)==expected['proof']['proof_sha256'],'Candidate LRAT bytes differ')
    proofs=[]
    damages=[]
    for name,flags in (('normal',[]),('optimized',['-O'])):
        proof=json.loads(run([sys.executable,*flags,checker,cnf,lrat],50))
        (work/('proof-'+name+'.json')).write_text(json.dumps(proof,indent=2)+'\n')
        proof.pop('seconds',None)
        need(proof==expected['proof'] and proof['mathematical_exclusion'],'No strict checked refutation')
        guards=json.loads(run([sys.executable,*flags,paths['proof_controls'],'--checker',checker,
                               '--cnf',cnf,'--lrat',lrat],50))
        need(guards==expected['proof_controls'],'Strict proof damage guards changed')
        proofs.append(proof);damages.append(guards)
    need(proofs[0]==proofs[1] and damages[0]==damages[1],'Strict replay differs under -O')
    result={'agent':'six-vdw-3','role':'researcher','status':'CONDITIONAL_THIRD_SATELLITE_LEMMA_AUTHOR_CHECKED',
            'complete_sparse_negative_coverage':True,'sparse_negative_inputs_checked':1,
            'mathematical_dependency':expected['cover']['dependency'],
            'at_least_three_satellites_with_cited_premise_and_written_bridge':True,
            'necessary_six_satellite_inputs':34,'necessary_input_reflection_classes':19,
            'global_colorings_counted':False,'full_deleted_robustness_proved':False,
            'length3704_coloring_found':False,'W_bound_improved':False,
            'expected_sha256':EXPECTED_SHA256,'cnf_sha256':models[0]['cnf_sha256'],
            'strict_proof_per_mode':proofs[0],'proof_controls_per_mode':damages[0],
            'source_controls_per_mode':source_guards[0],
            'actual_cyclic_pairs_audited_per_mode':audits[0]['all_actual_cyclic_pairs_checked'],
            'small_anchored_inputs_per_mode':controls[0]['anchored_orientation_inputs'],
            'small_positive_words_per_mode':controls[0]['positive_partial_words'],
            'model_damages_rejected_per_mode':controls[0]['model_damages_rejected'],
            'complete_q7_pair_inputs_per_mode':controls[0]['complete_q7_pair_inputs'],
            'q7_consistent_fixed_inputs_per_mode':controls[0]['q7_consistent_fixed_word_inputs'],
            'changed_checker_pin_rejected':True,'cached_candidate_untrusted':args.resume is not None,
            'fresh_native_proposal_run':args.resume is None,'native_proposal':native,
            'earlier_UNKNOWN_instances_not_retried':True,'existing_resource_caps_unchanged':True,
            'all_threads':1,'max_CPU_intensive_jobs':1,'native_external_seconds':35,
            'native_conflict_budget':100000,'converter_internal_seconds':25,'converter_external_seconds':30,
            'strict_replay_external_seconds':50,
            'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'pipeline_seconds':time.monotonic()-started}
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--tools',type=Path)
    parser.add_argument('--resume',type=Path)
    main(parser.parse_args())
