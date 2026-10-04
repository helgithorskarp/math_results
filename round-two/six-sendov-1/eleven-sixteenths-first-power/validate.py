#!/usr/bin/env python3
"""Bounded serial same-author whole replays and specific adverse gates."""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import itertools
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
FILES=('.gitignore','COVER.json','EXPECTED.json','PROOF.md','LITERATURE.md','README.md',
       'core.py','origin.py','check_origin.py','product.py','coupled.py','literal.py',
       'verify.py','validate.py','homothety.py')
GUARD=45
MATH={
 'last-polar-coefficient':'whole19 polar coefficients',
 'drop-polar-series':'all phase/deficit coefficients',
 'radial-lower-cap':'radial lower root',
 'radial-coefficient':'all radial coefficients',
 'chord-slope':'whole chord endpoint identity',
 'wrong-T-lower':'retained full lower radial/energy coupling',
 'uncouple-energy':'whole mean/energy coupling',
 'centered-third-underpay':'all seven centered Newton payments',
 'newton-eighth':'all seven centered Newton payments',
 'origin-odd-root':'whole odd square-root coefficients',
 'origin-drop-eighth':'ALL seven centered orders',
 'false-empty':'false whole-box pruning rejected',
 'unsafe-anchor':'convex anchor boundary payment',
 'uncouple-T':'ALL13x19 coupled coefficient identities',
 'energy-integral-coefficient':'ALL13 coupled beta integral identities',
 'omit-face-leaf':'missing closed face leaf',
 'ET-last-bivariate-coefficient':'ALL13x19 coupled coefficient identities',
 'ET-last-Bernstein-control':'ALL13 Bernstein reconstruction coefficients',
 'drop-upper-anchor':'BOTH exact endpoint anchor',
 'drop-lower-anchor':'BOTH exact endpoint anchor',
 'quartic-variance-coefficient':'whole squared-variable centering coefficient',
 'quartic-real-norm-underpay':'whole real centered quartic norm payment',
 'quartic-cross-coefficient':'whole real quartic complexification coefficients',
 'quartic-Hilbert-factor':'whole real-to-complex Hilbert quartic factor',
 'linear-norm-root-underpay':'whole positive linear mean-norm payment',
 'last-cleared-coefficient':'ALL10 cleared origin coefficients',
 'tenth-Bernstein-control':'ALL10 final cleared Bernstein controls paid',
 'anchor-above-marked':'BOTH exact endpoint anchor',
 'centered-energy-decouple':'whole retained centered-energy identity',
 'odd-root-underpay':'whole odd square-root payment',
 'synchronized-denominator':'actual mean norm must remain separate',
 'diagonal-last-coefficient':'ALL9 diagonal coefficients',
 'last-bivariate-coefficient':'ALL90 centered u/t coefficients',
 'drop-eighth':'ALL seven centered orders',
 'last-Bernstein-control':'ALL9 final Bernstein controls paid',
 'product-floor-endpoint':'whole per-box floor endpoint',
 'product-F-endpoint':'whole radius sum upper endpoint',
 'product-variance-endpoint':'whole centered variance upper endpoint',
 'product-root-underpay':'whole centered coordinate square-root payment',
 'product-log-last':'whole logarithmic derivative coefficient identity',
 'product-exp-drop-fourth':'ALL FIVE positive exponential terms',
 'product-exp-sign':'whole logarithmic and exponential comparison signs',
 'floor-endpoint':'floor endpoint',
 'radius-seven-floors':'other radius floors',
 'J-omit-differentiated-floor':'excluding differentiated slot',
 'J-integral-denominator':'derivative integrals',
 'J-underpaid-bound':'J Lipschitz',
 'E-path-underpayment':'squared-norm path',
 'mean-path-underpayment':'mean path',
 'O-missing-slot-square':'AM-GM coefficients',
 'O-linear-marked-endpoint':'AM-GM coefficients',
 'slot-square-coefficient':'removed-slot',
 'O-drop-odd-norm-factor':'odd norm factor',
 'O-drop-last-cubic-coefficient':'cubic majorant coefficients',
 'O-weighted-integral-underpayment':'weighted cubic integral',
 'O-underpaid-bound':'origin Lipschitz',
 'ratio-last-coefficient':'ratio coefficients',
 'critical-location-sign':'ALL nine affine-derivative versus factor-channel coefficients',
 'monic-leading-factor-eight':'whole monic ninth-degree primitive with marked zero',
 'primitive-factor-eight':'full original-primitive and normalized channel values',
 'primitive-a-power':'full original-primitive and normalized channel values',
 'channel-drop-last-coefficient':'ALL nine affine-derivative versus factor-channel coefficients',
 'gradient-missing-factor-nine':'all slot derivatives by exact full multilinear differences',
 'clip-wrong-denominator':'whole l1 clipping displacement',
 'transform-leading-power-eight':'entire degree-nine leading coefficient',
 'transform-centre-sign':'marked original root retained',
 'derivative-leading-power-nine':'ALL NINE derivative chain coefficients',
 'last-polynomial-coefficient':'entire degree-nine leading coefficient',
 'omit-critical-slot':'ALL eight critical multiplicity slots',
 'reciprocal-orientation':'ALL eight affine reciprocal coordinates',
 'mass-ratio-inversion':'finite positive mass threshold contraction',
 'zero-contraction':'positive contraction domain',
 'disk-majorant':'ALL nine exact closed-disk contraction bounds'}

def require(ok,message):
    if not ok:raise ValueError(message)

def hashes(directory):
    return {name:dict(bytes=len((directory/name).read_bytes()),
        sha256=hashlib.sha256((directory/name).read_bytes()).hexdigest()) for name in FILES}

def seal(directory):
    (directory/'MANIFEST.json').write_text(json.dumps({'files':hashes(directory)},
        indent=2,sort_keys=True)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seal',action='store_true')
    parser.add_argument('--private-dir',type=Path);args=parser.parse_args()
    start=time.monotonic();before=hashes(HERE)
    if args.seal:seal(HERE)
    else:require(json.loads((HERE/'MANIFEST.json').read_text())=={'files':before},
        'whole source manifest')
    if args.private_dir:
        require(HERE!=args.private_dir.resolve() and HERE not in args.private_dir.resolve().parents,
            'verbose validation scratch stays outside publication')
        args.private_dir.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ)
    for name in THREADS:env[name]='1'
    expected=json.loads((HERE/'EXPECTED.json').read_text());sha=expected['full_checked_record_sha256']
    rows=[];positives=[];negatives=[];whole_blob=None
    progress=args.private_dir/'validation-progress.json' if args.private_dir else None
    def run(directory,options,mode,success,label,marker=None,record_path=None):
        nonlocal whole_blob
        flags=['-I','-B']+(['-O'] if mode=='optimized' else [])
        command=[sys.executable,*flags,str(directory/'verify.py'),*options]
        if record_path:command+=['--record',str(record_path)]
        child_start=time.monotonic()
        result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=GUARD)
        seconds=time.monotonic()-child_start
        require((result.returncode==0)==success,
            'unexpected child outcome '+label+' '+result.stdout+' '+result.stderr)
        if success:
            metadata=json.loads(result.stdout)
            require(metadata.get('result')=='PASS' and metadata['record_sha256']==sha,
                'positive whole record status '+label)
            blob=record_path.read_bytes()
            require(hashlib.sha256(blob.rstrip(b'\n')).hexdigest()==sha,
                'complete canonical positive mathematical record '+label)
            if whole_blob is None:whole_blob=blob
            require(blob==whole_blob,'ENTIRE positive mathematical record bytes '+label)
            positives.append(label)
        else:
            require(result.returncode==1 and result.stderr.startswith('FAIL: ')
                and marker in result.stderr and 'failed to reject' not in result.stderr,
                'intended controlled rejection '+label+' '+result.stderr)
            negatives.append(label)
        rows.append(dict(label=label,mode=mode,seconds=seconds,exit_code=result.returncode,
            positive=success,intended_rejection=marker))
        if progress:progress.write_text(json.dumps(dict(agent='six-sendov-1',role='researcher',
            status='IN_PROGRESS_NOT_A_PROOF',last_child=label,completed_runs=len(rows),
            completed_full_positives=len(positives),completed_rejections=len(negatives),
            seconds=time.monotonic()-start),indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='sendov-eleven-sixteenths-',dir=args.private_dir) as td:
        root=Path(td);cold=root/'cold';cold.mkdir()
        for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,cold/name)
        for mode in ('normal','optimized'):
            for directory,label in ((HERE,'local'),(cold,'cold')):
                run(directory,[],mode,True,label+'-whole-'+mode,
                    record_path=root/(label+'-'+mode+'.json'))
        for mode in ('normal','optimized'):
            for damage,marker in MATH.items():
                run(HERE,['--damage',damage],mode,False,'math-'+damage+'-'+mode,marker)
        fixtures=[]
        x=deepcopy(expected);x['least_polar']['margin']='0';fixtures.append(('wrong-polar-margin',x,'value expected'))
        x=deepcopy(expected);x['full_mean_remainder_matrices']-=7;fixtures.append(('missing-mean-matrix',x,'value expected'))
        x=deepcopy(expected);x['full_checked_record_sha256']='0'*64;fixtures.append(('wrong-fingerprint',x,'value expected'))
        x=deepcopy(expected);x['closed_face_leaves']=True;fixtures.append(('wrong-type',x,'type expected'))
        x=deepcopy(expected);x['unexpected']=True;fixtures.append(('extra-key',x,'keys expected'))
        x=deepcopy(expected);del x['full_coupled_payment_sha256'];fixtures.append(('missing-key',x,'keys expected'))
        x=deepcopy(expected);x['marked_interval'][0]='54/80';fixtures.append(('noncanonical-expected',x,'value expected'))
        for label,x,marker in fixtures:
            path=root/(label+'.json');path.write_text(json.dumps(x))
            for mode in ('normal','optimized'):
                run(HERE,['--expected',str(path)],mode,False,'expected-'+label+'-'+mode,marker)
        dup=root/'duplicate-expected.json'
        text=json.dumps(expected);dup.write_text(text[:-1]+',"annular_gap":"1/10000"}')
        for mode in ('normal','optimized'):
            run(HERE,['--expected',str(dup)],mode,False,'expected-duplicate-'+mode,'duplicate JSON object key')
        cover=json.loads((HERE/'COVER.json').read_text());cut=next(iter(cover['splits']))
        leaf=next(iter(cover['leaves']));unused=next(''.join(p) for p in itertools.product('01',repeat=13)
            if ''.join(p) not in cover['splits'] and ''.join(p) not in cover['leaves'])
        changed=[]
        x=deepcopy(cover);x['splits'][cut]['axis']=True;changed.append(('bool-axis',x,'exact face cut path/axis/rational types'))
        x=deepcopy(cover);x['splits'][cut]['axis']=4;changed.append(('fifth-axis',x,'exact face cut path/axis/rational types'))
        x=deepcopy(cover);x['splits'][cut]['cut']=cover['root'][2*cover['splits'][cut]['axis']];changed.append(('boundary-cut',x,'strict canonical rational face parent cut'))
        x=deepcopy(cover);x['splits'][cut]['cut']='00/1';changed.append(('noncanonical-cut',x,'strict canonical rational face parent cut'))
        x=deepcopy(cover);x['splits'][cut]['half_open']=True;changed.append(('half-open-key',x,'exact face cut path/axis/rational types'))
        x=deepcopy(cover);x['leaves'][leaf]='unresolved';changed.append(('unpaid-leaf',x,'exact face leaf path/role types'))
        x=deepcopy(cover);del x['leaves'][leaf];changed.append(('missing-leaf',x,'missing closed face leaf'))
        x=deepcopy(cover);x['leaves'][unused]='standard-polar';changed.append(('unreachable-leaf',x,'all face entries reached'))
        x=deepcopy(cover);x['leaves'][cut]='standard-polar';changed.append(('leaf-split-overlap',x,'face internal/leaf disjointness'))
        x=deepcopy(cover);x['root']=cover['root'][:4]+['37/5','8']+cover['root'][4:];changed.append(('old-five-dimensional-root',x,'length face-root'))
        x=deepcopy(cover);x['root'][0]='5/8';changed.append(('wrong-marked-root',x,'value face-root'))
        x=deepcopy(cover);x['root'][2]='00/1';changed.append(('noncanonical-root',x,'value face-root'))
        for label,x,marker in changed:
            path=root/('cover-'+label+'.json');path.write_text(json.dumps(x))
            for mode in ('normal','optimized'):
                run(HERE,['--cover',str(path)],mode,False,'cover-'+label+'-'+mode,marker)
        dup=root/'duplicate-cover.json'
        text=json.dumps(cover);dup.write_text(text[:-1]+',"root":[]}')
        for mode in ('normal','optimized'):
            run(HERE,['--cover',str(dup)],mode,False,'cover-duplicate-'+mode,'duplicate JSON object key')
        for mode in ('normal','optimized'):
            damaged=root/('source-'+mode);damaged.mkdir()
            for name in (*FILES,'MANIFEST.json'):shutil.copyfile(HERE/name,damaged/name)
            # If imported, this emits an unmistakable marker. The source-pin
            # guard must reject first; accepting this fixture is impossible.
            with (damaged/'origin.py').open('a') as out:
                out.write('\nraise RuntimeError("MUTATED_HELPER_WAS_IMPORTED")\n')
            run(damaged,[],mode,False,'preimport-source-pin-'+mode,
                'manifest preimport whole local source bytes')
    require(hashes(HERE)==before,'source unchanged throughout complete validation')
    record=dict(agent='six-sendov-1',role='researcher',result='PASS',
        checked_at=datetime.now(timezone.utc).isoformat(),python=sys.version.split()[0],
        interpreter='CPython standard library',record_sha256=sha,
        whole_canonical_mathematical_bytes=len(whole_blob.rstrip(b'\n')),
        full_typed_positives=positives,rejections=negatives,runs=rows,
        mathematical_damage_cases=len(MATH),expected_fixture_cases=len(fixtures)+1,
        cover_fixture_cases=len(changed)+1,source_pin_cases=1,
        guard_seconds=GUARD,serial=True,native_threads={name:1 for name in THREADS},
        resource_scope='unchanged one CPU/two GiB; no escalation',
        max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        max_child_seconds=max(row['seconds'] for row in rows),total_seconds=time.monotonic()-start,
        source_unchanged=True,ENTIRE_mathematical_bytes_compared=True,
        independent_review=False,formalized=False,runtime_ancestor_or_reviewer_input=False,
        omitted_large_artifact=True,
        omission='Large private complete coefficient/control records; all defining inputs and complete comparisons regenerate from compact local source')
    if args.seal:(HERE/'VALIDATION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        archived=json.loads((HERE/'VALIDATION.json').read_text())
        require(archived['result']=='PASS' and archived['record_sha256']==sha,
            'archived source validation evidence')
    if progress:progress.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(result='PASS',record_sha256=sha,full_typed_positives=len(positives),
        rejections=len(negatives),max_child_seconds=record['max_child_seconds'],
        max_child_rss_kib=record['max_child_rss_kib'],total_seconds=record['total_seconds'])))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
