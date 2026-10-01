"""Serial reproducibility check; normal and optimized independent outputs agree."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--evidence-output',type=Path)
    args = parser.parse_args()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    outputs, jobs = [], []
    with tempfile.TemporaryDirectory(prefix='tammes23-review-') as tmp:
        for flags in ([],['-O']):
            complete = Path(tmp)/('optimized.json' if flags else 'normal.json')
            begin = time.monotonic()
            process = subprocess.run([sys.executable,'-B',*flags,str(HERE/'audit.py'),
                                      '--certificate',str(args.certificate),
                                      '--output',str(complete)],
                                     env=env,capture_output=True,text=True,timeout=180)
            if process.returncode:
                raise ValueError(process.stderr)
            outputs.append(json.loads(complete.read_text()))
            jobs.append({'optimized':bool(flags),'elapsed_seconds':time.monotonic()-begin,
                         'returncode':process.returncode,
                         'child_peak_rss_upper_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    if outputs[0] != outputs[1]:
        raise ValueError('normal/optimized independent outputs differ')
    if args.evidence_output:
        args.evidence_output.write_text(json.dumps(outputs[0],indent=2,sort_keys=True)+'\n')
    result = {'status':'VERIFIED','python':sys.version.split()[0],
              'normal_optimized_complete_evidence_agreement':True,
              'fixed_per_child_timeout_seconds':180,'math_jobs_parallel':1,
              'native_threads':1,'jobs':jobs,
              'complete_evidence_sha256':hashlib.sha256(json.dumps(outputs[0],sort_keys=True,
                                            separators=(',',':')).encode()).hexdigest()}
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
