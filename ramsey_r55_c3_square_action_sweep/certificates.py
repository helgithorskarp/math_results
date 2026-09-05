#!/usr/bin/env python3
"""Extract general DRAT cores, reconstruct their formulas, audit support."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import re
import subprocess
import time
import model
from run import atomic


def partition(result):
    model.require(len(result['cases']) == 18 and result['complete_bounded_sweep'], 'incomplete 18-case sweep')
    for row, case in zip(result['cases'], model.cases()):
        model.require(all(row[k] == v for k, v in case.items()), 'case meaning changed')
        model.require(row['status'] in ('excluded', 'open'), 'unexpected case status')
    excluded = [r for r in result['cases'] if r['status'] == 'excluded']
    opened = [r['index'] for r in result['cases'] if r['status'] == 'open']
    model.require(result['excluded_indices'] == [r['index'] for r in excluded]
                  and result['open_indices'] == opened and not result['target_graph_found'], 'summary mismatch')
    return excluded


def replay(drat, cnf, proof, log, extra=()):
    before = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run([str(drat), str(cnf), str(proof), *map(str, extra), '-t', '600'],
                                stdout=stream, stderr=subprocess.STDOUT, timeout=660)
    text = log.read_text()
    model.require(result.returncode == 0 and 's VERIFIED' in text, 'DRAT replay failed: '+str(log))
    match = re.search(r'(\d+) RAT lemmas in core', text)
    model.require(match is not None, 'proof statistic missing')
    return {'rat_core_lemmas': int(match.group(1)), 'seconds': round(time.monotonic()-before, 6)}


def support(cnf, core, nv):
    lines = core.read_text().splitlines()
    model.require(lines and lines[0] == f'p cnf {nv} {len(lines)-1}', 'core header')
    wanted = set()
    for line in lines[1:]:
        row = list(map(int, line.split()))
        model.require(row and row[-1] == 0 and all(1 <= abs(l) <= nv for l in row[:-1]), 'core literals')
        clause = tuple(sorted(row[:-1]))
        model.require(len(set(clause)) == len(clause) and not any(-l in clause for l in clause), 'malformed core clause')
        wanted.add(clause)
    total = len(wanted)
    with cnf.open() as stream:
        header = stream.readline().split()
        model.require(header[:3] == ['p', 'cnf', str(nv)], 'full header')
        for line in stream:
            row = list(map(int, line.split()))
            model.require(row and row[-1] == 0, 'full clause terminator')
            wanted.discard(tuple(sorted(row[:-1])))
    model.require(not wanted, 'unsupported core axiom')
    return {'core_clause_occurrences': len(lines)-1, 'distinct_core_clauses': total}


def extract(sweep, output, drat, workers):
    result = json.loads((sweep / 'result.json').read_text())
    rows = partition(result)
    directory = output / 'certificates'
    directory.mkdir(parents=True, exist_ok=True)

    def one(row):
        index = row['index']
        full, original = sweep / f'case_{index:02}.cnf', sweep / f'case_{index:02}.drat'
        model.require(model.info(full) == {k: row['formula'][k] for k in ('bytes', 'sha256')}, 'formula changed')
        model.require(model.info(original) == row['proof'], 'proof changed')
        core, proof = directory / f'case_{index:02}.cnf', directory / f'case_{index:02}.drat'
        replay(drat, full, original, output / f'extract_{index:02}.log', ('-c', core, '-l', proof))
        checked = support(full, core, row['formula']['variables'])
        direct = replay(drat, core, proof, output / f'compact_{index:02}.log')
        answer = dict(model.cases()[index], core=model.info(core), proof=model.info(proof),
                      support=checked, rat_core_lemmas=direct['rat_core_lemmas'])
        print(json.dumps({'index': index, 'bytes': answer['core']['bytes']+answer['proof']['bytes'],
                          'rat': direct['rat_core_lemmas']}), flush=True)
        return answer

    with ThreadPoolExecutor(workers) as pool:
        entries = list(pool.map(one, rows))
    manifest = {'format': 'r55-c3-square-certificates-v1', 'sweep': result, 'cases': entries,
                'certificate_bytes': sum(r['core']['bytes']+r['proof']['bytes'] for r in entries),
                'drat_trim': model.info(drat)}
    atomic(output / 'manifest.json', manifest)
    return manifest


def verify(work, directory, manifest_path, drat):
    start = time.monotonic()
    manifest = json.loads(manifest_path.read_text())
    rows = partition(manifest['sweep'])
    model.require([r['index'] for r in manifest['cases']] == [r['index'] for r in rows], 'certificate cover')
    model.classify()
    work.mkdir(parents=True, exist_ok=True)
    checker = work / 'check_formula'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(model.ROOT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    verified = []
    for row, certificate in zip(rows, manifest['cases']):
        index = row['index']
        case = model.cases()[index]
        model.require(all(certificate[k] == v for k, v in case.items()), 'wrong certificate type')
        cnf = work / f'case_{index:02}.cnf'
        model.require(model.generate(case, cnf) == row['formula'], 'regenerated formula changed')
        with (work / f'check_{index:02}.log').open('w') as stream:
            subprocess.run([str(checker), *map(str, [case['a'], *case['b'], case['c']]), str(cnf)],
                           stdout=stream, stderr=subprocess.STDOUT, check=True)
        core, proof = directory / f'case_{index:02}.cnf', directory / f'case_{index:02}.drat'
        model.require(model.info(core) == certificate['core'] and model.info(proof) == certificate['proof'], 'certificate digest')
        checked = support(cnf, core, row['formula']['variables'])
        model.require(checked == certificate['support'], 'support statistic changed')
        direct = replay(drat, core, proof, work / f'replay_{index:02}.log')
        model.require(direct['rat_core_lemmas'] == certificate['rat_core_lemmas'], 'proof statistic changed')
        verified.append(dict(index=index, support=checked, **direct))
        print('VERIFIED '+str(index), flush=True)
    report = {'verified_indices': [r['index'] for r in verified],
              'open_indices': manifest['sweep']['open_indices'], 'cases': verified,
              'all_18_types_excluded': len(verified) == 18, 'target_graph_found': False,
              'core_clause_occurrences': sum(r['support']['core_clause_occurrences'] for r in verified),
              'elapsed_seconds': round(time.monotonic()-start, 6)}
    atomic(work / 'verification.json', report)
    print(json.dumps({k: report[k] for k in ('verified_indices', 'open_indices', 'all_18_types_excluded')}), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    e = sub.add_parser('extract')
    e.add_argument('--sweep', required=True, type=Path)
    e.add_argument('--output', required=True, type=Path)
    e.add_argument('--workers', type=int, default=2)
    v = sub.add_parser('verify')
    v.add_argument('--work', required=True, type=Path)
    v.add_argument('--certificates', required=True, type=Path)
    v.add_argument('--manifest', required=True, type=Path)
    for p in (e, v):
        p.add_argument('--drat-trim', required=True, type=Path)
    args = parser.parse_args()
    output = args.output if args.command == 'extract' else args.work
    model.require(not output.resolve().is_relative_to(model.ROOT.parent), 'generated output outside Git')
    if args.command == 'extract':
        model.require(1 <= args.workers <= 4, 'worker count')
        extract(args.sweep.resolve(), output.resolve(), args.drat_trim.resolve(), args.workers)
    else:
        verify(output.resolve(), args.certificates.resolve(), args.manifest.resolve(), args.drat_trim.resolve())
