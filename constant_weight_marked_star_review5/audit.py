"""Cold, one-process independent replay. All generated data require new scratch."""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import platform
import resource
import time
from marked import canonical,require,Incomplete
from audit_raw import run
from classify import classify,unique_object
from controls import controls
from bridge import bridge

THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
         'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def compact(raw,classification,tests,arithmetic):
    census={k:v for k,v in raw.items() if k not in ('nodes','packings')}
    cls={k:v for k,v in classification.items() if k!='maps_from_each_raw_positive'}
    cls['raw_positive_map_count_distribution']={str(n):classification['maps_from_each_raw_positive'].count(n)
                                             for n in sorted(set(classification['maps_from_each_raw_positive']))}
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',
                census=census,classification=cls,controls=tests,arithmetic_and_fixtures=arithmetic)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--controls-only',action='store_true');args=parser.parse_args()
    here=Path(__file__).resolve().parent;work=args.work.resolve()
    require(work!=here and here not in work.parents,'scratch must be outside source directory')
    require(not work.exists(),'work directory must be new');work.mkdir(parents=True)
    for name in THREADS:require(os.environ.get(name)=='1','set '+name+'=1')
    started=time.monotonic()
    expected=json.loads((here/'expected.json').read_text(),object_pairs_hook=unique_object)
    inputs=json.loads((here/'INPUT.json').read_text(),object_pairs_hook=unique_object)
    target=inputs['target_fixture']
    require(sha256(canonical(target)).hexdigest()==inputs['canonical_target_data_sha256'],'target fixture data mismatch')
    try:
        if args.controls_only:
            ref=tuple(tuple(q) for q in expected['classification']['own_reference'])
            tests=controls(ref);arithmetic=bridge(ref,target)
            require(canonical(tests)==canonical(expected['controls']) and canonical(arithmetic)==canonical(expected['arithmetic_and_fixtures']),
                    'normal/optimized controls mismatch')
            result=dict(status='COMPLETE',scope='controls and literal fixtures only',controls=tests,arithmetic_and_fixtures=arithmetic)
        else:
            raw=run();(work/'raw.json').write_bytes(canonical(raw))
            cls=classify(raw,target);tests=controls(tuple(tuple(q) for q in cls['own_reference']))
            arithmetic=bridge(tuple(tuple(q) for q in cls['own_reference']),target)
            result=compact(raw,cls,tests,arithmetic)
            require(canonical(result)==canonical(expected),'cold result differs from compact expected record')
        (work/'result.json').write_bytes(canonical(result))
        record=dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',
                    scope=result.get('scope','all1001 labelled cases, full classification, controls and coding arithmetic'),
                    python=platform.python_version(),python_optimized=not __debug__,
                    elapsed_seconds=time.monotonic()-started,peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                    result_bytes=len(canonical(result)),result_sha256=sha256(canonical(result)).hexdigest())
        (work/'run.json').write_bytes(canonical(record));print(json.dumps(record,indent=2))
    except Incomplete as error:
        record=dict(status='INCOMPLETE',reason=str(error));(work/'run.json').write_bytes(canonical(record))
        print(json.dumps(record));raise SystemExit(3)

if __name__=='__main__':main()
