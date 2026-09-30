#!/usr/bin/env python3
"""Full sanitizer phase generation and representative implication replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

from check import implications, qr

SOURCE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--release-workdir',type=Path,required=True)
    parser.add_argument('--workdir',type=Path,required=True)
    args=parser.parse_args();release=args.release_workdir.resolve();out=args.workdir.resolve()
    if out.is_relative_to(SOURCE):parser.error('generated state must be outside source')
    out.mkdir(parents=True,exist_ok=True);env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    env['ASAN_OPTIONS']='detect_leaks=1:abort_on_error=1';env['UBSAN_OPTIONS']='halt_on_error=1'
    flags=['-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',
           '-fsanitize=address,undefined','-fno-omit-frame-pointer']
    start=time.monotonic();compiler=os.environ.get('CXX','g++')
    for name in ['first','second','implications']:
        subprocess.run([compiler,*flags,str(SOURCE/f'generate_{name}.cpp'),'-o',str(out/f'generate_{name}')],env=env,check=True)
    results={}
    for name,arguments in [('first',[565,out/'first.bin']),
                           ('second',[out/'first.bin',release/'first_star_supports.txt',out/'second.bin',90])]:
        r=subprocess.run([str(out/f'generate_{name}'),*map(str,arguments)],env=env,check=True,text=True,capture_output=True)
        results[name]=json.loads(r.stdout)
        if (out/f'{name}.bin').read_bytes()!=(release/f'{name}.bin').read_bytes():raise ValueError('sanitizer transcript mismatch: '+name)
    proofs=json.loads((release/'second_implications.json').read_text())['records']
    chosen={tuple(r['key']) for r in proofs[:12]+proofs[-12:]+[r for r in proofs if len(r['steps'])>=4]}
    chosen.add((1,616,1))
    lines=[]
    for line in (release/'residual_input.txt').read_text().splitlines():
        key=tuple(map(int,line.split()[:3]))
        if key in chosen:lines.append(line)
    unit_input=out/'representative_input.txt';unit_input.write_text('\n'.join(lines)+'\n')
    if len(lines)!=len(chosen):raise ValueError('representative key coverage')
    r=subprocess.run([str(out/'generate_implications'),str(unit_input),str(out/'proofs'),'90','0'],env=env,check=True,text=True,capture_output=True)
    results['implications']=json.loads(r.stdout)
    if results['implications']['pending'] or results['implications']['not_refuted']:raise ValueError('incomplete representative generation')
    q=qr();checked=[]
    for file in sorted((out/'proofs').glob('proof-*.json')):
        record=json.loads(file.read_text())
        if file.read_bytes()!=(release/'implication_proofs'/file.name).read_bytes():raise ValueError('sanitizer implication mismatch')
        support=implications(record,tuple(record['key']),q,erased=record['erased_positions'])
        checked.append({'key':record['key'],'steps':len(record['steps']),'protected_support':len(support)})
    if len(checked)!=len(chosen):raise ValueError('missing representative proof')
    result={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_SANITIZER_REGENERATION',
            'full_first_and_second_transcripts_byte_identical':True,
            'representative_implication_proofs_byte_identical_and_directly_checked':len(checked),
            'representatives':checked,'seconds':time.monotonic()-start,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'generation':results}
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['representatives','generation']},indent=2))


if __name__=='__main__':main()
