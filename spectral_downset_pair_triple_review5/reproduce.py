"""One-process independent cold replay; all generated records stay in scratch."""
from hashlib import sha256
from pathlib import Path
import argparse,json,os,platform,resource,time
from exact import canonical,require
from audit import run as audit
from controls import run as controls

def unique(items):
    out={}
    for key,value in items:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
    here=Path(__file__).resolve().parent;work=args.work.resolve()
    require(work!=here and here not in work.parents and not work.exists(),'new scratch outside source required')
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):require(os.environ.get(name)=='1','set '+name+'=1')
    work.mkdir(parents=True);started=time.monotonic()
    inp=json.loads((here/'INPUT.json').read_text(),object_pairs_hook=unique)
    require(sha256(canonical(inp['target_fixture'])).hexdigest()==inp['canonical_fixture_sha256'],'target fixture changed')
    result=dict(audit=audit(inp['target_fixture']),controls=controls())
    expected=json.loads((here/'expected.json').read_text(),object_pairs_hook=unique)
    require(canonical(result)==canonical(expected),'independent result differs from compact expected')
    (work/'result.json').write_bytes(canonical(result))
    record=dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',
                python=platform.python_version(),python_optimized=not __debug__,elapsed_seconds=time.monotonic()-started,
                peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                result_bytes=len(canonical(result)),result_sha256=sha256(canonical(result)).hexdigest(),
                author_executable_imported=False,dense_full_slack_eliminations=0)
    (work/'run.json').write_bytes(canonical(record));print(json.dumps(record,indent=2))
