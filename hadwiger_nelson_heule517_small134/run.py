#!/usr/bin/env python3
"""Decide the frozen 195 survivors, with proof production on a negative target."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
from engine import E, initial, survivors


def save(path, obj):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj, indent=2)+'\n'); temp.replace(path)


def proof(work, name, n, clauses, args):
    raw = E.J.dimacs(n, clauses); cnf = work/(name+'.cnf'); trace = work/(name+'.drat')
    cnf.write_bytes(raw); start = time.monotonic()
    with (work/(name+'.log')).open('w') as log:
        result = subprocess.run([str(args.kissat), '--seed=0', '--conflicts=1000000', '--time=180', str(cnf), str(trace)], stdout=log, stderr=subprocess.STDOUT)
    out = dict(name=name, returncode=result.returncode, seconds=time.monotonic()-start,
               variables=n, clauses=len(clauses), cnf_sha256=sha256(raw).hexdigest(), verified=False)
    if result.returncode == 20:
        start = time.monotonic()
        with (work/(name+'.check.log')).open('w') as log:
            check = subprocess.run([str(args.drat), str(cnf), str(trace)], stdout=log, stderr=subprocess.STDOUT)
        out.update(check_returncode=check.returncode, check_seconds=time.monotonic()-start,
                   verified=check.returncode == 0 and 's VERIFIED' in (work/(name+'.check.log')).read_text())
    if trace.exists(): out.update(proof_bytes=trace.stat().st_size, proof_sha256=sha256(trace.read_bytes()).hexdigest())
    print(json.dumps(out), flush=True)
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True); parser.add_argument('--drat', type=Path, required=True)
    args = parser.parse_args(); w = args.work; w.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3,)*2)
    start = time.monotonic(); data = E.inputs(); S = data['small']; rows = initial(data)
    candidates = survivors(rows, S); save(w/'survivors.json', candidates)
    solvers = []
    for k in range(20):
        n, cs = E.activated_case(data, k); (w/f'activation_{k:02d}.cnf').write_bytes(E.J.dimacs(n, cs))
        solvers.append(Solver(name='cadical195', bootstrap_with=cs))
    native = []; history = []; proofs = []; skipped = []; status = 'RUNNING'; target = None
    for index, omitted in enumerate(candidates):
        O = set(omitted)
        if any(set(row['D']) <= O for row in native):
            skipped.append(index); continue
        selected = sorted(set(S)-O); active = set(selected); assert len(selected) == 134
        rec = dict(index=index, omitted=omitted, cases=[]); winner = None
        for k, solver in enumerate(solvers):
            assumptions = [(4*len(S)+i+1)*(1 if v in active else -1) for i,v in enumerate(S)]
            solver.conf_budget(100000); t = time.monotonic(); answer = solver.solve_limited(assumptions=assumptions)
            rec['cases'].append(dict(case=k, answer=answer, seconds=time.monotonic()-t))
            if answer is None: status = 'CASE_UNKNOWN'; break
            if answer is False: continue
            positive = {x for x in solver.get_model() if x > 0}
            c = ''.join(str(next(c for c in range(4) if 4*i+c+1 in positive)) if v in active else '.' for i,v in enumerate(S))
            winner = E.extend(c, k, data); assert set(winner['D']) <= O
            native.append(winner); rows = E.minimal(rows+[winner]); rec['new_D'] = winner['D']; break
        history.append(rec)
        save(w/'progress.json', dict(history=history, rows=rows, native=native, skipped=skipped, status=status))
        print(json.dumps(dict(index=index, cases=len(rec['cases']), D=rec.get('new_D'), status=status)), flush=True)
        if status == 'CASE_UNKNOWN': break
        if winner is None:
            target = sorted(data['large']+selected); save(w/'target_vertices.json', target)
            status = 'TARGET_UNVERIFIED'
            for k in range(20):
                n, cs = E.J.small_case(selected, data['small_edges'], data['cross_edges'], data['boundary'], data['profiles'][k]['pattern'])
                proofs.append(proof(w, f'target_{k:02d}', n, cs, args)); save(w/'proofs.json', proofs)
                if not proofs[-1]['verified']: break
            if len(proofs) == 20 and all(p['verified'] for p in proofs):
                n, cs = E.P.graph_cnf(target, data['edges'], 5)
                with Solver(name='cadical195', bootstrap_with=cs) as solver:
                    solver.conf_budget(100000); answer = solver.solve_limited()
                    if answer is True:
                        positive = {x for x in solver.get_model() if x > 0}
                        c = ''.join(str(next(c for c in range(5) if 5*i+c+1 in positive)) for i in range(len(target)))
                        colours = dict(zip(target, c)); assert all(colours[u] != colours[v] for u,v in data['edges'] if u in colours and v in colours)
                        save(w/'target_five_colouring.json', dict(vertices=target, colouring=c)); status = 'TARGET_FIVE_CHROMATIC_VERIFIED_BY_CASES'
                n, cs = E.P.graph_cnf(target, data['edges'], 4)
                proofs.append(proof(w, 'target_full', n, cs, args)); save(w/'proofs.json', proofs)
                if proofs[-1]['verified'] and (w/'target_five_colouring.json').exists(): status = 'TARGET_FIVE_CHROMATIC_VERIFIED_DIRECTLY'
            break
    else: status = 'FIXED_L_SMALL134_FAMILY_CLOSED'
    for solver in solvers: solver.delete()
    save(w/'certificate.json', dict(rows=rows)); save(w/'native_witnesses.json', native)
    result = dict(status=status, survivor_count=len(candidates), tested=len(history), skipped=len(skipped),
                  case_calls=sum(len(r['cases']) for r in history), positive_extensions=len(native),
                  initial_cuts=206, final_cuts=len(rows), forced=sum(len(r['D']) == 1 for r in rows),
                  seconds=time.monotonic()-start, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  target=target, proofs=proofs, history=history, skipped_indices=skipped)
    save(w/'result.json', result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['history', 'target', 'skipped_indices']}, indent=2), flush=True)


if __name__ == '__main__': main()
