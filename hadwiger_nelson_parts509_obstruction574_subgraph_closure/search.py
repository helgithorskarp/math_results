#!/usr/bin/env python3
"""One bounded fixed-H574 L-deletion audit; never shrinks the graph."""
import argparse
import json
from hashlib import sha256
from pathlib import Path
import resource
import time
from pysat.solvers import Solver
import pysat
from activation import load_graph, encode, decode, dimacs, require

HERE = Path(__file__).resolve().parent
WORK = None


def save(name, data):
    path = WORK / name
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    tmp.replace(path)


def main():
    global WORK
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    WORK = args.work.resolve()
    WORK.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    require(not (WORK/'audit.json').exists(), 'refuse to overwrite a started audit')
    plan = json.loads((HERE/'plan.json').read_text())
    require(pysat.__version__ == '1.8.dev24', 'PySAT version')
    resource.setrlimit(resource.RLIMIT_AS, (plan['memory_address_space_bytes'],)*2)
    labels, edges, cert = load_graph()
    require(plan['order'] == list(range(374)), 'frozen query order')
    rows, meta = encode(labels, edges, plan['order'], plan['symmetry_triangle'])
    cnf = dimacs(rows, meta['variables'])
    (WORK/'activation.cnf').write_bytes(cnf)
    results = []
    certificate = dict(labels=labels, deletions=[])
    state = dict(status='running', encoding_variables=meta['variables'], encoding_clauses=len(rows),
                 encoding_sha256=sha256(cnf).hexdigest(), solver='CaDiCaL 1.9.5',
                 pysat_version=pysat.__version__, order=plan['order'], queries=results,
                 fixed_graph_vertices=len(labels), positive_L_deletions=0,
                 negative_answers_independently_certified=False)
    with Solver(name='cadical195', bootstrap_with=rows, use_timer=True) as solver:
        for v in plan['order']:
            selected = set(labels)-{v}
            solver.conf_budget(plan['conflicts_per_query'])
            answer = solver.solve_limited(assumptions=[meta['activation'][w] for w in range(374) if w != v])
            native = solver.time()
            row = dict(vertex=v, status={True:'SAT', False:'UNSAT', None:'UNKNOWN'}[answer],
                       native_seconds=native)
            if answer is True:
                colours = decode(labels, edges, meta, solver.get_model(), selected)
                require(colours.count('.') == 1 and colours[v] == '.', 'deletion marker')
                certificate['deletions'].append(dict(vertex=v, colours=colours))
                state['positive_L_deletions'] += 1
            results.append(row)
            state.update(native_seconds=solver.time_accum(), wall_seconds=time.monotonic()-start,
                         maximum_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            save('certificate.json', certificate)
            save('audit.json', state)
            print(json.dumps(dict(query=len(results), **row, positives=state['positive_L_deletions'],
                                  cumulative_native_seconds=state['native_seconds'])), flush=True)
            if state['positive_L_deletions'] >= plan['stop_after_positive_L_deletions']:
                state['stop_reason'] = '309 positive L deletions reached'; break
            if state['native_seconds'] >= plan['native_seconds_stop_between_queries']:
                state['stop_reason'] = 'native budget reached between queries'; break
        else:
            state['stop_reason'] = 'all 374 L deletions attempted'
    state.update(status='completed', unattempted_vertices=plan['order'][len(results):],
                 forced_vertices_lower_bound=200+state['positive_L_deletions'],
                 wall_seconds=time.monotonic()-start)
    save('audit.json', state)
    print(json.dumps({k: v for k, v in state.items() if k not in ('queries', 'order')}, indent=2), flush=True)


if __name__ == '__main__':
    main()
