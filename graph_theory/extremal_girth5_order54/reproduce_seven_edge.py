#!/usr/bin/env python3
"""Regenerate all 50 incidence cases and independently check every refutation."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
from seven_edge_sat import build, motifs
from verify_seven_edge import coverage, controls

HERE=Path(__file__).resolve().parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--checker',type=Path,required=True)
    ap.add_argument('--conflicts',type=int,default=100000);args=ap.parse_args()
    work=args.work.resolve();checker=args.checker.resolve()
    if work.is_relative_to(HERE.parents[1]):raise ValueError('generated files must be outside the repository')
    if not checker.is_file():raise ValueError('DRAT-trim executable missing')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    validation={'coverage':coverage(),'controls':controls()}
    expected={r['case']:r for r in json.loads((HERE/'seven_edge_expected.json').read_text())['cases']}
    results=[]
    for matching in ('46','10'):
        for motif in range(len(motifs(matching))):
            for pattern in ((1,1),(1,2)):
                name=f'{matching}_{motif}_{pattern[0]}{pattern[1]}'
                cnf,E,nv=build(pattern,matching,motif)
                cp=work/(name+'.cnf');pp=work/(name+'.drup');cnf.to_file(str(cp))
                record={'case':name,'variables':nv,'clauses':len(cnf.clauses),'cnf_sha256':digest(cp)}
                if record['cnf_sha256']!=expected[name]['cnf_sha256']:raise RuntimeError('CNF hash mismatch: '+name)
                with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as sol:
                    sol.conf_budget(args.conflicts);t=time.monotonic();answer=sol.solve_limited(expect_interrupt=True)
                    record.update(status='UNSAT' if answer is False else 'SAT' if answer else 'UNKNOWN',solver_seconds=time.monotonic()-t,statistics=sol.accum_stats())
                    if answer is True:
                        model=set(sol.get_model())
                        (work/(name+'_candidate.json')).write_text(json.dumps({'n':54,'edges':[uv for uv,e in E.items() if e in model]}))
                    if answer is not False:
                        (work/'incomplete.json').write_text(json.dumps(record,indent=2)+'\n')
                        raise RuntimeError('complete exclusion not established: '+name)
                    pp.write_text('\n'.join(sol.get_proof())+'\n')
                t=time.monotonic()
                checked=subprocess.run([str(checker),str(cp),str(pp),'-t','120'],capture_output=True,text=True)
                (work/(name+'_check.txt')).write_text(checked.stdout+checked.stderr)
                if checked.returncode!=0 or 's VERIFIED' not in checked.stdout:raise RuntimeError('proof check failed: '+name)
                record.update(checker_status='VERIFIED',checker_seconds=time.monotonic()-t,proof_sha256=digest(pp),cnf_bytes=cp.stat().st_size,proof_bytes=pp.stat().st_size)
                results.append(record);(work/'cases.json').write_text(json.dumps(results,indent=2)+'\n')
                print(name+' UNSAT; proof VERIFIED',flush=True)
    if len(results)!=50:raise RuntimeError('incomplete case coverage')
    validation.update(cases=results,verified_unsat=50,total_seconds=time.monotonic()-start,peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps({'verified_unsat':50,'total_seconds':validation['total_seconds'],'peak_rss_kb':validation['peak_rss_kb']},sort_keys=True))

if __name__=='__main__':main()
