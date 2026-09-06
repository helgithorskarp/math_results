#!/usr/bin/env python3
"""One frozen large-block projection pilot, with checked exhaustion if found."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
import engine as E


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--kissat', type=Path, required=True)
    ap.add_argument('--drat', type=Path, required=True)
    args = ap.parse_args(); w = args.work; w.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3,)*2)
    start = time.monotonic(); _, sep = E.geometry()
    (w/'separator.json').write_text(json.dumps(sep, separators=(',', ':'))+'\n')
    vertices = sep['large']; boundary = sep['boundary']; edges = sep['large_edges']
    pos = {v:i for i,v in enumerate(vertices)}
    n, clauses = E.cnf(vertices, edges); (w/'base.cnf').write_bytes(E.dimacs(n, clauses))
    solver = Solver(name='cadical195', bootstrap_with=clauses)
    rows = []; history = []; status = 'BOUND_REACHED'; proof = None
    for turn in range(128):
        solver.conf_budget(200000); t = time.monotonic(); answer = solver.solve_limited()
        history.append({'turn':turn, 'answer':answer, 'seconds':time.monotonic()-t})
        if answer is not True:
            status = 'NATIVE_UNSAT_UNVERIFIED' if answer is False else 'UNKNOWN'
            break
        positive = {v for v in solver.get_model() if v > 0}
        colour = ''.join(str(next(c for c in range(4) if 4*i+c+1 in positive)) for i in range(len(vertices)))
        assert all(colour[pos[u]] != colour[pos[v]] for u,v in edges)
        pattern, colour = E.normalized(colour, vertices, boundary)
        assert pattern not in {r['pattern'] for r in rows}
        rows.append({'pattern':pattern, 'colouring':colour})
        for clause in E.blocking(pattern, vertices, boundary):
            solver.add_clause(clause); clauses.append(clause)
        (w/'progress.json').write_text(json.dumps({'rows':rows,'history':history},separators=(',',':'))+'\n')
        print(json.dumps({'patterns':len(rows),'seconds':history[-1]['seconds']}), flush=True)
    solver.delete()
    raw = E.dimacs(n, clauses); (w/'exhaustion.cnf').write_bytes(raw)
    (w/'certificate.json').write_text(json.dumps({'rows':rows},separators=(',',':'))+'\n')
    if status == 'NATIVE_UNSAT_UNVERIFIED':
        t = time.monotonic()
        with (w/'kissat.log').open('w') as log:
            r = subprocess.run([str(args.kissat),'--seed=0','--conflicts=1000000','--time=180',str(w/'exhaustion.cnf'),str(w/'exhaustion.drat')], stdout=log, stderr=subprocess.STDOUT)
        proof = {'kissat_returncode':r.returncode,'seconds':time.monotonic()-t,'verified':False}
        if r.returncode == 20:
            t = time.monotonic()
            with (w/'drat_check.log').open('w') as log:
                try:
                    c = subprocess.run([str(args.drat),str(w/'exhaustion.cnf'),str(w/'exhaustion.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=180)
                    proof.update(check_returncode=c.returncode, check_seconds=time.monotonic()-t,
                                 verified=c.returncode==0 and 's VERIFIED' in (w/'drat_check.log').read_text())
                except subprocess.TimeoutExpired: proof['checker_timeout'] = True
        trace = w/'exhaustion.drat'
        if trace.exists(): proof.update(proof_bytes=trace.stat().st_size, proof_sha256=sha256(trace.read_bytes()).hexdigest())
        if proof['verified']: status = 'COMPLETE_CHECKED_RELATION'
    result = {'status':status,'patterns':len(rows),'native_calls':len(history),'history':history,
              'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'cnf_variables':n,'cnf_clauses':len(clauses),'cnf_sha256':sha256(raw).hexdigest(),
              'proof':proof,'full_H517_queries':0,'small_side_queries':0,'record_improvement':False}
    (w/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2),flush=True)


if __name__ == '__main__': main()
