"""Run Kissat on the full 537 CNF; independently check any SAT model."""
import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

from audit import audit
from check import defects
from encode import write

HERE = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=('plain','rgs'), default='rgs')
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path)
    p.add_argument('--seconds', type=int, default=300)
    p.add_argument('--seed', type=int, default=20260930)
    p.add_argument('--out', type=Path, default=Path('/tmp/schur-six-537-word.txt'))
    a = p.parse_args()
    assert a.seconds > 0 and a.seed >= 0
    expected = json.loads((HERE/'expected.json').read_text(encoding='ascii'))
    with tempfile.TemporaryDirectory(prefix='schur-six-full537-') as temp:
        cnf = Path(temp)/'case.cnf'
        proof = Path(temp)/'case.drat'
        log = Path(temp)/'solver.log'
        info = write(cnf,a.mode)
        assert info == expected[a.mode]['cnf']
        audit(cnf,a.mode)
        cmd = [str(a.kissat),'--sat',f'--time={a.seconds}',
               f'--seed={a.seed}',str(cnf)]
        if a.drat_trim:cmd.append(str(proof))
        start = time.monotonic()
        with log.open('w',encoding='ascii') as output:
            result = subprocess.run(cmd,stdout=output,stderr=subprocess.STDOUT,
                                    check=False)
        elapsed = round(time.monotonic()-start,2)
        content = log.read_text(encoding='ascii')
        if result.returncode == 10 and 's SATISFIABLE' in content:
            positive = {int(t) for line in content.splitlines() if line.startswith('v ')
                        for t in line.split()[1:] if int(t)>0}
            word = ''.join(str(next(c for c in range(1,7)
                                    if 6*(v-1)+c in positive))
                           for v in range(1,538))
            bad = defects(word)
            assert not bad,bad
            a.out.write_text(word+'\n',encoding='ascii')
            print('VERIFIED_537',f'mode={a.mode}',f'seconds={elapsed}',
                  f'word_sha256={hashlib.sha256((word+chr(10)).encode()).hexdigest()}',
                  f'out={a.out}')
        elif result.returncode == 20 and 's UNSATISFIABLE' in content:
            if not a.drat_trim:
                print('UNVERIFIED_UNSAT; rerun with --drat-trim',
                      f'mode={a.mode}',f'seconds={elapsed}')
                return
            checked = subprocess.run([str(a.drat_trim),str(cnf),str(proof)],
                                     capture_output=True,text=True,check=False)
            if checked.returncode != 0 or 's VERIFIED' not in checked.stdout:
                raise RuntimeError(f'DRAT checker rejected proof: {checked.stdout} {checked.stderr}')
            print('CERTIFIED_UNSAT',f'mode={a.mode}',f'seconds={elapsed}',
                  f'proof_sha256={hashlib.sha256(proof.read_bytes()).hexdigest()}')
        elif result.returncode == 0 and 'UNKNOWN' in content:
            print('UNKNOWN',f'mode={a.mode}',f'seconds={elapsed}',
                  f'seed={a.seed}',f'time_limit={a.seconds}')
        else:
            raise RuntimeError(f'unexpected solver exit {result.returncode}: '
                               +content[-2000:])


if __name__ == '__main__':main()
