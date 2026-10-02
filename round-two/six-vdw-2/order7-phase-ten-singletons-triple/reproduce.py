"""Reconstruct all38 definitions and replay strict proofs; native statuses are proposals."""
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
GROUPS=[('fixed',10,'EXACT_H7_LENGTH6_FIXED10_DEFINITION_AUDIT'),('long',28,'EXACT_H7_RUN45_UNIQUE28_DEFINITION_AUDIT')]

def stage(work,label,argv,seconds=30):
    p=subprocess.run(list(map(str,argv)),capture_output=True,text=True,env=ENV,timeout=seconds)
    (work/(label+'.stdout')).write_text(p.stdout);(work/(label+'.stderr')).write_text(p.stderr)
    require(p.returncode==0,'bounded stage failed: '+label+' '+p.stderr[-700:])
    return p.stdout

def semantic(data):return {k:v for k,v in data.items() if k not in ('seconds','maxrss_kib')}

def reproduce(work,converter,cache=None,resume=False):
    began=time.monotonic();dependency=pins()
    require(sha(converter.parent/'drat-trim.c')==dependency['converter']['sha256'],'converter source differs')
    require(work.exists()==resume,'fresh directory or explicit --resume required')
    if not resume:work.mkdir(parents=True)
    python=Path(sys.executable).absolute()
    phase=[json.loads(stage(work,'phase-'+mode,[python,*flags,HERE/'phase_consequences.py'],20))
           for mode,flags in [('normal',[]),('optimized',['-O'])]]
    require(phase[0]==phase[1]==json.loads((HERE/'PHASE_EXPECTED.json').read_text()),'whole phase consequence record differs')
    with (HERE/'EXPECTED.csv').open(newline='') as f:expected=list(csv.DictReader(f))
    require(len(expected)==38,'incomplete canonical38 fixture')
    records=[];audits=[];guards=[]
    for group,count,status in GROUPS:
        directory=work/group
        if not resume:stage(work,group+'-generate',[python,HERE/(group+'_generate.py'),'--work',directory],55)
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            stage(work,group+'-definitions-'+mode,[python,*flags,HERE/(group+'_audit.py'),'--work',directory],55)
        definitions=[json.loads((directory/('audit-'+mode+'.json')).read_text()) for mode in ('normal','optimized')]
        require(definitions[0]['status']==status and semantic(definitions[0])==semantic(definitions[1]),'whole normal/O definitions differ')
        audits.append(semantic(definitions[0]))
        models=json.loads((directory/'models.json').read_text())
        require(models['producer_sha256']==sha(HERE/(group+'_generate.py')) and len(models['records'])==count,'wrong complete producer/models')
        records.extend(dict(r,group=group) for r in models['records'])
        if not resume:
            damage=[json.loads(stage(work,group+'-guards-'+mode,[python,*flags,HERE/(group+'_guards.py'),'--work',directory,'--output',work/(group+'-guards-'+mode)],55))
                    for mode,flags in [('normal',[]),('optimized',['-O'])]]
            require(semantic(damage[0])==semantic(damage[1]) and len(damage[0]['positive_controls'])==1,'full damage records differ')
            guards.append(semantic(damage[0]))
        print(json.dumps(dict(group=group,status='EXACT_DEFINITIONS_AND_DAMAGE_CHECKS_COMPLETE',models=count)),flush=True)
    for record,reference in zip(records,expected):
        t=6 if record['group']=='fixed' else record['long_run_length']
        parameter=record['deficient_gap'] if record['group']=='fixed' else record['next_singleton']
        require(str(t)==reference['run_length'] and str(parameter)==reference['parameter']
                and all(str(record[k])==reference[k] for k in ('group','stem','background','variables','clauses','cnf_sha256')),'canonical fixture differs')
    if resume:
        prior=json.loads((work/'result.json').read_text());require(prior['fixture_sha256']==sha(HERE/'EXPECTED.csv'),'changed resumed fixture')
        require(all(r['mathematical_exclusion'] for r in prior['cases']),'unchecked/incomplete identical native input cannot be retried')
        previous={(r['group'],r['stem']):r for r in prior['cases']};guards=prior['damage_controls']
    else:previous={}
    result=dict(agent='six-vdw-2',role='researcher',status='INCOMPLETE_SINGLETONS_TRIPLE_EXCLUSION',cases=[],fixture_sha256=sha(HERE/'EXPECTED.csv'),definition_audits=audits,damage_controls=guards,global_W_bound=False,whole_H7_exclusion=False,phase_endpoint_exclusion=False,selected_no_adjacency=False)
    def save():
        result.update(seconds=time.monotonic()-began,maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        p=work/'result.json.tmp';p.write_text(json.dumps(result,indent=2)+'\n');p.replace(work/'result.json')
    save()
    for record,reference in zip(records,expected):
        group,stem=record['group'],record['stem'];directory=work/group;cnf=directory/(stem+'.cnf');lrat=cnf.with_suffix('.lrat')
        require(sha(cnf)==record['cnf_sha256'],'audited CNF changed')
        item=dict(group=group,stem=stem,status='PENDING',mathematical_exclusion=False);result['cases'].append(item);save()
        try:
            old=previous.get((group,stem))
            if old:
                require(lrat.exists() and sha(lrat)==old['RUP']['proof_sha256'],'resumed positive certificate changed');item['proposal_source']='resumed_positive_certificate'
            elif cache is not None:
                candidate=cache/group/(stem+'.lrat')
                require(sha(cache/group/(stem+'.cnf'))==record['cnf_sha256'] and sha(candidate)==reference['lrat_sha256'],'wrong cached candidate proof')
                shutil.copyfile(candidate,lrat);item['proposal_source']='cached_candidate_proof_not_trusted'
            else:
                p=json.loads(stage(directory,stem+'-native',[python,BASE/'solve.py',cnf,'--conflicts',50000]))
                require(p['cnf_sha256']==record['cnf_sha256'],'native input binding differs');item.update(proposal=p,status=p['status']);save()
                if p['status']!='UNSAT_PENDING_CHECK':break
                require('s VERIFIED' in stage(directory,stem+'-convert',[converter,cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat]),'conversion incomplete')
                item['proposal_source']='fresh_native_and_conversion'
            checks=[json.loads(stage(directory,stem+'-RUP-'+mode,[python,*flags,BASE/'check_rup_lrat.py',cnf,lrat])) for mode,flags in [('normal',[]),('optimized',['-O'])]]
            require(checks[0]['status']=='EXACT_RUP_LRAT_VERIFIED' and semantic(checks[0])==semantic(checks[1])
                and checks[0]['cnf_sha256']==record['cnf_sha256']==sha(cnf) and checks[0]['proof_sha256']==sha(lrat),'strict exact certificate binding differs')
            item.update(status='EXACT_CASE_REFUTATION',mathematical_exclusion=True,RUP=checks[0],RUP_optimized=checks[1],byte_reproduction=sha(lrat)==reference['lrat_sha256'],expected_counts=all(str(checks[0][key])==reference[column] for key,column in [('checked_additions','additions'),('deleted_clauses','deletions'),('propagation_hints_checked','hints')]))
        except subprocess.TimeoutExpired:item['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
        save();print(json.dumps(dict(group=group,stem=stem,status=item['status'],seconds=result['seconds'])),flush=True)
        if not item['mathematical_exclusion']:break
    if len(result['cases'])==38 and all(r['mathematical_exclusion'] for r in result['cases']):
        result.update(status='EXACT_H7_PHASE10_SINGLETONS_OR_UNIQUE_TRIPLE',excluded_selected_run_lengths=[4,5,6],allowed_selected_run_lengths=[1,3],at_most_one_triple=True,triple_following_background_length=1,both_phase_values_covered=True,phase_consequences=phase[0],total_additions=sum(r['RUP']['checked_additions'] for r in result['cases']),total_deletions=sum(r['RUP']['deleted_clauses'] for r in result['cases']),total_hints=sum(r['RUP']['propagation_hints_checked'] for r in result['cases']),all_candidate_bytes_reproduced=all(r['byte_reproduction'] for r in result['cases']))
    save();print(json.dumps({k:v for k,v in result.items() if k not in ('cases','definition_audits','damage_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--converter',type=Path,required=True);p.add_argument('--certificate-cache',type=Path);p.add_argument('--resume',action='store_true');a=p.parse_args()
    reproduce(a.work.absolute(),a.converter.absolute(),a.certificate_cache.absolute() if a.certificate_cache else None,a.resume)
