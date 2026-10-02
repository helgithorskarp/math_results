"""Bounded serial reproduction; native statuses never replace exact proof checks."""
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

ENV = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
GROUPS = [('head',8,'EXACT_K10_PAIR_K5_FIFTH8_AUDIT')]


def stage(work,label,argv,seconds=30):
    result = subprocess.run(list(map(str,argv)),capture_output=True,text=True,
                            env=ENV,timeout=seconds)
    (work/(label+'.stdout')).write_text(result.stdout)
    (work/(label+'.stderr')).write_text(result.stderr)
    require(result.returncode==0,'stage failed: '+label+' '+result.stderr[-700:])
    return result.stdout


def semantic(data):
    return {k:v for k,v in data.items() if k not in ('seconds','maxrss_kib')}


def reproduce(work,converter,cache=None,resume=False):
    began = time.monotonic()
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name = line.split('  ')
        require(sha(HERE/name)==digest,'changed published source: '+name)
    dependency = pins()
    require(sha(converter.parent/'drat-trim.c')==dependency['converter']['sha256'],
            'converter source differs from pinned upstream source')
    require(work.exists()==resume,'use a fresh work directory or explicit --resume')
    # Preserve the venv interpreter path; resolving its symlink loses the environment.
    python = Path(sys.executable).absolute()
    if not resume:work.mkdir(parents=True)
    with (HERE/'EXPECTED.csv').open(newline='') as stream:
        expected = list(csv.DictReader(stream))
    require(len(expected)==8,'incomplete canonical fixture')
    records = []
    for group,count,status in GROUPS:
        directory = work/group
        if not resume:
            stage(work,group+'-generate',
                  [python,HERE/(group+'_generate.py'),'--work',directory],55)
        audits = [json.loads(stage(work,group+'-definitions-'+mode,
                  [python,*flags,HERE/(group+'_audit.py'),'--work',directory],55))
                  for mode,flags in [('normal',[]),('optimized',['-O'])]]
        require(audits[0]['status']==status and semantic(audits[0])==semantic(audits[1]),
                'definition audits disagree: '+group)
        models = json.loads((directory/'models.json').read_text())
        require(models['producer_sha256']==sha(HERE/(group+'_generate.py')),
                'producer changed after generation')
        require(len(models['records'])==count,'missing or extra canonical models')
        for record in models['records']:
            records.append(dict(record,group=group))
        print(json.dumps(dict(group=group,status='EXACT_DEFINITIONS_CHECKED',
                              models=count)),flush=True)
    for record,reference in zip(records,expected):
        require(all(str(record[k])==reference[k] for k in
                    ('group','stem','fifth_selected_index','background','variables','clauses','cnf_sha256')),
                'canonical CNF fixture differs')
    if resume:
        result = json.loads((work/'result.json').read_text())
        require(result['fixture_sha256']==sha(HERE/'EXPECTED.csv'),
                'changed resumed fixture')
        for item in result['cases']:
            require(item['status'] not in ('UNKNOWN','BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'),
                    'this identical bounded failure cannot be retried')
        previous = {(r['group'],r['stem']):r for r in result['cases']}
    else:
        previous = {}
    result = dict(agent='six-vdw-2',role='researcher',
                  status='INCOMPLETE_THIRD_INDEX_FIVE_EXCLUSION',cases=[],
                  fixture_sha256=sha(HERE/'EXPECTED.csv'),
                  global_W_bound=False,whole_H7_exclusion=False,
                  endpoint_weights_excluded=False,phase_band_strengthened=False)

    def save():
        result.update(seconds=time.monotonic()-began,
            maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        (work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    save()
    for record,reference in zip(records,expected):
        group,stem = record['group'],record['stem']
        directory = work/group
        cnf,lrat = directory/(stem+'.cnf'),directory/(stem+'.lrat')
        require(sha(cnf)==record['cnf_sha256'],'changed audited CNF')
        item = dict(group=group,stem=stem,status='PENDING',mathematical_exclusion=False)
        result['cases'].append(item);save()
        try:
            old = previous.get((group,stem))
            if old:
                # Resume checked positives by exact replay; never repeat a native failure.
                require(old['mathematical_exclusion'] and lrat.exists(),
                        'interrupted unchecked native stage needs explicit diagnosis')
                require(sha(lrat)==old['RUP']['proof_sha256'],
                        'changed resumed positive certificate')
                item['proposal_source']='resumed_positive_certificate'
            elif cache is not None:
                candidate = cache/group/(stem+'.lrat')
                candidate_cnf = cache/group/(stem+'.cnf')
                require(sha(candidate_cnf)==record['cnf_sha256'] and
                        sha(candidate)==reference['lrat_sha256'],'wrong cached candidate input')
                shutil.copyfile(candidate,lrat)
                item['proposal_source']='cached_candidate_proof_not_trusted'
            else:
                proposal = json.loads(stage(directory,stem+'-native',
                    [python,BASE/'solve.py',cnf,'--conflicts',50000]))
                item.update(proposal=proposal,status=proposal['status']);save()
                if proposal['status']!='UNSAT_PENDING_CHECK':break
                converted = stage(directory,stem+'-convert',
                    [converter,cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat])
                require('s VERIFIED' in converted,'conversion incomplete')
                item['proposal_source']='fresh_native_and_conversion'
            checks = [json.loads(stage(directory,stem+'-RUP-'+mode,
                      [python,*flags,BASE/'check_rup_lrat.py',cnf,lrat]))
                      for mode,flags in [('normal',[]),('optimized',['-O'])]]
            require(checks[0]['status']=='EXACT_RUP_LRAT_VERIFIED' and
                    semantic(checks[0])==semantic(checks[1]),'strict RUP checks disagree')
            require(checks[0]['cnf_sha256']==record['cnf_sha256']==sha(cnf) and
                    checks[0]['proof_sha256']==sha(lrat),'changed checked certificate input')
            item.update(status='EXACT_CASE_REFUTATION',mathematical_exclusion=True,
                RUP=checks[0],RUP_optimized=checks[1],
                byte_reproduction=(sha(lrat)==reference['lrat_sha256']),
                expected_count_reproduction=(str(checks[0]['checked_additions'])==reference['additions']
                    and str(checks[0]['deleted_clauses'])==reference['deletions']
                    and str(checks[0]['propagation_hints_checked'])==reference['hints']))
        except subprocess.TimeoutExpired:
            item['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
        save()
        print(json.dumps(dict(group=group,stem=stem,status=item['status'],
                              seconds=result['seconds'])),flush=True)
        if not item['mathematical_exclusion']:break
    if len(result['cases'])==8 and all(r['mathematical_exclusion'] for r in result['cases']):
        result.update(status='EXACT_H7_PHASE10_ADJACENT_THIRD_INDEX_AT_MOST4',
            selected_phase_count=10, adjacent_run_third_selected_index_upper_bound=4,
            normalized_third_index5_fifth_heads_excluded=8,
            third_index5_class_excluded=True, pair_following_cut=True, adjacent_density_cut=True, both_phase_values_covered=True,
            no_adjacency_cut=False, conditional_successor_cut=False,
            definition_audit=audits[0],
            total_checked_additions=sum(r['RUP']['checked_additions'] for r in result['cases']),
            total_checked_deletions=sum(r['RUP']['deleted_clauses'] for r in result['cases']),
            total_hints=sum(r['RUP']['propagation_hints_checked'] for r in result['cases']),
            all_proof_bytes_reproduced=all(r['byte_reproduction'] for r in result['cases']))
    save()
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}),flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--converter',type=Path,required=True)
    parser.add_argument('--certificate-cache',type=Path)
    parser.add_argument('--resume',action='store_true')
    args = parser.parse_args()
    reproduce(args.work.absolute(),args.converter.absolute(),
              args.certificate_cache.absolute() if args.certificate_cache else None,args.resume)
