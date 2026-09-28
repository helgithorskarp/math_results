"""Audit all cases and independently DRAT-check the certified union."""
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
    p.add_argument('--kissat',type=Path,required=True)
    p.add_argument('--drat-trim',type=Path,required=True)
    p.add_argument('--strict-proof-hash',action='store_true')
    a=p.parse_args()
    expected=json.loads((HERE/'expected.json').read_text(encoding='ascii'))
    assert digest(HERE/'sources.json')==expected['sources_sha256']
    assert digest(HERE/'cases.json')==expected['cases_sha256']
    assert set(expected['cases'])=={'two_347_alignments',
                                   'three_347_alignments_zero_fixed',
                                   'three_347_alignments_wide'}
    with tempfile.TemporaryDirectory(prefix='schur-multi-align-') as tmp:
        for case,reference in expected['cases'].items():
            cnf=Path(tmp)/(case+'.cnf')
            write(case,cnf)
            facts=audit(case,cnf)
            for key,value in facts.items(): assert value==reference[key],(case,key)
            assert cnf.stat().st_size==reference['cnf_bytes']
            assert digest(cnf)==reference['cnf_sha256']
            print(f'MATCH case={case} cnf_sha256={digest(cnf)}',flush=True)
            if reference['status']!='certified_unsat': continue
            proof=Path(tmp)/(case+'.drat')
            solve=subprocess.run([str(a.kissat),'--unsat','--seed=20260928',
                                  '--time=180',str(cnf),str(proof)],
                                 capture_output=True,text=True,timeout=240)
            assert solve.returncode==20,(case,solve.returncode,solve.stdout[-1000:])
            assert 's UNSATISFIABLE' in solve.stdout
            checked=subprocess.run([str(a.drat_trim),str(cnf),str(proof)],
                                   capture_output=True,text=True,timeout=240)
            assert checked.returncode==0,(case,checked.returncode,checked.stdout[-1000:])
            assert 's VERIFIED' in checked.stdout
            proof_hash=digest(proof)
            reference_match=(proof_hash==reference['reference_proof_sha256']
                             and proof.stat().st_size==reference['reference_proof_bytes'])
            if a.strict_proof_hash: assert reference_match
            print(f'PASS case={case} DRAT_verified=yes proof_sha256={proof_hash} '
                  f'proof_bytes={proof.stat().st_size} '
                  f'reference_proof_match={reference_match}',flush=True)
    print('PASS certified_cases=1 open_cases=2 exact_cnf_audits=3',flush=True)


if __name__=='__main__': main()
