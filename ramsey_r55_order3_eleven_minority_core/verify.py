#!/usr/bin/env python3
"""Fresh parent/cube reconstruction and replay of every successful full proof."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path
import argparse
import json
import time
import audit
import cores
import run


def invariants(cover):
    checked = 0
    for row in cover['cases']:
        for code in row['members']:
            adj = audit.graph(code)
            weights, phase = [], []
            for i, j in combinations(range(3), 2):
                neighbors = [t for t in range(3) if adj[3*i][3*j+t]]
                weights.append(len(neighbors))
                if len(neighbors) == 1:
                    phase.append(neighbors[0])
                elif len(neighbors) == 2:
                    phase.append(next(t for t in range(3) if t not in neighbors))
                else:
                    phase.append(None)
            holonomy = None if 0 in weights else int((phase[0]+phase[2]+3-phase[1]) % 3 != 0)
            cores.require([sorted(weights), holonomy] == row['invariant'], 'literal invariant mismatch')
            checked += 1
    cores.require(checked == 343, 'invariant coverage')
    return checked


def reject_mutations(work, parent, cube, bits):
    original = cube.read_bytes()
    header, body = original.split(b'\n', 1)
    lines = body.splitlines(keepends=True)
    units = lines[-9:]
    cases = {
        'missing_unit': header+b'\n'+b''.join(lines[:-1]),
        'wrong_unit_polarity': header+b'\n'+b''.join(lines[:-1])+str(-int(units[-1].split()[0])).encode()+b' 0\n',
        'unsupported_empty_unit': header+b'\n'+b''.join(lines[:-1])+b'0\n',
        'wrong_parent_prefix': header+b'\n'+b'0\n'+b''.join(lines[1:]),
    }
    rejected = []
    for name, data in cases.items():
        path = work / (name+'.cnf')
        path.write_bytes(data)
        try:
            audit.audit_cube(parent, path, bits)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted malformed cube: '+name)
        finally:
            path.unlink()
    return rejected


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--replay-seconds', type=int, default=300)
    a = p.parse_args()
    work = a.work.resolve()
    cores.require(not work.is_relative_to(run.ROOT.parent) and not work.exists(), 'fresh external verification directory')
    work.mkdir(parents=True)
    start = time.monotonic()
    old = json.loads((a.source_work / 'result.json').read_text())
    cores.require(old['complete'] and [r['index'] for r in old['cases']] == list(range(14)), 'incomplete source run')
    cores.require(old['contract']['sources'] == run.sources(), 'source drift')
    cores.require(old['contract']['drat_trim'] == run.gen.info(a.drat_trim), 'checker changed')
    cover, parent, parent_info = run.prepare(work)
    cores.require(parent_info == old['parent'], 'parent mismatch')
    cover = json.loads((work / 'cover.json').read_text())
    cores.require(cover == json.loads((a.source_work / 'cover.json').read_text()), 'cover mismatch')
    # JSON reloading makes tuple/list conventions explicit in the literal invariant check.
    invariant_count = invariants(json.loads((work / 'cover.json').read_text()))
    verified = []

    def one(pair):
        case, row = pair
        index = case['index']
        cores.require(row['bits'] == case['bits'], 'case representative mismatch')
        cnf = work / f'c{index:02}.cnf'
        info = run.make_cube(parent, cnf, case['bits'])
        check = audit.audit_cube(parent, cnf, case['bits'])
        cores.require(info == row['formula'] and check == row['audit'], 'full cube mismatch')
        result = dict(index=index, status=row['status'], formula=info, audited=True)
        proof = a.source_work / f'c{index:02}.drat'
        cores.require(run.gen.info(proof) == row['proof'], 'proof bytes changed')
        if row['status'] == 'excluded':
            cores.require(row['solver_code'] == 20, 'excluded source verdict')
            result['replay'] = run.replay(a.drat_trim, cnf, proof, work / f'c{index:02}.replay.log', a.replay_seconds)
        else:
            cores.require(row['status'] == 'open' and row['solver_code'] == 0, 'unknown case status')
        run.atomic(work / f'c{index:02}.json', result)
        return result

    with ThreadPoolExecutor(2) as pool:
        for future in as_completed([pool.submit(one, pair) for pair in zip(cover['cases'], old['cases'])]):
            row = future.result()
            verified.append(row)
            print('PASS case '+str(row['index'])+' '+row['status'], flush=True)
    mutants = reject_mutations(work, parent, work / 'c00.cnf', cover['cases'][0]['bits'])
    report = dict(format='r55-k11-r3-core-verification-v1', parent=parent_info,
                  complete_cube_reconstructions=14, literal_invariant_checks=invariant_count,
                  rejected_mutations=mutants, cases=sorted(verified, key=lambda r: r['index']),
                  proof_replays=sum(r['status'] == 'excluded' for r in verified),
                  excluded=[r['index'] for r in old['cases'] if r['status'] == 'excluded'],
                  open=[r['index'] for r in old['cases'] if r['status'] == 'open'],
                  elapsed_seconds=round(time.monotonic()-start, 6), verified=True)
    cores.require(report['excluded'] == old['excluded'] and report['open'] == old['open'], 'summary mismatch')
    run.atomic(work / 'verification.json', report)
    print('PASS '+json.dumps({k: report[k] for k in ('proof_replays', 'excluded', 'open', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
