#!/usr/bin/env python3
"""One bounded signature-propagation test of the three residual core extensions."""
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
import controls
import model

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'ramsey_r55_order3_eleven_cycle_obstruction'
CORE = ROOT.parent / 'ramsey_r55_order3_eleven_minority_core'
sys.path.insert(0, str(PARENT))
import generate as gen
spec = importlib.util.spec_from_file_location('parent_run', PARENT / 'run.py')
parent_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent_run)
atomic, replay = parent_run.atomic, parent_run.replay


def sources():
    paths = [ROOT / f for f in ('model.py', 'audit.py', 'controls.py', 'run.py')]
    paths += [PARENT / f for f in ('generate.py', 'check_formula.cpp', 'run.py', 'inspect_graph.py')]
    paths += [CORE / 'cover.json', CORE / 'result.json']
    return {str(p.relative_to(ROOT.parent)): gen.info(p) for p in paths}


def prepare(work):
    cover = json.loads((CORE / 'cover.json').read_text())
    original = json.loads((CORE / 'result.json').read_text())
    model.require(original['open'] == sorted(model.CORES), 'inherited residual cover')
    for i, bits in model.CORES.items():
        model.require(cover['cases'][i]['bits'] == bits, 'core convention')
    atomic(work / 'controls.json', controls.controls(work))
    parent = work / 'parent.cnf'
    result = subprocess.run([sys.executable, str(PARENT / 'generate.py'), '--red-cycles', '3',
                             '--output', str(parent)], capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    model.require(data == original['parent'], 'inherited parent mismatch')
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    with (work / 'parent.check.log').open('w') as log:
        subprocess.run([str(checker), '3', str(parent)], stdout=log, stderr=subprocess.STDOUT, check=True)
    model.require(' PASS' in (work / 'parent.check.log').read_text(), 'complete parent check')
    atomic(work / 'parent.json', data)
    return parent, data


def make_formula(parent, path, index):
    tail = model.core_units(index)+model.tail()
    with parent.open('rb') as source, path.open('wb') as out:
        _, _, nv, nc = source.readline().split()
        out.write(f'p cnf {int(nv)} {int(nc)+len(tail)}\n'.encode())
        shutil.copyfileobj(source, out)
        for row in tail:
            out.write((' '.join(map(str, row))+' 0\n').encode())
    return gen.info(path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--solve-seconds', type=int, default=60)
    p.add_argument('--replay-seconds', type=int, default=300)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    work = a.work.resolve()
    model.require(not work.is_relative_to(ROOT.parent), 'large evidence outside Git')
    model.require(min(a.solve_seconds, a.replay_seconds) > 0, 'time bounds')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-k11-fixed-signatures-v1', sources=sources(), python=sys.version.split()[0],
                    workers=2, solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=gen.info(a.kissat), drat_trim=gen.info(a.drat_trim))
    if (work / 'contract.json').exists():
        model.require(a.resume and json.loads((work / 'contract.json').read_text()) == contract, 'changed contract')
    atomic(work / 'contract.json', contract)
    parent, parent_info = prepare(work)
    print('PASS sharp signature lemma controls and entire parent reconstruction', flush=True)
    stop, rows = threading.Event(), {}

    def one(index):
        row = dict(index=index, bits=model.CORES[index], status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        checkpoint = work / f'c{index}.json'
        try:
            cnf, proof, log = [work / (f'c{index}'+ext) for ext in ('.cnf', '.drat', '.solve.log')]
            row['formula'] = make_formula(parent, cnf, index)
            row['audit'] = audit.audit_formula(parent, cnf, row['bits'])
            old = json.loads(checkpoint.read_text()) if a.resume and checkpoint.exists() else None
            if old:
                model.require(old['bits'] == row['bits'] and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                model.require(gen.info(proof) == old['proof'], 'changed proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=gen.info(proof),
                           solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(a.drat_trim, cnf, proof, work / f'c{index}.replay.log', a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = parent_run.candidate(3, log, work / f'c{index}.edges')
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                model.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as e:
            row.update(status='error', error=repr(e))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        report = dict(contract=contract, parent=parent_info, cases=[rows[i] for i in sorted(rows)],
                      complete=len(rows) == 3 and all(r['status'] in ('excluded', 'open') for r in rows.values()),
                      excluded=[i for i in sorted(rows) if rows[i]['status'] == 'excluded'],
                      open=[i for i in sorted(rows) if rows[i]['status'] == 'open'],
                      elapsed_seconds=round(time.monotonic()-start, 6),
                      largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, i) for i in model.CORES]):
            row = future.result()
            rows[row['index']] = row
            save()
            print(json.dumps(row), flush=True)
    model.require(sources() == contract['sources'], 'source drift')
    model.require(not any(r['status'] == 'error' for r in rows.values()), 'case error')
    result = save()
    print('FINISHED '+json.dumps({k: result[k] for k in ('complete', 'excluded', 'open', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
