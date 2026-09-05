#!/usr/bin/env python3
"""One bounded34-case full-extension sweep with mandatory full proof replay."""
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
    paths=[cube.ROOT/n for n in ('cube.py','audit.py','run.py','verify.py','summarize.py')]
    paths += [cube.PARENT/n for n in ('generate.py','check_formula.cpp','controls.py','run.py','inspect_graph.py')]
    paths += [cube.PREVIOUS/n for n in ('audit.py','anchors.json','result.json','verification.json','PROOF.md')]
    paths += [cube.BASES,cube.ROOT.parent/'ramsey_r55_order3_eleven_four_empty_split'/'boundary.json',
              cube.ROOT.parent/'ramsey_r55_order3_eleven_empty_signature'/'classification.json']
    return {str(p.relative_to(cube.ROOT.parent)):cube.info(p) for p in paths}


def make_case(work,case):
    key=f"c{case['index']}";parent=work/'parent.cnf';base=work/(key+'.base.cnf');full=work/(key+'.cnf')
    return dict(base=cube.make_base(parent,base,case),base_audit=audit.check_base(parent,base,case),
                formula=cube.make(base,full,case),audit=audit.check(base,full,case))


def prepare(work):
    work.mkdir(parents=True,exist_ok=True);parent=work/'parent.cnf'
    meta=json.loads(subprocess.check_output([sys.executable,'-B',str(cube.PARENT/'generate.py'),'--red-cycles','4','--output',str(parent)],text=True))
    cube.require(cube.info(parent)['sha256']==cube.PARENT_PIN,'complete parent hash')
    checker=work/'check_formula'
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(cube.PARENT/'check_formula.cpp'),'-o',str(checker)],check=True)
    with (work/'parent.check.log').open('w') as log:
        subprocess.run([str(checker),'4',str(parent)],stdout=log,stderr=subprocess.STDOUT,check=True)
    cube.require(' PASS' in (work/'parent.check.log').read_text(),'full parent audit')
    with (work/'parent.controls.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(cube.PARENT/'controls.py'),'--report',str(work/'parent.controls.json')],stdout=log,stderr=subprocess.STDOUT,check=True)
    spec=importlib.util.spec_from_file_location('anchor_literal_audit',cube.PREVIOUS/'audit.py')
    inherited=importlib.util.module_from_spec(spec);spec.loader.exec_module(inherited)
    anchor_check=inherited.validate(json.loads((cube.PREVIOUS/'anchors.json').read_text()))
    atomic(work/'inherited_anchors.json',anchor_check)
    cases=cube.cases();atomic(work/'cases.json',cases);checked=audit.check_cases(cases)
    control=make_case(work,cases[0])
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as log:
            subprocess.run([sys.executable,*flags,'-B',str(cube.ROOT/'audit.py'),'--parent',str(parent),
                '--base',str(work/'c88.base.cnf'),'--formula',str(work/'c88.cnf'),'--cases',str(work/'cases.json'),
                '--work',str(work/('controls_'+tag)),'--report',str(work/(tag+'.json'))],stdout=log,stderr=subprocess.STDOUT,check=True)
    cube.require((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls differ')
    answer=dict(parent=meta,inherited_anchors=anchor_check,cases=checked,control_case=control,
                controls=json.loads((work/'normal.json').read_text()))
    atomic(work/'preparation.json',answer)
    return json.loads((work/'preparation.json').read_text())


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=20);p.add_argument('--replay-seconds',type=int,default=300)
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();cube.require(not work.is_relative_to(cube.ROOT.parent),'external work directory')
    cube.require(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-r4-anchor-propagation-v1',python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,sources=sources(),kissat=cube.info(a.kissat),drat_trim=cube.info(a.drat_trim))
    if (work/'contract.json').exists():cube.require(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing or changed contract')
    atomic(work/'contract.json',contract);prep=prepare(work);cases=cube.cases();rows={};stop=threading.Event()
    print('PASS full parent, complete34-case application cover, inherited literal anchors and controls',flush=True)

    def one(case):
        key=f"c{case['index']}";row=dict(case,status='not_started')
        if stop.is_set() or (work/'STOP').exists():return row
        path=work/(key+'.json');cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log')
        try:
            row.update(make_case(work,case))
            old=json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                cube.require(all(old[k]==row[k] for k in (*case.keys(),'formula','audit','base_audit')),'saved case differs')
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
            complete=len(rows)==34 and all(r['status'] in ('excluded','open') for r in rows.values()),
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
