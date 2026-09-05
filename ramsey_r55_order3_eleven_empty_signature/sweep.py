#!/usr/bin/env python3
"""One bounded 11-case full extension sweep, with mandatory proof/graph checking."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import importlib.util
import json
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time
import audit
import controls
import cube
import check_lemma
import lemma_controls

sys.path.insert(0, str(cube.PARENT))
spec = importlib.util.spec_from_file_location('parent_run', cube.PARENT/'run.py')
parent_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent_run)
atomic, replay = parent_run.atomic, parent_run.replay


def sources():
    paths = [cube.ROOT/name for name in ('cube.py', 'audit.py', 'controls.py', 'sweep.py', 'verify.py', 'classify.py', 'check_lemma.py', 'lemma_controls.py')]
    paths += [cube.PARENT/name for name in ('generate.py', 'check_formula.cpp', 'run.py', 'inspect_graph.py', 'controls.py')]
    paths += [cube.INPUT, cube.ROOT/'fixtures.json', cube.ROOT.parent/'ramsey_r55_order3_eleven_residual_sweep/result.json', cube.ROOT.parent/'ramsey_r55_order3_eleven_residual_sweep/cases.json']
    return {str(path.relative_to(cube.ROOT.parent)): cube.info(path) for path in paths}


def prepare(work):
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    parent = work/'parent.cnf'
    result = subprocess.run([sys.executable, '-B', str(cube.PARENT/'generate.py'), '--red-cycles', '4', '--output', str(parent)], text=True, capture_output=True, check=True)
    metadata = json.loads(result.stdout)
    cube.require(cube.info(parent)['sha256'] == cube.PARENT_PIN, 'reviewed parent hash')
    checker = work/'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror', str(cube.PARENT/'check_formula.cpp'), '-o', str(checker)], check=True)
    with (work/'parent.check.log').open('w') as stream:
        subprocess.run([str(checker), '4', str(parent)], stdout=stream, stderr=subprocess.STDOUT, check=True)
    cube.require(' PASS' in (work/'parent.check.log').read_text(), 'parent audit output')
    with (work/'parent.controls.log').open('w') as stream:
        subprocess.run([sys.executable, '-B', str(cube.PARENT/'controls.py'), '--report', str(work/'parent.controls.json')], stdout=stream, stderr=subprocess.STDOUT, check=True)
    control = controls.run(parent, work/'cube_controls')
    atomic(work/'lemma_check.json', check_lemma.check(cube.ROOT))
    atomic(work/'lemma_controls.json', lemma_controls.run(cube.ROOT, work/'lemma_controls'))
    rows = cube.cases()
    atomic(work/'cases.json', rows)
    atomic(work/'parent.json', metadata)
    return rows, parent, metadata, dict(elapsed_seconds=round(time.monotonic()-start, 6), cube_controls=control)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--workers', type=int, default=2)
    p.add_argument('--solve-seconds', type=int, default=20)
    p.add_argument('--replay-seconds', type=int, default=300)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    work = a.work.resolve()
    cube.require(not work.is_relative_to(cube.ROOT.parent), 'large evidence outside Git')
    cube.require(1 <= a.workers <= 2 and min(a.solve_seconds, a.replay_seconds) > 0, 'resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-k11-r4-empty-full-v1', python=sys.version.split()[0], sources=sources(),
                    workers=a.workers, solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=cube.info(a.kissat), drat_trim=cube.info(a.drat_trim))
    if (work/'contract.json').exists():
        cube.require(a.resume and json.loads((work/'contract.json').read_text()) == contract, 'existing or changed contract')
    atomic(work/'contract.json', contract)
    cases, parent, parent_info, preparation = prepare(work)
    print('PASS full parent generation, independent C++ audit and mutation controls', flush=True)
    stop, rows = threading.Event(), {}

    def one(case):
        index, bits = case['index'], case['bits']
        row = dict(index=index, bits=bits, status='not_started')
        if stop.is_set() or (work/'STOP').exists():
            return row
        path = work/f'c{index:03}.json'
        try:
            cnf, proof, log = [work/(f'c{index:03}'+suffix) for suffix in ('.cnf', '.drat', '.solve.log')]
            row['formula'] = cube.make(parent, cnf, bits)
            row['audit'] = audit.check(parent, cnf, bits)
            old = json.loads(path.read_text()) if a.resume and path.exists() else None
            if old:
                cube.require(old['bits'] == bits and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                cube.require(cube.info(proof) == old['proof'], 'changed saved proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)], stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=cube.info(proof), solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(a.drat_trim, cnf, proof, work/f'c{index:03}.replay.log', a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = parent_run.candidate(4, log, work/f'c{index:03}.edges')
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                cube.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN verdict')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(path, row)
        return row

    def save():
        out = dict(contract=contract, parent=parent_info, preparation=preparation,
                   cases=[rows[i] for i in sorted(rows)],
                   excluded=sorted(i for i in rows if rows[i]['status'] == 'excluded'),
                   open=sorted(i for i in rows if rows[i]['status'] == 'open'),
                   complete=len(rows) == 11 and all(r['status'] in ('excluded', 'open') for r in rows.values()),
                   target_graph=any(r['status'] == 'target_graph_verified' for r in rows.values()),
                   elapsed_seconds=round(time.monotonic()-start, 6),
                   largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work/'result.json', out)
        return out

    with ThreadPoolExecutor(a.workers) as pool:
        for future in as_completed([pool.submit(one, case) for case in cases]):
            row = future.result()
            rows[row['index']] = row
            save()
            print(json.dumps({k: row[k] for k in ('index', 'status')}), flush=True)
    cube.require(sources() == contract['sources'], 'source drift')
    result = save()
    cube.require(not any(r['status'] == 'error' for r in rows.values()), 'case error; inspect checkpoint')
    print('FINISHED '+json.dumps({k: result[k] for k in ('excluded', 'open', 'complete', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
