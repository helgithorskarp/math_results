"""Seal before any math import; whole-record exact normal/O checks and damages."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
NAMES=['COEFFICIENTS.json','PROOF.md','README.md','RECORD.json','REVIEW.md','SOURCE.json','literal.py','primal.py','validate.py']
expected_census=sorted(NAMES+['SHA256SUMS'])
if sorted(p.name for p in ROOT.iterdir())!=expected_census:
    raise ValueError('exact ten-file source census before mathematical imports')
manifest={}
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
    sha,name=line.split('  ',1)
    if name in manifest:
        raise ValueError('duplicate primary seal entry')
    manifest[name]=sha
if sorted(manifest)!=NAMES:
    raise ValueError('entire primary seal coverage')
for name,sha in manifest.items():
    p=ROOT/name
    if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
        raise ValueError('whole source seal before mathematical imports: '+name)
record=(ROOT/'RECORD.json').read_bytes()
environment={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}}
damages=['coefficient','duplicate-key','omit-aY','release-sign','empty-loop','basis','PSD-diagonal','action-sign','upper-metric','objective','endpoint']
runs=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
    for damage in [None]+damages:
        started=time.monotonic()
        try:
            result=subprocess.run([sys.executable,'-B',*flags,'primal.py',*([damage] if damage else [])],
                cwd=ROOT,env=environment,capture_output=True,timeout=45)
        except subprocess.TimeoutExpired:
            raise RuntimeError('fixed45s mathematical limit; no semantic or nonexistence conclusion')
        duration=time.monotonic()-started
        row=dict(mode=mode,damage=damage,exit_code=result.returncode,seconds=duration,
                 cumulative_child_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        if damage is None:
            if result.returncode or result.stdout!=record:
                raise ValueError('complete newly regenerated mathematical record: '+result.stderr.decode())
            row['whole_record_bytes']=len(record)
            row['whole_record_sha256']=hashlib.sha256(record).hexdigest()
        else:
            if result.returncode!=1 or b'ValueError:' not in result.stderr or b'Timeout' in result.stderr or b'MemoryError' in result.stderr:
                raise ValueError('actual declared semantic rejection '+damage+': '+result.stderr.decode())
            row['rejection']=result.stderr.decode().splitlines()[-1]
        runs.append(row)
        print(json.dumps({k:row[k] for k in ('mode','damage','exit_code','seconds')}),file=sys.stderr,flush=True)
print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',status='PASS',
    whole_record_bytes=len(record),whole_record_sha256=hashlib.sha256(record).hexdigest(),positive_replays=2,
    distinct_semantic_types=len(damages),actual_semantic_rejections=2*len(damages),fixed_child_timeout_seconds=45,
    interpreter=sys.version,native_threads=1,serial_math_jobs=1,runs=runs),sort_keys=True,indent=2))
