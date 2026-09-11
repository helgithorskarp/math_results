#!/usr/bin/env python3
"""Exact paired traversal, stream audit and global-cover accounting."""
from pathlib import Path
import argparse, concurrent.futures, csv, hashlib, json, os, subprocess, sys, time
SOURCE=Path(__file__).resolve().parent
PROFILE=SOURCE.parent/'p82_profiles'
sys.path.insert(0,str(SOURCE.parent/'p82_three_exclusion'))
from verify import input_check
from audit_controls import controls as audit_controls

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,x):
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,indent=2)+'\n');tmp.replace(p)
def source_hashes():return {p.name:digest(p)for p in sorted(SOURCE.iterdir())if p.suffix in ['.hpp','.cpp','.py','.txt']}
def run(args):
    p=subprocess.run(list(map(str,args)),capture_output=True,text=True);assert p.returncode==0,(args,p.stderr);assert not p.stderr,(args,p.stderr);return json.loads(p.stdout)
def build(name,work,sanitized=False):
    target=work/(name+('_sanitized'if sanitized else ''))
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie']if sanitized else ['-O3']
    subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Wconversion','-Werror',*flags,str(SOURCE/(name+'.cpp')),'-o',str(target)],check=True)
    return target

def paired_run(work,inputs,jobs,minimum,maximum,budget,shard):
    pipes=[work/f'global_{m}_{shard}.fifo'for m in [0,1]];processes=[];handles=[];audit=None;start=time.monotonic();report=work/f'comparison_{shard}.json'
    try:
        for pipe in pipes:os.mkfifo(pipe)
        for m in [0,1]:
            pre=work/f'global_{m}_{shard}';out=pre.with_suffix('.out').open('w');err=pre.with_suffix('.err').open('w');handles.extend([out,err])
            args=[work/'exclude',m,PROFILE/'weights.txt',inputs/f'full_{m}.bin',inputs/'orbit11.txt',minimum,maximum,shard,jobs,budget,pre.with_suffix('.csv'),pipes[m],pre.with_suffix('.done')]
            processes.append(subprocess.Popen(list(map(str,args)),stdout=out,stderr=err))
        ao=(work/f'audit_{shard}.json').open('w');ae=(work/f'audit_{shard}.err').open('w');handles.extend([ao,ae])
        args=[work/'audit_stream',PROFILE/'weights.txt',inputs/'orbit11.txt',minimum,maximum,shard,jobs,budget]
        audit=subprocess.Popen(list(map(str,args)),stdin=subprocess.PIPE,stdout=ao,stderr=ae)
        checksum=hashlib.sha256();total=0;last=0
        with pipes[0].open('rb',buffering=0)as left,pipes[1].open('rb',buffering=0)as right:
            a=b=b'';ea=eb=False
            while True:
                if not a and not ea:a=left.read(1<<18);ea=not a
                if not b and not eb:b=right.read(1<<18);eb=not b
                n=min(len(a),len(b))
                if n:
                    assert a[:n]==b[:n],('stream mismatch',shard,total)
                    block=a[:n];checksum.update(block);audit.stdin.write(block);total+=n;a=a[n:];b=b[n:]
                elif ea or eb:
                    assert ea and eb and not a and not b,('length mismatch',shard,total);break
                if time.monotonic()-last>=10:write_json(report,dict(complete=False,compared_bytes=total,sha256_prefix=checksum.hexdigest()));last=time.monotonic()
        audit.stdin.close();assert audit.wait()==0,'auditor failed'
        assert [p.wait()for p in processes]==[0,0],'traversal failed'
        for h in handles:h.flush()
        write_json(report,dict(complete=True,compared_bytes=total,sha256=checksum.hexdigest(),seconds=time.monotonic()-start))
        print(f'Shard {shard} complete: {total} exactly compared bytes.',flush=True)
    finally:
        for p in processes+([audit]if audit else []):
            if p.poll()is None:p.terminate()
        for p in processes+([audit]if audit else []):
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
        for h in handles:h.close()
        for p in pipes:p.unlink(missing_ok=True)

def verify(work,inputs,jobs,minimum,maximum,budget):
    expected=[{k:int(v)for k,v in r.items()}for r in csv.DictReader((PROFILE/'cases_2.csv').open())]
    all_rows=[];streams=[]
    for shard in range(jobs):
        tables=[]
        for m in [0,1]:
            p=work/f'global_{m}_{shard}';assert p.with_suffix('.done').read_text()=='complete\n'
            report=json.loads(p.with_suffix('.out').read_text());assert report['complete']
            assert not p.with_suffix('.err').read_text(),'Inspect possible witness or error.'
            table=[{k:int(v)for k,v in r.items()}for r in csv.DictReader(p.with_suffix('.csv').open())]
            assert [r['orbit']for r in table]==[q for q in range(maximum-1,minimum-1,-1)if q%jobs==shard]
            assert report['packings']==sum(r['packings']for r in table)
            assert report['sat']==sum(r['sat']for r in table)and report['unknown']==sum(r['unknown']for r in table)
            assert all(0<=v<2**64 for r in table for v in r.values());tables.append(table)
        assert tables[0]==tables[1];table=tables[0];all_rows+=table
        a=json.loads((work/f'audit_{shard}.json').read_text());c=json.loads((work/f'comparison_{shard}.json').read_text())
        assert not (work/f'audit_{shard}.err').read_text()
        assert a['verified']and c['complete']and a['bytes']==c['compared_bytes']==(table[-1]['trace_end']if table else 0)
        for k,ak in [('packings','pairs'),('unsat','unsat'),('unknown','unknown'),('sat','sat'),('calls','calls'),('queries','queries'),('options','options'),('leaves','leaves')]:assert a[ak]==sum(r[k]for r in table),k
        streams.append(dict(shard=shard,audit=a,comparison=c))
    all_rows.sort(key=lambda r:r['orbit'])
    assert [(r['orbit'],r['packings'])for r in all_rows]==[(r['orbit'],r['packings'])for r in expected if minimum<=r['orbit']<maximum]
    keys=['packings','unsat','unknown','sat','calls','queries','options','leaves']
    totals={k:sum(r[k]for r in all_rows)for k in keys}
    assert totals['unsat']+totals['unknown']+totals['sat']==totals['packings']
    assert totals['calls']<=totals['packings']*(budget+1)<2**64
    if totals['unknown']==totals['sat']==0:assert totals['calls']==totals['packings']+totals['options']
    cols=['orbit']+keys+['max_calls','parent_rows']
    with (work/'cases_completed.csv').open('w')as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');writer.writeheader();writer.writerows({k:r[k]for k in cols}for r in all_rows)
    return dict(verified=True,minimum=minimum,maximum=maximum,budget=budget,cases=len(all_rows),nonempty_cases=sum(r['packings']>0 for r in all_rows),totals=totals,max_pair_calls=max((r['max_calls']for r in all_rows),default=0),compared_bytes=sum(s['comparison']['compared_bytes']for s in streams),cases_sha256=digest(work/'cases_completed.csv'),streams=streams)

def main():
    if not __debug__:raise SystemExit('Python assertions required.')
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--jobs',type=int,default=4);p.add_argument('--minimum',type=int,default=1000);p.add_argument('--maximum',type=int,default=4107);p.add_argument('--budget',type=int,default=100000);p.add_argument('--sanitizers',action='store_true');args=p.parse_args()
    assert 1<=args.jobs<=12 and 0<=args.minimum<=args.maximum<=4107 and 1<=args.budget<=10**9
    work=args.work.resolve();work.mkdir(parents=True,exist_ok=True);assert not any(work.iterdir());assert SOURCE.parent.parent not in [work,*work.parents]
    start=time.monotonic();hashes=source_hashes();inputs=input_check(args.inputs.resolve());write_json(work/'start.json',dict(sources=hashes,inputs=inputs,args={k:str(v)if isinstance(v,Path)else v for k,v in vars(args).items()}))
    for name in ['exclude','audit_stream','controls']:build(name,work)
    commands=[work/'controls',PROFILE/'weights.txt',SOURCE/'query_fixture.txt',SOURCE.parent/'p80_extension_barrier/partition80.txt']
    controls=run(commands);sanitizers=None
    stream_controls=audit_controls(work/'audit_stream',PROFILE/'weights.txt',args.inputs/'orbit11.txt');sanitizer_stream=None
    if args.sanitizers:
        commands[0]=build('controls',work,True);sanitizers=run(commands)
        assert controls==sanitizers
        sanitizer_stream=audit_controls(build('audit_stream',work,True),PROFILE/'weights.txt',args.inputs/'orbit11.txt');assert stream_controls==sanitizer_stream
    write_json(work/'controls.json',dict(ordinary=controls,sanitizers=sanitizers,stream=stream_controls,sanitizer_stream=sanitizer_stream))
    print('Catalog identities and query/decision controls verified; starting paired sweep.',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs)as pool:
        futures=[pool.submit(paired_run,work,args.inputs.resolve(),args.jobs,args.minimum,args.maximum,args.budget,shard)for shard in range(args.jobs)]
        for f in futures:f.result()
    result=verify(work,args.inputs.resolve(),args.jobs,args.minimum,args.maximum,args.budget)
    assert source_hashes()==hashes,'Proof sources changed during run.'
    write_json(work/'validation.json',dict(verified=True,verification=result,controls=controls,sanitizers=sanitizers,stream_controls=stream_controls,sanitizer_stream=sanitizer_stream,source_hashes=hashes,inputs=inputs,seconds=time.monotonic()-start))
    print(json.dumps({k:v for k,v in result.items()if k!='streams'},indent=2))
if __name__=='__main__':main()
