#!/usr/bin/env python3
"""One bounded four-case decision checkpoint; incomplete search is OPEN."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import resource
import subprocess
import sys
import threading
import time

import extension_model as ext
import check_layer
import run as phase_run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--kissat', required=True, type=Path)
    parser.add_argument('--drat-trim', required=True, type=Path)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--solve-seconds', type=int, default=120)
    parser.add_argument('--replay-seconds', type=int, default=120)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    require, info, atomic = ext.parent.require, ext.parent.file_info, phase_run.atomic
    require(not work.is_relative_to(ext.ROOT.parent), 'generated work must be outside Git')
    require(1 <= args.workers <= 4 and min(args.solve_seconds, args.replay_seconds) > 0,
            'invalid resource limits')
    work.mkdir(parents=True, exist_ok=True)
    require(args.resume or not (work / 'contract.json').exists(), 'fresh directory or --resume required')
    start = time.monotonic()
    atomic(work / 'audit.json', check_layer.preflight())
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    contract = {'format': 'r55-k10-signature-propagation-v1', 'workers': args.workers,
                'solve_seconds': args.solve_seconds, 'replay_seconds': args.replay_seconds,
                'python': sys.version.split()[0], 'kissat': info(kissat), 'drat_trim': info(drat),
                'source': {name: info(ext.ROOT / name) for name in
                           ('extension_model.py', 'check_layer.py', 'solve.py', 'dependencies.json')}}
    if args.resume and (work / 'contract.json').exists():
        require(json.loads((work / 'contract.json').read_text()) == contract, 'resume contract changed')
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(ext.parent.PARENT / 'generate.py'),
                        '--red-cycles', '4', '--output', str(base)], check=True)
    require(info(base)['sha256'] == ext.parent.BASE_SHA, 'parent formula changed')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(ext.parent.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    atomic(work / 'contract.json', contract)
    print('PASS complete parent reconstruction and twelve-unit consequence', flush=True)
    stop = threading.Event()
    rows = {}

    def one(case):
        row = dict(case, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        prefix = f"case_{case['index']:02}"
        cnf, proof = work / (prefix+'.cnf'), work / (prefix+'.drat')
        log, replay = work / (prefix+'.solve.log'), work / (prefix+'.replay.log')
        checkpoint = work / (prefix+'.json')
        try:
            ext.generate(base, cnf, case)
            row['formula'] = check_layer.check_formula(base, cnf, case)
            old = json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else None
            if old is not None:
                require(all(old[k] == case[k] for k in case) and old['formula'] == row['formula'],
                        'resume case changed')
                if old['status'] == 'open':
                    return old
            if old is not None and old['status'] == 'excluded':
                require(info(proof) == old['proof'], 'resume proof changed')
                row.update(solver_code=20, solve_seconds=old['solve_seconds'], proof=old['proof'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    process = subprocess.run([str(kissat), f'--time={args.solve_seconds}', str(cnf), str(proof)],
                                             stdout=stream, stderr=subprocess.STDOUT,
                                             timeout=args.solve_seconds+60)
                row.update(solver_code=process.returncode, solve_seconds=round(time.monotonic()-before, 6),
                           proof=info(proof))
            if row['solver_code'] == 20:
                before = time.monotonic()
                with replay.open('w') as stream:
                    process = subprocess.run([str(drat), str(cnf), str(proof), '-t', str(args.replay_seconds)],
                                             stdout=stream, stderr=subprocess.STDOUT,
                                             timeout=args.replay_seconds+60)
                require(process.returncode == 0 and 's VERIFIED' in replay.read_text(), 'DRAT replay failed')
                row.update(status='excluded', replay_code=0, replay_seconds=round(time.monotonic()-before, 6))
            elif row['solver_code'] == 0:
                require('s UNKNOWN' in log.read_text(), 'timeout lacks explicit UNKNOWN')
                row['status'] = 'open'
            elif row['solver_code'] == 10:
                row.update(status='target_graph_verified',
                           graph=phase_run.inspect_candidate(log, work / (prefix+'.edges')))
                stop.set()
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
                  'complete_bounded_sweep': len(excluded)+len(opened) == 4,
                  'all_cases_excluded': len(excluded) == 4,
                  'target_graph_found': any(r['status'] == 'target_graph_verified' for r in rows.values()),
                  'elapsed_seconds': round(time.monotonic()-start, 6),
                  'largest_child_maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(args.workers) as pool:
        futures = [pool.submit(one, c) for c in ext.cases()]
        for future in as_completed(futures):
            row = future.result()
            rows[row['index']] = row
            save()
            print(json.dumps({k: row[k] for k in ('index', 'anchor', 'status')}), flush=True)
    final = save()
    require(not any(r['status'] == 'error' for r in rows.values()), 'case error: inspect checkpoint')
    print('FINISHED '+json.dumps({k: final[k] for k in
          ('excluded_indices', 'open_indices', 'complete_bounded_sweep', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
