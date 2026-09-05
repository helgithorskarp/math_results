#!/usr/bin/env python3
"""Bounded two-action solve, literal formula audit, and checked DRAT replay."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import os
import resource
import subprocess
import sys
import time
import audit
import generate as gen


def atomic(path, value):
    tmp = path.with_suffix(path.suffix+'.partial')
    with tmp.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
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
    gen.require(result.returncode == 0 and 's VERIFIED' in text, 'DRAT replay failed')
    import re
    match = re.search(r'(\d+) RAT lemmas in core', text)
    gen.require(match is not None, 'missing replay statistics')
    return dict(code=0, verified=True, rat_core_lemmas=int(match.group(1)),
                seconds=round(time.monotonic()-before, 6))


def candidate(index, log, output):
    assignment = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for x in map(int, line.split()[1:]):
                if x:
                    gen.require(abs(x) not in assignment or assignment[abs(x)] == (x > 0), 'conflicting SAT model')
                    assignment[abs(x)] = x > 0
    ids = gen.BASE.edge_orbits(gen.case(index))
    gen.require(all(v in assignment for v in ids.values()), 'incomplete SAT model')
    edges = [e for e, v in sorted(ids.items()) if assignment[v]]
    output.write_text(f'43 {len(edges)}\n'+''.join(f'{u} {v}\n' for u, v in edges))
    answer = gen.load('inspect_graph').inspect(output)
    gen.require(answer['vertices'] == 43 and answer['ramsey'], 'literal graph verification failed')
    return answer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--solve-seconds', type=int, default=180)
    p.add_argument('--replay-seconds', type=int, default=300)
    p.add_argument('--workers', type=int, default=2)
    p.add_argument('--resume', action='store_true')
    args = p.parse_args()
    work = args.work.resolve()
    gen.require(not work.is_relative_to(gen.ROOT.parent), 'generated evidence outside Git')
    gen.require(1 <= args.workers <= 2 and min(args.solve_seconds, args.replay_seconds) > 0, 'resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    start = time.monotonic()
    contract = dict(format='c3-square-normalized-v1', python=sys.version.split()[0],
                    solve_seconds=args.solve_seconds, replay_seconds=args.replay_seconds, workers=args.workers,
                    kissat=gen.info(kissat), drat_trim=gen.info(drat),
                    sources={n: gen.info(gen.ROOT / n) for n in ('generate.py', 'audit.py', 'run.py')},
                    parent_sources={n: gen.info(gen.PARENT / n) for n in gen.PINS})
    for name, pin in gen.PINS.items():
        gen.require(contract['parent_sources'][name]['sha256'] == pin, 'parent source changed')
    contract_path = work / 'contract.json'
    if contract_path.exists():
        gen.require(args.resume and json.loads(contract_path.read_text()) == contract, 'existing or changed contract')
    checker = work / 'check_base'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(gen.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    atomic(contract_path, contract)
    atomic(work / 'normalization_controls.json', {'cases': [audit.controls(i) for i in (9, 10)]})
    print('PASS both centralizer controls and Burnside counts', flush=True)

    def one(index):
        row = dict(index=index, action=gen.case(index), status='pending')
        checkpoint = work / f'case_{index:02}.json'
        if (work / 'STOP').exists():
            return dict(row, status='not_started')
        try:
            before = time.monotonic()
            row['formula'] = gen.generate(index, work)
            cnf, proof, log = [work / (f'case_{index:02}'+s) for s in ('.cnf', '.drat', '.solve.log')]
            row['audit'] = audit.audit(index, work / f'parent_{index:02}.cnf', cnf, checker)
            row['generation_check_seconds'] = round(time.monotonic()-before, 6)
            old = json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else None
            if old:
                gen.require(old['action'] == row['action'] and old['formula'] == row['formula'], 'changed checkpoint')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                gen.require(gen.info(proof) == old['proof'], 'changed saved proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(kissat), f'--time={args.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=args.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=gen.info(proof),
                           solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(drat, cnf, proof, work / f'case_{index:02}.replay.log', args.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = candidate(index, log, work / f'case_{index:02}.edges')
                row['status'] = 'target_graph_verified'
            elif row['solver_code'] == 0:
                gen.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN marker')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
        atomic(checkpoint, row)
        print(json.dumps(row), flush=True)
        return row

    with ThreadPoolExecutor(args.workers) as pool:
        rows = list(pool.map(one, (9, 10)))
    gen.require(all(gen.info(gen.ROOT / n) == value for n, value in contract['sources'].items()), 'source drift')
    report = dict(contract=contract, cases=rows,
                  excluded_indices=[r['index'] for r in rows if r['status'] == 'excluded'],
                  open_indices=[r['index'] for r in rows if r['status'] == 'open'],
                  target_graph_found=any(r['status'] == 'target_graph_verified' for r in rows),
                  complete_bounded_sweep=all(r['status'] in ('excluded', 'open', 'target_graph_verified') for r in rows),
                  elapsed_seconds=round(time.monotonic()-start, 6),
                  largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    atomic(work / 'result.json', report)
    gen.require(not any(r['status'] == 'error' for r in rows), 'case failed; inspect checkpoints')
    print('FINISHED '+json.dumps({k: report[k] for k in ('excluded_indices', 'open_indices', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
