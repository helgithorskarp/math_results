#!/usr/bin/env python3
"""Complete bounded 18-action decision, with full formula and proof checks."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import os
import resource
import subprocess
import sys
import threading
import time

import model
import inspect_graph


def atomic(path, data):
    temp = path.with_suffix(path.suffix+'.partial')
    with temp.open('w') as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def candidate(case, log, destination):
    values = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for token in line.split()[1:]:
                lit = int(token)
                if lit:
                    model.require(abs(lit) not in values or values[abs(lit)] == (lit > 0), 'inconsistent SAT model')
                    values[abs(lit)] = lit > 0
    ids = model.edge_orbits(case)
    model.require(all(v in values for v in ids.values()), 'incomplete SAT model')
    edges = [e for e, v in ids.items() if values[v]]
    destination.write_text(f'43 {len(edges)}\n'+''.join(f'{a} {b}\n' for a, b in edges))
    result = inspect_graph.inspect(destination)
    model.require(result['vertices'] == 43 and result['ramsey'], 'literal candidate verification failed')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--kissat', required=True, type=Path)
    parser.add_argument('--drat-trim', required=True, type=Path)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--solve-seconds', type=int, default=60)
    parser.add_argument('--replay-seconds', type=int, default=180)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    model.require(not work.is_relative_to(model.ROOT.parent), 'generated files outside Git')
    model.require(1 <= args.workers <= 4 and min(args.solve_seconds, args.replay_seconds) > 0, 'resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    model.require(args.resume or not (work / 'contract.json').exists(), 'fresh work or --resume required')
    start = time.monotonic()
    atomic(work / 'classification.json', model.classify())
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    contract = {'format': 'r55-c3-square-sweep-v1', 'python': sys.version.split()[0], 'workers': args.workers,
                'solve_seconds': args.solve_seconds, 'replay_seconds': args.replay_seconds,
                'kissat': model.info(kissat), 'drat_trim': model.info(drat),
                'sources': {n: model.info(model.ROOT / n) for n in
                            ('model.py', 'check_formula.cpp', 'run.py', 'inspect_graph.py')}}
    if args.resume and (work / 'contract.json').exists():
        model.require(json.loads((work / 'contract.json').read_text()) == contract, 'resume contract changed')
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(model.ROOT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    atomic(work / 'contract.json', contract)
    print('PASS 117 labeled multiplicities, 18 action classes, full projective S4 action', flush=True)
    stop = threading.Event()
    rows = {}

    def one(case):
        row = dict(case, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        stem = f"case_{case['index']:02}"
        cnf, proof = work / (stem+'.cnf'), work / (stem+'.drat')
        log, replay, check = [work / (stem+suffix) for suffix in ('.solve.log', '.replay.log', '.check.log')]
        checkpoint = work / (stem+'.json')
        try:
            before = time.monotonic()
            row['formula'] = model.generate(case, cnf)
            with check.open('w') as stream:
                subprocess.run([str(checker), *map(str, [case['a'], *case['b'], case['c']]), str(cnf)],
                               stdout=stream, stderr=subprocess.STDOUT, check=True)
            model.require(' PASS' in check.read_text(), 'missing formula audit')
            row['generation_check_seconds'] = round(time.monotonic()-before, 6)
            old = json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else None
            if old:
                model.require(all(old[k] == case[k] for k in case) and old['formula'] == row['formula'], 'resume case changed')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                model.require(model.info(proof) == old['proof'], 'resume proof changed')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(kissat), f'--time={args.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=args.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=model.info(proof),
                           solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                before = time.monotonic()
                with replay.open('w') as stream:
                    result = subprocess.run([str(drat), str(cnf), str(proof), '-t', str(args.replay_seconds)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=args.replay_seconds+60)
                model.require(result.returncode == 0 and 's VERIFIED' in replay.read_text(), 'proof replay failed')
                row.update(status='excluded', replay_seconds=round(time.monotonic()-before, 6), replay_code=0)
            elif row['solver_code'] == 10:
                row.update(status='target_graph_verified', graph=candidate(case, log, work / (stem+'.edges')))
                stop.set()
            elif row['solver_code'] == 0:
                model.require('s UNKNOWN' in log.read_text(), 'missing explicit UNKNOWN')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        excluded = sorted(i for i, r in rows.items() if r['status'] == 'excluded')
        opened = sorted(i for i, r in rows.items() if r['status'] == 'open')
        report = {'contract': contract, 'cases': [rows[i] for i in sorted(rows)],
                  'excluded_indices': excluded, 'open_indices': opened,
                  'complete_bounded_sweep': len(excluded)+len(opened) == 18,
                  'all_types_excluded': len(excluded) == 18,
                  'target_graph_found': any(r['status'] == 'target_graph_verified' for r in rows.values()),
                  'elapsed_seconds': round(time.monotonic()-start, 6),
                  'largest_child_maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(args.workers) as pool:
        futures = [pool.submit(one, c) for c in model.cases()]
        for future in as_completed(futures):
            row = future.result()
            rows[row['index']] = row
            save()
            print(json.dumps({k: row[k] for k in ('index', 'a', 'b', 'c', 'status')}), flush=True)
    report = save()
    model.require(not any(r['status'] == 'error' for r in rows.values()), 'case error; inspect checkpoint')
    print('FINISHED '+json.dumps({k: report[k] for k in
          ('excluded_indices', 'open_indices', 'complete_bounded_sweep', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
