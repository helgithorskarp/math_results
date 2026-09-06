#!/usr/bin/env python3
"""Frozen 77-profile pilot. Raw CNFs/models/logs stay in a new local output dir."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GRAPH_SHA = 'ec389ca801d42ff3c7661c8df5eb2a017e44b139a979d4545b9e2dc458e50177'


def load(p):
    return json.loads(p.read_text())


def save(p, x):
    p.write_text(json.dumps(x, indent=2) + '\n')


def module(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def check(c, edges):
    if len(c) != 514 or not set(c) <= set('.0123'):
        raise ValueError('colour domain')
    if any(c[u] != '.' and c[v] != '.' and c[u] == c[v] for u,v in edges):
        raise ValueError('improper colour witness')
    return [i for i,x in enumerate(c) if x == '.']


def worker(cnf, out):
    # Applied before the solver import; one process and fresh solver per graph.
    plan = load(HERE/'plan.json')
    cap = plan['bounds']['worker_address_space_bytes']
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    import pysat
    from pysat.formula import CNF
    from pysat.solvers import Cadical195
    formula = CNF(from_file=str(cnf)); start = time.monotonic()
    with Cadical195(bootstrap_with=formula.clauses) as s:
        s.conf_budget(plan['bounds']['conflicts_per_candidate'])
        answer = s.solve_limited()
        result = dict(status='SAT' if answer is True else 'UNSAT' if answer is False else 'UNKNOWN',
                      seconds=time.monotonic()-start, stats=s.accum_stats(),
                      model=s.get_model() if answer is True else None,
                      solver='CaDiCaL 1.9.5', python_sat=pysat.__version__,
                      maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save(out, result)


def run(graph, out):
    plan = load(HERE/'plan.json'); raw_candidates = (HERE/'candidates.json').read_bytes()
    if sha256(raw_candidates).hexdigest() != plan['candidate_sha256']:
        raise ValueError('frozen candidates changed')
    candidates = json.loads(raw_candidates)
    raw_graph = graph.read_bytes()
    if sha256(raw_graph).hexdigest() != GRAPH_SHA:
        raise ValueError('exact graph packet digest')
    lines = raw_graph.decode('ascii').splitlines()
    if lines[0] != '514 2526': raise ValueError('graph dimensions')
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    adj = [set() for _ in range(514)]
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    compiler = module('path_compiler', REPO/'hadwiger_nelson_heule514_path_projection/compile.py')
    relation = module('path_relation', REPO/'hadwiger_nelson_heule514_path_projection/relation.py')
    kernel = load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')
    out.mkdir(exist_ok=False); rows = []; certificates = []; start = time.monotonic()
    for candidate in candidates:
        i = candidate['index']; omitted = set(candidate['omitted'])
        row = dict(index=i, omitted=sorted(omitted), profile=candidate['profile'])
        remaining = plan['bounds']['total_pilot_wall_seconds']-(time.monotonic()-start)
        if remaining <= 0:
            row['status'] = 'UNQUERIED'; rows.append(row); continue
        n, clauses = compiler.build(edges, omitted, kernel)
        raw = compiler.dimacs(n, clauses); cnf = out/f'{i:02d}.cnf'
        cnf.write_bytes(raw)
        row.update(variables=n, clauses=len(clauses), cnf_bytes=len(raw), cnf_sha256=sha256(raw).hexdigest())
        answer_file = out/f'{i:02d}.model.json'
        t = time.monotonic()
        with (out/f'{i:02d}.log').open('w') as log:
            try:
                process = subprocess.run([sys.executable, '-B', str(HERE/'pilot.py'), '--worker', str(cnf), '--answer', str(answer_file)],
                                         stdout=log, stderr=subprocess.STDOUT,
                                         timeout=min(remaining, plan['bounds']['worker_wall_seconds']))
                if process.returncode:
                    row.update(status='UNKNOWN', reason='worker_error', returncode=process.returncode)
                else:
                    answer = load(answer_file)
                    row.update({k:v for k,v in answer.items() if k != 'model'})
                    row['model_file_sha256'] = sha256(answer_file.read_bytes()).hexdigest()
            except subprocess.TimeoutExpired:
                row.update(status='UNKNOWN', reason='wall_limit')
        row['worker_wall_seconds'] = time.monotonic()-t
        if row['status'] == 'SAT':
            truth = set(x for x in answer['model'] if x > 0)
            if not all(any((x in truth) if x > 0 else (-x not in truth) for x in clause) for clause in clauses):
                raise ValueError('invalid native model')
            c = ['.']*514
            for v in range(510):
                if v not in omitted:
                    c[v] = str(min(colour for colour in range(4) if 4*v+colour+1 in truth))
            lists = [sum(1 << colour for colour in range(3)
                         if all(c[v] != str(colour+1) for v in nb)) for nb in compiler.NEIGHBOURS]
            mask = sum(1 << j for j in range(4) if 510+j not in omitted)
            tail = relation.extension(mask, lists)
            if tail is None: raise ValueError('projection decoding failed')
            for j,x in enumerate(tail):
                if x >= 0: c[510+j] = str(x+1)
            if check(c, edges) != sorted(omitted): raise ValueError('candidate omission mismatch')
            candidate_colour = ''.join(c); fills = []
            while True:
                changed = False
                for v in sorted(omitted):
                    if c[v] != '.': continue
                    allowed = [str(x) for x in range(4) if all(c[u] != str(x) for u in adj[v])]
                    if allowed:
                        c[v] = allowed[0]; fills.append([v, c[v]]); changed = True
                if not changed: break
            D = check(c, edges)
            certificates.append(dict(index=i, candidate_colouring=candidate_colour,
                                     fills=fills, D=D, colouring=''.join(c)))
            row['final_omissions'] = D
        rows.append(row)
        save(out/'transcript.json', rows); save(out/'certificate.json', certificates)
        print(json.dumps(dict(index=i,status=row['status'],D=row.get('final_omissions'),seconds=row['worker_wall_seconds'])), flush=True)
        if row['status'] == 'UNSAT':
            for rest in candidates[i+1:]:
                rows.append(dict(index=rest['index'],omitted=rest['omitted'],profile=rest['profile'],status='UNQUERIED'))
            break
    save(out/'transcript.json', rows); save(out/'certificate.json', certificates)
    result = dict(status_counts=dict(Counter(r['status'] for r in rows)),
                  seconds=time.monotonic()-start, target_queries=sum(r['status']!='UNQUERIED' for r in rows),
                  positive_witnesses=len(certificates), candidate_sha256=plan['candidate_sha256'],
                  unique_positive_cuts=len({tuple(r['D']) for r in certificates}),
                  graph_sha256=GRAPH_SHA, record_improvement=False)
    save(out/'result.json', result); print(json.dumps(result), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--graph',type=Path);p.add_argument('--out',type=Path)
    p.add_argument('--worker',type=Path);p.add_argument('--answer',type=Path);a=p.parse_args()
    if a.worker: worker(a.worker, a.answer)
    else: run(a.graph,a.out)
