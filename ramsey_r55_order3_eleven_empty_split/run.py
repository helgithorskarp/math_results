#!/usr/bin/env python3
"""Bounded, complete four-case test using the inherited sharp signature lemma."""
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
import check_split
import split

ROOT = Path(__file__).resolve().parent
SIG = ROOT.parent / 'ramsey_r55_order3_eleven_signature_bound'
sys.path.insert(0, str(SIG))
spec = importlib.util.spec_from_file_location('signature_run', SIG / 'run.py')
base_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_run)
info, atomic, replay = base_run.gen.info, base_run.atomic, base_run.replay


def sources():
    result = base_run.sources()
    result.update({str(p.relative_to(ROOT.parent)): info(p) for p in
                   [ROOT / f for f in ('split.py', 'check_split.py', 'run.py')]+[SIG / 'result.json']})
    return result


def prepare(work):
    atomic(work / 'split_controls.json', check_split.controls(split))
    parent, parent_info = base_run.prepare(work)
    original = json.loads((SIG / 'result.json').read_text())
    split.require(original['open'] == [11, 13], 'inherited residual cores')
    bases = {}
    for core in (11, 13):
        path = work / f'base{core}.cnf'
        data = base_run.make_formula(parent, path, core)
        audit = base_run.audit.audit_formula(parent, path, base_run.model.CORES[core])
        old = next(row for row in original['cases'] if row['index'] == core)
        split.require(data == old['formula'] and audit == old['audit'], 'inherited full base mismatch')
        bases[core] = dict(formula=data, audit=audit)
    atomic(work / 'bases.json', bases)
    return bases, parent_info


def make(base, path, branch):
    tail = split.units(branch)
    with base.open('rb') as a, path.open('wb') as b:
        _, _, nv, nc = a.readline().split()
        b.write(f'p cnf {int(nv)} {int(nc)+len(tail)}\n'.encode())
        shutil.copyfileobj(a, b)
        for lit in tail:
            b.write(f'{lit} 0\n'.encode())
    return info(path)


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
    split.require(not work.is_relative_to(ROOT.parent) and min(a.solve_seconds, a.replay_seconds) > 0, 'work/resource bounds')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-k11-empty-split-v1', sources=sources(), python=sys.version.split()[0],
                    workers=2, solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=info(a.kissat), drat_trim=info(a.drat_trim))
    if (work / 'contract.json').exists():
        split.require(a.resume and json.loads((work / 'contract.json').read_text()) == contract, 'changed contract')
    atomic(work / 'contract.json', contract)
    bases, parent_info = prepare(work)
    print('PASS complete split and both fully reconstructed signature bases', flush=True)
    stop, rows = threading.Event(), {}

    def one(case):
        core, branch = case
        name = split.name(*case)
        row = dict(name=name, core=core, branch=branch, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        checkpoint = work / (name+'.json')
        try:
            cnf, proof, log = [work / (name+s) for s in ('.cnf', '.drat', '.solve.log')]
            base = work / f'base{core}.cnf'
            row['formula'] = make(base, cnf, branch)
            row['audit'] = check_split.audit(base, cnf, branch)
            old = json.loads(checkpoint.read_text()) if a.resume and checkpoint.exists() else None
            if old:
                split.require(old['name'] == name and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                split.require(info(proof) == old['proof'], 'changed proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    result = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=result.returncode, proof=info(proof),
                           solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(a.drat_trim, cnf, proof, work / (name+'.replay.log'), a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = base_run.parent_run.candidate(3, log, work / (name+'.edges'))
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                split.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver exit')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        ordered = [rows[split.name(*case)] for case in split.CASES if split.name(*case) in rows]
        report = dict(contract=contract, bases=bases, parent=parent_info, cases=ordered,
                      complete=len(rows) == 4 and all(r['status'] in ('excluded', 'open') for r in ordered),
                      excluded=[r['name'] for r in ordered if r['status'] == 'excluded'],
                      open=[r['name'] for r in ordered if r['status'] == 'open'],
                      elapsed_seconds=round(time.monotonic()-start, 6),
                      largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', report)
        return report

    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, case) for case in split.CASES]):
            row = future.result()
            rows[row['name']] = row
            save()
            print(json.dumps(row), flush=True)
    split.require(contract['sources'] == sources(), 'source drift')
    split.require(not any(r['status'] == 'error' for r in rows.values()), 'case error')
    result = save()
    print('FINISHED '+json.dumps({k: result[k] for k in ('complete', 'excluded', 'open', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
