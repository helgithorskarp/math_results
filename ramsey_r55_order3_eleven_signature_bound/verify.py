#!/usr/bin/env python3
"""Fresh full-formula reconstruction, proof replay, and malformed-tail rejection."""
from pathlib import Path
import argparse
import json
import time
import audit
import model
import run


def mutations(work, parent, path, bits):
    raw = path.read_bytes()
    h, body = raw.split(b'\n', 1)
    lines = body.splitlines(keepends=True)
    wrong = lines[-1].split()
    wrong[0] = str(-int(wrong[0])).encode()
    cases = {
        'missing_clause': h+b'\n'+b''.join(lines[:-1]),
        'wrong_signature_polarity': h+b'\n'+b''.join(lines[:-1])+b' '.join(wrong)+b'\n',
        'unsupported_empty_clause': h+b'\n'+b''.join(lines[:-1])+b'0\n',
        'wrong_parent_prefix': h+b'\n'+b'0\n'+b''.join(lines[1:]),
    }
    rejected = []
    for name, value in cases.items():
        p = work / (name+'.cnf')
        p.write_bytes(value)
        try:
            audit.audit_formula(parent, p, bits)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed formula accepted')
        p.unlink()
    return rejected


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--replay-seconds', type=int, default=300)
    a = p.parse_args()
    work = a.work.resolve()
    model.require(not work.is_relative_to(run.ROOT.parent) and not work.exists(), 'fresh external verification directory')
    work.mkdir(parents=True)
    start = time.monotonic()
    old = json.loads((a.source_work / 'result.json').read_text())
    model.require(old['complete'] and [r['index'] for r in old['cases']] == sorted(model.CORES), 'source case coverage')
    model.require(old['contract']['sources'] == run.sources(), 'source drift')
    model.require(old['contract']['drat_trim'] == run.gen.info(a.drat_trim), 'checker drift')
    parent, data = run.prepare(work)
    model.require(data == old['parent'], 'parent mismatch')
    rows = []
    for old_row in old['cases']:
        i = old_row['index']
        cnf = work / f'c{i}.cnf'
        info = run.make_formula(parent, cnf, i)
        check = audit.audit_formula(parent, cnf, model.CORES[i])
        model.require(info == old_row['formula'] and check == old_row['audit'], 'formula mismatch')
        proof = a.source_work / f'c{i}.drat'
        model.require(run.gen.info(proof) == old_row['proof'], 'proof mismatch')
        row = dict(index=i, status=old_row['status'], formula=info, audit=check)
        if old_row['status'] == 'excluded':
            model.require(old_row['solver_code'] == 20, 'excluded source status')
            row['replay'] = run.replay(a.drat_trim, cnf, proof, work / f'c{i}.replay.log', a.replay_seconds)
        else:
            model.require(old_row['status'] == 'open' and old_row['solver_code'] == 0, 'open source status')
        run.atomic(work / f'c{i}.json', row)
        rows.append(row)
        print('PASS '+str(i)+' '+row['status'], flush=True)
    rejected = mutations(work, parent, work / 'c8.cnf', model.CORES[8])
    report = dict(format='r55-k11-signature-verification-v1', verified=True, parent=data, cases=rows,
                  full_formula_reconstructions=len(rows), proof_replays=sum(r['status'] == 'excluded' for r in rows),
                  excluded=[r['index'] for r in rows if r['status'] == 'excluded'],
                  open=[r['index'] for r in rows if r['status'] == 'open'],
                  rejected_mutations=rejected, elapsed_seconds=round(time.monotonic()-start, 6))
    model.require(report['excluded'] == old['excluded'] and report['open'] == old['open'], 'summary mismatch')
    run.atomic(work / 'verification.json', report)
    print('PASS '+json.dumps({k: report[k] for k in ('excluded', 'open', 'proof_replays', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
