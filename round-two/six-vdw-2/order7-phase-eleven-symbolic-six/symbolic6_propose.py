"""One native pilot only after whole paired source/physical/control gates."""
import json
from pathlib import Path
import sys
import time
from symbolic6_common import BASE, ROOT, pins, require, sha, write
from symbolic6_stage import stage

PYTHON=ROOT/'solver-env/bin/python'
WORK=ROOT/'symbolic6-models'
ATTEMPTS=ROOT/'symbolic6-native-attempts.json'
RESULT=ROOT/'symbolic6-result.json'


def semantic(d):
    return {k:v for k,v in d.items() if k not in ('seconds','maxrss_kib')}


def main():
    old,new=pins();produced=json.loads((WORK/'models.json').read_text())
    audits=[json.loads((WORK/('audit-'+mode+'.json')).read_text()) for mode in ('normal','optimized')]
    guards=[json.loads((ROOT/('symbolic6-guards-'+mode)/'result.json').read_text()) for mode in ('normal','optimized')]
    require(audits[0]==audits[1] and audits[0]['status']=='INDEPENDENT_ENTIRE_SYMBOLIC_TWO_MODELS_CHECKED'
            and guards[0]==guards[1] and guards[0]['status']=='ALL_SYMBOLIC_PHYSICAL_GATE_SOURCE_RUP_DAMAGES_REJECTED'
            and audits[0]['records']==produced['records'],'whole normal/O pre-native gate differs')
    require(not ATTEMPTS.exists() and not RESULT.exists() and not (ROOT/'symbolic6-frozen-INCOMPLETE.json').exists(),
            'prior symbolic native request/incomplete is frozen; no retry')
    require(sha(ROOT/'drat-trim.c')==new['converter_source_sha256'],'converter source changed')
    attempts=dict(agent='six-vdw-2',role='researcher',attempts=[])
    result=dict(agent='six-vdw-2',role='researcher',status='INCOMPLETE_NO_FULL_BRANCH_EXCLUSION',cases=[],
                longest_minority_run6_exclusion=False,phase_endpoint_exclusion=False,whole_H7_exclusion=False,
                interval3704_witness=False,global_W_bound=False,exact_negative_models=0)
    write(RESULT,result)
    for record in produced['records']:
        pins();background=record['background'];stem=record['stem'];cnf=WORK/(stem+'.cnf');lrat=cnf.with_suffix('.lrat')
        require(record['cnf_sha256']==sha(cnf) and record['cnf_sha256'] not in old['frozen_prior_cnfs'], 'changed/frozen original input')
        require(not any(a['cnf_sha256']==record['cnf_sha256'] for a in attempts['attempts']), 'identical native proposal')
        entry=dict(background=background,stem=stem,cnf_sha256=sha(cnf),status='REGISTERED_BEFORE_NATIVE',started=time.time())
        attempts['attempts'].append(entry);write(ATTEMPTS,attempts)
        item=dict(background=background,stem=stem,cnf_sha256=sha(cnf),status='INCOMPLETE',mathematical_exclusion=False)
        result['cases'].append(item);write(RESULT,result)
        try:
            proposal=json.loads(stage(stem+'-native',[PYTHON,BASE/'solve.py',cnf,'--conflicts',50000],30))
            require(proposal['cnf_sha256']==record['cnf_sha256'],'native original-CNF binding differs')
            item.update(status=proposal['status'],proposal=proposal);write(RESULT,result)
            require(type(proposal['stats']['conflicts']) is int and proposal['stats']['conflicts']<=50000,
                    'reported native conflicts exceed unchanged cap')
            if proposal['status']=='UNSAT_PENDING_CHECK':
                output=stage(stem+'-convert',[ROOT/'drat-trim',cnf,cnf.with_suffix('.drat'),'-t',25,'-L',lrat],30)
                require('s VERIFIED' in output,'converter incomplete')
                checked=[json.loads(stage(stem+'-RUP-'+mode,[PYTHON,*flags,BASE/'check_rup_lrat.py',cnf,lrat],30))
                         for mode,flags in [('normal',[]),('optimized',['-O'])]]
                require(semantic(checked[0])==semantic(checked[1]) and checked[0]['status']=='EXACT_RUP_LRAT_VERIFIED'
                        and checked[0]['cnf_sha256']==sha(cnf)==record['cnf_sha256']
                        and checked[0]['proof_sha256']==sha(lrat),'whole strict original proof normal/O binding differs')
                item.update(status='EXACT_BACKGROUND_REFUTATION',mathematical_exclusion=True,RUP=checked[0],RUP_optimized=checked[1])
            elif proposal['status']=='SAT_PENDING_INDEPENDENT_CHECK':
                for mode,flags in [('normal',[]),('optimized',['-O'])]:
                    stage(stem+'-witness-'+mode,[PYTHON,*flags,ROOT/'symbolic6_audit.py','--work',WORK,'--witness',background],55)
                receipts=[json.loads((WORK/(stem+'-witness-'+mode+'.json')).read_text()) for mode in ('normal','optimized')]
                require(receipts[0]==receipts[1] and receipts[0]['status']=='INDEPENDENT_ACTUAL_FIELD_WITNESS','whole actual witness normal/O differs')
                item.update(status='INDEPENDENT_ACTUAL_FIELD_WITNESS',witness=receipts[0])
            else:
                item.update(status='UNKNOWN_NO_EXCLUSION')
        except BaseException as error:
            item.update(status='FAILED_OR_BARRIER_NO_EXCLUSION',failure=type(error).__name__)
            write(RESULT,result);raise
        finally:
            entry.update(status=item['status'],finished=time.time());write(ATTEMPTS,attempts)
            if item['status'] not in ('EXACT_BACKGROUND_REFUTATION','INDEPENDENT_ACTUAL_FIELD_WITNESS'):
                write(ROOT/'symbolic6-frozen-INCOMPLETE.json',dict(agent='six-vdw-2',role='researcher',
                    stem=stem,background=background,cnf_sha256=record['cnf_sha256'],status=item['status'],
                    mathematical_exclusion=False,identical_retry_forbidden=True,resource_cap_increase_forbidden=True))
            result['exact_negative_models']=sum(c['mathematical_exclusion'] for c in result['cases']);write(RESULT,result)
        print(json.dumps(dict(stem=stem,status=item['status'])),flush=True)
        if item['status']!='EXACT_BACKGROUND_REFUTATION':break
    if len(result['cases'])==2 and all(c['mathematical_exclusion'] for c in result['cases']):
        result.update(status='EXACT_BOTH_BACKGROUNDS_SIX_RUN_EXCLUSION',longest_minority_run6_exclusion=True,
                      necessary_phase_heads_covered=3752)
    elif any(c['status']=='INDEPENDENT_ACTUAL_FIELD_WITNESS' for c in result['cases']):
        result['status']='CHECKED_FIELD_WITNESS_NO_INTERVAL_WORD'
    else:
        result['status']='BOUNDED_INCOMPLETE_NO_FULL_BRANCH_EXCLUSION'
    write(RESULT,result);print(json.dumps({k:v for k,v in result.items() if k!='cases'}),flush=True)


if __name__=='__main__':main()
