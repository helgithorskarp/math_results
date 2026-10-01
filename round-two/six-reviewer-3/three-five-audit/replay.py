"""Replay the independent finite audit, comparing all bytes to its receipt."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    root=Path(__file__).absolute().parent
    fixture=args.fixture or root/'EXPECTED.json'
    expected=fixture.read_bytes();runs=[]
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
             NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1',
             PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='three-five-audit-') as folder:
        for flags in ([],['-O']):
            out=Path(folder)/'evidence.json';start=time.monotonic()
            result=subprocess.run([sys.executable,'-B',*flags,str(root/'audit.py'),'--output',str(out)],
                                  capture_output=True,env=env,timeout=60)
            if result.returncode or out.read_bytes()!=expected:
                raise ValueError('independent audit failed or complete expected bytes differ: '+result.stderr.decode())
            runs.append({'optimized':bool(flags),'seconds':time.monotonic()-start,
                         'complete_frozen_receipt_match':True})
    evidence=json.loads(expected)
    record={'status':'VERIFIED','actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'full_file_sha256':hashlib.sha256(expected).hexdigest(),'runs':runs,
            'raw_labeled_rows':sum(x['raw_ordered_three_neighbor_triples'] for x in evidence['censuses']),
            'mathematical_negative_controls':evidence['damaged_controls'],
            'trust':'This replays exact finite evidence; written geometric and coverage bridges are in REVIEW.md'}
    if args.output:args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))


if __name__=='__main__':main()
