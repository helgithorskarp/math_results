#!/usr/bin/env python3
"""One fixed eight-case full-extension split with mandatory certificate replay."""
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
import controls
import cube

sys.path.insert(0,str(cube.PARENT))
spec=importlib.util.spec_from_file_location('parent_run',cube.PARENT/'run.py')
parent_run=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent_run)
atomic,replay=parent_run.atomic,parent_run.replay


def sources():
    paths=[cube.ROOT/name for name in ('cube.py','audit.py','controls.py','run.py','verify.py','summarize.py')]
    paths += [cube.PARENT/name for name in ('generate.py','check_formula.cpp','run.py','inspect_graph.py','controls.py')]
    paths += [cube.INPUT]+[cube.PREVIOUS/name for name in ('check_lemma.py','classification.json','fixtures.json','boundary.json')]
    grand=cube.ROOT.parent/'ramsey_r55_order3_eleven_residual_sweep'
    paths += [grand/name for name in ('cases.json','result.json')]
    return {str(p.relative_to(cube.ROOT.parent)):cube.info(p) for p in paths}


def prepare(work):
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();parent=work/'parent.cnf'
    meta=json.loads(subprocess.check_output([sys.executable,'-B',str(cube.PARENT/'generate.py'),'--red-cycles','4','--output',str(parent)],text=True))
    cube.require(cube.info(parent)['sha256']==cube.PARENT_PIN,'reviewed parent bytes')
    checker=work/'check_formula'
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(cube.PARENT/'check_formula.cpp'),'-o',str(checker)],check=True)
    with (work/'parent.check.log').open('w') as log:
        subprocess.run([str(checker),'4',str(parent)],stdout=log,stderr=subprocess.STDOUT,check=True)
    cube.require(' PASS' in (work/'parent.check.log').read_text(),'complete parent audit')
    with (work/'parent.controls.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(cube.PARENT/'controls.py'),'--report',str(work/'parent.controls.json')],stdout=log,stderr=subprocess.STDOUT,check=True)
    with (work/'inherited_lemma.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(cube.PREVIOUS/'check_lemma.py'),'--source',str(cube.PREVIOUS),'--report',str(work/'inherited_lemma.json')],stdout=log,stderr=subprocess.STDOUT,check=True)
    bases={}
    for core in cube.cores():
        path=work/f"base{core['index']}.cnf"
        bases[str(core['index'])]=dict(formula=cube.make_base(parent,path,core),audit=audit.check_base(parent,path,core['bits']))
    report=controls.run(work/'base131.cnf',work/'controls')
    atomic(work/'controls.json',report);atomic(work/'bases.json',bases);atomic(work/'cases.json',cube.cases())
    return dict(parent=meta,bases=bases,controls=report,elapsed_seconds=round(time.monotonic()-start,6))


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=60);p.add_argument('--replay-seconds',type=int,default=300);p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();cube.require(not work.is_relative_to(cube.ROOT.parent),'external work directory');cube.require(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-k11-r4-four-empty-split-v1',python=sys.version.split()[0],workers=2,solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,sources=sources(),kissat=cube.info(a.kissat),drat_trim=cube.info(a.drat_trim))
    if (work/'contract.json').exists():cube.require(a.resume and json.loads((work/'contract.json').read_text())==contract,'changed/existing contract')
    atomic(work/'contract.json',contract);prep=prepare(work);rows={};stop=threading.Event()
    print('PASS complete parent, four pinned bases, inherited lemma and split controls',flush=True)

    def one(case):
        key=case['id'];row=dict(case,status='not_started')
        if stop.is_set() or (work/'STOP').exists():return row
        path=work/(key+'.json')
        try:
            base=work/f"base{case['index']}.cnf";cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log')
            row['formula']=cube.make(base,cnf,case['branch']);row['audit']=audit.check(base,cnf,case['branch'])
            old=json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                cube.require(all(old[k]==case[k] for k in case) and old['formula']==row['formula'],'saved case differs')
                cube.require(cube.info(proof)==old['proof'],'saved trace changed')
                if old['status']=='open':
                    cube.require(old['solver_code']==0 and 's UNKNOWN' in log.read_text(),'saved UNKNOWN');return old
            if old and old['status']=='excluded':row.update(solver_code=20,proof=old['proof'],solve_seconds=old['solve_seconds'])
            else:
                before=time.monotonic()
                with log.open('w') as stream:
                    result=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(proof)],stdout=stream,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode,proof=cube.info(proof),solve_seconds=round(time.monotonic()-before,6))
            if row['solver_code']==20:
                row['replay']=replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds);row['status']='excluded'
            elif row['solver_code']==10:
                row['graph']=parent_run.candidate(4,log,work/(key+'.edges'));row['status']='target_graph_verified';stop.set()
            elif row['solver_code']==0:
                cube.require('s UNKNOWN' in log.read_text(),'missing UNKNOWN');row['status']='open'
            else:raise ValueError('unexpected solver exit')
        except Exception as error:row.update(status='error',error=repr(error));stop.set()
        atomic(path,row);return row

    def save():
        result=dict(contract=contract,preparation=prep,cases=[rows[k] for k in sorted(rows)],excluded=sorted(k for k in rows if rows[k]['status']=='excluded'),open=sorted(k for k in rows if rows[k]['status']=='open'),complete=len(rows)==8 and all(r['status'] in ('open','excluded') for r in rows.values()),target_graph=any(r['status']=='target_graph_verified' for r in rows.values()),elapsed_seconds=round(time.monotonic()-start,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,case) for case in cube.cases()]):
            row=future.result();rows[row['id']]=row;save();print(json.dumps({k:row[k] for k in ('id','status')}),flush=True)
    cube.require(sources()==contract['sources'],'source drift');r=save();cube.require(not any(x['status']=='error' for x in rows.values()),'case errors; inspect checkpoint')
    print('FINISHED '+json.dumps({k:r[k] for k in ('complete','excluded','open','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
