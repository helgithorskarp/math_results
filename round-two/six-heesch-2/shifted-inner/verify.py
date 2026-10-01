"""Regenerate a bounded SAT proof, then check it without a solver library."""
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Timer
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from model import Model,BASE
from inverse import reconstructed
from check_geometry import check_coronas


def require(condition,message):
    if not condition:raise RuntimeError(message)


def main():
    require(__debug__,'Run with assertions enabled.')
    import pysat
    from pysat.solvers import Solver
    start=time.monotonic()
    expected=json.loads((HERE/'expected.json').read_text())
    control=Model(1,2)
    control.preflight();true=control.known_seed_assignment()
    for clause in control.clauses():
        require(any((v in true) if v>0 else (-v not in true) for v in clause),'Seed assignment violates a compiled clause.')
    tile,placements,_,_,_=control.decode(true)
    control_stats,_,_=check_coronas(tile,placements,False)
    require(control_stats==expected['seed_control'],'Seed control changed.')
    model=reconstructed(2,2);stats=model.preflight()
    require(all(stats[k]==v for k,v in expected['instance'].items()),'Canonical finite instance changed.')
    scratch=HERE/'scratch';scratch.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix='proof-',dir=scratch) as name:
        temp=Path(name);cnf=temp/'instance.cnf';proof=temp/'additions.rup';core=temp/'core.rup'
        digest=hashlib.sha256()
        with cnf.open('w') as out:
            out.write(f"p cnf {stats['total_variables']} {stats['clauses']}\n")
            for clause in model.clauses():
                row=' '.join(map(str,clause))+' 0\n';out.write(row);digest.update(row.encode())
        require(digest.hexdigest()==stats['cnf_sha256'],'Written inverse instance changed.')
        binary=temp/'rup_audit'
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',
                        str(HERE/'rup_audit.cpp'),'-o',str(binary)],check=True,timeout=30)
        controls=json.loads(subprocess.check_output([str(binary),'--self-test'],text=True,timeout=10))
        require(controls['exhaustive_controls']==2304,'RUP controls incomplete.')
        with Solver(name='g4',with_proof=True) as solver:
            for clause in model.clauses():solver.add_clause(clause)
            solver.conf_budget(100000);timer=Timer(40,solver.interrupt);timer.start()
            try:status=solver.solve_limited(expect_interrupt=True)
            finally:timer.cancel();solver.clear_interrupt()
            require(status is False,'No negative theorem: solver returned SAT, UNKNOWN or an incomplete result.')
            raw=solver.get_proof()
            additions=[line for line in raw if not line.startswith('d ')]
            proof.write_text('\n'.join(additions)+'\n')
        checked=json.loads(subprocess.check_output([str(binary),str(cnf),str(proof),str(core)],text=True,timeout=125))
        require(checked['complete'] is True,'Native RUP audit incomplete.')
        replay=json.loads(subprocess.check_output([str(binary),str(cnf),str(core),str(temp/'replayed.rup')],text=True,timeout=125))
        require(replay['complete'] is True,'Fresh RUP replay incomplete.')
        require(checked['input_variables']==stats['total_variables'] and checked['input_clauses']==stats['clauses'],'Audit instance mismatch.')
        result={'agent':'six-heesch-2','role':'researcher','claim':'The specified anchored factor-two shifted network cannot form two complete coronas.',
                'scope':'199-cell pool; root plus five and eleven designated copies; seven translation offsets per nonroot copy.',
                'status':'Verified finite necessary-constraint obstruction','instance':stats,
                'seed_control':control_stats,'geometric_incidence_check':'Forward and inverse entries agree exactly.',
                'pysat_version':pysat.__version__,'solver':'Glucose4','proof_additions':len(additions),
                'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
                'checked':checked,'fresh_replay':replay,'checker_controls':controls,
                'seconds':round(time.monotonic()-start,3),
                'parent_max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                'child_max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':main()
