#!/usr/bin/env python3
"""One bounded seven-case Core194 multiplicity sweep with mandatory full proof replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import importlib.util
import json
import resource
import subprocess
import sys
import threading
import time
import audit
import cube

sys.path.insert(0,str(cube.PARENT))
spec=importlib.util.spec_from_file_location('parent_run',cube.PARENT/'run.py')
parent_run=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent_run)
atomic,replay=parent_run.atomic,parent_run.replay


def sources():
    old=json.loads((cube.PREVIOUS/'result.json').read_text())
    paths=set(old['contract']['sources'])
    paths.update(str((cube.PREVIOUS/n).relative_to(cube.ROOT.parent)) for n in ('result.json','verification.json','boundary.json','PROOF.md'))
    paths.add(str((cube.BOUNDARY/'boundary.json').relative_to(cube.ROOT.parent)))
    paths.update(str((cube.ROOT/n).relative_to(cube.ROOT.parent)) for n in ('cube.py','audit.py','rebuild.py','run.py','verify.py','summarize.py','PROOF.md'))
    return {p:cube.info(cube.ROOT.parent/p) for p in sorted(paths)}


def make_case(work,case):
    base=work/'inherited'/'c194.cnf';full=work/(case['id']+'.cnf')
    return dict(formula=cube.make(base,full,case),audit=audit.check(base,full,case))


def prepare(work):
    work.mkdir(parents=True,exist_ok=True)
    with (work/'reconstruction.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(cube.ROOT/'rebuild.py'),'--work',str(work/'inherited')],stdout=log,stderr=subprocess.STDOUT,check=True)
    cases=cube.cases();cert=cube.certificate();atomic(work/'cases.json',cases);atomic(work/'certificate.json',cert)
    checked=audit.check_cases(cases,cert);classification=audit.classify(cert);control=[make_case(work,c) for c in cases[:2]]
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as log:
            subprocess.run([sys.executable,*flags,'-B',str(cube.ROOT/'audit.py'),'--base',str(work/'inherited'/'c194.cnf'),
                '--certificate',str(work/'certificate.json'),'--cases',str(work/'cases.json'),
                '--work',str(work/('controls_'+tag)),'--report',str(work/(tag+'.json'))],stdout=log,stderr=subprocess.STDOUT,check=True)
    cube.require((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls differ')
    answer=dict(inherited=json.loads((work/'inherited'/'reconstruction.json').read_text()),cases=checked,
        classification=classification,control_cases=control,controls=json.loads((work/'normal.json').read_text()))
    atomic(work/'preparation.json',answer);return answer


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=20);p.add_argument('--replay-seconds',type=int,default=300)
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();cube.require(not work.is_relative_to(cube.ROOT.parent),'external work directory')
    cube.require(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-core194-complete-empty-multiplicity-v1',python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,sources=sources(),kissat=cube.info(a.kissat),drat_trim=cube.info(a.drat_trim))
    if (work/'contract.json').exists():cube.require(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing or changed contract')
    atomic(work/'contract.json',contract);prep=prepare(work);cases=cube.cases();rows={};stop=threading.Event()
    print('PASS Core194 six-pattern rigidity and complete seven-case split',flush=True)

    def one(case):
        key=case['id'];row=dict(case,base=cube.BASE,status='not_started')
        if stop.is_set() or (work/'STOP').exists():return row
        path=work/(key+'.json');cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log')
        try:
            row.update(make_case(work,case))
            old=json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                cube.require(all(old[k]==row[k] for k in (*case,'base','formula','audit')),'saved case differs')
                cube.require(cube.info(proof)==old['proof'],'saved trace differs')
                if old['status']=='open':
                    cube.require(old['solver_code']==0 and 's UNKNOWN' in log.read_text(),'saved UNKNOWN');return old
            if old and old['status']=='excluded':row.update(solver_code=20,proof=old['proof'],solve_seconds=old['solve_seconds'])
            else:
                before=time.monotonic()
                with log.open('w') as f:
                    result=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode,proof=cube.info(proof),solve_seconds=round(time.monotonic()-before,6))
            if row['solver_code']==20:
                row['replay']=replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds);row['status']='excluded'
            elif row['solver_code']==10:
                row['graph']=parent_run.candidate(4,log,work/(key+'.edges'));row['status']='target_graph_verified';stop.set()
            elif row['solver_code']==0:
                cube.require('s UNKNOWN' in log.read_text(),'explicit UNKNOWN');row['status']='open'
            else:raise ValueError('unexpected solver exit')
        except Exception as error:row.update(status='error',error=repr(error));stop.set()
        atomic(path,row);return row

    def save():
        result=dict(scope="complete_Core194_one_empty_patterns_and_multiple_empty_branch",contract=contract,preparation=prep,cases=[rows[k] for k in sorted(rows)],
            complete=len(rows)==7 and all(r['status'] in ('excluded','open') for r in rows.values()),
            excluded=sorted(k for k in rows if rows[k]['status']=='excluded'),open=sorted(k for k in rows if rows[k]['status']=='open'),
            target_graph=any(r['status']=='target_graph_verified' for r in rows.values()),
            elapsed_seconds=round(time.monotonic()-start,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,c) for c in cases]):
            row=future.result();rows[row['id']]=row;save();print(json.dumps({k:row[k] for k in ('id','status')}),flush=True)
    cube.require(sources()==contract['sources'],'source drift');result=save()
    cube.require(not any(r['status']=='error' for r in rows.values()),'case error; inspect checkpoint')
    print('FINISHED '+json.dumps({k:result[k] for k in ('complete','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
