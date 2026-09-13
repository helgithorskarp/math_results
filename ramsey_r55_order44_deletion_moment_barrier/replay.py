"""Regenerate the full specified system and compare exact compact evidence."""
from pathlib import Path
import argparse,hashlib,json,time
from build import build_all
from verify import check,require

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--work-dir',type=Path,required=True)
    ap.add_argument('--validate-counting',action='store_true')
    args=ap.parse_args()
    source=Path(__file__).resolve().parent
    work=args.work_dir.resolve()
    require(not work.exists(),'Use a fresh work directory.')
    require(not work.is_relative_to(source.parent),'Work directory must be outside the repository.')
    work.mkdir(parents=True)
    started=time.monotonic()
    build_all(work)
    result=check(work,source/'exact_density.json')
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    require(result==json.loads((source/'EXPECTED.json').read_text()),'exact replay mismatch')
    if args.validate_counting:
        import validate
        validate.run(work/'counting_validation.json')
        value=json.loads((work/'counting_validation.json').read_text())
        expected=json.loads((source/'EXPECTED_COUNTING.json').read_text())
        value.pop('seconds');expected.pop('seconds')
        require(value==expected,'direct counting mismatch')
    out={'status':'EXACT_JOINT_DELETION_REPLAY_MATCH','seconds':time.monotonic()-started,
         'certificate_sha256':hashlib.sha256((source/'exact_density.json').read_bytes()).hexdigest(),
         'terminal_order44_classes_closed':0,'verified_good44_graphs':0}
    (work/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__=='__main__':
    main()
