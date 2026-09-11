#!/usr/bin/env python3
"""Regenerate and certify the complete four-edge all-sink layer outside Git."""
import argparse,hashlib,json,platform,resource,subprocess,time
from collections import Counter
from pathlib import Path
from pysat.solvers import Solver
from four_edge_sat import build,cases,proof_stage,case_name
from a0_unit_check import unit_contradiction

HERE=Path(__file__).resolve().parent
REPOSITORY=HERE.parents[1]

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def formula_row(r):
    return [r['case'],r['stage'],r['variables'],r['clauses'],r['slots'],
            r['edge_variables'],r['formula_sha256']]

def manifest(records):
    groups=[]
    for index,fid in sorted({tuple(r['case'][:2]) for r in records}):
        rows=[r for r in records if r['case'][:2]==[index,fid]]
        groups.append(dict(index=index,fid=fid,cases=len(rows),
                           formula_manifest_sha256=digest([formula_row(r) for r in rows])))
    return dict(cases=len(records),groups=groups,
                formula_manifest_sha256=digest([formula_row(r) for r in records]))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--case',help='Exact four_INDEX_FOREST_ORBIT name; default all3721.')
    p.add_argument('--replay',type=Path,help='Directory of named .drup files; unnecessary for unit cases.')
    p.add_argument('--conflicts',type=int,default=0,help='0 is unlimited; UNKNOWN is a failure.')
    args=p.parse_args();work=args.work.resolve();checker=args.checker.resolve()
    if work==REPOSITORY or REPOSITORY in work.parents:raise ValueError('Generated outputs must be outside the repository.')
    if args.conflicts<0:raise ValueError('Negative conflict budget')
    work.mkdir(parents=True,exist_ok=True)
    selected=[c for c in cases() if args.case is None or case_name(c)==args.case]
    if not selected:raise ValueError('Unknown case')
    records=[]
    for case in selected:
        name=case_name(case);formula=work/(name+'.cnf');proof=work/(name+'.drup')
        if formula.exists() or proof.exists():raise FileExistsError(name)
        start=time.perf_counter();cnf,data=build(*case,stage=proof_stage(case));cnf.to_file(str(formula))
        build_seconds=time.perf_counter()-start
        start=time.perf_counter()
        # The two large adjacency cases go directly to DRAT checking.
        unit=unit_contradiction(cnf.clauses) if proof_stage(case)!='near' else False
        unit_seconds=time.perf_counter()-start
        stats=None;solve_seconds=None;code=None;check_seconds=0.0
        verified=unit;method='unit' if unit else 'drat'
        certificate_sha256=sha(formula) if unit else None
        trace_bytes=0
        if not unit:
            if args.replay:
                proof=args.replay.resolve()/(name+'.drup')
                if not proof.is_file():raise FileNotFoundError(proof)
            else:
                start=time.perf_counter()
                with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as solver:
                    if args.conflicts:
                        solver.conf_budget(args.conflicts);answer=solver.solve_limited(expect_interrupt=True)
                    else:answer=solver.solve()
                    stats=solver.accum_stats();solve_seconds=time.perf_counter()-start
                    if answer is not False:
                        nonrefutation=dict(case=case,status='SAT' if answer else 'UNKNOWN')
                        if answer:
                            positive=set(solver.get_model())
                            nonrefutation['vertices']=[(i,d,sorted(B),j) for i,(d,B,j) in enumerate(data['vertices']) if data['X'][i] in positive]
                            nonrefutation['edges']=[uv for uv,e in data.get('E',{}).items() if e in positive]
                        (work/(name+'_nonrefutation.json')).write_text(json.dumps(nonrefutation,indent=2)+'\n')
                        raise RuntimeError('Coverage incomplete; nonrefutation preserved.')
                    proof.write_text('\n'.join(solver.get_proof())+'\n')
            log=work/(name+'_check.log');start=time.perf_counter()
            with log.open('w') as out:run=subprocess.run([str(checker),str(formula),str(proof)],stdout=out,stderr=subprocess.STDOUT)
            code=run.returncode;verified=code==0 and 's VERIFIED' in log.read_text()
            check_seconds=time.perf_counter()-start
            certificate_sha256=sha(proof);trace_bytes=proof.stat().st_size
        record=dict(case=list(case),stage=proof_stage(case),variables=cnf.nv,
                    clauses=len(cnf.clauses),slots=len(data['vertices']),
                    edge_variables=len(data.get('E',{})),formula_sha256=sha(formula),
                    method=method,verified=verified,checker_returncode=code,
                    certificate_sha256=certificate_sha256,trace_bytes=trace_bytes,
                    build_seconds=build_seconds,unit_seconds=unit_seconds,
                    solve_seconds=solve_seconds,check_seconds=check_seconds,statistics=stats)
        records.append(record)
        with (work/'progress.jsonl').open('a') as out:out.write(json.dumps(record)+'\n')
        print(json.dumps(dict(case=case,method=method,verified=verified)),flush=True)
        if not verified:raise RuntimeError('Contradiction check failed')
    complete=len(selected)==len(list(cases()));inputs=manifest(records)
    expected=HERE/'four_edge_expected.json';compared=False
    if complete and expected.exists():
        exp=json.loads(expected.read_text())
        if inputs!=exp['formula_manifest']:raise ValueError('Whole-layer input manifest mismatch')
        compared=True
    result=dict(complete_cover=complete,expected_manifest_checked=compared,formula_manifest=inputs,
                methods=dict(Counter(r['method'] for r in records)),python=platform.python_version(),
                checker_sha256=sha(checker),peak_self_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                peak_child_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,records=records)
    (work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':main()
