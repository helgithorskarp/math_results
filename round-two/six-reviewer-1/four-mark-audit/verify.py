"""Validate sealed source before importing any mathematical module."""
import argparse,hashlib,json,os,runpy,sys
from pathlib import Path
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--output',type=Path)
p.add_argument('--fixture')
p.add_argument('--integrity-only',action='store_true')
args=p.parse_args()
seal=json.loads((root/'PRIMARY_SEAL.json').read_text())
for name,digest in seal['files'].items():
    if Path(name).name!=name or hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('pre-import source integrity: '+name)
if args.integrity_only:
    print(json.dumps({'source_integrity':True,'mathematics_executed':False}));raise SystemExit(0)
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:
    os.environ[key]='1'
sys.path.insert(0,str(root))
if args.fixture:
    sys.argv=[str(root/'damage.py'),args.fixture]
    runpy.run_path(str(root/'damage.py'),run_name='__main__')
else:
    if args.output is None or args.output.exists():raise ValueError('a fresh output path is required')
    sys.argv=[str(root/'check.py'),str(args.output.resolve())]
    runpy.run_path(str(root/'check.py'),run_name='__main__')
    raw=args.output.read_bytes();expected=json.loads((root/'EXPECTED.json').read_text())
    if len(raw)!=expected['whole_record_bytes']or hashlib.sha256(raw).hexdigest()!=expected['whole_record_sha256']:
        raise ValueError('complete mathematical record differs from published expectation')
