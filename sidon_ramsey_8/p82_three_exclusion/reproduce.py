#!/usr/bin/env python3
"""Replay both complete traversals with exact byte comparison and stream audit."""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import time
from verify import SOURCE,PROFILE,input_check,verify_run,fractional_check
sys.path.append(str(PROFILE))
from checks import build,controls,same,run,partition,write_rows


def write_json(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(path)


def paired_run(work,inputs,jobs,minimum,shard):
    pipes=[work/f'global_{method}_{shard}.fifo'for method in [0,1]]
    processes=[];handles=[];audit=None;start=time.monotonic()
    report=work/f'global_pair_{shard}_comparison.json'
    try:
        for pipe in pipes:os.mkfifo(pipe)
        for method in [0,1]:
            pre=work/f'global_{method}_{shard}'
            out=pre.with_suffix('.out').open('w');err=pre.with_suffix('.err').open('w');handles.extend([out,err])
            args=[work/'exclude','sweep',method,3,inputs/'orbit11.txt',PROFILE/'weights.txt',inputs/f'full_{method}.bin',shard,jobs,pre.with_suffix('.csv'),pipes[method],pre.with_suffix('.jsonl'),pre.with_suffix('.done'),minimum]
            processes.append(subprocess.Popen(list(map(str,args)),stdout=out,stderr=err))
        audit_out=report.with_name(report.stem+'_audit.json').open('w');audit_err=report.with_name(report.stem+'_audit.err').open('w');handles.extend([audit_out,audit_err])
        audit=subprocess.Popen([str(work/'audit_stream'),str(PROFILE/'weights.txt')],stdin=subprocess.PIPE,stdout=audit_out,stderr=audit_err)
        checksum=hashlib.sha256();total=0;last_report=0
        with pipes[0].open('rb',buffering=0)as left,pipes[1].open('rb',buffering=0)as right:
            a=b=b'';end_a=end_b=False
            while True:
                if not a and not end_a:a=left.read(1<<18);end_a=not a
                if not b and not end_b:b=right.read(1<<18);end_b=not b
                length=min(len(a),len(b))
                if length:
                    assert a[:length]==b[:length],('candidate stream mismatch',shard,total)
                    block=a[:length];checksum.update(block);audit.stdin.write(block);total+=length;a=a[length:];b=b[length:]
                elif end_a or end_b:
                    assert end_a and end_b and not a and not b,('stream length mismatch',shard,total)
                    break
                if time.monotonic()-last_report>=5:
                    write_json(report,dict(compared_bytes=total,sha256_prefix=checksum.hexdigest(),complete=False));last_report=time.monotonic()
        audit.stdin.close();assert audit.wait()==0,'stream auditor failed'
        assert [process.wait()for process in processes]==[0,0],'traversal failed'
        for handle in handles:handle.flush()
        audit_record=json.loads(report.with_name(report.stem+'_audit.json').read_text())
        assert audit_record['verified']and audit_record['bytes']==total
        write_json(report,dict(compared_bytes=total,sha256=checksum.hexdigest(),complete=True,seconds=time.monotonic()-start))
        same(work/f'global_0_{shard}.jsonl',work/f'global_1_{shard}.jsonl')
        print(f'Completed exact stream comparison for shard {shard}: {total} bytes.',flush=True)
    finally:
        for process in processes+([audit]if audit else []):
            if process.poll()is None:process.terminate()
        for process in processes+([audit]if audit else []):
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait()
        for handle in handles:handle.close()
        for pipe in pipes:pipe.unlink(missing_ok=True)


def audit_controls(program,fixture):
    import struct
    item=json.loads(fixture.read_text());domain=sum(1<<x for x in item['domain']);candidate=sum(1<<x for x in item['candidate']);collision=sum(1<<x for x in item['collision'])
    head=domain.to_bytes(16,'little')+struct.pack('<8Q',5,10,10,10,10,9,item['upper'],1)
    good=head+candidate.to_bytes(16,'little');samples={'valid':good,'truncated':good[:-1]}
    changed=bytearray(head);struct.pack_into('<Q',changed,72,2);samples['duplicate']=bytes(changed)+2*candidate.to_bytes(16,'little')
    changed=bytearray(head);struct.pack_into('<Q',changed,64,item['candidate_weight']-1);samples['over_upper']=bytes(changed)+candidate.to_bytes(16,'little')
    samples['sum_collision']=head+collision.to_bytes(16,'little')
    reports=[]
    for name,data in samples.items():
        result=subprocess.run([str(program),str(PROFILE/'weights.txt')],input=data,capture_output=True)
        assert (result.returncode==0)==(name=='valid'),(name,result.stderr)
        if name=='sum_collision':assert result.stderr.strip()==b'pair-sum collision'
        reports.append(dict(name=name,accepted=result.returncode==0,stderr=result.stderr.decode().strip()))
    return reports


def prepare_cache_fixture(work,generator):
    fixture=json.loads((SOURCE/'cache_fixture.json').read_text())
    parent=fixture['parent'];domains=fixture['domains'];weights=list(map(int,(PROFILE/'weights.txt').read_text().split()))
    assert parent==sorted(set(parent))and len(parent)==60 and len(domains)==10
    for domain,classes in zip(domains,fixture['positive_partitions']):
        partition(domain,classes,[10,10,10,10,9])
        assert set(domain)<=set(parent)and sum(weights[x]for x in set(parent)-set(domain))<=4000000
    directory=work/'cache_controls_data';directory.mkdir()
    write_rows(directory/'parent.txt',[parent]);write_rows(directory/'domains.txt',domains)
    (directory/'weights.txt').write_text(' '.join(map(str,weights+[0,0]))+'\n')
    record=run([generator,0,directory/'parent.txt',directory/'catalog.bin',10,directory/'weights.txt'])
    assert record['complete']and record['sets']==1428965
    return directory


def check_cache_paths(program,directory):
    records=[run([program,method,PROFILE/'weights.txt',directory/'catalog.bin',directory/'parent.txt',directory/'domains.txt'])for method in [0,1]]
    assert all(r['verified']and r['positive_domains']==10 and r['parent_preparations']==10 for r in records)
    for key in ['positive_domains','parent_preparations','parent_rows','exact_compared_trace_bytes']:assert records[0][key]==records[1][key]
    return records


def main():
    if not __debug__:raise SystemExit('Proof checks require Python without -O/PYTHONOPTIMIZE.')
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--inputs',type=Path);parser.add_argument('--jobs',type=int,default=3);parser.add_argument('--sanitizers',action='store_true');parser.add_argument('--minimum',type=int,default=0)
    args=parser.parse_args();assert 1<=args.jobs<=12 and 0<=args.minimum<=4107
    work=args.work.resolve();work.mkdir(parents=True,exist_ok=True);assert not any(work.iterdir()),'Use a fresh empty work directory.'
    assert SOURCE.parent.parent not in [work,*work.parents], 'Keep generated work outside the repository.'
    start=time.monotonic()
    if args.inputs is None:
        inputs=work/'inputs'
        subprocess.run([sys.executable,str(PROFILE/'reproduce.py'),'--work',str(inputs),'--jobs','4','--workers','6'],check=True)
    else:inputs=args.inputs.resolve()
    input_hashes=input_check(inputs)
    build(SOURCE/'exclude.cpp',work/'exclude');build(SOURCE/'audit_stream.cpp',work/'audit_stream')
    build(PROFILE.parent/'p84_weight_certificates/weighted_catalog.cpp',work/'catalog')
    build(SOURCE/'cache_controls.cpp',work/'cache_controls')
    cache_fixture=prepare_cache_fixture(work,work/'catalog')
    cache_records=check_cache_paths(work/'cache_controls',cache_fixture)
    control_work=work/'controls';control_work.mkdir();control_records=controls(work/'exclude',control_work,work/'catalog')
    stream_controls=audit_controls(work/'audit_stream',SOURCE/'audit_fixture.json')
    sanitizer_records=[];sanitizer_audit=[];sanitizer_cache=[]
    if args.sanitizers:
        build(SOURCE/'exclude.cpp',work/'exclude_sanitized',True);build(SOURCE/'audit_stream.cpp',work/'audit_sanitized',True)
        build(SOURCE/'cache_controls.cpp',work/'cache_sanitized',True)
        sanitizer_cache=check_cache_paths(work/'cache_sanitized',cache_fixture)
        directory=work/'sanitizer_controls';directory.mkdir();sanitizer_records=controls(work/'exclude_sanitized',directory,work/'catalog');sanitizer_audit=audit_controls(work/'audit_sanitized',SOURCE/'audit_fixture.json')
    write_json(work/'controls.json',control_records);write_json(work/'sanitizer_controls.json',sanitizer_records)
    print('Input catalogs and all requested controls verified; starting paired global traversals.',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs)as pool:
        futures=[pool.submit(paired_run,work,inputs,args.jobs,args.minimum,shard)for shard in range(args.jobs)]
        for future in futures:future.result()
    verification=verify_run(work,inputs,args.jobs,args.minimum)
    result=dict(verified=True,cache_controls=cache_records,sanitizer_cache_controls=sanitizer_cache,inputs=input_hashes,verification=verification,controls=control_records,sanitizer_controls=sanitizer_records,audit_controls=stream_controls,sanitizer_audit_controls=sanitizer_audit,fractional_certificates=fractional_check(SOURCE/'fractional_profiles.json'),jobs=args.jobs,seconds=time.monotonic()-start)
    expected=SOURCE/'expected.json'
    if args.minimum==0 and expected.exists():
        reference=json.loads(expected.read_text())
        for key in ['eligible_cases','nonempty_cases','totals','exact_compared_bytes_per_method','nonempty_query_records','largest_option_list','terminal_checks','cases_sha256']:assert verification[key]==reference[key],key
    write_json(work/'validation.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
