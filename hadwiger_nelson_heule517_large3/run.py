#!/usr/bin/env python3
"""One frozen 256-query three-large family pilot; all bulky native state stays external."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
import engine as F


def save(path, value):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(value, separators=(',',':'))+'\n'); temp.replace(path)


def prove(work, selected, edges, args):
    n, clauses = F.E.P.graph_cnf(selected, edges); raw = F.E.P.dimacs(n, clauses)
    cnf = work/'target.cnf'; trace = work/'target.drat'; cnf.write_bytes(raw); t = time.monotonic()
    with (work/'target.log').open('w') as log:
        result = subprocess.run([str(args.kissat), '--seed=0', '--conflicts=1000000', '--time=180', str(cnf), str(trace)], stdout=log, stderr=subprocess.STDOUT)
    out = dict(returncode=result.returncode, seconds=time.monotonic()-t, cnf_sha256=sha256(raw).hexdigest(), variables=n, clauses=len(clauses), verified=False)
    if result.returncode == 20:
        t = time.monotonic()
        with (work/'target.check.log').open('w') as log:
            check = subprocess.run([str(args.drat), str(cnf), str(trace)], stdout=log, stderr=subprocess.STDOUT)
        out.update(check_returncode=check.returncode, check_seconds=time.monotonic()-t,
                   verified=check.returncode == 0 and 's VERIFIED' in (work/'target.check.log').read_text())
    if trace.exists(): out.update(proof_bytes=trace.stat().st_size, proof_sha256=sha256(trace.read_bytes()).hexdigest())
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True); parser.add_argument('--drat', type=Path, required=True)
    args = parser.parse_args(); w = args.work; w.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3,)*2)
    start = time.monotonic(); data, rows = F.inputs(); states = F.family(data, rows)
    save(w/'initial_counts.json', [dict(small_omitted=s['small_omitted'], triples=len(s['remaining'])) for s in states])
    n, clauses = F.E.P.activated(data['edges']); raw = F.E.P.dimacs(n, clauses)
    (w/'activation.cnf').write_bytes(raw)
    solver = Solver(name='cadical195', bootstrap_with=clauses)
    native = []; history = []; cursor = 0; status = 'BOUND_REACHED'; proof = None; target = None
    S = set(data['small']); L = set(data['large'])
    for turn in range(256):
        if not any(s['remaining'] for s in states): status = 'THREE_LARGE_FAMILY_CLOSED'; break
        while not states[cursor]['remaining']: cursor = (cursor+1) % len(states)
        index = cursor; state = states[index]; cursor = (cursor+1) % len(states)
        triple = list(F.uncode(min(state['remaining']))); O = set(triple+state['small_omitted'])
        selected = sorted(set(range(517))-O); assert len(selected) == 508 and len(O & L) == 3 and len(O & S) == 6
        assumptions = [(2069+v)*(-1 if v in O else 1) for v in range(517)]
        solver.conf_budget(100000); t = time.monotonic(); answer = solver.solve_limited(assumptions=assumptions)
        rec = dict(turn=turn, state=index, omitted=sorted(O), answer=answer, seconds=time.monotonic()-t)
        if answer is not True:
            status = 'GRAPH_UNKNOWN' if answer is None else 'TARGET_UNVERIFIED'; target = selected; history.append(rec)
            save(w/'target_vertices.json', selected); save(w/'progress.json', dict(history=history, native=native, status=status))
            if answer is False:
                proof = prove(w, selected, data['edges'], args); save(w/'proof.json', proof)
                if proof['verified']:
                    n5,c5 = F.E.P.graph_cnf(selected, data['edges'], 5)
                    with Solver(name='cadical195', bootstrap_with=c5) as five:
                        five.conf_budget(100000); ok = five.solve_limited()
                        if ok is True:
                            positive = {x for x in five.get_model() if x > 0}
                            c = ''.join(str(next(c for c in range(5) if 5*i+c+1 in positive)) for i in range(508))
                            mp = dict(zip(selected,c)); assert all(mp[u] != mp[v] for u,v in data['edges'] if u in mp and v in mp)
                            save(w/'five_colouring.json', dict(vertices=selected, colouring=c)); status = 'TARGET_FIVE_CHROMATIC_VERIFIED'
            break
        positive = {x for x in solver.get_model() if x > 0}
        c = ''.join('.' if v in O else str(next(c for c in range(4) if 4*v+c+1 in positive)) for v in range(517))
        assert set(F.E.P.check_colouring(c, data['edges'])) == O
        c = F.E.P.extend(c, data['adj'], data['large']+data['small'])
        D = list(F.E.P.check_colouring(c, data['edges'])); assert set(D) <= O
        row = dict(kind='native', D=D, colouring=c); native.append(row)
        before = sum(len(s['remaining']) for s in states); F.apply_cut(states, row, S)
        remaining = sum(len(s['remaining']) for s in states)
        rec.update(D=D, removed=before-remaining, remaining=remaining); history.append(rec)
        save(w/'progress.json', dict(history=history, native=native, status=status))
        print(json.dumps(rec), flush=True)
    if not any(s['remaining'] for s in states): status = 'THREE_LARGE_FAMILY_CLOSED'
    solver.delete(); save(w/'native_witnesses.json', native)
    frontier = [dict(small_omitted=s['small_omitted'], triples=len(s['remaining']), first_triple=list(F.uncode(min(s['remaining']))) if s['remaining'] else None) for s in states]
    save(w/'frontier.json', frontier)
    result = dict(status=status, queries=len(history), positives=len(native), initial_small_choices=38,
                  initial_triples=749066, remaining_triples=sum(s['triples'] for s in frontier),
                  remaining_small_choices=sum(bool(s['triples']) for s in frontier),
                  seconds=time.monotonic()-start, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  activation_sha256=sha256(raw).hexdigest(), proof=proof, target=target, history=history)
    save(w/'result.json', result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['history','target']},indent=2),flush=True)


if __name__ == '__main__': main()
