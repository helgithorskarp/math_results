"""Frozen source-only normal/O replay. Fixed45s serial children; no solver."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def require(ok,message):
    if not ok:raise ValueError(message)


def source_files(root):
    rows=[]
    for line in (root/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        require(len(sha)==64 and name==Path(name).name,'manifest exact local path')
        raw=(root/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==sha,'ENTIRE source seal before any math import: '+name)
        rows.append((name,raw,sha))
    require(len(rows)==len({a[0] for a in rows}) and len(rows)>=10,'entire distinct source set')
    return rows


def run(output):
    root=Path(__file__).resolve().parent
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    frozen=source_files(root)
    snapshot_sha=hashlib.sha256((root/'SHA256SUMS').read_bytes()).hexdigest()
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    programs=[('diagnostic','diagnose.py',[]),('physical-zero','physical.py',['--tau','0']),
              ('physical-max','physical.py',['--tau','219061/3080192']),
              ('capacity','capacity.py',[]),('defects','defects.py',[])]
    observations=[];complete={};modes=[]
    with tempfile.TemporaryDirectory(prefix='q19-source-only-',dir=output) as tmp:
        cold=Path(tmp)/'source';cold.mkdir()
        for name,raw,sha in frozen:
            (cold/name).write_bytes(raw)
            require(hashlib.sha256((cold/name).read_bytes()).hexdigest()==sha,'ENTIRE cold source bytes')
        (cold/'SHA256SUMS').write_bytes((root/'SHA256SUMS').read_bytes())
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal';current={}
            for tag,script,extra in programs:
                target=output/(mode+'-'+tag+'.json')
                args=[sys.executable,'-B','-s']+(['-O'] if optimized else [])+[
                    str(cold/script),'--coefficients',str(cold/'COEFFICIENTS.json'),'--out',str(target)]+extra
                start=time.monotonic()
                result=subprocess.run(args,cwd=cold,env=env,capture_output=True,text=True,timeout=45)
                seconds=time.monotonic()-start
                require(result.returncode==0,'complete mathematical child '+tag+': '+result.stderr)
                record=json.loads(target.read_bytes())
                runtime={key:record.pop(key) for key in ('observed_seconds','peak_RSS_KiB') if key in record}
                mathraw=canonical(record)+b'\n';current[tag]=record
                observations.append(dict(mode=mode,tag=tag,seconds=seconds,
                                         runtime=runtime,whole_math_bytes=len(mathraw),
                                         whole_math_sha256=hashlib.sha256(mathraw).hexdigest(),
                                         returncode=0,stderr=result.stderr,
                                         fixed_child_guard_seconds=45,native_threads_one=True))
                print(json.dumps(observations[-1]),flush=True)
            raw=canonical(current)+b'\n'
            if not complete:complete=current
            else:require(raw==canonical(complete)+b'\n','ENTIRE complete mathematical outputs normal/O equality')
            # Bind every independently decoded original point, not just its small blocks.
            for name,idx in [('physical-zero',0),('physical-max',1)]:
                a=current['diagnostic']['q19_trials'][idx]['entry_audit'];b=current[name]
                require(a['original_L_rational_sha256']==b['original_L_rational_sha256'] and
                        a['original_T_rational_sha256']==b['original_T_rational_sha256'],
                        'ENTIRE independent original L/T agrees across entry/spectral readers')
                require(a['all_entry_inequalities_paid'] and
                        all(x['positive_definite'] for x in b['fresh_block_certificates'].values()),
                        'every actual floor and all12 fresh physical comparisons')
            require(current['defects']['rejection_count']==18,'all mathematical defects actually rejected')
            modes.append(dict(mode=mode,whole_mathematical_bytes=len(raw),
                              whole_mathematical_sha256=hashlib.sha256(raw).hexdigest()))
    mathematical=canonical(complete)+b'\n';(output/'MATHEMATICS.json').write_bytes(mathematical)
    expected=root/'EXPECTED.json'
    if expected.exists():
        reference=json.loads(expected.read_bytes())
        require(reference['whole_mathematical_bytes']==len(mathematical) and
                reference['whole_mathematical_sha256']==hashlib.sha256(mathematical).hexdigest(),
                'ENTIRE declared expected mathematical record')
    record=dict(agent='six-downset-2',role='researcher',all_completed=True,
                frozen_manifest_sha256=snapshot_sha,frozen_source_files=len(frozen),
                entire_source_bytes_verified_before_mathematical_import=True,
                source_only_cold=True,normal_optimized_entire_mathematics_equal=True,
                only_two_explicit_runtime_observation_fields_removed=True,
                mathematical_record_bytes=len(mathematical),mathematical_record_sha256=hashlib.sha256(mathematical).hexdigest(),
                modes=modes,observations=observations,serial_mathematical_children=1,
                fixed_child_guard_seconds=45,native_threads_one=True,total_children=len(observations),
                actual_semantic_rejections=36,
                max_observed_child_seconds=max(a['seconds'] for a in observations),
                peak_observed_child_RSS_KiB=max(a['runtime'].get('peak_RSS_KiB',0) for a in observations),
                no_mathematical_nonexistence_from_resource_status=True,
                ordinary_bridges_unformalized=True,independent_review=False,
                verification_run_does_not_publish_or_submit=True)
    (output/'VALIDATION.json').write_bytes(canonical(record)+b'\n')
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args()
    print(json.dumps(run(args.out)),flush=True)
