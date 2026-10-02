#!/usr/bin/env python3
"""Rebuild every certificate locally in serial children with fixed20s guards."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();work=args.work.resolve();src=Path(__file__).resolve().parent
    if work.exists() and any(work.iterdir()):raise ValueError('Use a new empty private work directory')
    work.mkdir(parents=True,exist_ok=True)
    pins=json.loads((src/'SOURCE_PINS.json').read_text())
    for name,digest in pins['files'].items():
        if hashlib.sha256((src/name).read_bytes()).hexdigest()!=digest:raise ValueError('Changed source pin: '+name)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    stages=[];start=time.monotonic()
    record={'agent':'six-vdw-3','role':'researcher','child_guard_seconds':20,'threads':1,'stages':stages,'status':'RUNNING'}
    def save():
        record['elapsed_seconds']=time.monotonic()-start
        (work/'verification.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    def run(label,script,argv,flag=()):
        # The operation barrier is campaign-specific; outside it no barrier file is assumed.
        state_root=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
        if state_root and any((Path(state_root)/name).exists() for name in ('PAUSED.json','HANDOVER.json')):
            record['status']='OPERATIONS_BARRIER_STOPPED_INCOMPLETE';save();raise SystemExit(record['status'])
        began=time.monotonic()
        try:
            p=subprocess.run([sys.executable,*flag,str(src/script),*map(str,argv)],env=env,text=True,capture_output=True,timeout=20)
            stage={'label':label,'exit':p.returncode,'seconds':time.monotonic()-began,'stdout':p.stdout,'stderr':p.stderr}
        except subprocess.TimeoutExpired:
            stage={'label':label,'seconds':time.monotonic()-began,'status':'TIMEOUT_INCOMPLETE_NO_EXCLUSION'}
        stages.append(stage);save()
        if stage.get('exit')!=0:
            record['status']='FAILED_OR_INCOMPLETE_NO_MATHEMATICAL_EXCLUSION';save()
            raise SystemExit(json.dumps(stage))
    run('geometry-cover','cover.py',['--output',work/'cover.json'])
    cover=json.loads((work/'cover.json').read_text())
    for mode,flag in (('normal',()),('optimized',('-O',))):
        folder=work/mode;(folder/'core').mkdir(parents=True);(folder/'roots').mkdir()
        for i,t in enumerate(cover['geometries'],1):
            data=folder/'core'/f't{t:03}.json';checked=folder/'core'/f't{t:03}-check.json'
            run(f'{mode}:core{t}:generate','generate.py',['--t',t,'--output',data],flag)
            run(f'{mode}:core{t}:check','check.py',['--input',data,'--output',checked],flag)
            if i%10==0 or i==103:print(json.dumps({'mode':mode,'checked_geometries':i,'elapsed_seconds':time.monotonic()-start}),flush=True)
        run(mode+':field-transport','check_cover.py',['--cover',work/'cover.json','--data',folder/'core','--output',folder/'cover-check.json'],flag)
        for a in range(0,617,16):
            b=min(a+16,617);data=folder/'roots'/f'roots{a:03}-{b:03}.json';checked=folder/'roots'/f'roots{a:03}-{b:03}-check.json'
            run(f'{mode}:roots{a}-{b}:generate','complete_roots.py',['--start',a,'--stop',b,'--output',data],flag)
            run(f'{mode}:roots{a}-{b}:check','check_roots.py',['--input',data,'--output',checked],flag)
        run(mode+':known-seed','seed.py',['--output',folder/'seed.json'],flag)
        run(mode+':merge','merge.py',['--cover',work/'cover.json','--core',folder/'core','--roots',folder/'roots',
                                      '--transport',folder/'cover-check.json','--seed',folder/'seed.json',
                                      '--expected',src/'expected.json','--output',folder/'final.json'],flag)
        run(mode+':damages','damage.py',['--work',work,'--mode',mode,'--output',folder/'damage-check.json'],flag)
    paths=sorted(path.relative_to(work/'normal') for path in (work/'normal').rglob('*.json'))
    optimized=sorted(path.relative_to(work/'optimized') for path in (work/'optimized').rglob('*.json'))
    if paths!=optimized:raise ValueError('Different full mode inventories')
    for path in paths:
        if (work/'normal'/path).read_bytes()!=(work/'optimized'/path).read_bytes():raise ValueError('Whole mode record disagreement: '+str(path))
    for name,digest in pins['files'].items():
        if hashlib.sha256((src/name).read_bytes()).hexdigest()!=digest:raise ValueError('Source changed during replay: '+name)
    record.update({'status':'COMPLETE_PINNED_BOOLEAN617_SOURCE_REPLAY','mathematical_children':len(stages),
                   'whole_normal_optimized_record_pairs':len(paths),'whole_mode_bytes_equal':True,
                   'damages_rejected_each_mode':22,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   'final_record_sha256':hashlib.sha256((work/'normal/final.json').read_bytes()).hexdigest(),
                   'source_pin_manifest_sha256':hashlib.sha256((src/'SOURCE_PINS.json').read_bytes()).hexdigest()})
    save();print(json.dumps({k:v for k,v in record.items() if k!='stages'}),flush=True)


if __name__=='__main__':main()
