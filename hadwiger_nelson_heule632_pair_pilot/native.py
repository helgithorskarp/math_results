"""Bounded native calls; full logs/proofs stay in the chosen local directory."""
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time

HERE=Path(__file__).resolve().parent


def limits():
    plan=json.loads((HERE/'plan.json').read_text())['limits']
    resource.setrlimit(resource.RLIMIT_AS,(plan['address_space_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(plan['proof_file_bytes'],)*2)


def call(executable,args,log,timeout):
    start=time.monotonic()
    with log.open('wb') as stream:
        try:
            p=subprocess.run([str(executable),*map(str,args)],stdout=stream,stderr=subprocess.STDOUT,timeout=timeout,preexec_fn=limits)
            code=p.returncode
        except subprocess.TimeoutExpired:code=None
    return {'exit_code':code,'seconds':time.monotonic()-start,'max_child_rss_so_far_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}


def solve(kissat,cnf,proof,log):
    plan=json.loads((HERE/'plan.json').read_text());info=call(kissat,plan['solver']['options']+[str(cnf),str(proof)],log,plan['limits']['solver_outer_wall_seconds'])
    text=log.read_text(errors='replace')
    status='SAT' if info['exit_code']==10 and 's SATISFIABLE' in text.splitlines() else 'UNSAT' if info['exit_code']==20 and 's UNSATISFIABLE' in text.splitlines() else 'UNKNOWN'
    info.update(status=status,proof_bytes=proof.stat().st_size if proof.exists() else 0)
    return info


def check_proof(checker,cnf,proof,log):
    plan=json.loads((HERE/'plan.json').read_text());info=call(checker,[cnf,proof,*plan['proof_checker']['options']],log,plan['limits']['checker_outer_wall_seconds'])
    text=log.read_text(errors='replace');info['verified']=info['exit_code']==0 and 's VERIFIED' in text.splitlines()
    if proof.exists():info.update(proof_bytes=proof.stat().st_size,proof_sha256=sha256(proof.read_bytes()).hexdigest())
    return info
