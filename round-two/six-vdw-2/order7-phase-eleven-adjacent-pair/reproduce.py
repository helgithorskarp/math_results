"""Reconstruct all 72 physical models and check every positive RUP certificate."""
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
from common import BASE, HERE, pins, require, sha

ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
JOURNAL = None

def journal_save():
    path=JOURNAL['path']; data={k:v for k,v in JOURNAL.items() if k!='path'}
    temporary=path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data,indent=2)+'\n'); temporary.replace(path)

def semantic(data):
    return {k:v for k,v in data.items() if k not in ('seconds','maxrss_kib')}

def stage(work,label,args,seconds=30):
    entry=dict(label=label,status='RUNNING_INCOMPLETE',wall_limit_seconds=seconds,
               started=time.time())
    JOURNAL['stages'].append(entry); journal_save()
    print(json.dumps(dict(stage=label,status=entry['status'])),flush=True)
    try:
        p=subprocess.run(list(map(str,args)),capture_output=True,text=True,env=ENV,timeout=seconds)
    except subprocess.TimeoutExpired as exc:
        for suffix,data in [('stdout',exc.stdout),('stderr',exc.stderr)]:
            (work/(label+'.'+suffix)).write_text(data.decode(errors='replace') if isinstance(data,bytes) else data or '')
        entry.update(status='TIMEOUT_INCOMPLETE',finished=time.time()); journal_save()
        raise
    (work/(label+'.stdout')).write_text(p.stdout)
    (work/(label+'.stderr')).write_text(p.stderr)
    entry.update(status='COMPLETE' if p.returncode==0 else 'FAILED_INCOMPLETE',
                 returncode=p.returncode,finished=time.time())
    journal_save()
    require(p.returncode==0,'bounded stage failed: '+label+' '+p.stderr[-700:])
    return p.stdout

def reproduce(work,converter,cache=None):
    global JOURNAL
    began=time.monotonic(); dependency=pins()
    require(not work.exists(),'fresh proof workspace required; no identical failed native retry')
    require(sha(converter.parent/'drat-trim.c')==dependency['converter']['sha256'],'converter source differs')
    work.mkdir(parents=True); python=Path(sys.executable).absolute(); models=work/'models'
    JOURNAL=dict(path=work/'stage-ledger.json',status='INCOMPLETE',
                 reproduction_source_sha256=sha(HERE/'reproduce.py'),stages=[])
    journal_save()
    fixture=list(csv.DictReader((HERE/'EXPECTED.csv').open(newline='')))
    expected=json.loads((HERE/'VERIFICATION.json').read_text())
    order=sorted(range(8,40),key=lambda j:(abs(j-22),j))+[7,40,5,42]
    require(len(fixture)==72 and [(int(r['minimum_pair_start']),int(r['background'])) for r in fixture]
            ==[(j,b) for j in order for b in (0,1)],'incomplete whole72-case proof fixture')
    stage(work,'generate',[python,HERE/'generate.py','--work',models],55)
    audits=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        batches=[]
        for batch in range(9):
            stage(work,'definitions-'+mode+'-'+str(batch),
                  [python,*flags,HERE/'audit.py','--work',models,'--batch',batch],55)
            batches.append(json.loads((models/('audit-'+mode+'-batch-'+str(batch)+'.json')).read_text()))
        stage(work,'controls-'+mode,[python,*flags,HERE/'audit.py','--work',models,'--controls'],55)
        controls=json.loads((models/('audit-'+mode+'-controls.json')).read_text())
        common=lambda d:{k:v for k,v in d.items() if k not in
            ('records','tiny_controls','ordinary_pair_cover_controls','actual_scalar_controls',
             'literal_field_reconstructed','bounded_batch','seconds','maxrss_kib')}
        require(all(common(b)==common(controls) and b['literal_field_reconstructed'] is True for b in batches),
                'bounded literal definitions/census differ')
        records=[r for batch in batches for r in batch['records']]
        require([r['stem'] for r in records]==[r['stem'] for r in fixture],'incomplete nine-batch physical audit')
        merged=dict(controls,records=records,literal_field_reconstructed=True,bounded_batch=None,
                    bounded_batches=9,seconds=sum(b['seconds'] for b in batches)+controls['seconds'],
                    maxrss_kib=max(b['maxrss_kib'] for b in [*batches,controls]))
        (models/('audit-'+mode+'.json')).write_text(json.dumps(merged,indent=2)+'\n'); audits.append(merged)
    require(semantic(audits[0])==semantic(audits[1])==expected['expected_complete_definition_record'],
            'ENTIRE normal/O definition, threshold, rule, coverage and gauge records differ')
    produced=json.loads((models/'models.json').read_text())
    require(produced['producer_sha256']==sha(HERE/'generate.py') and len(produced['records'])==72,
            'complete producer/source identity changed')
    require(len({r['cnf_sha256'] for r in produced['records']})==72
            and not(set(dependency['frozen_prior_cnfs']) & {r['cnf_sha256'] for r in produced['records']}),
            'duplicate or frozen failed native input')
    for record,row in zip(produced['records'],fixture):
        require(all(str(record[k])==row[k] for k in
                    ('stem','minimum_pair_start','background','phase_K','variables','clauses','cnf_sha256')),
                'whole72 canonical model fixture differs')
    guards=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        stage(work,'guards-'+mode,[python,*flags,HERE/'guards.py','--work',models,
                                  '--output',work/('guards-'+mode)],55)
        guards.append(json.loads((work/('guards-'+mode)/'result.json').read_text()))
    require(semantic(guards[0])==semantic(guards[1])==expected['expected_complete_public_damage_record'],
            'ENTIRE source/physical/count/cover/RUP damage records differ')
    print(json.dumps(dict(status='ALL72_DEFINITIONS_AND_DAMAGE_CHECKS_COMPLETE',
                          tests_per_mode=len(guards[0]['tests']))),flush=True)
    result=dict(agent='six-vdw-2',role='researcher',status='INCOMPLETE_PAIR_CASE_REPLAY',cases=[],
                fixture_sha256=sha(HERE/'EXPECTED.csv'),definition_audit=semantic(audits[0]),
                damage_controls=semantic(guards[0]),global_W_bound=False,whole_H7_exclusion=False,
                phase_endpoint_exclusion=False,all_isolated_eleven_branch_exclusion=False)
    def save():
        result.update(seconds=time.monotonic()-began,
                      maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        path=work/'result.json.tmp';path.write_text(json.dumps(result,indent=2)+'\n');path.replace(work/'result.json')
    save()
    for record,row in zip(produced['records'],fixture):
        stem=record['stem'];cnf=models/(stem+'.cnf');lrat=cnf.with_suffix('.lrat')
        item=dict(stem=stem,status='PENDING',mathematical_exclusion=False);result['cases'].append(item);save()
        try:
            pins();require(sha(cnf)==record['cnf_sha256'],'independently audited canonical CNF changed')
            if cache is not None:
                candidate=cache/(stem+'.lrat')
                require(sha(candidate)==row['lrat_sha256'],'changed untrusted cached candidate')
                shutil.copyfile(candidate,lrat);item['proposal_source']='cached_candidate_not_trusted'
            else:
                proposal=json.loads(stage(models,stem+'-native',[python,BASE/'solve.py',cnf,'--conflicts',50000]))
                require(proposal['cnf_sha256']==record['cnf_sha256'],'native input binding differs')
                item.update(proposal=proposal,status=proposal['status']);save()
                if proposal['status']!='UNSAT_PENDING_CHECK':break
                require('s VERIFIED' in stage(models,stem+'-convert',
                    [converter,cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat]),'conversion incomplete')
                item['proposal_source']='fresh_bounded_native_and_conversion'
            checks=[json.loads(stage(models,stem+'-RUP-'+mode,
                     [python,*flags,BASE/'check_rup_lrat.py',cnf,lrat]))
                    for mode,flags in [('normal',[]),('optimized',['-O'])]]
            require(checks[0]['status']=='EXACT_RUP_LRAT_VERIFIED' and semantic(checks[0])==semantic(checks[1])
                    and checks[0]['cnf_sha256']==record['cnf_sha256']==sha(cnf)
                    and checks[0]['proof_sha256']==sha(lrat),'strict positive-only RUP binding/replay differs')
            item.update(status='EXACT_CASE_REFUTATION',mathematical_exclusion=True,
                        RUP=checks[0],RUP_optimized=checks[1],byte_reproduction=sha(lrat)==row['lrat_sha256'],
                        expected_counts=all(str(checks[0][k])==row[c] for k,c in
                        [('checked_additions','additions'),('deleted_clauses','deletions'),('propagation_hints_checked','hints')]))
        except subprocess.TimeoutExpired:
            item['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
        save();print(json.dumps(dict(stem=stem,status=item['status'],seconds=result['seconds'])),flush=True)
        if not item['mathematical_exclusion']:break
    if len(result['cases'])==72 and all(r['mathematical_exclusion'] for r in result['cases']):
        result.update(status='EXACT_H7_ELEVEN_ADJACENT_MINORITY_PAIR',phase_weights=[11,33],
                      all_isolated_eleven_branch_exclusion=True,
                      total_additions=sum(r['RUP']['checked_additions'] for r in result['cases']),
                      total_deletions=sum(r['RUP']['deleted_clauses'] for r in result['cases']),
                      total_hints=sum(r['RUP']['propagation_hints_checked'] for r in result['cases']),
                      all_candidate_bytes_reproduced=all(r['byte_reproduction'] for r in result['cases']),
                      all_expected_counts_match=all(r['expected_counts'] for r in result['cases']))
    if result['status']=='EXACT_H7_ELEVEN_ADJACENT_MINORITY_PAIR':
        require(all(s['status']=='COMPLETE' for s in JOURNAL['stages']),
                'incomplete source replay stage')
        JOURNAL['status']='ALL_SOURCE_STAGES_COMPLETED'; journal_save()
    save();print(json.dumps({k:v for k,v in result.items() if k not in
                ('cases','definition_audit','damage_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--converter',type=Path,required=True);p.add_argument('--certificate-cache',type=Path)
    args=p.parse_args();reproduce(args.work.absolute(),args.converter.absolute(),
                                 args.certificate_cache.absolute() if args.certificate_cache else None)
