#!/usr/bin/env python3
"""Bounded, restartable sweep; an exclusion is recorded only after DRAT replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import threading
import time

import audit
from verify_graph import inspect


def file_info(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            digest.update(data)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.partial')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def decode_candidate(log, destination):
    assignment = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for word in line.split()[1:]:
                literal = int(word)
                if literal:
                    variable = abs(literal)
                    audit.require(variable not in assignment or assignment[variable] == (literal > 0), 'inconsistent model')
                    assignment[variable] = literal > 0
    audit.require(all(v in assignment for v in range(1, 344)), 'incomplete primary model')
    ids = audit.orbit_edge_ids()
    red = [edge for edge in combinations(range(43), 2)
           if (assignment[ids[edge]] if edge in ids else edge[0] // 3 < 4)]
    destination.write_text(f'43 {len(red)}\n' + ''.join(f'{u} {v}\n' for u, v in red))
    result = inspect(destination)
    audit.require(result['vertices'] == 43 and result['ramsey'], 'SAT candidate failed direct Ramsey check')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--solve-seconds', type=int, default=30)
    parser.add_argument('--replay-seconds', type=int, default=120)
    parser.add_argument('--resume', action='store_true', help='retain completed bounded cases; replay cached exclusions')
    args = parser.parse_args()
    work = args.work.resolve()
    audit.require(not work.is_relative_to(audit.ROOT.parent), 'work directory must be outside Git')
    audit.require(1 <= args.workers <= 4 and args.solve_seconds > 0 and args.replay_seconds > 0, 'invalid bounds')
    work.mkdir(parents=True, exist_ok=True)
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    start = time.monotonic()
    contract = {'format': 'r55-order3-k10-anchor-sweep-v1', 'workers': args.workers,
                'solver_seconds_per_cube': args.solve_seconds, 'replay_seconds_per_cube': args.replay_seconds,
                'kissat': file_info(kissat), 'drat_trim': file_info(drat), 'python': sys.version.split()[0],
                'audit': audit.audit(), 'source': {name: file_info(audit.ROOT / name)
                for name in ('audit.py', 'sweep.py', 'verify_graph.py', 'parent_manifest.json')}}
    print('PASS preflight ' + json.dumps(contract['audit'], sort_keys=True), flush=True)
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(audit.PARENT / 'generate.py'), '--red-cycles', '4', '--output', str(base)], check=True)
    audit.require(file_info(base)['sha256'] == audit.BASE_SHA256, 'wrong parent formula')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(audit.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    contract['base'] = file_info(base)
    atomic_json(work / 'contract.json', contract)
    weights = audit.load_weights()
    stop = threading.Event()

    def one(index):
        if stop.is_set() or (work / 'STOP').exists():
            return {'index': index, 'status': 'not_started'}
        cnf = work / f'cube_{index:02}.cnf'
        proof = work / f'cube_{index:02}.drat'
        solve_log = work / f'cube_{index:02}.solve.log'
        replay_log = work / f'cube_{index:02}.replay.log'
        checkpoint = work / f'cube_{index:02}.json'
        row = {'index': index, 'weights': weights[index], 'status': 'pending'}
        try:
            units = [(1 + 3 * j + t) * (1 if t < w else -1)
                     for j, w in enumerate(weights[index]) for t in range(3)]
            with base.open('rb') as source, cnf.open('wb') as destination:
                source.readline()
                destination.write(audit.CUBE_HEADER)
                shutil.copyfileobj(source, destination)
                destination.write(''.join(f'{x} 0\n' for x in units).encode())
            row['formula'] = audit.check_cube(base, cnf, index)
            old = json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else None
            if old is not None:
                audit.require(old['formula'] == row['formula'] and old['weights'] == row['weights'], 'resume case mismatch')
                if old['status'] == 'open':
                    return old
            if old is not None and old['status'] == 'excluded':
                audit.require(file_info(proof) == old['proof'], 'resume proof mismatch')
                row.update(solver_code=20, solve_seconds=old['solve_seconds'], proof=old['proof'], reused_proof=True)
            else:
                before = time.monotonic()
                with solve_log.open('w') as log:
                    process = subprocess.run([str(kissat), f'--time={args.solve_seconds}', str(cnf), str(proof)],
                                             stdout=log, stderr=subprocess.STDOUT, timeout=args.solve_seconds + 60)
                row.update(solver_code=process.returncode, solve_seconds=round(time.monotonic() - before, 6), proof=file_info(proof))
            if row['solver_code'] == 20:
                before = time.monotonic()
                with replay_log.open('w') as log:
                    process = subprocess.run([str(drat), str(cnf), str(proof), '-t', str(args.replay_seconds)],
                                             stdout=log, stderr=subprocess.STDOUT, timeout=args.replay_seconds + 60)
                row.update(replay_code=process.returncode, replay_seconds=round(time.monotonic() - before, 6))
                audit.require(process.returncode == 0 and 's VERIFIED' in replay_log.read_text(), 'UNSAT replay failed')
                row['status'] = 'excluded'
            elif row['solver_code'] == 0:
                row['status'] = 'open'
            elif row['solver_code'] == 10:
                row['graph'] = decode_candidate(solve_log, work / f'candidate_{index:02}.edges')
                row['status'] = 'target_graph_verified'
                stop.set()
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic_json(checkpoint, row)
        return row

    rows = {}

    def save():
        excluded = sorted(i for i, row in rows.items() if row['status'] == 'excluded')
        open_ids = sorted(i for i, row in rows.items() if row['status'] == 'open')
        complete = len(excluded) + len(open_ids) == 98
        report = {'contract': contract, 'cases': [rows[i] for i in sorted(rows)],
                  'complete_bounded_sweep': complete, 'excluded_indices': excluded, 'open_indices': open_ids,
                  'all_98_cubes_excluded': len(excluded) == 98,
                  'target_graph_found': any(row['status'] == 'target_graph_verified' for row in rows.values()),
                  'elapsed_seconds': round(time.monotonic() - start, 6),
                  'largest_child_maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        atomic_json(work / 'sweep.json', report)
        return report

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(one, index): index for index in range(98)}
        for future in as_completed(futures):
            row = future.result()
            rows[row['index']] = row
            report = save()
            print(json.dumps({'index': row['index'], 'status': row['status'], 'excluded': len(report['excluded_indices']),
                              'open': len(report['open_indices']), 'error': row.get('error')}, sort_keys=True), flush=True)
    final = save()
    audit.require(not any(row['status'] == 'error' for row in rows.values()), 'sweep has errors; inspect case checkpoints')
    print('FINISHED ' + json.dumps({key: final[key] for key in ('complete_bounded_sweep', 'all_98_cubes_excluded',
                                                               'target_graph_found', 'elapsed_seconds')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
