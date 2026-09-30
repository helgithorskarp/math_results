#!/usr/bin/env python3
"""Reproduce six-reviewer-2's QR617 review from compact pinned source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def need(condition,message):
    if not condition:
        raise ValueError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--reuse-corpus',action='store_true',help='Check an existing generated corpus without source regeneration.')
    args=parser.parse_args();work=args.workdir.resolve()
    need(work!=HERE and HERE not in work.parents,'corpus must be outside published source')
    work.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((HERE/'INPUT.json').read_text())
    target=HERE.parent/manifest['directory']
    need(target!=work and target not in work.parents,'workdir must be outside target source')
    for row in manifest['files']:
        data=(target/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'pinned source differs: '+row['path'])
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[name]='1'
    if not args.reuse_corpus:
        with (work/'source-validation.stdout').open('w') as out,(work/'source-validation.stderr').open('w') as err:
            subprocess.run([sys.executable,'-B',str(target/'validate.py'),'--workdir',str(work),'--max-batches','8','--output',str(work/'source-validation.json')],env=env,check=True,timeout=1000,stdout=out,stderr=err)
    output=work/'review2-audit.json';profile=work/'review2-profile.json'
    subprocess.run([sys.executable,'-B',str(HERE/'audit.py'),'--workdir',str(work),'--output',str(output),'--profile',str(profile)],env=env,check=True,timeout=150)
    need(output.read_bytes()==(HERE/'expected.json').read_bytes(),'independent evidence differs')
    need(profile.read_bytes()==(HERE/'phase_profile.json').read_bytes(),'complete phase profile differs')
    print('PASS: pinned compact source; independent complete617-phase evidence and profile; strengthened40/73 and18-per-color bounds.')

if __name__=='__main__':main()
