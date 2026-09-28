"""Regenerate and check the bare 110-point proof; Python stdlib, Linux/Unix."""
import argparse
import hashlib
import json
import resource
import subprocess
import tempfile
import time
from pathlib import Path

from prefix import encoding
from audit import audit


def instance():
    m, clauses = encoding(110)
    raw = ('p cnf %d %d\n' % (m['variables'],len(clauses)) +
           ''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)).encode()
    return m,clauses,raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cadical',required=True)
    parser.add_argument('--drat-trim',required=True)
    parser.add_argument('--seconds',type=int,default=300)
    parser.add_argument('--checker-seconds',type=int,default=300)
    parser.add_argument('--output',default='proof.generated.json')
    args = parser.parse_args()
    if args.seconds <= 0 or args.checker_seconds <= 0:
        parser.error('time limits must be positive')
    cadical = str(Path(args.cadical).resolve())
    checker = str(Path(args.drat_trim).resolve())
    audit(110)
    m, clauses, raw = instance()
    digest = hashlib.sha256(raw).hexdigest()
    recorded = json.loads((Path(__file__).parent/'certificate.json').read_text())
    assert digest == recorded['cnf_sha256']
    result = dict(endpoint=110,variables=m['variables'],clauses=len(clauses),
                  cnf_bytes=len(raw),cnf_sha256=digest,
                  external_schur_number_assumptions=[],status='UNKNOWN')
    cap = 512*1024*1024
    def limits():
        resource.setrlimit(resource.RLIMIT_FSIZE,(cap,cap))
    with tempfile.TemporaryDirectory(prefix='paired-prefix-') as directory:
        source, proof = Path(directory)/'instance.cnf',Path(directory)/'proof.drat'
        source.write_bytes(raw)
        start = time.monotonic()
        try:
            solved = subprocess.run([cadical,'-t',str(args.seconds),str(source),str(proof)],
                                    text=True,capture_output=True,
                                    timeout=args.seconds+15,preexec_fn=limits)
            result.update(solver_returncode=solved.returncode,
                          solver_seconds=time.monotonic()-start)
            if solved.returncode == 20 and 's UNSATISFIABLE' in solved.stdout:
                result.update(status='UNSAT_PROOF_NOT_VERIFIED',proof_bytes=proof.stat().st_size,
                              proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
                start = time.monotonic()
                checked = subprocess.run([checker,str(source),str(proof),'-i','-t',str(args.checker_seconds)],
                                         text=True,capture_output=True,
                                         timeout=args.checker_seconds+15)
                result.update(checker_returncode=checked.returncode,
                              checker_seconds=time.monotonic()-start)
                if checked.returncode == 0 and 's VERIFIED' in checked.stdout:
                    result['status'] = 'UNSAT_DRAT_VERIFIED'
            elif solved.returncode == 10:
                result['status'] = 'UNEXPECTED_SAT_REQUIRES_INVESTIGATION'
        except subprocess.TimeoutExpired:
            result['timeout'] = True
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if result['status'] != 'UNSAT_DRAT_VERIFIED':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
