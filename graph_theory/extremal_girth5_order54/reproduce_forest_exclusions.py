#!/usr/bin/env python3
"""Reproduce the complete 22-case exclusion of three high-induced forests."""
import argparse,hashlib,json,resource,subprocess,time
from pathlib import Path
from pysat.solvers import Solver
from forest_sat import build,FORESTS,EXCLUDED
from forest_profiles import profiles
from verify_forest_reduction import certificate,coverage,graph_controls,symmetry_control

HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--checker',type=Path,required=True);ap.add_argument('--conflicts',type=int,default=100000);args=ap.parse_args()
    work=args.work.resolve();checker=args.checker.resolve()
    if work.is_relative_to(HERE.parents[1]):raise ValueError('work must be outside repository')
    if not checker.is_file():raise ValueError('DRAT-trim executable missing')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    validation={'certificates':[certificate(),certificate(True)],'coverage':coverage(),'graph_controls':graph_controls(),'symmetry_control':symmetry_control()}
    expected={x['case']:x for x in json.loads((HERE/'forest_expected.json').read_text())['cases']};results=[]
    for name in EXCLUDED:
        L=FORESTS[name];m=sum(x-1 for x in L);k=sum(x-2 for x in L)
        for i in range(len(profiles(m,k))):
            tag=name+'_'+str(i);cnf,E,nv=build(name,i);cp=work/(tag+'.cnf');pp=work/(tag+'.drup');cnf.to_file(str(cp))
            out={'case':tag,'forest':name,'profile':i,'variables':nv,'clauses':len(cnf.clauses),'cnf_sha256':digest(cp)}
            if out['cnf_sha256']!=expected[tag]['cnf_sha256']:raise RuntimeError('CNF hash mismatch: '+tag)
            with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as s:
                s.conf_budget(args.conflicts);t=time.monotonic();r=s.solve_limited(expect_interrupt=True)
                out.update(status='UNSAT' if r is False else 'SAT' if r else 'UNKNOWN',solver_seconds=time.monotonic()-t,statistics=s.accum_stats())
                if r:
                    model=set(s.get_model());(work/(tag+'_candidate.json')).write_text(json.dumps({'n':54,'edges':[uv for uv,e in E.items() if e in model]}))
                if r is not False:
                    (work/'incomplete.json').write_text(json.dumps(out,indent=2)+'\n');raise RuntimeError('exclusion incomplete: '+tag)
                pp.write_text('\n'.join(s.get_proof())+'\n')
            t=time.monotonic();checked=subprocess.run([str(checker),str(cp),str(pp),'-t','120'],capture_output=True,text=True)
            (work/(tag+'_check.txt')).write_text(checked.stdout+checked.stderr)
            if checked.returncode!=0 or 's VERIFIED' not in checked.stdout:raise RuntimeError('proof check failed: '+tag)
            out.update(checker_status='VERIFIED',checker_seconds=time.monotonic()-t,proof_sha256=digest(pp),cnf_bytes=cp.stat().st_size,proof_bytes=pp.stat().st_size)
            results.append(out);(work/'cases.json').write_text(json.dumps(results,indent=2)+'\n');print(tag+' UNSAT; proof VERIFIED',flush=True)
    if len(results)!=22:raise RuntimeError('incomplete coverage')
    validation.update(cases=results,verified_unsat=22,excluded_forests=list(EXCLUDED),total_seconds=time.monotonic()-start,peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps({'verified_unsat':22,'excluded_forests':list(EXCLUDED),'total_seconds':validation['total_seconds'],'peak_rss_kb':validation['peak_rss_kb']},sort_keys=True))

if __name__=='__main__':main()
