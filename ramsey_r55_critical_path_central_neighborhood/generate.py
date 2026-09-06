"""Two fixed-density necessary central-neighborhood decisions, no ordering."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

PARENT = Path(__file__).resolve().parent
from encoding import CounterEncoder


def need(ok, text):
    if not ok:
        raise ValueError(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(density):
    need(density in (92, 93), 'density domain')
    fixed = {(u, v): False for u in range(2) for v in range(u + 1, 10)}
    for bit, e in enumerate(it.combinations(range(2, 10), 2)):
        fixed[e] = not bool(5388912 >> bit & 1)
    for v in range(10, 20):
        fixed[0, v] = v < 14 or v >= 18
        fixed[1, v] = v >= 14
    edges = [e for e in it.combinations(range(20), 2) if e not in fixed]
    index = {e: i + 1 for i, e in enumerate(edges)}
    need((len(fixed), sum(fixed.values()), len(edges)) == (65, 30, 125), 'fixed interface')
    rows = set()
    census = {}
    for color, size in ((True, 4), (False, 5)):
        count = 0
        for vertices in it.combinations(range(20), size):
            pairs = list(it.combinations(vertices, 2))
            if any(fixed[e] != color for e in pairs if e in fixed):
                continue
            rows.add(tuple(sorted((-1 if color else 1) * index[e] for e in pairs if e in index)))
            count += 1
        census['red_K4' if color else 'blue_K5'] = count
    enc = CounterEncoder(len(edges), sorted(rows, key=lambda r: (len(r), r)))
    base = len(enc.clauses)
    enc.interval(list(range(1, 126)), density - 30, density - 30)
    return fixed, edges, enc, dict(density=density, base_clauses=base,
                                  possible_clique_counts=census, fixed_red=30,
                                  fixed_pairs=65, primary_variables=125,
                                  variable_red_sum=density-30, ordering='none')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--seconds', type=int, default=90)
    p.add_argument('--emit-only', action='store_true')
    a = p.parse_args()
    need(a.seconds > 0, 'positive cap')
    need(sha(PARENT / 'encoding.py') == '902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd', 'encoding identity')
    a.work.mkdir(exist_ok=False)
    for density in (92, 93):
        start = time.monotonic()
        work = a.work / str(density)
        work.mkdir()
        fixed, edges, enc, report = build(density)
        cnf = work / 'case.cnf'
        with cnf.open('x') as f:
            f.write(f'p cnf {enc.variables} {len(enc.clauses)}\n')
            for row in enc.clauses:
                f.write(' '.join(map(str, row)) + ' 0\n')
        report.update(status='EMITTED', variables=enc.variables, clauses=len(enc.clauses),
                      formula_sha256=sha(cnf), formula_bytes=cnf.stat().st_size,
                      source_sha256=sha(Path(__file__)), solver_cap_seconds=a.seconds,
                      encoding_sha256=sha(PARENT / 'encoding.py'),
                      build_seconds=time.monotonic()-start)

        def save():
            (work / 'result.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
            print(json.dumps(report), flush=True)

        save()
        if a.emit_only:
            continue
        log, trace = work / 'solver.log', work / 'trace.drat'
        t = time.monotonic()
        with log.open('x') as f:
            try:
                code = subprocess.run([str(a.kissat), f'--time={a.seconds}', str(cnf), str(trace)],
                                      stdout=f, stderr=subprocess.STDOUT, timeout=a.seconds+30).returncode
            except subprocess.TimeoutExpired:
                code = None
        report.update(solver_exit=code, solver_seconds=time.monotonic()-t,
                      status={0:'UNKNOWN', 10:'SAT_UNCHECKED', 20:'UNSAT_UNCHECKED'}.get(code, 'ERROR'),
                      solver_sha256=sha(a.kissat), max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        if code == 10:
            values = {}
            for row in log.read_text().splitlines():
                if row.startswith('v '):
                    for token in row.split()[1:]:
                        l = int(token)
                        if l:
                            need(abs(l) not in values or values[abs(l)] == (l > 0), 'model consistency')
                            values[abs(l)] = l > 0
            need(set(values) == set(range(1, enc.variables+1)), 'complete model')
            need(all(any(values[abs(l)] == (l > 0) for l in row) for row in enc.clauses), 'model clauses')
            red = {e for e, c in fixed.items() if c} | {e for i, e in enumerate(edges, 1) if values[i]}
            graph = work / 'graph.json'
            graph.write_text(json.dumps(dict(n=20, red_edges=sorted(red)), indent=2, sort_keys=True)+'\n')
            report.update(status='SAT_MODEL_CHECKED_GRAPH_PENDING_AUDIT', graph_sha256=sha(graph))
        report.update(total_seconds=time.monotonic()-start, trace_bytes=trace.stat().st_size,
                      trace_sha256=sha(trace), log_sha256=sha(log),
                      trace_is_checked_refutation=False, trace_is_solver_restart_state=False)
        save()


if __name__ == '__main__':
    main()
