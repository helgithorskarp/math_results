#!/usr/bin/env python3
"""Fresh full reconstruction and replay of exactly the claimed exclusions."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import time
import generate as gen
from run import atomic, replay


def mutations(checker, full, work):
    lines = full.read_text().splitlines()
    header = lines[0].split()
    nv = int(header[2])
    body = lines[1:]
    cases = {'missing_clause': body[1:], 'unsupported_empty_axiom': body+['0']}
    changed = body[:]
    first = list(map(int, changed[0].split()))
    first[0] = -first[0]
    changed[0] = ' '.join(map(str, first))
    cases['wrong_polarity'] = changed
    # r=0: primary320 + gate165 + deficit1584 + common190 + upper667.
    need = '-2926 0'
    gen.require(body.count(need) == 1, 'moving upper-counter overflow unit')
    changed = body[:]
    changed[changed.index(need)] = '2926 0'
    cases['wrong_moving_upper_counter_unit'] = changed
    rejected = []
    for name, clauses in cases.items():
        path = work / ('mutant_'+name+'.cnf')
        path.write_text(f'p cnf {nv} {len(clauses)}\n'+'\n'.join(clauses)+'\n')
        try:
            result = subprocess.run([str(checker), '0', str(path)], capture_output=True, text=True)
            gen.require(result.returncode != 0 and 'mismatch' in result.stderr,
                        'malformed formula was not rejected: '+name)
            rejected.append(name)
        finally:
            path.unlink()
    return rejected


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--replay-seconds', type=int, default=300)
    args = p.parse_args()
    work = args.work.resolve()
    gen.require(not work.is_relative_to(gen.ROOT.parent), 'generated evidence outside Git')
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    reference = json.loads((args.source_work / 'result.json').read_text())
    gen.require(reference['complete_bounded_sweep'] and not reference['target_graph_found'], 'not a completed negative sweep')
    gen.require([r['red_cycles'] for r in reference['cases']] == list(range(6)), 'incomplete color-count cover')
    for name, info in reference['contract']['sources'].items():
        gen.require(gen.info(gen.ROOT / name) == info, 'source changed: '+name)
    gen.require(gen.info(args.drat_trim) == reference['contract']['drat_trim'], 'checker binary changed')
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(gen.ROOT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    rows = []
    for source in reference['cases']:
        r = source['red_cycles']
        cnf = work / f'r{r}.cnf'
        result = subprocess.run([sys.executable, str(gen.ROOT / 'generate.py'), '--red-cycles', str(r),
                                 '--output', str(cnf)], capture_output=True, text=True, check=True)
        gen.require(json.loads(result.stdout) == source['formula'], 'fresh formula differs')
        with (work / f'r{r}.check.log').open('w') as stream:
            subprocess.run([str(checker), str(r), str(cnf)], stdout=stream, stderr=subprocess.STDOUT, check=True)
        row = dict(red_cycles=r, status=source['status'], formula=gen.info(cnf), full_formula_reconstructed=True)
        if source['status'] == 'excluded':
            proof = args.source_work / f'r{r}.drat'
            gen.require(gen.info(proof) == source['proof'], 'original proof differs')
            row['replay'] = replay(args.drat_trim, cnf, proof, work / f'r{r}.replay.log', args.replay_seconds)
        elif source['status'] == 'open':
            gen.require(source['solver_code'] == 0 and 's UNKNOWN' in
                        (args.source_work / f'r{r}.solve.log').read_text(), 'OPEN must be explicit UNKNOWN')
        else:
            raise ValueError('unexpected case status')
        rows.append(row)
        atomic(work / f'r{r}.json', row)
        print(f'VERIFIED r={r} status={row["status"]}', flush=True)
    excluded = [r['red_cycles'] for r in rows if r['status'] == 'excluded']
    opened = [r['red_cycles'] for r in rows if r['status'] == 'open']
    gen.require(excluded == reference['excluded_counts'] and opened == reference['open_counts'], 'case summary mismatch')
    report = dict(cases=rows, excluded_counts=excluded, open_counts=opened,
                  rejected_mutations=mutations(checker, work / 'r0.cnf', work),
                  elapsed_seconds=round(time.monotonic()-start, 6))
    atomic(work / 'verification.json', report)
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
