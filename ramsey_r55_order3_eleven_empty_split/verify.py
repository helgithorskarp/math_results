#!/usr/bin/env python3
"""Fresh full-chain reconstruction, every successful proof replay, and split mutants."""
from pathlib import Path
import argparse
import json
import time
import check_split
import split
import run


def mutations(work):
    one = work / 'c11_one.cnf'
    many = work / 'c11_many.cnf'
    raw = one.read_bytes()
    header, body = raw.split(b'\n', 1)
    rows = body.splitlines(keepends=True)
    raw_many = many.read_bytes()
    hm, bm = raw_many.split(b'\n', 1)
    rm = bm.splitlines(keepends=True)
    numeric = [0, 1, 1, 2, 2, 3, 4, 4, 5, 6]
    wrong_units = [v if mask & (1 << i) else -v for row, mask in enumerate(numeric) if row
                   for i in range(3) for v in [211+11*row+i]]
    cases = {
        'missing_equality_unit': ('one', header+b'\n'+b''.join(rows[:-1])),
        'numeric_mask_order': ('one', header+b'\n'+b''.join(rows[:-27])+
                               ''.join(f'{u} 0\n' for u in wrong_units).encode()),
        'unsupported_empty_axiom': ('one', header+b'\n'+b''.join(rows[:-1])+b'0\n'),
        'wrong_many_polarity': ('many', hm+b'\n'+b''.join(rm[:-1])+b'224 0\n'),
        'wrong_parent_prefix': ('one', header+b'\n'+b'0\n'+b''.join(rows[1:])),
    }
    rejected = []
    for name, (branch, data) in cases.items():
        path = work / (name+'.cnf')
        path.write_bytes(data)
        try:
            check_split.audit(work / 'base11.cnf', path, branch)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed split formula accepted')
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
    split.require(not work.is_relative_to(run.ROOT.parent) and not work.exists(), 'fresh external verification directory')
    work.mkdir(parents=True)
    start = time.monotonic()
    old = json.loads((a.source_work / 'result.json').read_text())
    split.require(old['complete'] and [r['name'] for r in old['cases']] == [split.name(*c) for c in split.CASES],
                  'source case coverage')
    split.require(old['contract']['sources'] == run.sources(), 'source drift')
    split.require(old['contract']['drat_trim'] == run.info(a.drat_trim), 'checker drift')
    bases, parent = run.prepare(work)
    split.require(json.loads(json.dumps(bases)) == old['bases'] and parent == old['parent'], 'full base mismatch')
    rows = []
    for old_row in old['cases']:
        core, branch, name = old_row['core'], old_row['branch'], old_row['name']
        split.require(name == split.name(core, branch), 'case label mismatch')
        base = work / f'base{core}.cnf'
        path = work / (name+'.cnf')
        data = run.make(base, path, branch)
        audit = check_split.audit(base, path, branch)
        split.require(data == old_row['formula'] and audit == old_row['audit'], 'full split mismatch')
        proof = a.source_work / (name+'.drat')
        split.require(run.info(proof) == old_row['proof'], 'proof mismatch')
        row = dict(name=name, formula=data, audit=audit, status=old_row['status'])
        if old_row['status'] == 'excluded':
            split.require(old_row['solver_code'] == 20, 'excluded source verdict')
            row['replay'] = run.replay(a.drat_trim, path, proof, work / (name+'.replay.log'), a.replay_seconds)
        else:
            split.require(old_row['status'] == 'open' and old_row['solver_code'] == 0, 'open source verdict')
        rows.append(row)
        run.atomic(work / (name+'.json'), row)
        print('PASS '+name+' '+row['status'], flush=True)
    report = dict(format='r55-k11-empty-split-verification-v1', verified=True, cases=rows,
                  parent=parent, bases=bases, reconstructed_formulas=4,
                  proof_replays=sum(r['status'] == 'excluded' for r in rows),
                  excluded=[r['name'] for r in rows if r['status'] == 'excluded'],
                  open=[r['name'] for r in rows if r['status'] == 'open'],
                  rejected_mutations=mutations(work), elapsed_seconds=round(time.monotonic()-start, 6))
    split.require(report['excluded'] == old['excluded'] and report['open'] == old['open'], 'summary mismatch')
    run.atomic(work / 'verification.json', report)
    print('PASS '+json.dumps({k: report[k] for k in ('excluded', 'open', 'proof_replays', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
