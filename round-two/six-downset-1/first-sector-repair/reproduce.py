"""Serial source-only normal/O/isolated-cold gates, without old cap replay.

six-downset-1 / researcher. Same-author reproducibility, not independent review.
One intensive child at a time, native1, each unchanged60s/32MiB/N80 guard.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
EARLY=('geometry.py','upper_reader.py','shift_reader.py','symbolic.py',
       'reader.py','adverse.py','reproduce.py','PROOF.md','README.md',
       'DEPENDENCIES.json','PROVENANCE.json')


def require(ok,message):
    if not ok:
        raise ValueError(message)


def barrier():
    state=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state)/name).exists() for name in
                ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')


def bind(raw):
    return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    barrier();require(not out.exists(),'unique source-only output')
    pins=json.loads((HERE/'SOURCE.json').read_bytes())
    require(set(pins['early'])==set(EARLY),'whole early source census')
    frozen={name:(HERE/name).read_bytes() for name in EARLY+('SOURCE.json','EXPECTED.json')}
    require(all(bind(frozen[name])==pins['early'][name] for name in EARLY),
            'whole source before any child')
    out.mkdir(parents=True)
    cold=out/'cold-source';cold.mkdir()
    for name,raw in frozen.items():
        (cold/name).write_bytes(raw)
    env=dict(os.environ);children=[];lanes=[];math=None;adverse=None
    def child(source,optimized,argv,expect_error=None):
        barrier()
        require(all((HERE/name).read_bytes()==raw for name,raw in frozen.items()),
                'whole frozen source before child')
        command=[sys.executable,'-I']+(['-O'] if optimized else [])+[str(source),*argv]
        started=time.monotonic()
        try:
            result=subprocess.run(command,cwd=out,env=env,capture_output=True,text=True,timeout=60)
        except subprocess.TimeoutExpired:
            raise TimeoutError('unchanged60s; incomplete is not mathematical nonexistence') from None
        receipt=dict(child=len(children)+1,source=source.name,cold=source.parent==cold,
                     optimized=optimized,expected_error=expect_error,
                     returncode=result.returncode,seconds=time.monotonic()-started,
                     stdout=result.stdout,stderr=result.stderr)
        children.append(receipt)
        (out/'CHILDREN.json').write_text(json.dumps(children,indent=2)+'\n')
        if expect_error:
            require(result.returncode!=0 and expect_error in result.stderr,
                    'designated source binding/semantic child rejection')
            require('UNBOUND_MODULE_EXECUTED' not in result.stderr,
                    'source rejection before unbound module executes')
        else:
            require(result.returncode==0,'actual reader/adverse child failure; inspect CHILDREN')
        require(all((HERE/name).read_bytes()==raw for name,raw in frozen.items()),
                'whole frozen source after child')
        print(json.dumps(dict(child=receipt['child'],source=source.name,optimized=optimized,
                              cold=receipt['cold'],seconds=receipt['seconds'],
                              passed=True,expected_rejection=bool(expect_error))),flush=True)
    for label,source,optimized in [('normal',HERE,False),('optimized',HERE,True),('cold',cold,False)]:
        lane=out/label;lane.mkdir()
        mathematical=lane/'MATHEMATICS.json';negative=lane/'ADVERSE.json'
        child(source/'reader.py',optimized,['--out',str(mathematical)])
        child(source/'adverse.py',optimized,['--out',str(negative)])
        record,damages=mathematical.read_bytes(),negative.read_bytes()
        require(len(record)<=32*1024*1024 and len(damages)<=32*1024*1024,'whole32MiB records')
        if math is None:
            math,adverse=record,damages
        else:
            require(record==math and damages==adverse,
                    'ENTIRE normal/O/cold mathematical and semantic bytes BEFORE digest')
        require(record==frozen['EXPECTED.json'],'whole reader-facing compact EXPECTED bytes')
        lanes.append(dict(name=label,whole_mathematics=bind(record),whole_adverse=bind(damages)))
    for name in ['geometry.py','upper_reader.py','shift_reader.py','symbolic.py']:
        damaged=out/('source-damage-'+name);damaged.mkdir()
        for filename,raw in frozen.items():(damaged/filename).write_bytes(raw)
        with (damaged/name).open('a') as file:
            file.write("\nraise RuntimeError('UNBOUND_MODULE_EXECUTED')\n")
        child(damaged/'reader.py',False,['--out',str(damaged/'never.json')],
              'source pin mismatch '+name)
    # A rebound arithmetic defect is separate from a stale source binding.
    damaged=out/'rebound-symbolic-defect';damaged.mkdir()
    for filename,raw in frozen.items():(damaged/filename).write_bytes(raw)
    before='3 * k * h * h * (delta + t * (2 * q + 6 * k - t))'
    after='3 * k * h * h * (delta + t * (2 * q + 5 * k - t))'
    text=(damaged/'symbolic.py').read_text();require(text.count(before)==1,'designated generic formula defect')
    (damaged/'symbolic.py').write_text(text.replace(before,after))
    changed=json.loads(frozen['SOURCE.json']);changed['early']['symbolic.py']=bind((damaged/'symbolic.py').read_bytes())
    (damaged/'SOURCE.json').write_text(json.dumps(changed,sort_keys=True,separators=(',',':'))+'\n')
    child(damaged/'reader.py',False,['--out',str(damaged/'never.json')],
          'generic polynomial identity whole shifted light W inverse numerator')
    report=dict(agent='six-downset-1',role='researcher',status='COMPLETE SOURCE-ONLY DELIVERY GATES',
                actual_children=len(children),valid_readers=3,adverse_reader_children=3,
                source_before_import_rejections=4,rebound_generic_semantic_rejections=1,
                semantic_rejections_per_lane=json.loads(adverse)['rejection_count'],
                mathematical_rejections_per_lane=json.loads(adverse)['mathematical_rejections'],
                preflight_rejections_per_lane=json.loads(adverse)['preflight_rejections'],
                lanes=lanes,source_pins=pins,whole_source_unchanged=True,
                whole_mathematics=bind(math),whole_adverse=bind(adverse),
                max_child_seconds=max(row['seconds'] for row in children),
                new_source_commit=None,new_graph_ref=None,formalized=False,independent_review=False,
                no_old_cap_checker_factor_or_private_corpus_imported=True,
                credited_geometry_program_is_verbatim_b7d=True,large_original_constructed=False)
    (out/'MATHEMATICS.json').write_bytes(math);(out/'ADVERSE.json').write_bytes(adverse)
    (out/'GATES.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','actual_children','semantic_rejections_per_lane',
                                                'whole_mathematics','max_child_seconds')}))


if __name__=='__main__':
    main()
