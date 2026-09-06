"""Reproduce the frozen, two-endpoint AllSAT pilot in a fresh local directory.

Requires python-sat 1.8.dev24 (Glucose 4.1), Kissat and drat-trim. This search
is not a premise of the standalone verifier or the separator gluing proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'hadwiger_nelson_heule632_pair_pilot'))
import build as B


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for f, h in plan['input_files'].items():
        need(hashlib.sha256((REPO / f).read_bytes()).hexdigest() == h, 'input hash')
    points, edges, _ = B.geometry()
    b = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m, u = set(b['mandatory_vertices']), set(b['optional_vertices'])
    v = m | u
    large = {v for v in v if all(points[v][a][i] == 0 for a in (0, 1) for i in (2, 3, 6, 7))}
    cross = [(a, b) if a in large else (b, a) for a, b in edges if a in v and b in v and (a in large) != (b in large)]
    q = sorted({a for a, b in cross})
    return plan, m, large, q, cross, edges


def formula(vertices, edges, q):
    clauses, _, _, triangle = B.formula(vertices, edges, 4)
    if triangle:
        clauses = clauses[:-len(triangle)]
    index = {v: i for i, v in enumerate(vertices)}
    var = lambda v, c: 4 * index[v] + c + 1
    for i, v in enumerate(q):
        for c in range(1, 4):
            clauses.append([-var(v, c)] + [var(w, c - 1) for w in q[:i]])
    return clauses, var


def dimacs(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode()


def native_limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def main():
    from pysat.solvers import Solver
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    plan, mandatory, large, q, cross, edges = prepare()
    resource.setrlimit(resource.RLIMIT_AS, (plan['memory_bytes'], plan['memory_bytes']))
    # Proof traces have their separately bounded native output limit.
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))
    certificate = {'separator': q, 'cross_matching': [[v, min(b for a, b in cross if a == v)] for v in q],
                   'optional_large': sorted(large - mandatory), 'blocks': {},
                   'record_improvement': False, 'whole560_family_closed': False}
    reports = {}
    for name, vertices in [('mandatory', sorted(mandatory & large)), ('full', sorted(large))]:
        clauses, var = formula(vertices, edges, q)
        base = list(clauses); rows = {}; t = time.monotonic(); status = None
        stream = args.out / (name + '_states.jsonl')
        with stream.open('w') as out, Solver(name='g4', bootstrap_with=clauses) as solver:
            while len(rows) < plan['state_cap']:
                remain = plan['total_solver_seconds'] - (time.monotonic() - t)
                if remain <= 0:
                    status = 'TOTAL_TIME_LIMIT'; break
                solver.conf_budget(plan['query_conflicts'])
                timer = threading.Timer(min(remain, plan['query_seconds']), solver.interrupt)
                timer.start()
                try:
                    answer = solver.solve_limited(expect_interrupt=True)
                finally:
                    timer.cancel(); timer.join()
                solver.clear_interrupt()
                if answer is None:
                    status = 'QUERY_LIMIT'; break
                if answer is False:
                    status = 'ENUMERATION_UNSAT_UNCERTIFIED'; break
                model = {x for x in solver.get_model() if x > 0}
                colour = {}
                for v in vertices:
                    choices = [c for c in range(4) if var(v, c) in model]
                    need(len(choices) == 1, 'one-hot model'); colour[v] = choices[0]
                need(all(colour[a] != colour[b] for a, b in edges if a in colour and b in colour), 'proper model')
                state = ''.join(str(colour[v]) for v in q)
                need(state not in rows, 'new state')
                row = {'state': state, 'colouring': ''.join(str(colour[v]) for v in vertices)}
                rows[state] = row; out.write(json.dumps(row, separators=(',', ':')) + '\n'); out.flush()
                need(stream.stat().st_size <= plan['raw_output_bytes'], 'raw output bound')
                solver.add_clause([-var(v, colour[v]) for v in q])
            if status is None:
                status = 'STATE_CAP'
            reports[name] = {'status': status, 'states': len(rows), 'seconds': time.monotonic() - t, 'solver_stats': solver.accum_stats()}
        (args.out / 'progress.json').write_text(json.dumps(reports, indent=2) + '\n')
        if status != 'ENUMERATION_UNSAT_UNCERTIFIED':
            print(json.dumps(reports)); return
        base.extend([[-var(v, int(c)) for v, c in zip(q, s)] for s in sorted(rows)])
        raw = dimacs(4 * len(vertices), base)
        cnf = args.out / (name + '_complete.cnf'); cnf.write_bytes(raw)
        proof = args.out / (name + '_complete.drat')
        with (args.out / (name + '_kissat.log')).open('wb') as log:
            result = subprocess.run([args.kissat, '--seed=0', '--conflicts=2000000', '--time=120', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=native_limits)
        need(result.returncode == 20, 'proof solver UNSAT')
        logpath = args.out / (name + '_drat.log')
        with logpath.open('wb') as log:
            result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=native_limits)
        need(result.returncode == 0 and b's VERIFIED' in logpath.read_bytes().splitlines(), 'checked exhaustion')
        reports[name]['status'] = 'COMPLETE_DRAT_VERIFIED'
        certificate['blocks'][name] = {'vertices': vertices, 'states': [rows[s] for s in sorted(rows)]}
        (args.out / 'progress.json').write_text(json.dumps(reports, indent=2) + '\n')
    (args.out / 'certificate.json').write_text(json.dumps(certificate, indent=2, sort_keys=True) + '\n')
    need({r['state'] for r in certificate['blocks']['full']['states']} <= {r['state'] for r in certificate['blocks']['mandatory']['states']}, 'monotonicity')
    print(json.dumps(reports, sort_keys=True))


if __name__ == '__main__':
    main()
