"""One bounded invocation on the full rank-at-most-eight branch."""
from pathlib import Path
import hashlib
import json
import resource
import subprocess
import sys
import time
from witness import verify
from counter import require

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(12<<30,12<<30))
    resource.setrlimit(resource.RLIMIT_FSIZE,(4<<30,4<<30))

def main():
    out=Path(sys.argv[1]);solver=Path(sys.argv[2]);drat=Path(sys.argv[3])
    require(not(out/'SOLVER_STARTED.json').exists(),'prior target invocation exists; reconcile it, never retry')
    cnf=out/'input.cnf';proof=out/'proof.drat'
    expected=json.loads((Path(__file__).resolve().parent/'PREPARATION.json').read_text())
    require(hashlib.sha256(cnf.read_bytes()).hexdigest()==expected['cnf_sha256'],'full branch input hash')
    command=[str(solver),'-c','1000000','-t','600','--seed=0',str(cnf),str(proof)]
    before=time.monotonic()
    with (out/'solver.log').open('wb') as stream:
        p=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,preexec_fn=limits)
        (out/'SOLVER_STARTED.json').write_text(json.dumps({'pid':p.pid,'command':command,'started_unix':time.time()},indent=2)+'\n')
        print('single target solver PID',p.pid,flush=True)
        try:rc=p.wait(timeout=610)
        except subprocess.TimeoutExpired:p.kill();p.wait();rc='PARENT_WALL_LIMIT'
    result={'solver_returncode':rc,'solver_wall_seconds':time.monotonic()-before,
            'family_status':'UNKNOWN','gate_pass':False,'good43_found':False,
            'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest()}
    log=(out/'solver.log').read_text(errors='replace')
    if rc==10 and 's SATISFIABLE' in log:
        chosen=[]
        for line in log.splitlines():
            if line.startswith('v '):chosen.extend(x for x in map(int,line[2:].split()) if 1<=x<=255)
        chosen=sorted(set(chosen));require(len(chosen)>=43,'SAT coordinate cardinality')
        coordinates=chosen[:43]
        physical=verify(coordinates)
        (out/'TARGET.json').write_text(json.dumps({'coordinates':coordinates,'physical':physical},indent=2)+'\n')
        result.update(family_status='SAT_PHYSICAL_GOOD43',gate_pass=True,good43_found=True)
    elif rc==20 and 's UNSATISFIABLE' in log:
        with (out/'proof-check.log').open('wb') as stream:
            try:q=subprocess.run([str(drat),str(cnf),str(proof),'-i','-t','600'],stdout=stream,stderr=subprocess.STDOUT,timeout=610,preexec_fn=limits);check_rc=q.returncode
            except subprocess.TimeoutExpired:check_rc='CHECKER_WALL_LIMIT'
        result['proof_check_returncode']=check_rc
        if check_rc==0 and b's VERIFIED' in (out/'proof-check.log').read_bytes():
            result.update(family_status='UNSAT_CERTIFIED',gate_pass=True)
        else:result['family_status']='SOLVER_UNSAT_UNCERTIFIED'
    if proof.exists():
        digest=hashlib.sha256()
        with proof.open('rb') as f:
            for block in iter(lambda:f.read(1<<20),b''):digest.update(block)
        result.update(proof_bytes=proof.stat().st_size,proof_sha256=digest.hexdigest())
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)

if __name__=='__main__':main()
