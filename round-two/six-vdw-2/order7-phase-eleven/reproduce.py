"""Whole8 source reconstruction, damage audits and independent strict replay."""
import argparse
import csv
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time
from common import BASE,HERE,pins,require,sha

ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def semantic(data):return {k:v for k,v in data.items() if k not in ('seconds','maxrss_kib')}

def stage(work,label,argv,seconds=30):
    try:
        p=subprocess.run(list(map(str,argv)),capture_output=True,text=True,env=ENV,timeout=seconds)
    except subprocess.TimeoutExpired as exc:
        for suffix,value in (('stdout',exc.stdout),('stderr',exc.stderr)):
            (work/(label+'.'+suffix)).write_text(value.decode(errors='replace') if isinstance(value,bytes) else value or '')
        raise
    (work/(label+'.stdout')).write_text(p.stdout);(work/(label+'.stderr')).write_text(p.stderr)
    require(p.returncode==0,'bounded stage failed: '+label+' '+p.stderr[-700:])
    return p.stdout

def reproduce(work,converter,cache=None,resume=False):
    began=time.monotonic();dependency=pins()
    require(sha(converter.parent/'drat-trim.c')==dependency['converter']['sha256'],'converter source differs')
    require(work.exists()==resume,'fresh directory or explicit --resume required')
    if not resume:work.mkdir(parents=True)
    python=Path(sys.executable).absolute()
    fixture=list(csv.DictReader((HERE/'EXPECTED.csv').open(newline='')))
    require(len(fixture)==8 and [(int(r['second_singleton']),int(r['background'])) for r in fixture]
            ==[(m,b) for m in range(8,4,-1) for b in (0,1)],'incomplete canonical eight-head maximum-gap fixture')
    definitions_expected=json.loads((HERE/'VERIFICATION.json').read_text())
    models=work/'models'
    if not resume:stage(work,'generate',[python,HERE/'generate.py','--work',models],55)
    for mode,flags in (('normal',[]),('optimized',['-O'])):
        stage(work,'definitions-'+mode,[python,*flags,HERE/'audit.py','--work',models],55)
    # The full saved records contain every per-case entry; stdout is only a summary.
    audits=[json.loads((models/('audit-'+mode+'.json')).read_text()) for mode in ('normal','optimized')]
    require(audits[0]['status']=='EXACT_H7_SINGLETON8_DEFINITION_AUDIT'
            and semantic(audits[0])==semantic(audits[1])==definitions_expected['expected_complete_definition_record'],
            'whole normal/O definition records differ')
    produced=json.loads((models/'models.json').read_text())
    require(produced['producer_sha256']==sha(HERE/'generate.py') and len(produced['records'])==8,
            'complete producer/model identity changed')
    for record,expected in zip(produced['records'],fixture):
        require(str(record['next_singleton'])==expected['second_singleton'] and str(record['maximum_background_gap'])==expected['maximum_background_gap']
                and all(str(record[k])==expected[k] for k in ('stem','background','variables','clauses','cnf_sha256')),
                'whole canonical model fixture differs')
    if not resume:
        for mode,flags in (('normal',[]),('optimized',['-O'])):
            stage(work,'guards-'+mode,[python,*flags,HERE/'guards.py','--work',models,'--output',work/('guards-'+mode)],55)
        guards=[json.loads((work/('guards-'+mode)/'result.json').read_text()) for mode in ('normal','optimized')]
        require(semantic(guards[0])==semantic(guards[1])==definitions_expected['expected_complete_public_damage_record'],
                'whole normal/O damage records differ')
        damages=semantic(guards[0]);previous={}
    else:
        prior=json.loads((work/'result.json').read_text())
        require(prior['fixture_sha256']==sha(HERE/'EXPECTED.csv') and len(prior['cases'])==8
                and all(r['mathematical_exclusion'] for r in prior['cases']),
                'incomplete/failed identical native input cannot be resumed')
        previous={r['stem']:r for r in prior['cases']};damages=prior['damage_controls']
        require(damages==definitions_expected['expected_complete_public_damage_record'],'resumed damages changed')
    print(json.dumps(dict(status='ALL_EIGHT_DEFINITIONS_AND_DAMAGE_CHECKS_COMPLETE',models=8,
                          tests_per_mode=len(damages['tests']))),flush=True)
    result=dict(agent='six-vdw-2',role='researcher',status='INCOMPLETE_PHASE_ENDPOINT_PROOF',
                cases=[],fixture_sha256=sha(HERE/'EXPECTED.csv'),definition_audit=semantic(audits[0]),
                damage_controls=damages,global_W_bound=False,whole_H7_exclusion=False,
                phase_endpoint_exclusion=False)
    def save():
        result.update(seconds=time.monotonic()-began,maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        path=work/'result.json.tmp';path.write_text(json.dumps(result,indent=2)+'\n');path.replace(work/'result.json')
    save()
    for record,expected in zip(produced['records'],fixture):
        stem=record['stem'];cnf=models/(stem+'.cnf');lrat=cnf.with_suffix('.lrat')
        item=dict(stem=stem,status='PENDING',mathematical_exclusion=False);result['cases'].append(item);save()
        try:
            pins();require(sha(cnf)==record['cnf_sha256'],'audited canonical CNF changed')
            if stem in previous:
                require(lrat.exists() and sha(lrat)==previous[stem]['RUP']['proof_sha256'],'resumed positive certificate changed')
                item['proposal_source']='resumed_positive_certificate'
            elif cache is not None:
                candidate=cache/(stem+'.lrat')
                require(sha(candidate)==expected['lrat_sha256'],'changed cached candidate proof')
                shutil.copyfile(candidate,lrat);item['proposal_source']='cached_candidate_not_trusted'
            else:
                proposal=json.loads(stage(models,stem+'-native',[python,BASE/'solve.py',cnf,'--conflicts',50000]))
                require(proposal['cnf_sha256']==record['cnf_sha256'],'native input binding differs')
                item.update(proposal=proposal,status=proposal['status']);save()
                if proposal['status']!='UNSAT_PENDING_CHECK':break
                require('s VERIFIED' in stage(models,stem+'-convert',[converter,cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat]),
                        'conversion incomplete')
                item['proposal_source']='fresh_bounded_native_and_conversion'
            checks=[json.loads(stage(models,stem+'-RUP-'+mode,[python,*flags,BASE/'check_rup_lrat.py',cnf,lrat]))
                    for mode,flags in (('normal',[]),('optimized',['-O']))]
            require(checks[0]['status']=='EXACT_RUP_LRAT_VERIFIED' and semantic(checks[0])==semantic(checks[1])
                    and checks[0]['cnf_sha256']==record['cnf_sha256']==sha(cnf)
                    and checks[0]['proof_sha256']==sha(lrat),'strict whole certificate binding/replay differs')
            item.update(status='EXACT_CASE_REFUTATION',mathematical_exclusion=True,RUP=checks[0],RUP_optimized=checks[1],
                        byte_reproduction=sha(lrat)==expected['lrat_sha256'],
                        expected_counts=all(str(checks[0][k])==expected[c] for k,c in
                            (('checked_additions','additions'),('deleted_clauses','deletions'),('propagation_hints_checked','hints'))))
        except subprocess.TimeoutExpired:item['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
        save();print(json.dumps(dict(stem=stem,status=item['status'],seconds=result['seconds'])),flush=True)
        if not item['mathematical_exclusion']:break
    if len(result['cases'])==8 and all(r['mathematical_exclusion'] for r in result['cases']):
        result.update(status='EXACT_H7_PHASE10_34_EXCLUDED',phase_endpoint_exclusion=True,
                      both_phase_values_covered=True,nonconstant_phase_band=[11,33],
                      total_additions=sum(r['RUP']['checked_additions'] for r in result['cases']),
                      total_deletions=sum(r['RUP']['deleted_clauses'] for r in result['cases']),
                      total_hints=sum(r['RUP']['propagation_hints_checked'] for r in result['cases']),
                      all_candidate_bytes_reproduced=all(r['byte_reproduction'] for r in result['cases']),
                      all_expected_counts_match=all(r['expected_counts'] for r in result['cases']))
    save();print(json.dumps({k:v for k,v in result.items() if k not in ('cases','definition_audit','damage_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--converter',type=Path,required=True)
    p.add_argument('--certificate-cache',type=Path);p.add_argument('--resume',action='store_true');a=p.parse_args()
    reproduce(a.work.absolute(),a.converter.absolute(),a.certificate_cache.absolute() if a.certificate_cache else None,a.resume)
