"""Serial normal/optimized complete-evidence comparison under fixed guards."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--evidence-output',type=Path)
    args = parser.parse_args()
    environment = dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
                       MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    outputs,jobs = [],[]
    with tempfile.TemporaryDirectory(prefix='strip-review-') as tmp:
        for flags in ([],['-O']):
            path = Path(tmp)/('optimized.json' if flags else 'normal.json')
            begin = time.monotonic()
            process = subprocess.run([sys.executable,'-B',*flags,str(HERE/'audit.py'),
                                      '--input-dir',str(args.input_dir),'--output',str(path)],capture_output=True,text=True,
                                     timeout=60,env=environment)
            if process.returncode:
                raise ValueError(process.stderr)
            outputs.append(json.loads(path.read_text()))
            jobs.append({'optimized':bool(flags),'returncode':process.returncode,
                         'elapsed_seconds':time.monotonic()-begin,
                         'child_peak_RSS_upper_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    if outputs[0] != outputs[1]:
        raise ValueError('complete normal/optimized evidence differs')
    frozen_before=args.expected.exists()
    if frozen_before and json.loads(args.expected.read_text()) != outputs[0]:
        raise ValueError('complete frozen evidence differs')
    if not args.expected.exists() and not args.evidence_output:
        raise ValueError('missing frozen evidence; no unchecked pass')
    if args.evidence_output:
        args.evidence_output.write_text(json.dumps(outputs[0],indent=2,sort_keys=True)+'\n')
    digest = hashlib.sha256(json.dumps(outputs[0],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    record = {'status':'VERIFIED','python':sys.version.split()[0],
              'complete_normal_optimized_agreement':True,'complete_evidence_sha256':digest,
              'complete_frozen_evidence_agreement':frozen_before,
              'fixed_per_child_guard_seconds':60,'native_threads':1,
              'parallel_mathematical_jobs':1,'jobs':jobs}
    if args.output:
        args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))


if __name__ == '__main__':
    main()
