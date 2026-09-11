#!/usr/bin/env python3
"""Regenerate all one-quad formulas and checked refutations outside the source tree."""
import argparse,hashlib,json,platform,resource,subprocess,time
from pathlib import Path
from pysat.solvers import Solver
from a0_one_quad_sat import build,cases,case_name,REPS,proof_stage

HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--case',help='Optional exact case name; default is the complete cover.')
    p.add_argument('--replay',type=Path,help='Replay existing traces against freshly regenerated formulas.')
    p.add_argument('--conflicts',type=int,default=0,help='Zero means no conflict limit; UNKNOWN fails.')
    a=p.parse_args();a.work=a.work.resolve();a.checker=a.checker.resolve()
    if a.work==HERE or HERE in a.work.parents:raise ValueError('Use an output directory outside source.')
    a.work.mkdir(parents=True,exist_ok=True)
    selected=[c for c in cases() if a.case is None or case_name(c)==a.case]
    if not selected:raise ValueError('Unknown case')
    records=[]
    for case in selected:
        name=case_name(case);index,branch,role=case;r=2 if branch=='A' else 3
        cnfpath=a.work/(name+'.cnf');proofpath=a.work/(name+'.drup')
        if cnfpath.exists() or proofpath.exists():raise FileExistsError(name)
        t=time.monotonic();cnf,E,ds,cs=build(index,branch,REPS[r][role]);cnf.to_file(str(cnfpath))
        discovery,searchE,searchd,searchc=build(index,branch,REPS[r][role],stage=proof_stage(case))
        if cnf.clauses[:len(discovery.clauses)]!=discovery.clauses or E!=searchE or ds!=searchd or cs!=searchc:
            raise ValueError('Search stage is not an exact final-formula prefix')
        searchpath=a.work/(name+'.search.cnf');discovery.to_file(str(searchpath));build_seconds=time.monotonic()-t
        if a.replay:
            proofpath=a.replay/(name+'.drup')
            if not proofpath.is_file():raise FileNotFoundError(proofpath)
            solve_seconds=None;stats=None
        else:
            t=time.monotonic()
            with Solver(name='g4',bootstrap_with=discovery,with_proof=True) as solver:
                if a.conflicts:solver.conf_budget(a.conflicts)
                ans=solver.solve_limited(expect_interrupt=True) if a.conflicts else solver.solve()
                stats=solver.accum_stats();solve_seconds=time.monotonic()-t
                if ans is not False:
                    out={'case':case,'status':'SAT' if ans is True else 'UNKNOWN'}
                    if ans:
                        positive=set(solver.get_model());out['edges']=[uv for uv,e in E.items() if e in positive]
                    (a.work/(name+'_nonrefutation.json')).write_text(json.dumps(out,indent=2)+'\n')
                    raise RuntimeError(out['status']+' is not a refutation')
                proofpath.write_text('\n'.join(solver.get_proof())+'\n')
        log=a.work/(name+'_check.log');t=time.monotonic()
        with log.open('w') as f:check=subprocess.run([str(a.checker),str(cnfpath),str(proofpath)],stdout=f,stderr=subprocess.STDOUT)
        verified=check.returncode==0 and 's VERIFIED' in log.read_text()
        record={'case':list(case),'name':name,'variables':cnf.nv,'clauses':len(cnf.clauses),'edge_variables':len(E),
                'cnf_sha256':sha(cnfpath),'search_cnf_sha256':sha(searchpath),'exact_clause_prefix':True,'proof_sha256':sha(proofpath),'proof_bytes':proofpath.stat().st_size,
                'verified':verified,'proof_input_stage':proof_stage(case),'build_seconds':build_seconds,'solve_seconds':solve_seconds,
                'check_seconds':time.monotonic()-t,'statistics':stats}
        records.append(record)
        with (a.work/'progress.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
        print(json.dumps({'case':case,'verified':verified}),flush=True)
        if not verified:raise RuntimeError('Proof checker failed')
    result={'complete_cover':len(selected)==len(list(cases())),'python':platform.python_version(),
            'checker_sha256':sha(a.checker),'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'peak_self_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'records':records,'replay':a.replay is not None}
    (a.work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    expected=HERE/'a0_one_quad_expected.json'
    if expected.exists():
        exp=json.loads(expected.read_text());byname={r['name']:r for r in exp['refutations']}
        for r in records:
            old=byname[r['name']]
            for key in ('variables','clauses','edge_variables','cnf_sha256','search_cnf_sha256'):
                if r[key]!=old[key]:raise ValueError('Formula mismatch: '+r['name']+' '+key)
    return result

if __name__=='__main__':main()
