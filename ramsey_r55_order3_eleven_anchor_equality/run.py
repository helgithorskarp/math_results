#!/usr/bin/env python3
"""Exactly two full anchor-equality tests, with full certificate replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import importlib.util
import json
import resource
import subprocess
import sys
import time
import anchor
import audit

sys.path.insert(0,str(anchor.PARENT))
spec=importlib.util.spec_from_file_location('parent_run',anchor.PARENT/'run.py')
parent_run=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent_run)
atomic,replay=parent_run.atomic,parent_run.replay


def sources():
    paths=[anchor.ROOT/n for n in ('anchor.py','audit.py','run.py','verify.py')]
    paths += [anchor.PARENT/n for n in ('generate.py','check_formula.cpp','controls.py','run.py','inspect_graph.py')]
    paths += [anchor.CLASSIFICATION,anchor.PREVIOUS/'boundary.json']
    paths += [anchor.ROOT.parent/'ramsey_r55_order3_eleven_signature_bound'/'PROOF.md']
    return {str(p.relative_to(anchor.ROOT.parent)):anchor.info(p) for p in paths}


def prepare(work):
    work.mkdir(parents=True,exist_ok=True);parent=work/'parent.cnf'
    meta=json.loads(subprocess.check_output([sys.executable,'-B',str(anchor.PARENT/'generate.py'),'--red-cycles','4','--output',str(parent)],text=True))
    anchor.require(anchor.info(parent)['sha256']==anchor.PARENT_PIN,'parent bytes')
    checker=work/'check_formula'
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(anchor.PARENT/'check_formula.cpp'),'-o',str(checker)],check=True)
    with (work/'parent.check.log').open('w') as log:
        subprocess.run([str(checker),'4',str(parent)],stdout=log,stderr=subprocess.STDOUT,check=True)
    anchor.require(' PASS' in (work/'parent.check.log').read_text(),'full parent audit')
    with (work/'parent.controls.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(anchor.PARENT/'controls.py'),'--report',str(work/'parent.controls.json')],stdout=log,stderr=subprocess.STDOUT,check=True)
    data=anchor.classify();atomic(work/'anchors.json',data);checked=audit.validate(data)
    formulas={}
    for case in anchor.cases():
        path=work/(case['id']+'.cnf')
        formulas[case['id']]=dict(formula=anchor.make(parent,path,case),audit=audit.check(parent,path,case['type']))
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as log:
            subprocess.run([sys.executable,*flags,'-B',str(anchor.ROOT/'audit.py'),'--parent',str(parent),'--formula',str(work/'a11_equality.cnf'),'--classification',str(work/'anchors.json'),'--work',str(work/('controls_'+tag)),'--report',str(work/(tag+'.json'))],stdout=log,stderr=subprocess.STDOUT,check=True)
    anchor.require((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls differ')
    result=dict(parent=meta,anchors=anchor.info(work/'anchors.json'),classification_check=checked,
                controls=json.loads((work/'normal.json').read_text()),formulas=formulas)
    atomic(work/'preparation.json',result)
    return json.loads((work/'preparation.json').read_text())


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=60);p.add_argument('--replay-seconds',type=int,default=300)
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();anchor.require(not work.is_relative_to(anchor.ROOT.parent),'external work')
    anchor.require(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-r4-anchor-equality-v1',python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,sources=sources(),kissat=anchor.info(a.kissat),drat_trim=anchor.info(a.drat_trim))
    if (work/'contract.json').exists():anchor.require(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing/changed contract')
    atomic(work/'contract.json',contract);prep=prepare(work);rows={}
    print('PASS complete parent, two full formulas, 45-anchor census, 34-core mapping and controls',flush=True)

    def one(case):
        key=case['id'];row=dict(case,**prep['formulas'][key],status='pending')
        if (work/'STOP').exists():return dict(row,status='not_started')
        path=work/(key+'.json');cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log')
        try:
            old=json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                anchor.require(all(old[k]==row[k] for k in ('id','type','bits','formula','audit')),'saved case identity')
                anchor.require(anchor.info(proof)==old['proof'],'saved trace changed')
                if old['status']=='open':
                    anchor.require(old['solver_code']==0 and 's UNKNOWN' in log.read_text(),'saved UNKNOWN');return old
            if old and old['status']=='excluded':row.update(solver_code=20,proof=old['proof'],solve_seconds=old['solve_seconds'])
            else:
                before=time.monotonic()
                with log.open('w') as f:
                    result=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode,proof=anchor.info(proof),solve_seconds=round(time.monotonic()-before,6))
            if row['solver_code']==20:
                row['replay']=replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds);row['status']='excluded'
            elif row['solver_code']==10:
                row['graph']=parent_run.candidate(4,log,work/(key+'.edges'));row['status']='target_graph_verified'
            elif row['solver_code']==0:
                anchor.require('s UNKNOWN' in log.read_text(),'explicit UNKNOWN');row['status']='open'
            else:raise ValueError('unexpected solver exit')
        except Exception as error:row.update(status='error',error=repr(error))
        atomic(path,row);return row

    def save():
        result=dict(contract=contract,preparation=prep,cases=[rows[k] for k in sorted(rows)],
            complete=len(rows)==2 and all(r['status'] in ('excluded','open') for r in rows.values()),
            excluded=sorted(k for k in rows if rows[k]['status']=='excluded'),open=sorted(k for k in rows if rows[k]['status']=='open'),
            target_graph=any(r['status']=='target_graph_verified' for r in rows.values()),
            elapsed_seconds=round(time.monotonic()-start,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,c) for c in anchor.cases()]):
            row=future.result();rows[row['id']]=row;save();print(row['id']+' '+row['status'],flush=True)
    anchor.require(contract['sources']==sources(),'source drift');result=save()
    anchor.require(not any(r['status']=='error' for r in rows.values()),'case error; inspect checkpoint')
    print('FINISHED '+json.dumps({k:result[k] for k in ('complete','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
