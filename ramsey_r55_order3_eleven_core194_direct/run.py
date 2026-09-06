#!/usr/bin/env python3
"""Two complete direct cases; bounded solves and mandatory checked terminal evidence."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import argparse
import json
import os
import re
import resource
import subprocess
import sys
import time
import check
import decode
import generate

ROOT=Path(__file__).resolve().parent


def atomic(path,value):
    temporary=path.with_suffix(path.suffix+'.partial')
    with temporary.open('w') as stream:
        json.dump(value,stream,indent=2,sort_keys=True);stream.write('\n')
        stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)


def sources():
    own=['generate.py','check.py','decode.py','controls.py','run.py','verify.py','PROOF.md','blue_pair14.edges','red_pair15.edges']
    paths=[ROOT/n for n in own]
    for directory,names in [
        ('ramsey_r55_order3_eleven_core194_multiplicity',['PROOF.md','result.json','verification.json']),
        ('ramsey_r55_order3_eleven_core194_multiplicity_review1',['README.md','result.json']),
        ('ramsey_r55_order3_eleven_core194_pair',['boundary.json','PROOF.md'])]:
        paths += [ROOT.parent/directory/n for n in names]
    return {str(p.relative_to(ROOT.parent)):generate.identity(p) for p in sorted(paths)}


def prepare(work):
    work.mkdir(parents=True,exist_ok=True)
    rows=[]
    for color in ('blue','red'):
        rows.append(generate.write(color,work/(color+'.cnf')))
    for label,flags in [('normal',[]),('optimized',['-O'])]:
        with (work/(label+'.log')).open('w') as log:
            subprocess.run([sys.executable,'-B',*flags,str(ROOT/'controls.py'),'--formulas',str(work),
                '--work',str(work/('controls_'+label)),'--report',str(work/(label+'.json'))],
                stdout=log,stderr=subprocess.STDOUT,check=True)
    generate.need((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'normal/optimized checks differ')
    audit=json.loads((work/'normal.json').read_text())
    for row,independent in zip(rows,audit['formulas']):
        generate.need(row['color']==independent['color'] and row['formula']==dict(bytes=independent['bytes'],sha256=independent['sha256']), 'complete formula identity')
        generate.need({k:v for k,v in row['census'].items() if k!='all_five_sets'}==independent['census'],'entrywise reconstruction census')
    result=dict(generation=rows,audit=audit)
    atomic(work/'preparation.json',result)
    return result


def replay(executable,cnf,trace,log,limit):
    before=time.monotonic()
    with log.open('w') as stream:
        result=subprocess.run([str(executable),str(cnf),str(trace),'-t',str(limit)],stdout=stream,stderr=subprocess.STDOUT,timeout=limit+60)
    output=log.read_text()
    generate.need(result.returncode==0 and 's VERIFIED' in output,'full DRAT replay failed')
    rat=re.search(r'(\d+) RAT lemmas in core',output)
    generate.need(rat is not None,'full RAT statistic')
    return dict(verified=True,rat_core_lemmas=int(rat.group(1)),seconds=round(time.monotonic()-before,6))


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--solve-seconds',type=int,default=60);p.add_argument('--replay-seconds',type=int,default=300)
    p.add_argument('--resume',action='store_true');a=p.parse_args()
    work=a.work.resolve();generate.need(not work.is_relative_to(ROOT.parent),'external work directory')
    generate.need(min(a.solve_seconds,a.replay_seconds)>0,'positive limits');work.mkdir(parents=True,exist_ok=True)
    before=time.monotonic()
    contract=dict(format='r55-core194-direct-primary-v1',sources=sources(),python=sys.version.split()[0],workers=2,
        solve_seconds=a.solve_seconds,replay_seconds=a.replay_seconds,kissat=generate.identity(a.kissat),drat_trim=generate.identity(a.drat_trim))
    if (work/'contract.json').exists():
        generate.need(a.resume and json.loads((work/'contract.json').read_text())==contract,'existing or changed contract')
    atomic(work/'contract.json',contract)
    preparation=prepare(work)
    print('PASS complete direct formulas and independent controls',flush=True)
    def one(color):
        row=dict(color=color,status='not_started')
        if (work/'STOP').exists():return row
        cnf=work/(color+'.cnf');trace=work/(color+'.drat');log=work/(color+'.solve.log');path=work/(color+'.json')
        try:
            row['formula']=generate.identity(cnf)
            if a.resume and path.exists():
                old=json.loads(path.read_text())
                generate.need(old['color']==color and old['formula']==row['formula'] and old['trace']==generate.identity(trace),'saved case identity')
                if old['status']=='open':
                    generate.need(old['solver_code']==0 and 's UNKNOWN' in log.read_text(),'saved explicit UNKNOWN')
                    return old
                if old['status']=='excluded':row.update(old)
            if row['status']!='excluded':
                start=time.monotonic()
                with log.open('w') as stream:
                    solver=subprocess.run([str(a.kissat),f'--time={a.solve_seconds}',str(cnf),str(trace)],stdout=stream,stderr=subprocess.STDOUT,timeout=a.solve_seconds+60)
                row.update(solver_code=solver.returncode,trace=generate.identity(trace),solve_seconds=round(time.monotonic()-start,6))
            if row['solver_code']==20:
                row['replay']=replay(a.drat_trim,cnf,trace,work/(color+'.replay.log'),a.replay_seconds);row['status']='excluded'
            elif row['solver_code']==10:
                model=decode.write(log,work/(color+'.edges'));decode.satisfies(model,cnf)
                row['graph']=check.graph(work/(color+'.edges'),color);row['status']='target_graph_verified'
            elif row['solver_code']==0:
                generate.need('s UNKNOWN' in log.read_text(),'explicit UNKNOWN');row['status']='open'
            else:raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error',error=repr(error))
        atomic(path,row)
        return row
    rows={}
    def save():
        result=dict(contract=contract,preparation=preparation,cases=[rows[k] for k in sorted(rows)],
            complete=len(rows)==2 and all(r['status'] in ('excluded','open','target_graph_verified') for r in rows.values()),
            excluded=sorted(k for k,r in rows.items() if r['status']=='excluded'),open=sorted(k for k,r in rows.items() if r['status']=='open'),
            target_graph=any(r['status']=='target_graph_verified' for r in rows.values()),
            elapsed_seconds=round(time.monotonic()-before,6),largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json',result);return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one,c) for c in ('blue','red')]):
            row=future.result();rows[row['color']]=row;save();print(json.dumps(row),flush=True)
    generate.need(sources()==contract['sources'],'sources changed during run')
    final=save();generate.need(final['complete'],'incomplete bounded decision; inspect checkpoint')
    print('COMPLETE '+json.dumps({k:final[k] for k in ('excluded','open','target_graph','elapsed_seconds')}),flush=True)


if __name__=='__main__':main()
