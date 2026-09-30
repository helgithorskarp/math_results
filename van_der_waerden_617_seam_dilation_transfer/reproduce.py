#!/usr/bin/env python3
"""Bounded sequential source-dependent regeneration and exact verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

HERE=Path(__file__).resolve().parent
FLAGS=['-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow']


def save(path,data):
    partial=path.with_suffix(path.suffix+'.partial')
    partial.write_text(json.dumps(data,indent=2)+'\n');partial.replace(path)


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def clean(record):
    return {k:v for k,v in record.items() if k!='seconds'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--repo',type=Path,default=HERE.parent)
    parser.add_argument('--seconds',type=float,default=90)
    args=parser.parse_args()
    if not 0<args.seconds<=90:parser.error('each child budget must be in(0,90]')
    out=args.workdir.resolve();out.mkdir(exist_ok=True,parents=True);repo=args.repo.resolve()
    provenance=json.loads((HERE/'provenance.json').read_text());expected=json.loads((HERE/'expected.json').read_text())
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    started=time.monotonic();stages=[]
    def run(label,command):
        t=time.monotonic()
        try:r=subprocess.run(command,text=True,capture_output=True,env=env,check=True,timeout=args.seconds)
        except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as error:
            save(out/'interrupted.json',{'status':'REPRODUCTION_INCOMPLETE_NO_MATHEMATICAL_EXCLUSION','stage':label,'error':str(error),'seconds':time.monotonic()-t})
            raise
        if r.stderr:(out/(label+'.log')).write_text(r.stderr)
        stages.append({'label':label,'seconds':time.monotonic()-t});return r.stdout
    paths=[]
    for i,dep in enumerate(provenance['inputs']):
        directory=repo/dep['directory'];local=i==1
        generator=directory/('generate_packing.cpp' if local else 'generate.cpp')
        verifier=directory/('verify_packing.cpp' if local else 'verify.cpp')
        for path in (generator,verifier):
            if not path.is_file():raise ValueError('missing declared public source: '+str(path))
        for pinned in dep['source_files']:
            if digest(directory/pinned['name'])!=pinned['sha256']:raise ValueError('declared dependency source hash mismatch')
        binary=out/('local18.bin' if local else 'full44.bin');paths.append(binary)
        genexe=out/('generate18' if local else 'generate44');checkexe=out/('verify18' if local else 'verify44')
        run('compile-base-generator-'+str(i),['g++',*FLAGS,str(generator),'-o',str(genexe)])
        run('compile-base-checker-'+str(i),['g++',*FLAGS,str(verifier),'-o',str(checkexe)])
        if not binary.exists():
            generation=json.loads(run('generate-base-'+str(i),[str(genexe),'0','617',str(binary)]));save(out/('generation-'+str(i)+'.json'),generation)
        if binary.stat().st_size!=dep['bytes'] or digest(binary)!=dep['transcript_sha256']:raise ValueError('base input bytes/hash mismatch')
        check=json.loads(run('check-base-'+str(i),[str(checkexe),str(binary)]))
        if not check['full_domain'] or check['cases']!=760761 or check['packing_bound']!=dep['bound']:raise ValueError('incomplete base verification')
        save(out/('base-check-'+str(i)+'.json'),check)
    executable=out/'check-lifts';run('compile-lift-checker',['g++',*FLAGS,str(HERE/'check_lifts.cpp'),'-o',str(executable)])
    check=json.loads(run('check-all-lifts',[str(executable),*map(str,paths)]))
    if clean(check)!=expected:raise ValueError('complete lift profile differs from expected')
    save(out/'lift-check.json',check)
    transfer=json.loads(run('check-transfer-identities',['python3',str(HERE/'verify_transfer.py')]))
    save(out/'transfer-check.json',transfer)
    result={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_COMPLETE_SEAM_DILATION_REPRODUCTION',
            'cold_base_transcripts_generated':sum(row['label'].startswith('generate-base-') for row in stages),
            'lift_check':clean(check),'transfer_check':clean(transfer),'stages':stages,
            'seconds':time.monotonic()-started,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'self_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'limits':'One sequential CPU job, all numerical threads1; each child<=90s; unchanged scope limits.'}
    save(out/'reproduction.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('lift_check','transfer_check','stages')},indent=2))


if __name__=='__main__':main()
