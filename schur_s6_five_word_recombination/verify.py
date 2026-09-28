"""Regenerate, independently audit, and DRAT-check the five-word exclusion."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from audit import audit
from encode import HERE, write


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cadical',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--strict-proof-hash',action='store_true')
    a=p.parse_args()
    expected=json.loads((HERE/'expected.json').read_text(encoding='ascii'))
    assert digest(HERE/'sources.json')==expected['sources_sha256']
    with tempfile.TemporaryDirectory(prefix='schur-five-recombine-') as tmp:
        cnf=Path(tmp)/'problem.cnf'
        proof=Path(tmp)/'proof.drat'
        write(cnf)
        audit(cnf)
        assert cnf.stat().st_size==expected['cnf_bytes']
        assert digest(cnf)==expected['cnf_sha256']
        solve=subprocess.run([str(a.cadical),'-q','--seed=20260928','-t','120',
                              str(cnf),str(proof)],capture_output=True,
                             text=True,timeout=180)
        assert solve.returncode==20,(solve.returncode,solve.stdout,solve.stderr)
        assert 's UNSATISFIABLE' in solve.stdout,solve.stdout
        checked=subprocess.run([str(a.drat_trim),str(cnf),str(proof)],
                               capture_output=True,text=True,timeout=180)
        assert checked.returncode==0,(checked.returncode,checked.stdout,checked.stderr)
        assert 's VERIFIED' in checked.stdout,checked.stdout
        proof_hash=digest(proof)
        reference_match=(proof_hash==expected['reference_proof_sha256']
                         and proof.stat().st_size==expected['reference_proof_bytes'])
        if a.strict_proof_hash:
            assert reference_match
        print(f'PASS DRAT_verified=yes cnf_sha256={digest(cnf)} '
              f'proof_sha256={proof_hash} proof_bytes={proof.stat().st_size} '
              f'reference_proof_match={reference_match}',flush=True)


if __name__=='__main__': main()
