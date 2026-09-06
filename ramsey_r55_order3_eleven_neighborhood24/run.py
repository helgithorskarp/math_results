#!/usr/bin/env python3
"""Bounded six-case local-neighborhood test; literal SAT checks and full DRAT replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import os
import re
import resource
import subprocess
import sys
import time
import audit
import controls
import generate as gen


def atomic(path,data):
    tmp=path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as f:
        json.dump(data,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def sources():
    paths=[gen.ROOT/n for n in ('generate.py','audit.py','controls.py','run.py','verify.py')]
    paths += [gen.OLD/n for n in gen.PINS]
    return {str(p.relative_to(gen.ROOT.parent)):gen.info(p) for p in paths}


def replay(drat,cnf,proof,log,seconds):
    start=time.monotonic()
    with log.open('w') as f:
        r=subprocess.run([str(drat),str(cnf),str(proof),'-t',str(seconds)],stdout=f,stderr=subprocess.STDOUT,timeout=seconds+60)
    text=log.read_text();match=re.search(r'(\d+) RAT lemmas in core',text)
    gen.need(r.returncode==0 and 's VERIFIED' in text and match is not None,'full DRAT replay')
    return dict(verified=True,rat_core_lemmas=int(match.group(1)),seconds=round(time.monotonic()-start,6))


def prepare(work):
    work.mkdir(parents=True,exist_ok=True)
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as f:
            subprocess.run([sys.executable,*flags,'-B',str(gen.ROOT/'controls.py'),'--work',str(work/tag),
                            '--report',str(work/(tag+'.json'))],stdout=f,stderr=subprocess.STDOUT,check=True)
    gen.need((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls')
    cases=gen.cases();atomic(work/'cases.json',cases)
    return json.loads((work/'normal.json').read_text())


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--solve-seconds',type=int,default=60)
    p.add_argument('--replay-seconds',type=int,default=300);p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();gen.need(not work.is_relative_to(gen.ROOT.parent),'large evidence outside repository')
    gen.need(a.solve_seconds>0 and a.replay_seconds>0,'positive caps');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='r55-local24-six-cores-v1',python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,kissat=gen.info(a.kissat),drat_trim=gen.info(a.drat_trim),sources=sources())
    if (work/'contract.json').exists():gen.need(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing or changed contract')
    atomic(work/'contract.json',contract);prep=prepare(work);cases=gen.cases();rows={}
    print('PASS six-case cover, literal local formulas,2074 small graphs and normal/optimized controls',flush=True)
    def one(case):
        key='c'+str(case['index']);row=dict(case,status='not_started')
        if (work/'STOP').exists():return row
        cnf=work/(key+'.cnf');proof=work/(key+'.drat');log=work/(key+'.solve.log');edges=work/(key+'.edges');saved=work/(key+'.json')
        try:
            row.update(formula=gen.write(cnf,case),audit=audit.check_formula(cnf,case))
            old=json.loads(saved.read_text()) if a.resume and saved.exists() else None
            if old:
                gen.need(all(row[k]==old[k] for k in row if k!='status'),'saved input changed')
                gen.need(old['trace']==gen.info(proof),'saved trace changed')
                row.update(solver_code=old['solver_code'],solve_seconds=old['solve_seconds'],trace=old['trace'])
            else:
                before=time.monotonic()
                with log.open('w') as f:
                    r=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=r.returncode,solve_seconds=round(time.monotonic()-before,6),trace=gen.info(proof))
            if row['solver_code']==20:
                row.update(replay=replay(a.drat_trim,cnf,proof,work/(key+'.replay.log'),a.replay_seconds),status='local_excluded')
            elif row['solver_code']==10:
                gen.decode(log,edges);row.update(graph=audit.check_graph(edges,case),status='local_witness',edge_file=gen.info(edges),
                    graph_controls=controls.graph_controls(edges,case,work/(key+'_controls')))
            elif row['solver_code']==0:
                gen.need('s UNKNOWN' in log.read_text(),'explicit UNKNOWN');row['status']='unknown'
            else:raise ValueError('unexpected solver code')
        except Exception as error:row.update(status='error',error=repr(error))
        atomic(saved,row);return row
    def save():
        result=dict(contract=contract,preparation=prep,cases=[rows[k] for k in sorted(rows)],
            complete=len(rows)==6 and all(r['status'] in ('local_excluded','local_witness','unknown') for r in rows.values()),
            local_excluded=sorted(k for k in rows if rows[k]['status']=='local_excluded'),
            local_witness=sorted(k for k in rows if rows[k]['status']=='local_witness'),unknown=sorted(k for k in rows if rows[k]['status']=='unknown'),
            new_whole_core_exclusions=[],target_graph=False,elapsed_seconds=round(time.monotonic()-start,6),
            largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,c) for c in cases]):
            row=future.result();rows[row['index']]=row;save();print(json.dumps({k:row[k] for k in ('index','status')}),flush=True)
    gen.need(sources()==contract['sources'],'frozen source drift');r=save();gen.need(r['complete'],'incomplete run; inspect checkpoint')
    print('FINISHED '+json.dumps({k:r[k] for k in ('complete','local_excluded','local_witness','unknown','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
