"""Regenerate every case, obtain binary DRAT, and independently check it."""
from pathlib import Path
import argparse, hashlib, json, subprocess, time
from generate import generate
from verify import verify

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
p.add_argument('--kissat',type=Path,required=True);p.add_argument('--drat-trim',type=Path,required=True)
p.add_argument('--solver-seconds',type=int,default=120)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
finite=verify();expected=json.loads(Path(__file__).with_name('finite_expected.json').read_text())
assert finite==expected
results=[]
for case in range(5):
    stem=a.out/f'case{case}';cnf=stem.with_suffix('.cnf');proof=stem.with_suffix('.drat')
    item=generate(case,cnf);start=time.monotonic()
    with stem.with_suffix('.solver.log').open('w') as log:
        ret=subprocess.run([str(a.kissat.resolve()),f'--time={a.solver_seconds}',str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT)
    item.update(solver_exit_code=ret.returncode,solver_seconds=time.monotonic()-start)
    if ret.returncode!=20:raise RuntimeError(f'Case {case} not proved UNSAT; files retained')
    checklog=stem.with_suffix('.checker.log');start=time.monotonic()
    with checklog.open('w') as log:
        chk=subprocess.run([str(a.drat_trim.resolve()),str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT)
    if chk.returncode!=0 or 's VERIFIED' not in checklog.read_text():
        raise RuntimeError(f'Case {case} proof not verified')
    item.update(checker_exit_code=chk.returncode,checker_seconds=time.monotonic()-start,
                proof_sha256=sha(proof),proof_bytes=proof.stat().st_size,status='VERIFIED_UNSAT')
    results.append(item)
    (a.out/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
result={'status':'SPARSE_DIRECTION_EXCLUSION_VERIFIED','covered_flags':450,'cases':results,
        'kissat_sha256':sha(a.kissat),'drat_trim_sha256':sha(a.drat_trim)}
(a.out/'verified.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
