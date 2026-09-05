#!/usr/bin/env python3
"""One bounded six-count sweep; UNSAT is accepted only after full DRAT replay."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path
import argparse
import json
import os
import re
import resource
import subprocess
import sys
import threading
import time
import generate as gen
import inspect_graph


def atomic(path, data):
    tmp = path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


def replay(drat, cnf, proof, log, seconds):
    before = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run([str(drat), str(cnf), str(proof), '-t', str(seconds)],
                                stdout=stream, stderr=subprocess.STDOUT, timeout=seconds+60)
    text = log.read_text()
    gen.require(result.returncode == 0 and 's VERIFIED' in text, 'DRAT replay failed: '+str(log))
    match = re.search(r'(\d+) RAT lemmas in core', text)
    gen.require(match is not None, 'missing RAT statistic')
    return dict(exit_code=0, verified=True, rat_core_lemmas=int(match.group(1)),
                seconds=round(time.monotonic()-before, 6))


def candidate(r, log, path):
    values = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for literal in map(int, line.split()[1:]):
                if literal:
                    gen.require(abs(literal) not in values or values[abs(literal)] == (literal > 0), 'model conflict')
                    values[abs(literal)] = literal > 0
    primary, _, _, _, _, edge = gen.model(r)
    gen.require(all(v in values for v in range(1, primary+1)), 'incomplete model')
    red = []
    for a, b in combinations(range(43), 2):
        literal = edge(a, b)
        color = literal == gen.T if abs(literal) == gen.T else values[literal]
        if color:
            red.append((a, b))
    path.write_text(f'43 {len(red)}\n'+''.join(f'{a} {b}\n' for a, b in red))
    answer = inspect_graph.inspect(path)
    gen.require(answer['vertices'] == 43 and answer['ramsey'], 'candidate fails literal verification')
    return answer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--workers', type=int, default=2)
    p.add_argument('--solve-seconds', type=int, default=180)
    p.add_argument('--replay-seconds', type=int, default=300)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    work, kissat, drat = a.work.resolve(), a.kissat.resolve(), a.drat_trim.resolve()
    gen.require(not work.is_relative_to(gen.ROOT.parent), 'large evidence outside Git')
    gen.require(1 <= a.workers <= 2 and min(a.solve_seconds, a.replay_seconds) > 0, 'resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    sources = ('generate.py', 'check_formula.cpp', 'controls.py', 'run.py', 'inspect_graph.py')
    contract = dict(format='r55-order3-k11-v1', python=sys.version.split()[0],
                    workers=a.workers, solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    sources={n: gen.info(gen.ROOT / n) for n in sources},
                    kissat=gen.info(kissat), drat_trim=gen.info(drat))
    if (work / 'contract.json').exists():
        gen.require(a.resume and json.loads((work / 'contract.json').read_text()) == contract, 'existing or changed contract')
    atomic(work / 'contract.json', contract)
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(gen.ROOT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    with (work / 'controls.log').open('w') as stream:
        subprocess.run([sys.executable, str(gen.ROOT / 'controls.py'), '--report', str(work / 'controls.json')],
                       stdout=stream, stderr=subprocess.STDOUT, check=True)
    print('PASS exact local arithmetic, counter and normalization controls', flush=True)
    stop = threading.Event()
    rows = {}

    def one(r):
        row = dict(red_cycles=r, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        checkpoint = work / f'r{r}.json'
        try:
            cnf, proof, log = [work / (f'r{r}'+s) for s in ('.cnf', '.drat', '.solve.log')]
            before = time.monotonic()
            result = subprocess.run([sys.executable, str(gen.ROOT / 'generate.py'), '--red-cycles', str(r),
                                     '--output', str(cnf)], capture_output=True, text=True, check=True)
            row['formula'] = json.loads(result.stdout)
            with (work / f'r{r}.check.log').open('w') as stream:
                subprocess.run([str(checker), str(r), str(cnf)], stdout=stream, stderr=subprocess.STDOUT, check=True)
            gen.require(' PASS' in (work / f'r{r}.check.log').read_text(), 'formula audit absent')
            row.update(formula_audited=True, generation_check_seconds=round(time.monotonic()-before, 6))
            old = json.loads(checkpoint.read_text()) if a.resume and checkpoint.exists() else None
            if old:
                gen.require(old['red_cycles'] == r and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                gen.require(gen.info(proof) == old['proof'], 'changed proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=gen.info(proof),
                           solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(drat, cnf, proof, work / f'r{r}.replay.log', a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = candidate(r, log, work / f'r{r}.edges')
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                gen.require('s UNKNOWN' in log.read_text(), 'UNKNOWN not explicit')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        report = dict(contract=contract, cases=[rows[r] for r in sorted(rows)],
                      excluded_counts=sorted(r for r in rows if rows[r]['status'] == 'excluded'),
                      open_counts=sorted(r for r in rows if rows[r]['status'] == 'open'),
                      complete_bounded_sweep=len(rows) == 6 and all(row['status'] in ('excluded', 'open') for row in rows.values()),
                      all_counts_excluded=len(rows) == 6 and all(row['status'] == 'excluded' for row in rows.values()),
                      target_graph_found=any(row['status'] == 'target_graph_verified' for row in rows.values()),
                      elapsed_seconds=round(time.monotonic()-start, 6),
                      largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(a.workers) as pool:
        for future in as_completed([pool.submit(one, r) for r in range(6)]):
            row = future.result()
            rows[row['red_cycles']] = row
            save()
            print(json.dumps(row), flush=True)
    gen.require(all(gen.info(gen.ROOT / n) == value for n, value in contract['sources'].items()), 'source changed during run')
    result = save()
    gen.require(not any(row['status'] == 'error' for row in rows.values()), 'case error; inspect saved state')
    print('FINISHED '+json.dumps({k: result[k] for k in ('excluded_counts', 'open_counts', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
