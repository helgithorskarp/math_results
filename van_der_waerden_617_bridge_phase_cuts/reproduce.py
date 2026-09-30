#!/usr/bin/env python3
"""Sequential regeneration and independent checking; standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from check import verify
from check_sharpness import run as sharpness
from controls import run as controls

SOURCE = Path(__file__).resolve().parent


def compare(actual, expected, label):
    # Expected evidence is JSON: integer histogram keys become strings.
    actual = json.loads(json.dumps(actual))
    for key, value in expected.items():
        if actual.get(key) != value:
            raise ValueError(f'{label}: expected field {key} differs')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--sanitizers',action='store_true')
    args=parser.parse_args()
    out=args.workdir.resolve()
    if out.is_relative_to(SOURCE):
        parser.error('keep generated transcripts outside the publication source directory')
    out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[key]='1'
    compiler=os.environ.get('CXX','g++')
    flags=['-std=c++17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow']
    if args.sanitizers:
        flags+=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']
        env['ASAN_OPTIONS']='detect_leaks=1:abort_on_error=1'
        env['UBSAN_OPTIONS']='halt_on_error=1'
    else:
        flags+=['-O3']
    executable=out/('generate-san' if args.sanitizers else 'generate')
    start=time.monotonic()
    subprocess.run([compiler,*flags,str(SOURCE/'generate.cpp'),'-o',str(executable)],env=env,check=True)
    expected=json.loads((SOURCE/'expected.json').read_text())
    checks={}
    generation={}
    for width in [1106,1130]:
        transcript=out/f'bridge{width}.bin'
        if not transcript.exists():
            result=subprocess.run([str(executable),str(width//2),str(transcript)],env=env,
                                  check=True,text=True,capture_output=True)
            generation[str(width)]=json.loads(result.stdout)
            (out/f'generation{width}.json').write_text(json.dumps(generation[str(width)],indent=2)+'\n')
        supplement=SOURCE/'implications.json' if width==1130 else None
        result=verify(transcript,supplement,width//2)
        compare(result,expected['bridges'][str(width)],str(width))
        checks[str(width)]=result
    sharp=sharpness()
    compact={k:v for k,v in sharp.items() if k!='seconds'}
    compact['cases']=[{k:v for k,v in case.items() if k!='forced_centers'} for case in sharp['cases']]
    compare(compact,expected['sharpness'],'sharpness')
    rejected=controls(out/'bridge1130.bin',SOURCE/'implications.json',out)
    compare(rejected,expected['controls'],'controls')
    result={'status':'VERIFIED_ALL_PUBLISHED_BRIDGE_CLAIMS','sanitizers':args.sanitizers,
            'bridge_checks':checks,'sharpness':sharp,'controls':rejected,
            'seconds':time.monotonic()-start,
            'source_sha256':{path.name:hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in sorted(SOURCE.iterdir()) if path.is_file()}}
    (out/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checked_cases_per_bridge':760761,
                      'bridge_width':1130,'three_petal_stars':51,
                      'sharp_symmetric_completion_width':1106,
                      'rejection_controls':rejected['rejections_checked'],
                      'sanitizers':args.sanitizers,'seconds':result['seconds']},indent=2))


if __name__=='__main__':
    main()
