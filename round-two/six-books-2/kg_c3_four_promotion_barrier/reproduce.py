"""Serial empty-work replay, or explicit source-bound completed-phase resume.

Every native child is bounded to25 soft seconds and30 hard seconds. Full
entry comparison and all-positive checking have90-second guards fixed before
the cold run. A failed guard records an operational limit, not a theorem.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import model as m

HERE = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')


def barrier():
    state = Path('/scratch/research-team-sol61-six-20260929/state')
    for name in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json'):
        m.need(not (state/name).exists(), 'pause/handover barrier')


def source_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
            if p.is_file() and (p.suffix in ('.py','.cpp','.rows') or
                               p.name in ('expected.json','saturation-markers.json'))}


def run(argv,work,env,label,deadline):
    barrier()
    log = work/(label+'.stdout'); err = work/(label+'.stderr')
    try:
        with log.open('w') as out,err.open('w') as error:
            result = subprocess.run([str(x) for x in argv],env=env,stdout=out,stderr=error,timeout=deadline)
        m.need(result.returncode == 0, 'child failed: '+label+'; '+err.read_text()[-1500:])
    except (subprocess.TimeoutExpired,ValueError) as error:
        (work/'operational-limit.json').write_text(json.dumps(dict(status='INCOMPLETE_REPLAY',
            label=label,deadline_seconds=deadline,error=str(error),mathematical_nonexistence=False),indent=2)+'\n')
        raise


def completed(directory,prefix,total):
    next_index = 0
    for path in sorted(directory.glob(prefix+'-*.summary.json')):
        x = json.loads(path.read_text())
        m.need(x['first'] == next_index and next_index < x['next'] <= total, 'completed summary boundaries')
        next_index = x['next']
    return next_index


def main(args):
    started = time.monotonic(); barrier()
    work = args.work.resolve()
    m.need(work != HERE and HERE not in work.parents, 'work must be outside source')
    work.mkdir(parents=True,exist_ok=True)
    m.need(args.resume or not list(work.iterdir()), 'nonempty work needs explicit --resume')
    m.need(not (work/'operational-limit.json').exists(), 'inspect recorded operational limit; do not blindly resume')
    hashes = source_hashes(); snapshot = work/'sources.json'
    if args.resume:
        m.need(json.loads(snapshot.read_text()) == hashes, 'resume source or fixture drift')
    else: snapshot.write_text(json.dumps(hashes,indent=2,sort_keys=True)+'\n')
    env = dict(os.environ); env.update({k:'1' for k in THREADS})
    producer = work/'producer'; native = work/'native'
    producer.mkdir(exist_ok=True); native.mkdir(exist_ok=True)
    while not (producer/'join-34.metadata.json').exists():
        count = len(list(producer.glob('join-*.metadata.json')))
        run([sys.executable,HERE/'cases.py','--work',producer],work,env,'cases-'+str(count),30)
        print(json.dumps(dict(stage='case-blocks',next=len(list(producer.glob('join-*.metadata.json'))),total=35)),flush=True)
    if not (producer/'cases.json').exists():
        run([sys.executable,HERE/'cases.py','--work',producer,'--merge'],work,env,'case-merge',30)
    frozen = json.loads((HERE/'expected.json').read_text())
    m.need(hashlib.sha256((producer/'cases.txt').read_bytes()).hexdigest() == frozen['manifest_sha256'],
           'cold full manifest differs from frozen domain')
    for name,directory,total in (('producer',producer,305874),('native',native,1832600)):
        position = completed(directory,name,total)
        while position < total:
            run([sys.executable,HERE/(name+'_phase.py'),directory],work,env,name+'-phase-'+str(position),60)
            next_index = completed(directory,name,total)
            m.need(next_index > position, 'no completed case progress')
            print(json.dumps(dict(stage=name,first=position,next=next_index,total=total)),flush=True)
            position = next_index
    run([sys.executable,HERE/'compare.py','--native',native,'--producer',producer,
         '--output',work/'comparison.json'],work,env,'comparison',90)
    print('complete entrywise comparison',flush=True)
    for optimized,name in ((False,'normal'),(True,'optimized')):
        prefix = [sys.executable]+(['-O'] if optimized else [])
        run(prefix+[HERE/'saturation.py',producer],work,env,'saturation-'+name,30)
        report = json.loads((producer/'saturation-summary.json').read_text())
        (work/('saturation-'+name+'.json')).write_text(json.dumps(report,indent=2)+'\n')
        for key in ('counts','local_lemma_test','damage_rejections','markers_bytes','markers_sha256'):
            m.need(report[key] == frozen['saturation'][key], 'frozen saturation field: '+key)
        run(prefix+[HERE/'check.py','--work',work,'--output',work/('check-'+name+'.json')],
            work,env,'check-'+name,90)
        print('all-positive and saturation checks '+name+' complete',flush=True)
    m.need(json.loads((work/'check-normal.json').read_text()) ==
           json.loads((work/'check-optimized.json').read_text()), 'normal/-O mathematical evidence differs')
    m.need(source_hashes() == hashes, 'source drift during replay')
    phases = {}
    for name,directory in (('producer',producer),('native',native)):
        values = [json.loads(p.read_text()) for p in sorted(directory.glob(name+'-*.summary.json'))]
        phases[name] = dict(phases=len(values),next=values[-1]['next'],
            program_seconds=sum(x.get('program_seconds',x.get('boundary',{}).get('seconds',0)) for x in values),
            wrapper_seconds=sum(x.get('wall_seconds',x.get('seconds',0)) for x in values),
            peak_recorded_child_rss_kib=max(x['peak_child_rss_kib'] for x in values))
    result = dict(status='COMPLETE_EMPTY_WORK_FROZEN_P4_REPLAY',sources=hashes,
        expected_fixture_preexisted=True,seconds=time.monotonic()-started,threads=1,
        native_phase_soft_seconds=25,native_child_guard_seconds=30,full_check_guard_seconds=90,
        phases=phases,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        python=sys.version.split()[0],compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0])
    (work/'replay-summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--resume',action='store_true')
    main(ap.parse_args())
