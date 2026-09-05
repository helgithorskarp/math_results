#!/usr/bin/env python3
"""One bounded obstruction-side extraction; negative results remain provisional."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import os
import resource
import time
from pysat.solvers import Solver
import activation
import argparse

PACKAGE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--work', type=Path, required=True)
args = ap.parse_args()
HERE = args.work.resolve()
HERE.mkdir(parents=True, exist_ok=True)


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


plan = dict(initial_omitted_global_vertex=374, conflicts_per_query=100000, maximum_queries=304, cumulative_native_seconds=150)
assert not (HERE / 'extraction.json').exists()
source, U = activation.input_data()
rows, meta = activation.encode(source)
raw = activation.dimacs(rows, meta['variables'])
(HERE / 'activation.cnf').write_bytes(raw)
X = set(range(len(U))) - {U.index(plan['initial_omitted_global_vertex'])}
state = dict(status='running', started_at=now(), worker_pid=os.getpid(),
             source_sha256=sha256(raw).hexdigest(), queries=[],
             selected_labels=[U[v] for v in sorted(X)],
             native_seconds=0.0, deletion_colourings={},
             independently_certified_noncolourability=False,
             target_record_established=False)
save(HERE / 'active_job.json', dict(status='bounded extraction running', pid=os.getpid()))
started = time.monotonic()
with Solver(name='cadical195', bootstrap_with=rows, use_timer=True) as solver:
    def query(selected, removed=None):
        solver.conf_budget(plan['conflicts_per_query'])
        before = time.monotonic()
        truth = solver.solve_limited(assumptions=[v+1 for v in sorted(selected)])
        row = dict(query=len(state['queries']), removed_global=removed,
                   selected_count=len(selected), truth=truth,
                   solver_seconds=solver.time(), wall_seconds=time.monotonic()-before)
        core = None
        if truth is True:
            colouring = activation.decode(source, meta, solver.get_model(), selected)
            row['colouring'] = colouring
            if removed is not None:
                state['deletion_colourings'][str(removed)] = colouring
        elif truth is False:
            literals = solver.get_core()
            assert literals and len(set(literals)) == len(literals)
            assert all(v > 0 and v-1 in selected for v in literals)
            core = {v-1 for v in literals}
            row['core_labels'] = [U[v] for v in sorted(core)]
        state['queries'].append(row)
        state['native_seconds'] = solver.time_accum()
        state['updated_at'] = now()
        save(HERE / 'extraction.json', state)
        print(json.dumps({k:v for k,v in row.items() if k not in ['core_labels','colouring']}), flush=True)
        return truth, core

    truth, core = query(X)
    if truth is not False:
        state['status'] = 'seed colourable' if truth else 'seed query unknown'
    else:
        X = core
        state['selected_labels'] = [U[v] for v in sorted(X)]
        state['status'] = 'provisional non-four-colourable core'
        save(HERE / 'extraction.json', state)
        order = sorted(X, key=lambda v:(U[v] >= 509, U[v]))
        for v in order:
            if v not in X:
                continue
            if (len(state['queries']) >= plan['maximum_queries'] or
                    state['native_seconds'] >= plan['cumulative_native_seconds']):
                state['status'] = 'bounded extraction checkpoint; minimality unproved'
                break
            truth, core = query(X - {v}, U[v])
            if truth is False:
                X = core
                state['selected_labels'] = [U[w] for w in sorted(X)]
                save(HERE / 'extraction.json', state)
        else:
            state['status'] = 'single deletion pass completed'
        state['pool_relative_minimality_witnesses_complete'] = all(
            str(U[v]) in state['deletion_colourings'] for v in X)
        state['vertices_with_L'] = 374 + len(X)
        state['added_Q5'] = sum(U[v] >= 509 for v in X)
        state['omitted_S'] = [v for v in range(374,509) if v not in state['selected_labels']]
state.update(completed_at=now(), wall_seconds=time.monotonic()-started,
             peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             background_jobs=0)
save(HERE / 'extraction.json', state)
save(HERE / 'active_job.json', dict(status='none; bounded extraction completed', pid=None,
                                  result='extraction.json'))
print(json.dumps({k:v for k,v in state.items() if k not in ['queries','deletion_colourings','selected_labels']},
                 indent=2, sort_keys=True), flush=True)
