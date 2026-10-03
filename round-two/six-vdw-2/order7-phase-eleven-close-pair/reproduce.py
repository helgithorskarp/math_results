"""Regenerate all four models; audit full definitions/damages; strictly check every certificate."""
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
    try:p=subprocess.run(list(map(str,argv)),capture_output=True,text=True,env=ENV,timeout=seconds)
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
    require(work.exists()==resume,'fresh directory or explicit successful --resume required')
    if not resume:work.mkdir(parents=True)
    python=Path(sys.executable).absolute()
    fixture=list(csv.DictReader((HERE/'EXPECTED.csv').open(newline='')))
    require(len(fixture)==4 and [(r['branch'],int(r['background'])) for r in fixture]
            ==[('4',0),('4',1),('3',0),('3',1)],'incomplete four-case minimum-distance cover')
    expected=json.loads((HERE/'VERIFICATION.json').read_text())
    previous={};prior=None
    if resume:
        prior=json.loads((work/'result.json').read_text())
        require(prior['fixture_sha256']==sha(HERE/'EXPECTED.csv') and len(prior['cases'])==4
                and all(r['mathematical_exclusion'] for r in prior['cases']),
                'incomplete or failed identical native model cannot be resumed')
        previous={r['stem']:r for r in prior['cases']}
    produced={};definitions={};damages={}
    for branch in ('4','3'):
        models=work/('models-'+branch)
        if not resume:stage(work,'generate-'+branch,[python,HERE/f'generate{branch}.py','--work',models],55)
        for mode,flags in (('normal',[]),('optimized',['-O'])):
            stage(work,f'definitions-{branch}-{mode}',[python,*flags,HERE/f'audit{branch}.py','--work',models],55)
        audits=[json.loads((models/f'audit-{mode}.json').read_text()) for mode in ('normal','optimized')]
        require(semantic(audits[0])==semantic(audits[1])==expected['expected_complete_definition_records'][branch],
                'whole normal/O definition records differ: '+branch)
        definitions[branch]=semantic(audits[0]);produced[branch]=json.loads((models/'models.json').read_text())
        require(produced[branch]['producer_sha256']==sha(HERE/f'generate{branch}.py')
                and len(produced[branch]['records'])==2,'complete producer/model identity differs')
        if not resume:
            for mode,flags in (('normal',[]),('optimized',['-O'])):
                stage(work,f'guards-{branch}-{mode}',[python,*flags,HERE/f'guards{branch}.py','--work',models,
                    '--output',work/f'guards-{branch}-{mode}'],55)
            checks=[json.loads((work/f'guards-{branch}-{mode}'/'result.json').read_text()) for mode in ('normal','optimized')]
            require(semantic(checks[0])==semantic(checks[1])==expected['expected_complete_public_damage_records'][branch],
                    'whole normal/O source/semantic/kernel damages differ: '+branch)
            damages[branch]=semantic(checks[0])
        else:
            damages[branch]=prior['damage_controls'][branch]
            require(damages[branch]==expected['expected_complete_public_damage_records'][branch],'resumed damages changed')
        print(json.dumps(dict(status='COMPLETE_BRANCH_DEFINITIONS_AND_DAMAGES',minimum_selected_distance=int(branch),
            cases=2,damages_per_mode=len(damages[branch]['tests']))),flush=True)
    all_records=produced['4']['records']+produced['3']['records']
    for record,item in zip(all_records,fixture):
        require(all(str(record[k])==item[k] for k in ('stem','minimum_selected_distance','background','phase_K',
                    'variables','clauses','cnf_sha256')),'entire canonical model fixture differs')
    result=dict(agent='six-vdw-2',role='researcher',status='INCOMPLETE_CLOSE_PAIR_PROOF',
        cases=[],fixture_sha256=sha(HERE/'EXPECTED.csv'),definition_audits=definitions,damage_controls=damages,
        close_pair_lemma=False,phase_endpoint_exclusion=False,global_W_bound=False,whole_H7_exclusion=False)
    def save():
        result.update(seconds=time.monotonic()-began,maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        path=work/'result.json.tmp';path.write_text(json.dumps(result,indent=2)+'\n');path.replace(work/'result.json')
    save()
    for record,item in zip(all_records,fixture):
        stem=record['stem'];models=work/('models-'+item['branch']);cnf=models/(stem+'.cnf');lrat=cnf.with_suffix('.lrat')
        case=dict(stem=stem,minimum_selected_distance=int(item['branch']),background=record['background'],
                  status='PENDING',mathematical_exclusion=False);result['cases'].append(case);save()
        try:
            pins();require(sha(cnf)==record['cnf_sha256'],'audited canonical model changed')
            if stem in previous:
                require(lrat.exists() and sha(lrat)==previous[stem]['RUP']['proof_sha256'],'resumed positive certificate changed')
                case['proposal_source']='resumed_positive_certificate'
            elif cache is not None:
                candidate=cache/(stem+'.lrat')
                require(sha(candidate)==item['lrat_sha256'],'changed untrusted cached candidate')
                shutil.copyfile(candidate,lrat);case['proposal_source']='cached_candidate_not_trusted'
            else:
                proposal=json.loads(stage(models,stem+'-native',[python,BASE/'solve.py',cnf,'--conflicts',50000]))
                require(proposal['cnf_sha256']==record['cnf_sha256'],'bounded native input differs')
                case.update(proposal=proposal,status=proposal['status']);save()
                if proposal['status']!='UNSAT_PENDING_CHECK':break
                require('s VERIFIED' in stage(models,stem+'-convert',[converter,cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat]),
                        'bounded conversion incomplete')
                case['proposal_source']='fresh_bounded_native_and_conversion'
            checks=[json.loads(stage(models,stem+'-RUP-'+mode,[python,*flags,BASE/'check_rup_lrat.py',cnf,lrat]))
                    for mode,flags in (('normal',[]),('optimized',['-O']))]
            require(checks[0]['status']=='EXACT_RUP_LRAT_VERIFIED' and semantic(checks[0])==semantic(checks[1])
                    and checks[0]['cnf_sha256']==record['cnf_sha256']==sha(cnf)
                    and checks[0]['proof_sha256']==sha(lrat),'strict whole certificate binding/check differs')
            case.update(status='EXACT_CASE_REFUTATION',mathematical_exclusion=True,RUP=checks[0],RUP_optimized=checks[1],
                byte_reproduction=sha(lrat)==item['lrat_sha256'],
                expected_counts=all(str(checks[0][k])==item[c] for k,c in
                    (('checked_additions','additions'),('deleted_clauses','deletions'),('propagation_hints_checked','hints'))))
        except subprocess.TimeoutExpired:case['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
        save();print(json.dumps(dict(stem=stem,status=case['status'],seconds=result['seconds'])),flush=True)
        if not case['mathematical_exclusion']:break
    if len(result['cases'])==4 and all(c['mathematical_exclusion'] for c in result['cases']):
        result.update(status='EXACT_H7_ELEVEN_CLOSE_PAIR_LEMMA',close_pair_lemma=True,
            phase_weights=[11,33],selected_pair_cyclic_distance_at_most=2,both_backgrounds_explicit=True,
            total_additions=sum(c['RUP']['checked_additions'] for c in result['cases']),
            total_deletions=sum(c['RUP']['deleted_clauses'] for c in result['cases']),
            total_hints=sum(c['RUP']['propagation_hints_checked'] for c in result['cases']),
            all_candidate_bytes_reproduced=all(c['byte_reproduction'] for c in result['cases']),
            all_expected_counts_match=all(c['expected_counts'] for c in result['cases']))
    else:
        hashes=[r['cnf_sha256'] for r,c in zip(all_records,result['cases']) if not c['mathematical_exclusion']]
        (work/'frozen-UNKNOWN-hashes.json').write_text(json.dumps(dict(status='INCOMPLETE_HASHES_FROZEN_NO_IDENTICAL_RETRY',
            hashes=hashes,mathematical_exclusions=False),indent=2)+'\n')
    save();print(json.dumps({k:v for k,v in result.items() if k not in ('cases','definition_audits','damage_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--converter',type=Path,required=True)
    p.add_argument('--certificate-cache',type=Path);p.add_argument('--resume',action='store_true');args=p.parse_args()
    reproduce(args.work.absolute(),args.converter.absolute(),args.certificate_cache.absolute() if args.certificate_cache else None,args.resume)
