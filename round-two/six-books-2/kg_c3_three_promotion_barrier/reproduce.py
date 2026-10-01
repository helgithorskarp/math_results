"""Fresh or explicit resumable serial replay against a pre-existing fixture."""
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

ROOT=Path(__file__).resolve().parent


def run(command,env,work,stdout=None,deadline=30):
    try:
        result=subprocess.run(command,env=env,text=True,
                              stdout=stdout if stdout is not None else subprocess.PIPE,
                              stderr=subprocess.PIPE,timeout=deadline)
    except subprocess.TimeoutExpired:
        (work/'operational-limit.json').write_text(json.dumps(dict(
            status='OPERATIONAL_LIMIT',deadline_seconds=deadline,
            command=[str(x) for x in command],absence_inference=False),indent=2)+'\n')
        raise RuntimeError('unchanged operational deadline reached; saved partial output is not a proof')
    m.need(result.returncode==0,'child failed: '+result.stderr[-2000:])
    return result.stdout


def completed(path,first,total):
    expected=first;footer=None
    for line in path.open():
        z=json.loads(line)
        if z.get('segment'):
            m.need(footer is None,'duplicate phase footer')
            footer=z
        else:
            m.need(footer is None and type(z['index']) is int and z['index']==expected,
                   'phase case gap/overlap')
            expected+=1
    m.need(footer is not None and footer['first']==first and footer['next']==expected and
           footer['total']==total and footer['complete']==(expected==total) and expected>first,
           'phase is not a completed nonempty prefix')
    return footer


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--resume',action='store_true')
    args=ap.parse_args()
    start=time.monotonic();work=args.work.resolve();expected=ROOT/'expected.json'
    m.need(expected.is_file(),'frozen expected.json must pre-exist the replay')
    m.need(work!=ROOT and ROOT not in work.parents,'generated evidence must be outside source directory')
    work.mkdir(parents=True,exist_ok=True)
    m.need(args.resume or not list(work.iterdir()),'nonempty work directory requires explicit --resume')
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(ROOT.iterdir()) if p.is_file()}
    source_path=work/'source.json'
    if args.resume:
        m.need(source_path.is_file() and json.loads(source_path.read_text())==sources,
               'resume source/fixture hash mismatch')
        m.need(not (work/'operational-limit.json').exists(),
               'inspect recorded operational limit before resuming expensive work')
    else:
        source_path.write_text(json.dumps(sources,indent=2,sort_keys=True)+'\n')
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    for name in ('produce','independent'):
        run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',
             str(ROOT/(name+'.cpp')),'-o',str(work/name)],env,work)
    cases=work/'cases.txt'
    if not cases.exists():
        print(run([sys.executable,str(ROOT/'cases.py'),'--output',str(cases)],env,work),flush=True)
    fixture=json.loads(expected.read_text())
    m.need(hashlib.sha256(cases.read_bytes()).hexdigest()==fixture['case_manifest_sha256'],
           'case manifest differs from frozen complete domain')
    producer_files=sorted(work.glob('producer-*.jsonl'))
    critical_files=sorted(work.glob('critical-*.txt'))
    m.need({p.stem.replace('producer-','') for p in producer_files}==
           {p.stem.replace('critical-','') for p in critical_files},'producer/critical phase pairing')
    position=0
    for path in producer_files:
        m.need(int(path.stem.split('-')[-1])==position,'producer resume phase gap')
        position=completed(path,position,38313)['next']
    while position<38313:
        path=work/f'producer-{position:05}.jsonl';critical=work/f'critical-{position:05}.txt'
        with path.open('w') as out:
            run([str(work/'produce'),'--manifest',str(cases),'--critical',str(critical),
                 '--first',str(position),'--limit','38313','--seconds','25'],env,work,stdout=out)
        footer=completed(path,position,38313)
        position=footer['next'];print(json.dumps(dict(stage='producer',**footer)),flush=True)
    native_files=sorted(work.glob('native-*.jsonl'))
    metadata_files=sorted(work.glob('native-*.metadata.json'))
    m.need({p.name.replace('.jsonl','') for p in native_files}==
           {p.name.replace('.metadata.json','') for p in metadata_files},'native data/metadata pairing')
    position=0
    native_source=sources['independent.cpp']
    for path in native_files:
        m.need(int(path.stem.split('-')[-1])==position,'native resume phase gap')
        footer=completed(path,position,229075)
        meta=json.loads(path.with_name(path.stem+'.metadata.json').read_text())
        m.need(meta['segment']==footer and meta['source_sha256']==native_source,
               'native resume metadata/source mismatch')
        position=footer['next']
    while position<229075:
        path=work/f'native-{position:06}.jsonl';phase_start=time.monotonic()
        with path.open('w') as out:
            run([str(work/'independent'),'--first',str(position),'--limit','229075',
                 '--seconds','25'],env,work,stdout=out)
        footer=completed(path,position,229075)
        meta=dict(segment=footer,source_sha256=native_source,
                  wall_seconds=time.monotonic()-phase_start)
        path.with_name(path.stem+'.metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
        position=footer['next'];print(json.dumps(dict(stage='independent',**footer)),flush=True)
    for optimized,name in ((False,'normal'),(True,'optimized')):
        command=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/'check.py'),
                 '--work',str(work),'--output',str(work/f'check-{name}.json'),
                 '--expected',str(expected)]
        output=run(command,env,work)
        (work/f'check-{name}.log').write_text(output)
        print('checker',name,'complete',flush=True)
    normal=json.loads((work/'check-normal.json').read_text())
    optimized=json.loads((work/'check-optimized.json').read_text())
    m.need(normal==optimized,'normal/-O mathematical evidence differs')
    summary=dict(status='COMPLETE_FROZEN_REPLAY',fixture_preexisted=True,fixture_compared=True,
                 sources=sources,expected_sha256=sources['expected.json'],
                 seconds=time.monotonic()-start,
                 peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                 threads=1,case_phase_seconds=25,child_deadline_seconds=30,
                 versions=dict(python=sys.version.split()[0],
                               cpp=run(['g++','--version'],env,work,deadline=10).splitlines()[0]),
                 native_cases=normal['native_cases'],representatives=normal['representatives'],
                 blue_valid=normal['blue_valid'],damage_controls=normal['damage_controls'])
    (work/'manifest.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True),flush=True)


if __name__=='__main__':main()
