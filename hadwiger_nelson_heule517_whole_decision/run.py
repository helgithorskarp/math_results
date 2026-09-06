#!/usr/bin/env python3
"""Frozen 256-query decision on all remaining H517 block compositions."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
import engine as E


def save(path,obj):
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,separators=(',',':'))+'\n'); tmp.replace(path)


def certify(work,selected,edges,args):
    n,clauses = E.P.graph_cnf(selected,edges); raw = E.P.dimacs(n,clauses)
    cnf = work/'target.cnf'; proof = work/'target.drat'; cnf.write_bytes(raw); t = time.monotonic()
    with (work/'target.log').open('w') as log:
        p = subprocess.run([str(args.kissat),'--seed=0','--conflicts=1000000','--time=180',str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT)
    result = dict(returncode=p.returncode,seconds=time.monotonic()-t,cnf_sha256=sha256(raw).hexdigest(),variables=n,clauses=len(clauses),verified=False)
    if p.returncode == 20:
        with (work/'target.check.log').open('w') as log:
            p = subprocess.run([str(args.drat),str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT)
        result.update(check_returncode=p.returncode,verified=p.returncode == 0 and 's VERIFIED' in (work/'target.check.log').read_text())
    if proof.exists(): result.update(proof_bytes=proof.stat().st_size,proof_sha256=sha256(proof.read_bytes()).hexdigest())
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--frontier',type=Path,required=True); parser.add_argument('--kissat',type=Path,required=True); parser.add_argument('--drat',type=Path,required=True)
    args = parser.parse_args(); w = args.work; w.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,)*2)
    start = time.monotonic(); data,buckets = E.inputs(args.frontier)
    save(w/'initial_counts.json',{str(i):len(ts) for i,ts in buckets.items()})
    n,clauses = E.P.activated(data['edges']); raw = E.P.dimacs(n,clauses); (w/'activation.cnf').write_bytes(raw)
    native = []; history = []; cursor = 5; status = 'BOUND_REACHED'; target = proof = None
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        for turn in range(256):
            if not any(buckets.values()): status = 'WHOLE_H517_FAMILY_CLOSED'; break
            while not buckets[cursor]: cursor = 5+(cursor-4)%5
            bucket = cursor; O = set(buckets[bucket][0]); cursor = 5+(cursor-4)%5
            selected = sorted(set(range(517))-O); E.P.require(len(selected) == 508, 'target order')
            assumptions = [(2069+v)*(-1 if v in O else 1) for v in range(517)]
            solver.conf_budget(100000); t = time.monotonic(); answer = solver.solve_limited(assumptions=assumptions)
            rec = dict(turn=turn,bucket=bucket,omitted=sorted(O),answer=answer,seconds=time.monotonic()-t)
            if answer is not True:
                status = 'GRAPH_UNKNOWN' if answer is None else 'TARGET_UNVERIFIED'; target = selected; history.append(rec)
                save(w/'target_vertices.json',target); save(w/'progress.json',dict(status=status,history=history,native=native))
                (w/'frontier.txt').write_bytes(E.stream(buckets))
                if answer is False:
                    proof = certify(w,selected,data['edges'],args); save(w/'proof.json',proof)
                    if proof['verified']:
                        n5,c5 = E.P.graph_cnf(selected,data['edges'],5)
                        with Solver(name='cadical195',bootstrap_with=c5) as five:
                            five.conf_budget(100000); ok = five.solve_limited()
                            if ok is True:
                                positive = {x for x in five.get_model() if x > 0}
                                c = ''.join(str(next(c for c in range(5) if 5*i+c+1 in positive)) for i in range(508))
                                mp = dict(zip(selected,c)); E.P.require(all(mp[u] != mp[v] for u,v in data['edges'] if u in mp and v in mp),'five-colouring')
                                save(w/'five_colouring.json',dict(vertices=selected,colouring=c)); status = 'TARGET_AWAITING_INDEPENDENT_CNF_AUDIT'
                break
            positive = {x for x in solver.get_model() if x > 0}
            c = ''.join('.' if v in O else str(next(c for c in range(4) if 4*v+c+1 in positive)) for v in range(517))
            E.P.require(set(E.P.check_colouring(c,data['edges'])) == O,'candidate colouring')
            c = E.P.extend(c,data['adj'],data['large']+data['small'])
            D = list(E.P.check_colouring(c,data['edges'])); E.P.require(D and set(D) <= O,'extended colouring')
            row = dict(D=D,colouring=c); native.append(row)
            before = sum(map(len,buckets.values())); E.prune(buckets,D); remaining = sum(map(len,buckets.values()))
            rec.update(D=D,removed=before-remaining,remaining=remaining,remaining_by_large={str(i):len(ts) for i,ts in buckets.items()}); history.append(rec)
            save(w/'progress.json',dict(status=status,history=history,native=native)); (w/'frontier.txt').write_bytes(E.stream(buckets))
            print(json.dumps(rec),flush=True)
    if not any(buckets.values()): status = 'WHOLE_H517_FAMILY_CLOSED'
    save(w/'native_witnesses.json',native); final = E.stream(buckets); (w/'frontier.txt').write_bytes(final)
    result = dict(status=status,queries=len(history),positives=len(native),initial_candidates=39453,
                  remaining_candidates=sum(map(len,buckets.values())),remaining_by_large={str(i):len(ts) for i,ts in buckets.items()},
                  frontier_bytes=len(final),frontier_sha256=sha256(final).hexdigest(),seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,activation_sha256=sha256(raw).hexdigest(),proof=proof,target=target,history=history)
    save(w/'result.json',result); print(json.dumps({k:v for k,v in result.items() if k not in ['history','target']},sort_keys=True),flush=True)


if __name__ == '__main__': main()
