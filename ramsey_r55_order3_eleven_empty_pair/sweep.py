#!/usr/bin/env python3
"""Complete bounded pair-color test of the two residual eleven-cycle cores."""
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
import pair_audit
import pair_model

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parent / 'ramsey_r55_order3_eleven_empty_split'
sys.path.insert(0, str(PREV))
spec = importlib.util.spec_from_file_location('empty_split_run', PREV / 'run.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
info, atomic, replay = previous.info, previous.atomic, previous.replay


def sources():
    files = previous.sources()
    files.update({str(p.relative_to(ROOT.parent)): info(p) for p in
                  [ROOT / f for f in ('pair_model.py', 'pair_audit.py', 'sweep.py')]+[PREV / 'result.json']})
    return files


def prepare(work):
    atomic(work / 'pair_controls.json', pair_audit.controls(pair_model, work / 'pair_fixtures'))
    signature_bases, parent = previous.prepare(work)
    old = json.loads((PREV / 'result.json').read_text())
    pair_model.require(old['open'] == ['c11_many', 'c13_many'], 'inherited residual scope')
    bases = {}
    for core in (11, 13):
        path = work / f'many{core}.cnf'
        base = work / f'base{core}.cnf'
        data = previous.make(base, path, 'many')
        audit = previous.check_split.audit(base, path, 'many')
        saved = next(r for r in old['cases'] if r['name'] == f'c{core}_many')
        pair_model.require(data == saved['formula'] and audit == saved['audit'], 'reviewed many-empty base mismatch')
        bases[core] = dict(formula=data, audit=audit)
    result = dict(parent=parent, signature_bases=signature_bases, many_bases=bases)
    atomic(work / 'chain.json', result)
    return result


def make(base, path, color):
    tail = pair_model.tail(color)
    with base.open('rb') as a, path.open('wb') as b:
        _, _, nv, nc = a.readline().split()
        b.write(f'p cnf {int(nv)} {int(nc)+len(tail)}\n'.encode())
        shutil.copyfileobj(a, b)
        for row in tail:
            b.write((' '.join(map(str, row))+' 0\n').encode())
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
    pair_model.require(not work.is_relative_to(ROOT.parent) and min(a.solve_seconds, a.replay_seconds) > 0, 'work/resources')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-k11-empty-pair-v1', sources=sources(), python=sys.version.split()[0], workers=2,
                    solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=info(a.kissat), drat_trim=info(a.drat_trim))
    if (work / 'contract.json').exists():
        pair_model.require(a.resume and json.loads((work / 'contract.json').read_text()) == contract, 'changed contract')
    atomic(work / 'contract.json', contract)
    chain = prepare(work)
    print('PASS sharp pair lemma controls and complete inherited chain', flush=True)
    stop, rows = threading.Event(), {}

    def one(case):
        core, color = case
        name = pair_model.name(*case)
        row = dict(name=name, core=core, color=color, status='pending')
        if stop.is_set() or (work / 'STOP').exists():
            return dict(row, status='not_started')
        checkpoint = work / (name+'.json')
        try:
            cnf, proof, log = [work / (name+s) for s in ('.cnf', '.drat', '.solve.log')]
            base = work / f'many{core}.cnf'
            row['formula'] = make(base, cnf, color)
            row['audit'] = pair_audit.audit(base, cnf, color)
            old = json.loads(checkpoint.read_text()) if a.resume and checkpoint.exists() else None
            if old:
                pair_model.require(old['name'] == name and old['formula'] == row['formula'], 'changed case')
                if old['status'] == 'open':
                    return old
            if old and old['status'] == 'excluded':
                pair_model.require(info(proof) == old['proof'], 'changed proof')
                row.update(solver_code=20, proof=old['proof'], solve_seconds=old['solve_seconds'])
            else:
                before = time.monotonic()
                with log.open('w') as stream:
                    answer = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(proof)],
                                            stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds+60)
                row.update(solver_code=answer.returncode, proof=info(proof), solve_seconds=round(time.monotonic()-before, 6))
            if row['solver_code'] == 20:
                row['replay'] = replay(a.drat_trim, cnf, proof, work / (name+'.replay.log'), a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                row['graph'] = previous.base_run.parent_run.candidate(3, log, work / (name+'.edges'))
                row['status'] = 'target_graph_verified'
                stop.set()
            elif row['solver_code'] == 0:
                pair_model.require('s UNKNOWN' in log.read_text(), 'missing UNKNOWN')
                row['status'] = 'open'
            else:
                raise ValueError('unexpected solver code')
        except Exception as error:
            row.update(status='error', error=repr(error))
            stop.set()
        atomic(checkpoint, row)
        return row

    def save():
        ordered = [rows[pair_model.name(*c)] for c in pair_model.CASES if pair_model.name(*c) in rows]
        result = dict(contract=contract, chain=chain, cases=ordered,
                      complete=len(ordered) == 4 and all(r['status'] in ('open', 'excluded') for r in ordered),
                      excluded=[r['name'] for r in ordered if r['status'] == 'excluded'],
                      open=[r['name'] for r in ordered if r['status'] == 'open'],
                      elapsed_seconds=round(time.monotonic()-start, 6),
                      largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', result)
        return result

    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, c) for c in pair_model.CASES]):
            row = future.result()
            rows[row['name']] = row
            save()
            print(json.dumps(row), flush=True)
    pair_model.require(contract['sources'] == sources(), 'source drift')
    pair_model.require(not any(r['status'] == 'error' for r in rows.values()), 'case error')
    result = save()
    print('FINISHED '+json.dumps({k: result[k] for k in ('complete', 'excluded', 'open', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
