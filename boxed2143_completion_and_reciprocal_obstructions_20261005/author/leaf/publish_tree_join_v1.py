#!/usr/bin/env python3
"""Publish and verify one new checked packet on authorized main."""
import argparse
import fcntl
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parent
CAMPAIGN=Path('/scratch/research-team-colloquium-sol61-20261005')
REPO=Path('/tmp/quinn_boxed2143_publish_20261005')
DIRECTORY='boxed2143_tree_join_dynamics_20261005'
REMOTE='https://github.com/helgithorskarp/math_results'


def barrier():
    for p in [CAMPAIGN/'PAUSED.json',CAMPAIGN/'state/PAUSED.json',
              CAMPAIGN/'state/monitor/PAUSED.json',
              CAMPAIGN/'state/monitor/literature-first-20261005/PAUSED.json']:
        if p.exists(): raise RuntimeError('Active pause:'+str(p))
    for p in [CAMPAIGN/'HANDOVER.json',CAMPAIGN/'state/HANDOVER.json',
              CAMPAIGN/'state/monitor/HANDOVER.json']:
        if p.exists() and json.loads(p.read_text()).get('phase')!='completed':
            raise RuntimeError('Incomplete handover:'+str(p))


def git(*args,check=True):
    return subprocess.run(['git',*args],cwd=REPO,check=check,capture_output=True,text=True)


def push():
    barrier()
    receipt_path=ROOT/'tree_join_public_push_receipt_v1.json'
    if receipt_path.exists(): raise RuntimeError('Existing push receipt; inspect, never repeat blindly')
    replay=json.loads((ROOT/'publication_tree_join_portability_receipt_v1.json').read_text())
    if not replay['all_deterministic_fields_match']:
        raise RuntimeError('Portable replay verification missing')
    if git('remote','get-url','origin').stdout.strip()!=REMOTE:
        raise RuntimeError('Wrong remote')
    if git('branch','--show-current').stdout.strip()!='main':
        raise RuntimeError('Wrong branch')
    if git('status','--porcelain').stdout:
        raise RuntimeError('Checkout not clean after source commit')
    latest_names=git('diff-tree','--no-commit-id','--name-only','-r','HEAD').stdout.splitlines()
    if not latest_names or any(not n.startswith(DIRECTORY+'/') for n in latest_names):
        raise RuntimeError('Last commit includes unrelated changes')
    start=time.monotonic()
    with (CAMPAIGN/'locks/github-main.lock').open('r') as lock:
        while True:
            try:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
            except BlockingIOError:
                if time.monotonic()-start>30: raise RuntimeError('Short lock wait exceeded30s')
                time.sleep(0.1)
        held=time.monotonic()
        barrier()
        before=git('rev-parse','HEAD').stdout.strip()
        fetched=git('fetch','origin','main');print(fetched.stderr,end='',flush=True)
        if git('cat-file','-e','origin/main:'+DIRECTORY,check=False).returncode==0:
            raise RuntimeError('Directory already upstream; inspect before retry')
        rebase=git('-c','user.name=Quinn (literature-researcher-3)',
                   '-c','user.email=literature-researcher-3@users.noreply.github.com',
                   'rebase','origin/main')
        print(rebase.stdout+rebase.stderr,end='',flush=True)
        barrier()
        published=git('push','origin','HEAD:main')
        print(published.stdout+published.stderr,end='',flush=True)
        commit=git('rev-parse','HEAD').stdout.strip()
        receipt={'actor':'literature-researcher-3','before_rebase':before,'commit':commit,
                 'remote':REMOTE,'branch':'main','source_directory':DIRECTORY,
                 'ordinary_non_force_push':True,'lock_held_seconds':time.monotonic()-held,
                 'public_source_verified':False,'full_target_solved':False}
        fcntl.flock(lock,fcntl.LOCK_UN)
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


def fetch_public(url):
    with urlopen(Request(url,headers={'User-Agent':'Colloquium-Quinn-source-verifier'}),timeout=30) as response:
        if response.status!=200: raise RuntimeError('Public URL not200:'+url)
        return response.read()


def verify():
    barrier()
    receipt=json.loads((ROOT/'tree_join_public_push_receipt_v1.json').read_text())
    commit=receipt['commit']
    if re.fullmatch('[0-9a-f]{40}',commit) is None: raise RuntimeError('Not a40hex commit')
    url=REMOTE+'/tree/'+commit+'/'+DIRECTORY
    fetch_public(url)
    paths=git('ls-tree','-r','--name-only',commit+':'+DIRECTORY).stdout.splitlines()
    verified={}
    for i,name in enumerate(paths):
        data=fetch_public('https://raw.githubusercontent.com/helgithorskarp/math_results/'+commit+'/'+DIRECTORY+'/'+name)
        expected=subprocess.run(['git','show',commit+':'+DIRECTORY+'/'+name],cwd=REPO,check=True,capture_output=True).stdout
        if data!=expected: raise RuntimeError('Remote bytes differ:'+name)
        verified[name]={'sha256':sha256(data).hexdigest(),'bytes':len(data),'http_status':200}
        if (i+1)%10==0: print('Public bytes matched '+str(i+1)+'/'+str(len(paths)),flush=True)
    for name in ['author/TREE_STATE_LEMMA.md','author/REVERSE_MERGE_AND_JOIN_BOUND.md',
                 'review/QUINN_TREE_STATE_REVIEW.md','review/QUINN_REVERSE_JOIN_REVIEW.md']:
        fetch_public(REMOTE+'/blob/'+commit+'/'+DIRECTORY+'/'+name)
    manifest=json.loads(git('show',commit+':'+DIRECTORY+'/PUBLIC_FILE_MANIFEST.json').stdout)
    for name,r in manifest['files'].items():
        if any(verified[name][k]!=v for k,v in r.items()):
            raise RuntimeError('Public selected manifest differs:'+name)
    result={**receipt,'public_source_verified':True,'source_url':url,
            'directory_http_status':200,'public_files_verified':verified,
            'verification':'Every52 public file fetched anonymously and byte-matched against exact Git objects and public manifest; cited proof/review blobs200.'}
    (ROOT/'tree_join_public_source_verification_v1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='public_files_verified'},indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['push','verify'])
    args=p.parse_args()
    if args.action=='push': push()
    else: verify()


if __name__=='__main__': main()
