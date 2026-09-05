#!/usr/bin/env python3
"""One bounded 24-case milestone, with atomic checkpoints and proof replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import importlib.util
import json
import os
import resource
import subprocess
import sys
import threading
import time
from itertools import combinations

import audit
import model


def atomic(path, value):
    temporary = path.with_suffix(path.suffix + '.partial')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def inspect_candidate(log, destination):
    values = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for token in line.split()[1:]:
                lit = int(token)
                if lit:
                    model.require(abs(lit) not in values or values[abs(lit)] == (lit > 0), 'inconsistent SAT model')
                    values[abs(lit)] = lit > 0
    model.require(all(v in values for v in range(1, 344)), 'incomplete SAT model')
    ids = audit.pair_ids()
    edges = [e for e in combinations(range(43), 2)
             if (values[ids[e]] if e in ids else e[0]//3 < 4)]
    destination.write_text(f'43 {len(edges)}\n'+''.join(f'{a} {b}\n' for a, b in edges))
    spec = importlib.util.spec_from_file_location('literal_graph_verifier', model.PREVIOUS / 'verify_graph.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.inspect(destination)
    model.require(report['vertices'] == 43 and report['ramsey'], 'candidate failed literal verifier')
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--kissat', required=True, type=Path)
    parser.add_argument('--drat-trim', required=True, type=Path)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--solve-seconds', type=int, default=30)
    parser.add_argument('--replay-seconds', type=int, default=120)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    model.require(not work.is_relative_to(model.ROOT.parent), 'generated work must be outside Git')
    model.require(1 <= args.workers <= 4 and min(args.solve_seconds, args.replay_seconds) > 0, 'invalid bounds')
    work.mkdir(parents=True, exist_ok=True)
    model.require(args.resume or not (work / 'contract.json').exists(), 'use a fresh directory or --resume')
    start = time.monotonic()
    preflight = audit.audit()
    atomic(work / 'audit.json', preflight)
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    contract = {'format': 'r55-k10-phase-sweep-v1', 'workers': args.workers,
                'solve_seconds': args.solve_seconds, 'replay_seconds': args.replay_seconds,
                'python': sys.version.split()[0], 'kissat': model.file_info(kissat),
                'drat_trim': model.file_info(drat),
                'source': {name: model.file_info(model.ROOT / name)
                           for name in ('model.py', 'audit.py', 'run.py', 'dependencies.json')}}
    if args.resume and (work / 'contract.json').exists():
        model.require(json.loads((work / 'contract.json').read_text()) == contract, 'resume contract changed')
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(model.PARENT / 'generate.py'), '--red-cycles', '4', '--output', str(base)], check=True)
    model.require(model.file_info(base)['sha256'] == model.BASE_SHA, 'parent formula mismatch')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(model.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    atomic(work / 'contract.json', contract)
    print('PASS complete parent reconstruction and 24-case cover', flush=True)
    stop = threading.Event()
    rows = {}

    def one(case):
        index = case['index']
        row = dict(case, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        prefix = f'case_{index:02}'
        cnf, proof = work / (prefix+'.cnf'), work / (prefix+'.drat')
        log, replay = work / (prefix+'.solve.log'), work / (prefix+'.replay.log')
        checkpoint = work / (prefix+'.json')
        try:
            model.generate(base, cnf, case)
            row['formula'] = audit.check_formula(base, cnf, case)
            old = json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else None
            if old is not None:
                model.require(all(old[k] == case[k] for k in case) and old['formula'] == row['formula'], 'resume case changed')
                if old['status'] == 'open':
                    return old
            if old is not None and old['status'] == 'excluded':
                model.require(model.file_info(proof) == old['proof'], 'resume proof changed')
                row.update(solver_code=20, solve_seconds=old['solve_seconds'], proof=old['proof'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    process = subprocess.run([str(kissat), f'--time={args.solve_seconds}', str(cnf), str(proof)],
                                             stdout=stream, stderr=subprocess.STDOUT, timeout=args.solve_seconds+60)
                row.update(solver_code=process.returncode, solve_seconds=round(time.monotonic()-before, 6), proof=model.file_info(proof))
            if row['solver_code'] == 20:
                before = time.monotonic()
                with replay.open('w') as stream:
                    process = subprocess.run([str(drat), str(cnf), str(proof), '-t', str(args.replay_seconds)],
                                             stdout=stream, stderr=subprocess.STDOUT, timeout=args.replay_seconds+60)
                model.require(process.returncode == 0 and 's VERIFIED' in replay.read_text(), 'DRAT replay failed')
                row.update(status='excluded', replay_code=process.returncode, replay_seconds=round(time.monotonic()-before, 6))
            elif row['solver_code'] == 0:
                row['status'] = 'open'
            elif row['solver_code'] == 10:
                row.update(status='target_graph_verified', graph=inspect_candidate(log, work / (prefix+'.edges')))
                stop.set()
            else:
                raise ValueError('unexpected solver code')
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
                  'complete_bounded_sweep': len(excluded)+len(opened) == 24,
                  'all_cases_excluded': len(excluded) == 24,
                  'target_graph_found': any(r['status'] == 'target_graph_verified' for r in rows.values()),
                  'elapsed_seconds': round(time.monotonic()-start, 6),
                  'largest_child_maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(args.workers) as pool:
        futures = [pool.submit(one, case) for case in model.cases()]
        for future in as_completed(futures):
            row = future.result()
            rows[row['index']] = row
            report = save()
            print(json.dumps({k: row[k] for k in ('index', 'phase', 'anchor', 'status')}), flush=True)
    final = save()
    model.require(not any(r['status'] == 'error' for r in rows.values()), 'case error: inspect checkpoint')
    print('FINISHED '+json.dumps({k: final[k] for k in ('excluded_indices', 'open_indices', 'complete_bounded_sweep', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
