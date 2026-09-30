"""Complete sequential encodings and bounded, proof-producing G4 probes."""
import argparse
import hashlib
import json
import resource
import sys
import threading
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
if not (HERE/'sequential_sat.py').exists():sys.path.insert(0,str(HERE.parent))
from sequential_sat import generate,neg,replay


def augment(w,choices,pairs,bits,case,gates,frozen):
    traces={}
    def events(x,y):
        if (x,y) in traces:return traces[x,y]
        hits=[w.var() for _ in range(gates)]
        for t in range(gates):
            for j,(a,b) in enumerate(pairs):
                outside=[bits[x][t][a],bits[x][t][b],neg(bits[y][t][a]),neg(bits[y][t][b])]
                c=choices[t][j]
                for v in outside:w.add(-c,neg(v),hits[t])
                w.add(-c,-hits[t],*outside)
        traces[x,y]=hits
        return hits
    rows=case['critical_single_bounds']+case['selected_mixed_bounds']
    for r in rows:
        w.at_most(events(r['x'],r['y']),r['cap']+gates-14)
    if gates==14:
        # Independent scalar audit verifies J has v1<=v8 initially.
        # q8+r1-c<=2 and nonredundancy imply c=0, q8=r1=1.
        w.at_most(events(256,511),1)
        w.at_most(events(0,509),1)
        # Since one-hot7 and one-zero1 belong to J, those unique gates
        # are (7,8) and (0,1). Keeping trace constraints handles all phases.
        for row in choices:
            for j,pair in enumerate(pairs):
                if 8 in pair and pair!=(7,8):w.add(-row[j])
    if frozen:
        assert len(frozen)==gates
        for t,pair in enumerate(frozen):w.add(choices[t][pairs.index(tuple(pair))])
    return dict(case=case['case'],reference_budget=14,critical_single_bounds=len(case['critical_single_bounds']),
                mixed_bounds=len(case['selected_mixed_bounds']),
                derived_single_passages=gates==14,filters='No depth, lex, interval, kernel, or nonredundancy encoding',
                pruning_sha256=hashlib.sha256((HERE/'pruning.json').read_bytes()).hexdigest())


def make(case_id,path,gates,freeze=False):
    data=json.loads((HERE/'pruning.json').read_text())['cases'][case_id]
    checked=json.loads((HERE/'targets-checked.json').read_text())['cases'][case_id]
    frozen=checked['control_network'] if freeze else None
    if frozen:gates=len(frozen)
    meta=generate(9,data['residual_states'],gates,path,commute=False,encode_sorted=True,
                  augment=lambda w,c,p,b:augment(w,c,p,b,data,gates,frozen))
    print(json.dumps({k:v for k,v in meta.items() if k not in ('choices','pairs','states','pruning_budgets')}),flush=True)
    return meta


def solve(path,conflicts,seconds):
    import pysat
    from pysat.solvers import Glucose4
    start=time.monotonic();meta=json.loads(path.with_suffix('.meta.json').read_text())
    result=dict(instance=str(path),solver='Glucose4 via python-sat',pysat=pysat.__version__,
                conflict_budget=conflicts,wall_budget_seconds=seconds,cnf_sha256=meta['cnf_sha256'])
    with Glucose4(with_proof=True,use_timer=True) as solver:
        with path.open() as f:
            for line in f:
                if line.strip() and line[:1] not in 'cp':solver.add_clause([int(v) for v in line.split()[:-1]])
        print(json.dumps(dict(stage='loaded',vars=solver.nof_vars(),clauses=solver.nof_clauses(),seconds=time.monotonic()-start)),flush=True)
        timer=threading.Timer(seconds,solver.interrupt);timer.start()
        solver.conf_budget(conflicts)
        try:status=solver.solve_limited(expect_interrupt=True)
        finally:timer.cancel();timer.join();solver.clear_interrupt()
        result['status']='SAT' if status is True else 'UNSAT_unchecked' if status is False else 'UNKNOWN'
        result['stats']=solver.accum_stats();result['solver_seconds']=solver.time()
        if status is True:
            model=solver.get_model();positive={v for v in model if v>0}
            result['network']=[meta['pairs'][next(j for j,v in enumerate(row) if v in positive)] for row in meta['choices']]
            replay(9,meta['states'],result['network'])
            path.with_suffix('.model.json').write_text(json.dumps(model)+'\n')
        if status is False:
            proof=solver.get_proof()
            assert proof and proof[-1].strip()=='0','Missing terminal empty clause'
            path.with_suffix('.drat').write_text('\n'.join(proof)+'\n')
            result['proof_sha256']=hashlib.sha256(path.with_suffix('.drat').read_bytes()).hexdigest()
    result.update(seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path.with_suffix('.result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('command',choices=['generate','solve'])
    ap.add_argument('--case',type=int,choices=range(3),default=0)
    ap.add_argument('--path',type=Path,required=True)
    ap.add_argument('--gates',type=int,default=14)
    ap.add_argument('--freeze-control',action='store_true')
    ap.add_argument('--conflicts',type=int,default=20000)
    ap.add_argument('--seconds',type=float,default=40)
    args=ap.parse_args()
    if args.command=='generate':make(args.case,args.path,args.gates,args.freeze_control)
    else:solve(args.path,args.conflicts,args.seconds)
