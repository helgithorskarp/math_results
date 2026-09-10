#!/usr/bin/env python3
"""Regenerate and independently proof-check the complete 124-case reduction."""
import argparse,hashlib,json,resource,subprocess,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from pysat.solvers import Solver
from shared_center_cases import proof_cases
from verify_shared_center import main as check_coverage
HERE=Path(__file__).resolve().parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run_case(task):
    kind,p,i,j,work,checker,budget=task;work=Path(work);tag=f'{kind}_{p}_{i}_{j}'
    expected={r['case']:r for r in json.loads((HERE/'shared_center_expected.json').read_text())['cases']}[tag]
    if kind=='base':
        from forest_sat import build
        cnf,E,nv=build('5_2b',p)
    elif kind=='joint':
        from shared_center_sat import build
        cnf,E,nv=build(p,i)
    elif kind=='star':
        from shared_star_sat import build
        cnf,E,nv=build(p,i,j)
    else:raise ValueError(kind)
    cp=work/(tag+'.cnf');pp=work/(tag+'.drup');cnf.to_file(str(cp));out={'case':tag,'kind':kind,'profile':p,'center_case':i,'star_case':j,'variables':nv,'clauses':len(cnf.clauses),'cnf_sha256':digest(cp)}
    if out['cnf_sha256']!=expected['cnf_sha256']:raise RuntimeError('CNF hash mismatch: '+tag)
    with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as s:
        s.conf_budget(budget);t=time.monotonic();r=s.solve_limited(expect_interrupt=True)
        out.update(status='UNSAT' if r is False else 'SAT' if r else 'UNKNOWN',solver_seconds=time.monotonic()-t,statistics=s.accum_stats())
        if r:
            model=set(s.get_model());(work/(tag+'_candidate.json')).write_text(json.dumps({'n':54,'edges':[uv for uv,e in E.items() if e in model]}))
        if r is not False:
            (work/(tag+'_incomplete.json')).write_text(json.dumps(out,indent=2)+'\n');raise RuntimeError('incomplete exclusion: '+tag)
        pp.write_text('\n'.join(s.get_proof())+'\n')
    if digest(pp)!=expected['proof_sha256']:raise RuntimeError('proof hash mismatch: '+tag)
    t=time.monotonic();checked=subprocess.run([checker,str(cp),str(pp),'-t','300'],capture_output=True,text=True);(work/(tag+'_check.txt')).write_text(checked.stdout+checked.stderr)
    if checked.returncode or 's VERIFIED' not in checked.stdout:raise RuntimeError('proof check failed: '+tag)
    out.update(checker_status='VERIFIED',checker_seconds=time.monotonic()-t,proof_sha256=digest(pp),cnf_bytes=cp.stat().st_size,proof_bytes=pp.stat().st_size,worker_peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/(tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--checker',type=Path,required=True);ap.add_argument('--jobs',type=int,default=4);ap.add_argument('--conflicts',type=int,default=100000);a=ap.parse_args()
    work=a.work.resolve();checker=a.checker.resolve()
    if work.is_relative_to(HERE.parents[1]):raise ValueError('work must be outside repository')
    if not checker.is_file() or a.jobs<1:raise ValueError('checker or jobs')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();coverage=check_coverage();results=[];cases=proof_cases()
    with ProcessPoolExecutor(max_workers=a.jobs) as pool:
        futures=[pool.submit(run_case,(*case,str(work),str(checker),a.conflicts)) for case in cases]
        for f in as_completed(futures):
            out=f.result();results.append(out);(work/'cases.json').write_text(json.dumps(sorted(results,key=lambda x:x['case']),indent=2)+'\n');print(f"{len(results)}/{len(cases)} {out['case']} UNSAT; proof VERIFIED",flush=True)
    if len(results)!=124:raise RuntimeError('incomplete proof plan')
    final={'coverage':coverage,'cases':sorted(results,key=lambda x:x['case']),'verified_unsat':124,'residual_center_states':33,'jobs':a.jobs,'total_seconds':time.monotonic()-start,'max_worker_peak_rss_kb':max(x['worker_peak_rss_kb'] for x in results),'parent_peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (work/'validation.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({k:v for k,v in final.items() if k not in ('coverage','cases')},sort_keys=True))
if __name__=='__main__':main()
