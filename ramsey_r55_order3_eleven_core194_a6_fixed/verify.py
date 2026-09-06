#!/usr/bin/env python3
"""Reconstruct complete cases, then independently replay every terminal certificate."""
from pathlib import Path
import argparse
import json
import time
import run


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--replay-seconds', type=int, default=600)
    a = p.parse_args(); start = time.monotonic()
    work = a.work.resolve(); source = a.source_work.resolve()
    run.need(not work.exists() and not work.is_relative_to(run.ROOT.parent) and work != source, 'fresh external verification path')
    old = json.loads((source / 'result.json').read_text())
    run.need(old['complete'] and old['contract']['sources'] == run.sources(), 'complete run and frozen sources')
    run.need(run.identity(a.drat_trim) == old['contract']['drat_trim'], 'pinned full DRAT checker')
    run.need([x['id'] for x in old['cases']] == list(run.IDS), 'complete three-case list')
    prep = run.preparation(work)
    run.need(prep == old['preparation'], 'entire fresh preparation')
    rows = []; replays = 0
    for case, saved in zip(prep['cases'], old['cases']):
        key = case['id']; cnf = work / (key + '.cnf')
        trace = source / (key + '.drat'); log = source / (key + '.solve.log')
        run.need(saved['formula'] == case['formula'] == run.identity(cnf) and saved['counts'] == case['counts'], 'exact case formula')
        run.need(run.identity(trace) == saved['trace'] and run.identity(log) == saved['solver_log'], 'exact saved evidence')
        status = run.terminal(saved['solver_code'], log.read_text())
        expected = {'open': 'open', 'excluded': 'unsat_pending', 'target_graph_verified': 'sat_pending'}
        run.need(saved['status'] in expected and status == expected[saved['status']], 'terminal status consistent')
        row = {k: saved[k] for k in ('id', 'counts', 'formula', 'trace', 'solver_log', 'status')}
        if saved['status'] == 'excluded':
            run.need(saved['replay']['verified'], 'first full replay required')
            row['replay'] = run.replay(a.drat_trim, cnf, trace, work / (key + '.replay.log'), a.replay_seconds)
            replays += 1
        elif saved['status'] == 'target_graph_verified':
            model = run.decode.write(log, work / (key + '.edges'))
            run.decode.satisfies(model, cnf)
            row['graph'] = run.prepare.checker.graph(work / (key + '.edges'), 'blue')
            run.need(row['graph'] == saved['graph'] and run.identity(work / (key + '.edges')) == saved['edges'], 'literal graph verification')
        rows.append(row)
        print('VERIFIED ' + key + ' ' + saved['status'], flush=True)
    excluded = [r['id'] for r in rows if r['status'] == 'excluded']
    opened = [r['id'] for r in rows if r['status'] == 'open']
    target = any(r['status'] == 'target_graph_verified' for r in rows)
    run.need(excluded == old['excluded'] and opened == old['open'] and target == old['target_graph'], 'summary matches every case')
    run.need(run.sources() == old['contract']['sources'], 'frozen sources unchanged after checking')
    answer = dict(verified=True, cases=rows, proof_replays=replays, excluded=excluded, open=opened,
                  target_graph=target, whole_core_exclusions=[], seconds=round(time.monotonic() - start, 6))
    run.atomic(work / 'verification.json', answer)
    print('PASS ' + json.dumps({k: answer[k] for k in ('excluded', 'open', 'target_graph', 'proof_replays', 'seconds')}), flush=True)


if __name__ == '__main__':
    main()
