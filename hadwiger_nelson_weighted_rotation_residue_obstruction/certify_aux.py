"""Regenerate and independently check the auxiliary two-distance UNSAT proof."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time
from exact import points, require
from verify import auxiliary

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output',help='transient directory outside the repository')
    parser.add_argument('--kissat',default='kissat')
    parser.add_argument('--drat-trim',default='drat-trim')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True,exist_ok=True)
    _,cnf,_ = auxiliary(points())
    inp,proof = output/'augmented114.cnf',output/'augmented114.drat'
    inp.write_text(cnf)
    t = time.monotonic()
    with (output/'kissat.log').open('w') as f:
        solved = subprocess.run([args.kissat,str(inp),str(proof)],
                                stdout=f,stderr=subprocess.STDOUT,timeout=60)
    require(solved.returncode == 20, 'auxiliary solver did not return UNSAT')
    solver_seconds = time.monotonic()-t
    t = time.monotonic()
    with (output/'drat-trim.log').open('w') as f:
        checked = subprocess.run([args.drat_trim,str(inp),str(proof)],
                                 stdout=f,stderr=subprocess.STDOUT,timeout=60)
    require(checked.returncode == 0 and 's VERIFIED' in (output/'drat-trim.log').read_text(),
            'DRAT verification failed')
    print(json.dumps({'claim':'auxiliary TWO-DISTANCE graph is not four-colourable',
                      'cnf_sha256':sha256(inp.read_bytes()).hexdigest(),
                      'proof_sha256':sha256(proof.read_bytes()).hexdigest(),
                      'proof_bytes':proof.stat().st_size,'drat_status':'VERIFIED',
                      'solver_seconds':solver_seconds,
                      'checker_seconds':time.monotonic()-t},indent=2))
