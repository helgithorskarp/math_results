#!/usr/bin/env python3
"""Sequential bounded reproduction, mathematical controls and sanitizers."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

from check import check_cut,check_family,qr,require
from controls import run_controls

HERE=Path(__file__).resolve().parent


def build(source,output,env):
    subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic',
                    '-fsanitize=address,undefined','-fno-omit-frame-pointer',str(HERE/source),'-o',str(output)],env=env,check=True)


def sanitizer_check(work,env):
    start=time.monotonic();directory=Path(tempfile.mkdtemp(prefix='sanitizers-',dir=work))
    sanitizer_env=env.copy();sanitizer_env['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1'
    sanitizer_env['UBSAN_OPTIONS']='halt_on_error=1'
    for name,filename in [('generate_seeds','seeds.json'),('generate_inner','inner.json')]:
        executable=directory/name;build(name+'.cpp',executable,env)
        output=directory/filename
        if not output.exists():subprocess.run([str(executable),str(output)],env=sanitizer_env,check=True,capture_output=True,text=True)
        require(output.read_bytes()==(work/filename).read_bytes(),'sanitizer full transcript differs: '+name)
    executable=directory/'generate_implications';build('generate_implications.cpp',executable,env)
    q=qr();representative_rows=[]
    for count in (2,3,16,31,33):
        cases=[]
        for s in (0,49,112,198,309):
            data=json.loads((work/f'canonical-{s}.json').read_text());cuts=data['cuts']
            if len(cuts)<count or cuts[count-1]['type']!='implication':continue
            checked=check_family(cuts[:count-1],[s,s,1],q);erased=checked['root_union']
            cases.append((s,erased,cuts[count-1]))
        if not cases:continue
        stage=directory/f'round-{count}';stage.mkdir(exist_ok=True)
        input_path=stage/'input.txt';input_path.write_text('\n'.join(' '.join(map(str,[s,s,1,len(erased),*erased])) for s,erased,cut in cases)+'\n')
        subprocess.run([str(executable),str(input_path),str(stage/'proofs'),'90','0'],env=sanitizer_env,check=True,capture_output=True,text=True)
        for s,erased,cut in cases:
            file=stage/'proofs'/f'proof-565-{s}-{s}-1.json';r=json.loads(file.read_text())
            require(r['status']=='UNIT_CONTRADICTION_CERTIFICATE' and r['erased_positions']==erased,'sanitizer proof instance/status')
            actual={'type':'implication','record':{k:r[k] for k in ['key','steps','final_ap']}}
            require(actual==cut,'sanitizer representative certificate differs')
            release_file=work/f'round-{count}'/'proofs'/file.name
            require(release_file.read_bytes()==file.read_bytes(),'sanitizer representative native bytes differ')
            support=check_cut(actual,[s,s,1],q,set(erased));representative_rows.append([s,count,len(support),len(r['steps'])])
    return {'status':'VERIFIED_SANITIZER_REGENERATION','full_seed_and_inner_transcripts_byte_identical':True,
            'representative_implications_byte_identical_and_directly_checked':representative_rows,
            'seconds':time.monotonic()-start}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--max-batches',type=int,default=8)
    parser.add_argument('--sanitizers',action='store_true');args=parser.parse_args()
    require(1<=args.max_batches<=12,'bounded validation batch count');work=args.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    start=time.monotonic();batches=[];reproduction=None
    for index in range(args.max_batches):
        log=work/f'validation-batch-{index+1}.txt'
        with log.open('w') as stream:subprocess.run([sys.executable,str(HERE/'reproduce.py'),'--workdir',str(work),'--seconds','90'],env=env,check=True,stdout=stream)
        reproduction=json.loads((work/'reproduction.json').read_text())
        batches.append({k:reproduction[k] for k in ['status','batch_seconds','peak_self_rss_kib','peak_child_rss_kib']})
        print(json.dumps({'batch':index+1,**batches[-1]}),flush=True)
        if reproduction['status']=='VERIFIED_COMPLETE_OPPOSITE_PHASE_PACKING':break
        require(not reproduction['unrefuted_representatives'],'unrefuted closure: pause research; no exclusion claim')
    require(reproduction and reproduction['status']=='VERIFIED_COMPLETE_OPPOSITE_PHASE_PACKING','incomplete bounded regeneration: no uniform claim')
    controls=run_controls(work);sanitizers=sanitizer_check(work,env) if args.sanitizers else None
    result={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_COMPLETE_71_EDIT_SOURCE',
            'reproduction':reproduction,'validation_batches':batches,'controls':controls,'sanitizers':sanitizers,
            'seconds':time.monotonic()-start,'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'versions':{'python':sys.version.split()[0],'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]},
            'limits':'One sequential CPU job; all threads1; each native search invocation<=90seconds. Existing CPU1/memory2GiB/tasks128 unchanged.',
            'trust':'Exact Python direct checker and elementary support/reflection/affine proof. Same-author implementation independence; no peer-review/formalization claim.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['reproduction','controls']},indent=2))


if __name__=='__main__':main()
