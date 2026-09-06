#!/usr/bin/env python3
"""Nineteen complete a5 fixed-attachment decisions with a frozen, resumable bounded contract."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import re
import resource
import subprocess
import sys
import time

import build

ROOT = Path(__file__).resolve().parent
ATTACH = ROOT.parent / 'ramsey_r55_order3_eleven_core194_attachments'
DIRECT = ROOT.parent / 'ramsey_r55_order3_eleven_core194_direct'
sys.path.insert(0, str(ATTACH))
import prepare
sys.path.insert(0, str(DIRECT))
import decode

need = prepare.profiles.require
identity = prepare.generator.identity
atomic = prepare.atomic
IDS = build.IDS


def sources():
    result = prepare.sources()
    paths = [ROOT / n for n in ('run.py','verify.py','controls.py','PROOF.md','build.py','audit_fixed.py')]
    paths += [DIRECT / 'decode.py', ATTACH / 'result.json']
    previous = ROOT.parent / 'ramsey_r55_order3_eleven_core194_attachment_decisions'
    paths += [previous / n for n in ('PROOF.md','result.json')]
    for directory in ('ramsey_r55_core194_a6_fixed_review1', 'ramsey_r55_core194_attachment_decisions_review1'):
        paths += [ROOT.parent / directory / n for n in ('README.md','result.json')]
    for path in paths: result[str(path.relative_to(ROOT.parent))] = identity(path)
    return result


def terminal(code, output):
    statuses = [line for line in output.splitlines() if line.startswith('s ')]
    expected = {0: 's UNKNOWN', 10: 's SATISFIABLE', 20: 's UNSATISFIABLE'}
    need(code in expected and statuses == [expected[code]], 'exact solver exit/status agreement')
    return {0: 'open', 10: 'sat_pending', 20: 'unsat_pending'}[code]


def replay(executable, cnf, trace, log, limit):
    start = time.monotonic()
    with log.open('w') as stream:
        p = subprocess.run([str(executable), str(cnf), str(trace), '-t', str(limit)],
                           stdout=stream, stderr=subprocess.STDOUT, timeout=limit + 60)
    output = log.read_text()
    need(p.returncode == 0 and 's VERIFIED' in output, 'full DRAT verification failed')
    rat = re.search(r'(\d+) RAT lemmas in core', output)
    need(rat is not None, 'full DRAT RAT statistics missing')
    return dict(verified=True, rat_core_lemmas=int(rat.group(1)),
                seconds=round(time.monotonic() - start, 6), log=identity(log))


def preparation(work):
    fresh = build.build(work)
    need([x['id'] for x in fresh['cases']] == list(IDS), 'complete nineteen-case cover')
    atomic(work / 'preparation.json', fresh)
    return fresh


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--solve-seconds', type=int, default=90)
    p.add_argument('--replay-seconds', type=int, default=600)
    p.add_argument('--resume', action='store_true')
    a = p.parse_args()
    work = a.work.resolve()
    need(not work.is_relative_to(ROOT.parent), 'external work directory required')
    need(min(a.solve_seconds, a.replay_seconds) > 0, 'positive caps required')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    contract = dict(format='r55-core194-a5-nineteen-fixed-decisions-v1', sources=sources(),
                    python=sys.version.split()[0], workers=2, case_order=list(IDS),
                    solve_seconds=a.solve_seconds, replay_seconds=a.replay_seconds,
                    kissat=identity(a.kissat), drat_trim=identity(a.drat_trim))
    if (work / 'contract.json').exists():
        need(a.resume and json.loads((work / 'contract.json').read_text()) == contract,
             'existing or changed run contract')
    atomic(work / 'contract.json', contract)
    prep = preparation(work)
    print('PASS fresh complete nineteen-case preparation and profile/formula controls', flush=True)

    def one(case):
        key = case['id']
        row = dict(id=key, counts=case['counts'], formula=case['formula'], status='not_started')
        path = work / (key + '.json')
        cnf = work / (key + '.cnf')
        trace = work / (key + '.drat')
        log = work / (key + '.solve.log')
        if (work / 'STOP').exists():
            return row
        try:
            need(identity(cnf) == row['formula'], 'complete child identity')
            if a.resume and path.exists():
                old = json.loads(path.read_text())
                need(old['id'] == key and old['formula'] == row['formula'] and old['counts'] == row['counts'], 'saved case identity')
                if old['status'] in ('excluded', 'open', 'target_graph_verified', 'unsat_pending') or (old['status'] == 'error' and old.get('solver_code') == 20):
                    need(identity(trace) == old['trace'] and identity(log) == old['solver_log'], 'saved evidence identity')
                    status = terminal(old['solver_code'], log.read_text())
                    need(status == {'excluded': 'unsat_pending', 'open': 'open', 'target_graph_verified': 'sat_pending', 'unsat_pending': 'unsat_pending', 'error': 'unsat_pending'}[old['status']], 'saved evidence status')
                    row.update(old)
                    if status == 'unsat_pending':
                        row['status'] = 'unsat_pending'
                        row.pop('error', None)
            if row['status'] not in ('excluded', 'open', 'target_graph_verified', 'unsat_pending'):
                before = time.monotonic()
                with log.open('w') as stream:
                    solver = subprocess.run([str(a.kissat), f'--time={a.solve_seconds}', str(cnf), str(trace)],
                        stdout=stream, stderr=subprocess.STDOUT, timeout=a.solve_seconds + 60)
                row.update(solver_code=solver.returncode, trace=identity(trace), solver_log=identity(log),
                           solve_seconds=round(time.monotonic() - before, 6))
                row['status'] = terminal(solver.returncode, log.read_text())
            if row['solver_code'] == 20:
                row['status'] = 'unsat_pending'
                atomic(path, row)  # Preserve the proof before beginning mandatory replay.
                row['replay'] = replay(a.drat_trim, cnf, trace, work / (key + '.replay.log'), a.replay_seconds)
                row['status'] = 'excluded'
            elif row['solver_code'] == 10:
                model = decode.write(log, work / (key + '.edges'))
                decode.satisfies(model, cnf)
                row['graph'] = prepare.checker.graph(work / (key + '.edges'), 'blue')
                row['edges'] = identity(work / (key + '.edges'))
                row['status'] = 'target_graph_verified'
        except Exception as error:
            row.update(status='error', error=repr(error))
        atomic(path, row)
        return row

    rows = {}
    def save():
        result = dict(contract=contract, preparation=prep,
            cases=[rows[k] for k in IDS if k in rows],
            complete=len(rows) == 19 and all(r['status'] in ('excluded', 'open', 'target_graph_verified') for r in rows.values()),
            excluded=[k for k in IDS if k in rows and rows[k]['status'] == 'excluded'],
            open=[k for k in IDS if k in rows and rows[k]['status'] == 'open'],
            target_graph=any(r['status'] == 'target_graph_verified' for r in rows.values()),
            whole_core_exclusions=[], elapsed_seconds=round(time.monotonic() - start, 6),
            largest_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        atomic(work / 'result.json', result)
        return result
    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, c) for c in prep['cases']]):
            row = future.result(); rows[row['id']] = row; save()
            print(json.dumps(row, sort_keys=True), flush=True)
    need(sources() == contract['sources'], 'frozen sources changed')
    final = save()
    need(final['complete'], 'incomplete bounded decision; inspect saved state')
    print('COMPLETE ' + json.dumps({k: final[k] for k in ('excluded', 'open', 'target_graph', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
