#!/usr/bin/env python3
"""Bounded resumable generation and exact verification of the 71-edit cut.

No generated corpus, earlier transcript, SAT solver or external input is needed.
One sequential CPU job, native search batches at most90 seconds. Re-run the
same command after a partial batch. Incomplete or unrefuted cases prove nothing.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

from check import check_cut,check_family,qr,representatives,require,target,verify

HERE=Path(__file__).resolve().parent


def save(path,data):
    temporary=path.with_suffix(path.suffix+'.partial')
    temporary.write_text(json.dumps(data,indent=2)+'\n');temporary.replace(path)


def compile_source(source,executable,env):
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',str(source),'-o',str(executable)],env=env,check=True)


def generate(source_name,output,work,env):
    if not output.exists():
        executable=work/source_name
        compile_source(HERE/(source_name+'.cpp'),executable,env)
        r=subprocess.run([str(executable),str(output)],env=env,check=True,text=True,capture_output=True)
        save(work/(source_name+'-generation.json'),json.loads(r.stdout))


def compare_expected(result):
    path=HERE/'expected.json'
    if path.exists():
        expected=json.loads(path.read_text())
        for key,value in expected.items():
            actual=json.loads(json.dumps(result[key]))
            require(actual==value,f'expected field differs: {key}')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=90)
    args=parser.parse_args();require(0<args.seconds<=90,'search batch budget in (0,90]')
    work=args.workdir.resolve();require(work!=HERE,'generated data requires a separate workdir');work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();q=qr();env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    generate('generate_seeds',work/'seeds.json',work,env)
    generate('generate_inner',work/'inner.json',work,env)
    seed_data=json.loads((work/'seeds.json').read_text())
    require(seed_data['format']=='QR617_EQUAL_PHASE_SEEDS_V1' and seed_data['length']==3704 and seed_data['half_width']==565,'seed format')
    seeds={}
    for row in seed_data['records']:
        s=row['key'][0];require(type(s) is int and 0<=s<617 and row['key']==[s,s,1] and s not in seeds,'seed coverage')
        # Every direct first/second seed is checked, including those which
        # reflection later permits us to omit from native propagation.
        first={'type':'opposed','record':row['first']};used=check_cut(first,row['key'],q)
        if row['second'] is not None:check_cut({'type':'opposed','record':row['second']},row['key'],q,used)
        seeds[s]=row
    require(set(seeds)==set(range(617)),'full seed phase coverage')
    cases={};used={}
    for s in representatives():
        path=work/f'canonical-{s}.json'
        if path.exists():data=json.loads(path.read_text())
        else:
            row=seeds[s];cuts=[{'type':'opposed','record':row['first']}]
            if row['second'] is not None:cuts.append({'type':'opposed','record':row['second']})
            data={'key':[s,s,1],'cuts':cuts};save(path,data)
        require(data['key']==[s,s,1],'saved phase key')
        check=check_family(data['cuts'],data['key'],q);cases[s]=data;used[s]=set(check['root_union'])
    executable=work/'generate_implications'
    if any(len(d['cuts'])<target(s) for s,d in cases.items()):compile_source(HERE/'generate_implications.cpp',executable,env)
    rounds=[];pending=[];unrefuted=[]
    for count in range(2,34):
        active=[s for s,d in cases.items() if len(d['cuts'])==count-1 and count<=target(s)]
        if not active:continue
        if time.monotonic()-start>=args.seconds:pending=active;break
        directory=work/f'round-{count}';directory.mkdir(exist_ok=True)
        lines=[' '.join(map(str,[s,s,1,len(used[s]),*sorted(used[s])])) for s in active]
        input_path=directory/'input.txt';input_path.write_text('\n'.join(lines)+'\n')
        remaining=max(0.1,args.seconds-(time.monotonic()-start))
        r=subprocess.run([str(executable),str(input_path),str(directory/'proofs'),str(remaining),'0'],env=env,check=True,text=True,capture_output=True)
        generation=json.loads(r.stdout);save(directory/'generation.json',generation)
        for s in active:
            proof_path=directory/'proofs'/f'proof-565-{s}-{s}-1.json'
            if not proof_path.exists():pending.append(s);continue
            record=json.loads(proof_path.read_text())
            require(record['key']==[s,s,1] and record['erased_positions']==sorted(used[s]),'proof instance/erasure equality')
            if record['status']=='NOT_REFUTED_BY_UNIT_PROPAGATION':unrefuted.append(s);continue
            require(record['status']=='UNIT_CONTRADICTION_CERTIFICATE','certificate status')
            cut={'type':'implication','record':{k:record[k] for k in ['key','steps','final_ap']}}
            support=check_cut(cut,[s,s,1],q,used[s]);used[s].update(support);cases[s]['cuts'].append(cut)
            save(work/f'canonical-{s}.json',cases[s])
        row={'cut_count':count,'active':len(active),'pending':pending[:],'unrefuted':unrefuted[:],'generation':generation}
        rounds.append(row);save(directory/'check.json',row)
        print(json.dumps({k:v for k,v in row.items() if k!='generation'}),flush=True)
        if pending or unrefuted:break
    complete=all(len(d['cuts'])>=target(s) for s,d in cases.items())
    if complete:
        result=verify(work,work/'inner.json');compare_expected(result)
        result['expected_comparison']='PASSED' if (HERE/'expected.json').exists() else 'NOT_YET_RECORDED'
    else:
        result={'agent':'six-vdw-3','role':'researcher','status':'PARTIAL_GENERATION_NO_UNIFORM_71_EDIT_CLAIM',
                'pending_representatives':pending,'unrefuted_representatives':unrefuted,
                'minimum_current_canonical_cut_count':min(len(d['cuts']) for d in cases.values()),
                'next_step':'Re-run the same bounded command for pending cases. An unrefuted closure is not satisfiability or an edit optimum.'}
    result.update({'batch_seconds':time.monotonic()-start,
                   'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   'seed_sha256':hashlib.sha256((work/'seeds.json').read_bytes()).hexdigest()})
    save(work/'reproduction.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
