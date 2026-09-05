#!/usr/bin/env python3
"""Fresh complete formula reconstruction, proof replay and negative controls."""
from pathlib import Path
import argparse
import json
import subprocess
import time
import audit
import generate as gen
from run import atomic, replay


def mutations(index, parent, full, checker, work):
    nv = audit.BASES[index][0]
    nc = audit.BASES[index][1]
    lines = full.read_text().splitlines()
    prefix, tail = lines[1:nc+1], lines[nc+1:]
    tests = {}
    tests['missing_tail_clause'] = prefix+tail[1:]
    changed = tail[:]
    literals = list(map(int, changed[0].split()))
    literals[0] = -literals[0]
    changed[0] = ' '.join(map(str, literals))
    tests['wrong_polarity'] = prefix+changed
    changed = tail[:]
    literals = list(map(int, changed[0].split()))
    literals[0] = 1  # unit variable does not occur in this cross-word clause
    changed[0] = ' '.join(map(str, literals))
    tests['wrong_orbit_variable'] = prefix+changed
    tests['unsupported_empty_axiom'] = prefix+tail+['0']
    changed = prefix[:]
    changed[0] = '-1 0'
    tests['parent_complement_changed'] = changed+tail
    rejected = []
    for name, body in tests.items():
        path = work / ('mutant_'+name+'.cnf')
        path.write_text(f'p cnf {nv} {len(body)}\n'+'\n'.join(body)+'\n')
        try:
            audit.audit(index, parent, path, checker)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted malformed formula: '+name)
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
    gen.require(not work.is_relative_to(gen.ROOT.parent), 'generated data outside Git')
    work.mkdir(parents=True, exist_ok=True)
    before = time.monotonic()
    source = json.loads((a.source_work / 'result.json').read_text())
    gen.require([r['index'] for r in source['cases']] == [9, 10] and source['complete_bounded_sweep'], 'incomplete case cover')
    for name, value in source['contract']['sources'].items():
        gen.require(gen.info(gen.ROOT / name) == value, 'frozen source differs')
    for name, value in source['contract']['parent_sources'].items():
        gen.require(gen.info(gen.PARENT / name) == value and value['sha256'] == gen.PINS[name], 'parent source differs')
    gen.require(gen.info(a.drat_trim) == source['contract']['drat_trim'], 'checker binary differs')
    checker = work / 'check_base'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(gen.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    verified = []
    for row in source['cases']:
        index = row['index']
        gen.require(row['action'] == gen.case(index), 'case meaning differs')
        gen.require(gen.generate(index, work) == row['formula'], 'fresh formula differs')
        cnf, parent = work / f'case_{index:02}.cnf', work / f'parent_{index:02}.cnf'
        result = audit.audit(index, parent, cnf, checker)
        gen.require(result == row['audit'], 'fresh audit differs')
        result['status'] = row['status']
        if row['status'] == 'excluded':
            proof = a.source_work / f'case_{index:02}.drat'
            gen.require(gen.info(proof) == row['proof'], 'saved proof differs')
            result['replay'] = replay(a.drat_trim, cnf, proof, work / f'replay_{index:02}.log', a.replay_seconds)
        elif row['status'] == 'open':
            gen.require(row['solver_code'] == 0, 'OPEN is not UNKNOWN')
            gen.require('s UNKNOWN' in (a.source_work / f'case_{index:02}.solve.log').read_text(), 'missing UNKNOWN log')
        else:
            raise ValueError('unexpected status; inspect literal graph separately')
        result['rejected_mutations'] = mutations(index, parent, cnf, checker, work)
        verified.append(result)
        print('VERIFIED '+str(index)+' '+result['status'], flush=True)
    excluded = [r['index'] for r in verified if r['status'] == 'excluded']
    opened = [r['index'] for r in verified if r['status'] == 'open']
    gen.require(excluded == source['excluded_indices'] and opened == source['open_indices'], 'summary mismatch')
    report = dict(cases=verified, excluded_indices=excluded, open_indices=opened,
                  elapsed_seconds=round(time.monotonic()-before, 6))
    atomic(work / 'verification.json', report)
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
