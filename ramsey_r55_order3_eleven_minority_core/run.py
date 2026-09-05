#!/usr/bin/env python3
"""Bounded full-extension test of all fourteen minority-core classes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import importlib.util
import json
import resource
import shutil
import subprocess
import sys
import threading
import time
import audit
import cores

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'ramsey_r55_order3_eleven_cycle_obstruction'
sys.path.insert(0, str(PARENT))
import generate as gen
spec = importlib.util.spec_from_file_location('parent_run', PARENT / 'run.py')
parent_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent_run)
atomic, replay = parent_run.atomic, parent_run.replay


def make_cube(parent, path, bits):
    variables = [1, 2, 3, 4, 5, 6, 31, 32, 33]
    with parent.open('rb') as source, path.open('wb') as dest:
        _, _, nv, nc = source.readline().split()
        dest.write(f'p cnf {int(nv)} {int(nc)+9}\n'.encode())
        shutil.copyfileobj(source, dest)
        for v, b in zip(variables, bits):
            dest.write(f'{v if b == "1" else -v} 0\n'.encode())
    return gen.info(path)


def sources():
    return {str(path.relative_to(ROOT.parent)): gen.info(path) for path in
            [ROOT / f for f in ('cores.py', 'audit.py', 'run.py')]+
            [PARENT / f for f in ('generate.py', 'check_formula.cpp', 'run.py', 'inspect_graph.py')]}


def prepare(work):
    cover = cores.cover()
    atomic(work / 'cover.json', cover)
    atomic(work / 'audit.json', audit.audit_cover(cover))
    parent = work / 'parent.cnf'
    p = subprocess.run([sys.executable, str(PARENT / 'generate.py'), '--red-cycles', '3',
                        '--output', str(parent)], capture_output=True, text=True, check=True)
    data = json.loads(p.stdout)
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    with (work / 'parent.check.log').open('w') as log:
        subprocess.run([str(checker), '3', str(parent)], stdout=log, stderr=subprocess.STDOUT, check=True)
    cores.require(' PASS' in (work / 'parent.check.log').read_text(), 'parent checker output')
    atomic(work / 'parent.json', data)
    return cover, parent, data


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--workers', type=int, default=2)
    p.add_argument('--solve-seconds', type=int, default=60)
    p.add_argument('--replay-seconds', type=int, default=300)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    work = a.work.resolve()
    cores.require(not work.is_relative_to(ROOT.parent), 'large evidence outside Git')
    cores.require(1 <= a.workers <= 2 and min(a.solve_seconds, a.replay_seconds) > 0, 'resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-k11-r3-core-sweep-v1', sources=sources(), python=sys.version.split()[0],
                    workers=a.workers, solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=gen.info(a.kissat), drat_trim=gen.info(a.drat_trim))
    if (work / 'contract.json').exists():
        cores.require(a.resume and json.loads((work / 'contract.json').read_text()) == contract, 'changed contract')
    atomic(work / 'contract.json', contract)
    cover, parent, parent_info = prepare(work)
    print('PASS fourteen-class cover and entire parent formula reconstruction', flush=True)
    stop, rows = threading.Event(), {}

    def one(case):
        index, bits = case['index'], case['bits']
        row = dict(index=index, bits=bits, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        checkpoint = work / f'c{index:02}.json'
        try:
            cnf, proof, log = [work / (f'c{index:02}'+suffix) for suffix in ('.cnf', '.drat', '.solve.log')]
            row['formula'] = make_cube(parent, cnf, bits)
            row['audit'] = audit.audit_cube(parent, cnf, bits)
            old = json.loads(checkpoint.read_text()) if a.resume and checkpoint.exists() else None
            if old:
                cores.require(old['bits'] == bits and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                cores.require(gen.info(proof) == old['proof'], 'changed proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode, solve_seconds=round(time.monotonic()-before, 6),
                           proof=gen.info(proof))
            if row['solver_code'] == 20:
                row['replay'] = replay(a.drat_trim, cnf, proof, work / f'c{index:02}.replay.log', a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = parent_run.candidate(3, log, work / f'c{index:02}.edges')
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                cores.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        data = dict(contract=contract, parent=parent_info, cases=[rows[i] for i in sorted(rows)],
                    excluded=sorted(i for i in rows if rows[i]['status'] == 'excluded'),
                    open=sorted(i for i in rows if rows[i]['status'] == 'open'),
                    complete=len(rows) == 14 and all(r['status'] in ('excluded', 'open') for r in rows.values()),
                    all_excluded=len(rows) == 14 and all(r['status'] == 'excluded' for r in rows.values()),
                    elapsed_seconds=round(time.monotonic()-start, 6),
                    largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', data)
        return data

    with ThreadPoolExecutor(a.workers) as pool:
        for future in as_completed([pool.submit(one, case) for case in cover['cases']]):
            row = future.result()
            rows[row['index']] = row
            save()
            print(json.dumps(row), flush=True)
    cores.require(contract['sources'] == sources(), 'sources changed during run')
    result = save()
    cores.require(not any(r['status'] == 'error' for r in rows.values()), 'case error')
    print('FINISHED '+json.dumps({k: result[k] for k in ('excluded', 'open', 'complete', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
