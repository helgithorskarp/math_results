#!/usr/bin/env python3
"""One bounded classifier/full-extension milestone with checked certificates."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse
import json
import os
import re
import resource
import subprocess
import sys
import time
import audit
import generate as gen


def atomic(path,data):
    temp=path.with_suffix(path.suffix+'.partial')
    with temp.open('w') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,path)


def sources():
    paths=[gen.ROOT/n for n in ('generate.py','audit.py','controls.py','run.py','verify.py')]+[gen.SEED,gen.ROOT.parent/'ramsey_r55_order3_eleven_local_bound_propagation/boundary.json']
    return {str(p.relative_to(gen.ROOT.parent)):gen.info(p) for p in paths}


def replay(drat,cnf,proof,log,seconds):
    start=time.monotonic()
    with log.open('w') as f:r=subprocess.run([str(drat),str(cnf),str(proof),'-t',str(seconds)],stdout=f,stderr=subprocess.STDOUT,timeout=seconds+60)
    text=log.read_text();m=re.search(r'(\d+) RAT lemmas in core',text)
    gen.need(r.returncode==0 and 's VERIFIED' in text and m is not None,'full DRAT replay')
    return dict(verified=True,rat_core_lemmas=int(m.group(1)),seconds=round(time.monotonic()-start,6))


def values(log):
    result={}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for v in map(int,line[2:].split()):
                if v:
                    gen.need(abs(v) not in result or result[abs(v)]==(v>0),'consistent model');result[abs(v)]=v>0
    return result


def witness(kind,log,path):
    from itertools import combinations
    assignment=values(log);n=24 if kind=='classification' else 43
    edge=gen.local()[1] if n==24 else gen.full()[1];red=[]
    for a,b in combinations(range(n),2):
        v=edge(a,b)
        if v if type(v)is bool else assignment[v]:red.append((a,b))
    path.write_text(f'{n} {len(red)}\n'+''.join(f'{a} {b}\n' for a,b in red))
    literal=set(red);physical=audit.physical(n)
    for pair,v in physical.items():gen.need((pair in literal)==(v if type(v)is bool else assignment[v]),'literal witness orbit mapping')
    for size,color in (((5,True),(4,False)) if n==24 else ((5,True),(5,False))):
        gen.need(not any(all((e in literal)==color for e in combinations(vs,2)) for vs in combinations(range(n),size)),'literal witness clique check')
    return dict(**gen.info(path),vertices=n,red_edges=len(red),literal_verified=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True);p.add_argument('--solve-seconds',type=int,default=60)
    p.add_argument('--replay-seconds',type=int,default=300);p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();gen.need(not work.is_relative_to(gen.ROOT.parent),'large outputs outside Git')
    gen.need(a.solve_seconds>0 and a.replay_seconds>0,'positive caps');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();contract=dict(format='core194-maximal-v1',sources=sources(),python=sys.version.split()[0],workers=2,
        kissat=gen.info(a.kissat),drat_trim=gen.info(a.drat_trim),solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds)
    if (work/'contract.json').exists():gen.need(a.resume and json.loads((work/'contract.json').read_text())==contract,'resume source/tool/resource contract')
    atomic(work/'contract.json',contract)
    for tag,flags in (('normal',[]),('optimized',['-O'])):
        with (work/(tag+'.log')).open('w') as f:subprocess.run([sys.executable,*flags,'-B',str(gen.ROOT/'controls.py'),'--work',str(work/tag),'--report',str(work/(tag+'.json'))],stdout=f,stderr=subprocess.STDOUT,check=True)
    gen.need((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized controls')
    reps=gen.representatives();atomic(work/'representatives.json',reps);rep_check=audit.check_representatives(reps)
    print('PASS normalization, literal graphs, complete formulas, representative maps and malformed controls',flush=True)
    rows={}
    def one(kind):
        row=dict(kind=kind,status='not_started');saved=work/(kind+'.json')
        if (work/'STOP').exists():return row
        try:
            cnf=work/(kind+'.cnf');proof=work/(kind+'.drat');log=work/(kind+'.solve.log')
            row.update(formula=gen.write(cnf,kind),audit=audit.check_formula(cnf,kind,reps))
            old=json.loads(saved.read_text()) if a.resume and saved.exists() else None
            if old:
                gen.need(all(row[k]==old[k] for k in row if k!='status'),'saved input identity');gen.need(old['proof']==gen.info(proof),'saved trace identity')
                row.update(solver_code=old['solver_code'],solve_seconds=old['solve_seconds'],proof=old['proof'])
            else:
                before=time.monotonic()
                with log.open('w') as f:r=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=r.returncode,solve_seconds=round(time.monotonic()-before,6),proof=gen.info(proof))
            if row['solver_code']==20:row.update(status='excluded',replay=replay(a.drat_trim,cnf,proof,work/(kind+'.replay.log'),a.replay_seconds))
            elif row['solver_code']==10:row.update(status='witness',witness=witness(kind,log,work/(kind+'.edges')))
            elif row['solver_code']==0:
                gen.need('s UNKNOWN' in log.read_text(),'explicit UNKNOWN');row['status']='unknown'
            else:raise ValueError('unexpected solver exit')
        except Exception as e:row.update(status='error',error=repr(e))
        atomic(saved,row);return row
    def save():
        out=dict(contract=contract,controls=json.loads((work/'normal.json').read_text()),representatives=rep_check,
            cases=[rows[k] for k in sorted(rows)],complete=len(rows)==2 and all(r['status'] in ('excluded','witness','unknown') for r in rows.values()),
            maximal_branch_excluded=len(rows)==2 and all(r['status']=='excluded' for r in rows.values()),new_whole_core_exclusions=[],
            target_graph=rows.get('extension',{}).get('status')=='witness',elapsed_seconds=round(time.monotonic()-start,6),
            largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',out);return out
    with ThreadPoolExecutor(2) as ex:
        for future in as_completed([ex.submit(one,k) for k in ('classification','extension')]):
            row=future.result();rows[row['kind']]=row;save();print(json.dumps(row),flush=True)
    gen.need(sources()==contract['sources'],'frozen source drift');out=save();gen.need(out['complete'],'incomplete; inspect checkpoint')
    if out['maximal_branch_excluded']:atomic(work/'boundary.json',gen.boundary())
    print('FINISHED '+json.dumps({k:out[k] for k in ('maximal_branch_excluded','target_graph','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
