#!/usr/bin/env python3
"""One bounded26-case full-extension sweep with mandatory full proof replay."""
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
    paths.update(str((cube.PREVIOUS/n).relative_to(cube.ROOT.parent)) for n in ('result.json','verification.json','cases.json','boundary.json','PROOF.md'))
    paths.update(str(p.relative_to(cube.ROOT.parent)) for p in cube.NOEMPTY.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md'))
    paths.update(str((cube.ROOT/n).relative_to(cube.ROOT.parent)) for n in ('cube.py','audit.py','rebuild.py','run.py','verify.py','summarize.py'))
    return {p:cube.info(cube.ROOT.parent/p) for p in sorted(paths)}


def make_case(work,case):
    base=work/'inherited'/f"c{case['index']}.cnf";full=work/f"c{case['index']}.cnf"
    return dict(formula=cube.make(base,full,case),audit=audit.check(base,full,case))


def prepare(work):
    work.mkdir(parents=True,exist_ok=True)
    with (work/'reconstruction.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(cube.ROOT/'rebuild.py'),'--work',str(work/'inherited')],stdout=log,stderr=subprocess.STDOUT,check=True)
    spec=importlib.util.spec_from_file_location('inherited_noempty_audit',cube.NOEMPTY/'audit.py')
    inherited=importlib.util.module_from_spec(spec);spec.loader.exec_module(inherited)
    inherited_cover=inherited.check_cover(json.loads((cube.NOEMPTY/'classification.json').read_text()))
    cases=cube.cases();atomic(work/'cases.json',cases);checked=audit.check_cases(cases);control=make_case(work,cases[0])
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as log:
            subprocess.run([sys.executable,*flags,'-B',str(cube.ROOT/'audit.py'),'--base',str(work/'inherited'/'c92.cnf'),
                '--formula',str(work/'c92.cnf'),'--cases',str(work/'cases.json'),
                '--work',str(work/('controls_'+tag)),'--report',str(work/(tag+'.json'))],stdout=log,stderr=subprocess.STDOUT,check=True)
        with (work/('local_'+tag+'.log')).open('w') as log:
            subprocess.run([sys.executable,*flags,'-B',str(cube.NOEMPTY/'check_local.py'),'--certificate',str(cube.NOEMPTY/'local_obstructions.json'),
                '--report',str(work/('local_'+tag+'.json'))],stdout=log,stderr=subprocess.STDOUT,check=True)
        cube.require((work/('local_'+tag+'.json')).read_bytes()==(cube.NOEMPTY/'local_check.json').read_bytes(),'inherited local certificate controls changed')
    cube.require((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls differ')
    answer=dict(inherited=json.loads((work/'inherited'/'reconstruction.json').read_text()),inherited_cover=inherited_cover,
        inherited_local=json.loads((work/'local_normal.json').read_text()),cases=checked,control_case=control,controls=json.loads((work/'normal.json').read_text()))
    atomic(work/'preparation.json',answer);return answer


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=20);p.add_argument('--replay-seconds',type=int,default=300)
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();cube.require(not work.is_relative_to(cube.ROOT.parent),'external work directory')
    cube.require(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-r4-empty-propagation-v1',python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,sources=sources(),kissat=cube.info(a.kissat),drat_trim=cube.info(a.drat_trim))
    if (work/'contract.json').exists():cube.require(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing or changed contract')
    atomic(work/'contract.json',contract);prep=prepare(work);cases=cube.cases();rows={};stop=threading.Event()
    print('PASS complete26 bases, inherited noempty evidence,312 blue edges,49152 assignments and controls',flush=True)

    def one(case):
        key=f"c{case['index']}";row=dict(case,base=case['formula'],status='not_started')
        if stop.is_set() or (work/'STOP').exists():return row
        path=work/(key+'.json');cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log')
        try:
            row.update(make_case(work,case))
            old=json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                cube.require(all(old[k]==row[k] for k in (*(k for k in case if k!='formula'),'base','formula','audit')),'saved case differs')
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
        result=dict(contract=contract,preparation=prep,cases=[rows[k] for k in sorted(rows)],
            complete=len(rows)==26 and all(r['status'] in ('excluded','open') for r in rows.values()),
            excluded=sorted(k for k in rows if rows[k]['status']=='excluded'),open=sorted(k for k in rows if rows[k]['status']=='open'),
            target_graph=any(r['status']=='target_graph_verified' for r in rows.values()),
            elapsed_seconds=round(time.monotonic()-start,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,c) for c in cases]):
            row=future.result();rows[row['index']]=row;save();print(json.dumps({k:row[k] for k in ('index','status')}),flush=True)
    cube.require(sources()==contract['sources'],'source drift');result=save()
    cube.require(not any(r['status']=='error' for r in rows.values()),'case error; inspect checkpoint')
    print('FINISHED '+json.dumps({k:result[k] for k in ('complete','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
