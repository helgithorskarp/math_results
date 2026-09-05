#!/usr/bin/env python3
"""Fresh full parent reconstruction, all cube audits and second proof replays."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json
from pathlib import Path
import time
import audit
import cube
import sweep


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--replay-seconds', type=int, default=300)
    a = p.parse_args()
    work = a.work.resolve()
    cube.require(not work.exists() and not work.is_relative_to(cube.ROOT.parent), 'fresh external work directory')
    old = json.loads((a.source_work/'result.json').read_text())
    cube.require(old['complete'], 'source sweep incomplete')
    cube.require(old['contract']['sources'] == sweep.sources(), 'source drift')
    cube.require(old['contract']['drat_trim'] == cube.info(a.drat_trim), 'checker changed')
    start = time.monotonic()
    cases, parent, parent_info, preparation = sweep.prepare(work)
    cube.require(parent_info == old['parent'], 'parent mismatch')
    cube.require([r['index'] for r in old['cases']] == [c['index'] for c in cases], 'complete 79-case coverage')
    result = []

    def one(pair):
        case, saved = pair
        i = case['index']
        cube.require(saved['bits'] == case['bits'], 'case identity')
        cnf = work/f'c{i:03}.cnf'
        info = cube.make(parent, cnf, case['bits'])
        checked = audit.check(parent, cnf, case['bits'])
        cube.require(info == saved['formula'] and checked == saved['audit'], 'cube mismatch')
        proof = a.source_work/f'c{i:03}.drat'
        cube.require(cube.info(proof) == saved['proof'], 'proof changed')
        row = dict(index=i, formula=info, status=saved['status'], entire_formula_audited=True)
        if saved['status'] == 'excluded':
            cube.require(saved['solver_code'] == 20, 'source solver verdict')
            row['replay'] = sweep.replay(a.drat_trim, cnf, proof, work/f'c{i:03}.replay.log', a.replay_seconds)
        else:
            cube.require(saved['status'] == 'open' and saved['solver_code'] == 0, 'open source verdict')
            cube.require('s UNKNOWN' in (a.source_work/f'c{i:03}.solve.log').read_text(), 'UNKNOWN log missing')
        sweep.atomic(work/f'c{i:03}.json', row)
        return row

    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, pair) for pair in zip(cases, old['cases'])]):
            row = future.result()
            result.append(row)
            print('PASS '+str(row['index'])+' '+row['status'], flush=True)
    report = dict(verified=True, complete_cube_reconstructions=79, parent=parent_info,
                  preparation=preparation, cases=sorted(result, key=lambda r: r['index']),
                  proof_replays=sum(r['status'] == 'excluded' for r in result),
                  excluded=sorted(r['index'] for r in result if r['status'] == 'excluded'),
                  open=sorted(r['index'] for r in result if r['status'] == 'open'),
                  elapsed_seconds=round(time.monotonic()-start, 6))
    cube.require(report['excluded'] == old['excluded'] and report['open'] == old['open'], 'summary mismatch')
    sweep.atomic(work/'verification.json', report)
    print('FINISHED '+json.dumps({k: report[k] for k in ('proof_replays', 'excluded', 'open', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
