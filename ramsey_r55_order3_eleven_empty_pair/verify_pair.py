#!/usr/bin/env python3
"""Fresh entire-chain reconstruction and replay of all successful pair cases."""
from pathlib import Path
import argparse
import json
import time
import pair_audit
import pair_model
import sweep


def mutations(work):
    blue = (work / 'c11_blue.cnf').read_bytes()
    header, body = blue.split(b'\n', 1)
    lines = body.splitlines(keepends=True)
    base_count = 617207
    red = (work / 'c11_red.cnf').read_bytes()
    changed = list(lines)
    changed[base_count] = b'166 0\n'
    targets = {
        'omitted_clause': ('blue', header+b'\n'+b''.join(lines[:-1])),
        'wrong_pair_color': ('blue', header+b'\n'+b''.join(changed)),
        'unsupported_empty_axiom': ('blue', header+b'\n'+b''.join(lines[:-1])+b'0\n'),
        'corrupted_base_prefix': ('blue', header+b'\n'+b'0\n'+b''.join(lines[1:])),
        'red_branch_extra_axiom': ('red', red+b'-166 0\n'),
    }
    rejected = []
    for name, (color, data) in targets.items():
        path = work / (name+'.cnf')
        path.write_bytes(data)
        try:
            pair_audit.audit(work / 'many11.cnf', path, color)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed formula accepted')
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
    pair_model.require(not work.is_relative_to(sweep.ROOT.parent) and not work.exists(), 'fresh external verification')
    work.mkdir(parents=True)
    start = time.monotonic()
    old = json.loads((a.source_work / 'result.json').read_text())
    pair_model.require(old['complete'] and [r['name'] for r in old['cases']] == [pair_model.name(*c) for c in pair_model.CASES], 'complete source coverage')
    pair_model.require(old['contract']['sources'] == sweep.sources(), 'source drift')
    pair_model.require(old['contract']['drat_trim'] == sweep.info(a.drat_trim), 'checker drift')
    chain = sweep.prepare(work)
    pair_model.require(json.loads(json.dumps(chain)) == old['chain'], 'complete chain mismatch')
    rows = []
    for previous in old['cases']:
        core, color, name = previous['core'], previous['color'], previous['name']
        pair_model.require(name == pair_model.name(core, color), 'case name')
        base, path = work / f'many{core}.cnf', work / (name+'.cnf')
        data = sweep.make(base, path, color)
        audit = pair_audit.audit(base, path, color)
        pair_model.require(data == previous['formula'] and audit == previous['audit'], 'formula mismatch')
        proof = a.source_work / (name+'.drat')
        pair_model.require(sweep.info(proof) == previous['proof'], 'trace mismatch')
        row = dict(name=name, formula=data, audit=audit, status=previous['status'])
        if row['status'] == 'excluded':
            pair_model.require(previous['solver_code'] == 20, 'excluded solver code')
            row['replay'] = sweep.replay(a.drat_trim, path, proof, work / (name+'.replay.log'), a.replay_seconds)
        else:
            pair_model.require(row['status'] == 'open' and previous['solver_code'] == 0, 'open solver code')
        rows.append(row)
        sweep.atomic(work / (name+'.json'), row)
        print('PASS '+name+' '+row['status'], flush=True)
    report = dict(format='r55-k11-empty-pair-verification-v1', verified=True, chain=chain, cases=rows,
                  reconstructed_formulas=4, proof_replays=sum(r['status'] == 'excluded' for r in rows),
                  excluded=[r['name'] for r in rows if r['status'] == 'excluded'],
                  open=[r['name'] for r in rows if r['status'] == 'open'],
                  rejected_mutations=mutations(work), elapsed_seconds=round(time.monotonic()-start, 6))
    pair_model.require(report['excluded'] == old['excluded'] and report['open'] == old['open'], 'outcome mismatch')
    sweep.atomic(work / 'verification.json', report)
    print('PASS '+json.dumps({k: report[k] for k in ('excluded', 'open', 'proof_replays', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
