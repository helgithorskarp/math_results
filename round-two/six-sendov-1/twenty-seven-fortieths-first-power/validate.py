#!/usr/bin/env python3
"""Bounded serial complete replay and intended rejection tests, SAME author."""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FILES=('.gitignore','PROOF.md','LITERATURE.md','README.md','verify.py',
       'validate.py','COVER.json','EXPECTED.json','origin.py','check_origin.py','product.py')
GUARD=45
BASE={
 'last-polar-coefficient':'whole19 polar coefficients',
 'drop-polar-series':'all phase/deficit coefficients',
 'radial-lower-cap':'radial lower root',
 'radial-coefficient':'all radial coefficients',
 'chord-slope':'whole chord endpoint identity',
 'drop-deficit':'all phase/deficit coefficients',
 'wrong-T-lower':'retained full lower radial/energy coupling',
 'uncouple-energy':'whole mean/energy coupling',
 'centered-third-underpay':'all seven centered Newton payments',
 'newton-eighth':'all seven centered Newton payments',
 'origin-odd-root':'whole odd square-root coefficients',
 'origin-drop-eighth':'ALL seven centered orders',
 'omit-leaf':'missing closed-cover leaf',
 'false-empty':'false whole-box pruning rejected',
 'unsafe-anchor':'convex anchor boundary payment',
 'synchronized-denominator':'actual mean denominator must not use envelope coefficient',
 'last-bivariate-coefficient':'ALL13x19 coupled coefficient identities',
 'uncouple-T':'ALL13x19 coupled coefficient identities',
 'energy-integral-coefficient':'ALL13 coupled beta integral identities',
 'last-Bernstein-control':'ALL13 Bernstein reconstruction coefficients'}
PRODUCT={
 'product-floor-endpoint':'whole per-box floor endpoint',
 'product-F-endpoint':'whole radius sum upper endpoint',
 'product-variance-endpoint':'whole centered variance upper endpoint',
 'product-root-underpay':'whole centered coordinate square-root payment',
 'product-log-last':'whole logarithmic derivative coefficient identity',
 'product-exp-drop-fourth':'ALL FIVE positive exponential terms',
 'product-exp-sign':'whole logarithmic and exponential comparison signs',
 'gap-product-last-coefficient':'ALL9 clipping product ratio coefficients',
 'gap-polar-lipschitz':'whole fresh J Lipschitz endpoint payment',
 'gap-origin-lipschitz':'whole fresh O Lipschitz endpoint payment'}
BASE.update(PRODUCT)
MEAN={
 'drop-upper-anchor':'BOTH exact endpoint anchor',
 'quartic-variance-coefficient':'whole squared-variable centering coefficient',
 'quartic-real-norm-underpay':'whole real centered quartic norm payment',
 'quartic-cross-coefficient':'whole real quartic complexification coefficients',
 'quartic-Hilbert-factor':'whole real-to-complex Hilbert quartic factor',
 'linear-norm-root-underpay':'whole positive linear mean-norm payment',
 'last-cleared-coefficient':'ALL10 cleared origin coefficients',
 'tenth-Bernstein-control':'ALL10 final cleared Bernstein controls paid',
 'drop-lower-anchor':'BOTH exact endpoint anchor',
 'anchor-above-marked':'BOTH exact endpoint anchor',
 'centered-energy-decouple':'whole retained centered-energy identity',
 'odd-root-underpay':'whole odd square-root payment',
 'synchronized-denominator':'actual mean norm must remain separate',
 'diagonal-last-coefficient':'ALL9 diagonal coefficients',
 'last-bivariate-coefficient':'ALL90 centered u/t coefficients',
 'drop-eighth':'ALL seven centered orders',
 'last-Bernstein-control':'ALL9 final Bernstein controls paid'}

def require(ok,msg):
    if not ok:raise ValueError(msg)
def hashes(directory):
    return {name:dict(bytes=len((directory/name).read_bytes()),
                     sha256=hashlib.sha256((directory/name).read_bytes()).hexdigest())
            for name in FILES}
def manifest(directory):
    x=dict(agent='six-sendov-1',role='researcher',files=hashes(directory),
           trust='Byte pins detect changes, not joint source/evidence replacement')
    (directory/'MANIFEST.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seal',action='store_true')
    parser.add_argument('--private-dir',type=Path,
                        help='Optional writable scratch directory outside this contribution')
    args=parser.parse_args();start=time.monotonic();before=hashes(HERE)
    if args.seal:manifest(HERE)
    else:require(json.loads((HERE/'MANIFEST.json').read_text())['files']==before,
                 'whole source manifest')
    if args.private_dir:
        require(HERE!=args.private_dir.resolve() and HERE not in args.private_dir.resolve().parents,
                'verbose validation scratch stays outside publication')
        args.private_dir.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ)
    for name in THREADS:env[name]='1'
    expected=json.loads((HERE/'EXPECTED.json').read_text());sha=expected['full_checked_record_sha256']
    runs=[];positives=[];negative=[];whole_records={};private_progress=None
    if args.private_dir:private_progress=args.private_dir/'validation-progress.json'
    def run(directory,options,mode,success,label,program='verify.py',marker=None,record_path=None):
        flags=['-I','-B']+(['-O'] if mode=='optimized' else [])
        command=[sys.executable,*flags,str(directory/program),*options]
        if record_path:command+=['--record',str(record_path)]
        child_start=time.monotonic()
        result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=GUARD)
        seconds=time.monotonic()-child_start
        require((result.returncode==0)==success,'unexpected child outcome '+label+' '+result.stderr)
        if success:
            metadata=json.loads(result.stdout)
            require(metadata.get('result',metadata.get('status'))=='PASS','positive status '+label)
            if program=='verify.py':require(metadata['record_sha256']==sha,'whole main record '+label)
            blob=record_path.read_bytes()
            if program not in whole_records:whole_records[program]=blob
            require(blob==whole_records[program],'ENTIRE positive mathematical record bytes '+label)
            positives.append(label)
        else:
            require(result.returncode==1 and result.stderr.startswith('FAIL: ')
                    and (marker is None or marker in result.stderr)
                    and 'failed to reject' not in result.stderr,
                    'intended controlled rejection '+label+' '+result.stderr)
            negative.append(label)
        runs.append(dict(label=label,program=program,mode=mode,seconds=seconds,
                         exit_code=result.returncode,positive=success,
                         intended_rejection=marker))
        if private_progress:
            private_progress.write_text(json.dumps(dict(agent='six-sendov-1',role='researcher',
                status='IN_PROGRESS_NOT_A_PROOF',last_child=label,completed_runs=len(runs),
                completed_full_positives=len(positives),completed_rejections=len(negative),
                seconds=time.monotonic()-start),indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='sendov-twenty-seven-fortieths-',
                                     dir=args.private_dir) as td:
        root=Path(td);cold=root/'cold';cold.mkdir()
        for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,cold/name)
        for mode in ('normal','optimized'):
            for directory,label in ((HERE,'local'),(cold,'cold')):
                for program,kind in (('verify.py','main'),('check_origin.py','literal-conditional')):
                    run(directory,[],mode,True,label+'-'+kind+'-'+mode,program,
                        record_path=root/(label+'-'+kind+'-'+mode+'.json'))
        for mode in ('normal','optimized'):
            for damage,marker in BASE.items():
                run(HERE,['--damage',damage],mode,False,'math-'+damage+'-'+mode,marker=marker)
            for damage,marker in MEAN.items():
                run(HERE,['--damage',damage],mode,False,'conditional-'+damage+'-'+mode,
                    program='check_origin.py',marker=marker)
        fixtures=[]
        x=deepcopy(expected);x['worst_successful_polar']['integral']='0';fixtures.append(('wrong-polar-integral',x))
        x=deepcopy(expected);x['full_mean_bivariate_vectors']-=7;fixtures.append(('missing-centered-matrix',x))
        x=deepcopy(expected);x['full_checked_record_sha256']='0'*64;fixtures.append(('wrong-full-fingerprint',x))
        x=deepcopy(expected);x['energy_shell_cells']=True;fixtures.append(('wrong-type',x))
        x=deepcopy(expected);x['unexpected']=True;fixtures.append(('extra-key',x))
        for label,x in fixtures:
            file=root/(label+'.json');file.write_text(json.dumps(x))
            for mode in ('normal','optimized'):
                run(HERE,['--expected',str(file)],mode,False,'fixture-'+label+'-'+mode,marker='expected')
        cuts=json.loads((HERE/'COVER.json').read_text());cutkey=next(iter(cuts['splits']))
        leafkey=next(iter(cuts['leaves']));changed=[]
        x=deepcopy(cuts);x['splits'][cutkey]['axis']=True;changed.append(('bool-axis',x,'whole exact-cut path and axis types'))
        x=deepcopy(cuts);x['splits'][cutkey]['cut']=cuts['root'][2*cuts['splits'][cutkey]['axis']+1];changed.append(('boundary-cut',x,'whole nondegenerate exact cut'))
        x=deepcopy(cuts);x['splits'][cutkey]['cut']='54/80';changed.append(('noncanonical-cut',x,'whole nondegenerate exact cut'))
        x=deepcopy(cuts);x['leaves'][leafkey]='unresolved';changed.append(('unpaid-leaf',x,'whole leaf path/status types'))
        x=deepcopy(cuts);x['root'][0]='5/8';changed.append(('old-root',x,'root'))
        x=deepcopy(cuts);x['splits'][cutkey]['extra']=0;changed.append(('extra-cut-key',x,'whole exact-cut path and axis types'))
        for label,x,marker in changed:
            damaged=root/('cover-'+label);damaged.mkdir()
            for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,damaged/name)
            (damaged/'COVER.json').write_text(json.dumps(x));manifest(damaged)
            for mode in ('normal','optimized'):
                run(damaged,[],mode,False,'cover-'+label+'-'+mode,marker=marker)
        for mode in ('normal','optimized'):
            damaged=root/('source-'+mode);damaged.mkdir()
            for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,damaged/name)
            with (damaged/'origin.py').open('a') as file:file.write('\n# changed source byte\n')
            run(damaged,[],mode,False,'source-pin-'+mode,marker='manifest')
    require(hashes(HERE)==before,'source changed during whole validation')
    record=dict(agent='six-sendov-1',role='researcher',result='PASS',
        checked_at=datetime.now(timezone.utc).isoformat(),python=sys.version.split()[0],
        interpreter='CPython standard library',record_sha256=sha,
        whole_main_record_bytes=len(whole_records['verify.py']),
        whole_conditional_record_bytes=len(whole_records['check_origin.py']),
        conditional_record_sha256=hashlib.sha256(whole_records['check_origin.py']).hexdigest(),
        guard_seconds=GUARD,serial=True,native_threads={name:1 for name in THREADS},
        resource_scope='unchanged one CPU/two GiB; no escalation',
        max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        max_child_seconds=max(row['seconds'] for row in runs),total_seconds=time.monotonic()-start,
        full_typed_positives=positives,rejections=negative,runs=runs,
        source_unchanged=True,ENTIRE_mathematical_bytes_compared=True,
        independent_review=False,formalized=False,omitted_large_artifact=True,
        omission='Large private pilot/full coefficient corpora; ALL defining inputs and complete comparisons regenerate from compact source')
    if args.seal:(HERE/'VALIDATION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        archived=json.loads((HERE/'VALIDATION.json').read_text())
        require(archived['result']=='PASS' and archived['record_sha256']==sha,
                'archived validation evidence')
    if private_progress:private_progress.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(result='PASS',record_sha256=sha,
        full_typed_positives=len(positives),rejections=len(negative),
        max_child_seconds=record['max_child_seconds'],max_child_rss_kib=record['max_child_rss_kib'],
        total_seconds=record['total_seconds'])))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
