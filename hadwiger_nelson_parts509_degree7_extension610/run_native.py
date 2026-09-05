#!/usr/bin/env python3
"""Bounded proof-producing run, with every completed refutation checked."""
from pathlib import Path
from hashlib import sha256
import argparse,json,subprocess,time,resource

HERE=Path(__file__).resolve().parent



def main():
    ap=argparse.ArgumentParser();ap.add_argument('name')
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--solver',type=Path,required=True)
    ap.add_argument('--checker',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=300)
    args=ap.parse_args();name=args.name
    assert args.seconds>0 and Path(name).name==name
    work=args.work.resolve();solver=args.solver.resolve();checker=args.checker.resolve()
    path=work/f'{name}.cnf';proof=work/f'{name}.drat'
    assert path.exists() and not proof.exists()
    def limits():resource.setrlimit(resource.RLIMIT_AS,(4<<30,4<<30))
    t=time.monotonic()
    with (work/f'{name}_solver.log').open('w') as f:
        result=subprocess.run([str(solver),f'--time={args.seconds}',str(path),str(proof)],stdout=f,stderr=subprocess.STDOUT,preexec_fn=limits)
    facts=dict(name=name,solver_sha256=sha256(solver.read_bytes()).hexdigest(),
               checker_sha256=sha256(checker.read_bytes()).hexdigest(),solver_exit_code=result.returncode,solver_wall_seconds=time.monotonic()-t,
               cnf_sha256=sha256(path.read_bytes()).hexdigest(),proof_bytes=proof.stat().st_size,
               proof_sha256=sha256(proof.read_bytes()).hexdigest(),negative_independently_verified=False)
    assert result.returncode in (0,10,20),facts
    if result.returncode==20:
        t=time.monotonic()
        check=subprocess.run([str(checker),str(path),str(proof)],capture_output=True,text=True)
        (work/f'{name}_checker.log').write_text(check.stdout+check.stderr)
        assert check.returncode==0 and 's VERIFIED' in check.stdout
        facts.update(checker_exit_code=check.returncode,checker_wall_seconds=time.monotonic()-t,
                     negative_independently_verified=True)
    facts['maximum_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    (work/f'{name}_native.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2),flush=True)


if __name__=='__main__':main()
