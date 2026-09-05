#!/usr/bin/env python3
"""Extract/replay DRAT cores and check every core clause against its case."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys
import time

import extension_model as ext
import check_layer
import certificates as phase_certificates
import audit as phase_audit
from run import atomic


def preflight():
    ext.parent.require(ext.parent.file_info(ext.PHASE / 'certificates.py')['sha256'] ==
                       'de18eccb4305a6d3b7a1ee1cef774078b4d36adaf7787bdd5680021d850aa790',
                       'parent certificate parser changed')
    return check_layer.preflight()


def partition(result):
    ext.parent.require(len(result['cases']) == 4, 'four-case partition')
    for row, case in zip(result['cases'], ext.cases()):
        ext.parent.require(all(row[k] == v for k, v in case.items()), 'case semantics changed')
        ext.parent.require(row['status'] in ('open', 'excluded'), 'unfinished case')
    excluded = [r for r in result['cases'] if r['status'] == 'excluded']
    opened = [r['index'] for r in result['cases'] if r['status'] == 'open']
    ext.parent.require(result['complete_bounded_sweep'] and not result['target_graph_found'], 'incomplete run')
    ext.parent.require(result['excluded_indices'] == [r['index'] for r in excluded]
                       and result['open_indices'] == opened, 'summary mismatch')
    return excluded


def replay(drat, cnf, proof, log, seconds, extra=()):
    before = time.monotonic()
    with log.open('w') as stream:
        process = subprocess.run([str(drat), str(cnf), str(proof), *map(str, extra), '-t', str(seconds)],
                                 stdout=stream, stderr=subprocess.STDOUT, timeout=seconds+60)
    text = log.read_text()
    ext.parent.require(process.returncode == 0 and 's VERIFIED' in text, 'DRAT failure: '+str(log))
    match = re.search(r'(\d+) RAT lemmas in core', text)
    ext.parent.require(match is not None, 'missing proof statistics')
    return {'rat_core_lemmas': int(match.group(1)), 'seconds': round(time.monotonic()-before, 6)}


def extract(sweep, output, drat, seconds, workers):
    result = json.loads((sweep / 'result.json').read_text())
    rows = partition(result)
    cert = output / 'certificates'
    cert.mkdir(parents=True, exist_ok=True)
    preflight()

    def one(row):
        index = row['index']
        case = ext.cases()[index]
        cnf, proof = sweep / f'case_{index:02}.cnf', sweep / f'case_{index:02}.drat'
        ext.parent.require(check_layer.check_formula(sweep / 'base.cnf', cnf, case) == row['formula'], 'formula changed')
        ext.parent.require(ext.parent.file_info(proof) == row['proof'], 'full proof changed')
        core, compact = cert / f'case_{index:02}.cnf', cert / f'case_{index:02}.drat'
        extraction = replay(drat, cnf, proof, output / f'extract_{index:02}.log', seconds,
                            ('-c', core, '-l', compact))
        direct = replay(drat, core, compact, output / f'compact_{index:02}.log', seconds)
        answer = dict(case, core=ext.parent.file_info(core), proof=ext.parent.file_info(compact),
                      rat_core_lemmas=direct['rat_core_lemmas'],
                      extraction_seconds=extraction['seconds'], replay_seconds=direct['seconds'])
        print(json.dumps({'index': index, 'compact_bytes': answer['core']['bytes']+answer['proof']['bytes'],
                          'rat': direct['rat_core_lemmas']}), flush=True)
        return answer

    with ThreadPoolExecutor(workers) as pool:
        entries = list(pool.map(one, rows))
    manifest = {'format': 'r55-k10-signature-certificates-v1', 'sweep': result, 'cases': entries,
                'certificate_bytes': sum(r['core']['bytes']+r['proof']['bytes'] for r in entries),
                'drat_trim': ext.parent.file_info(drat), 'replay_seconds_limit': seconds}
    atomic(output / 'manifest.json', manifest)
    return manifest


def membership(base, cert, entries):
    wanted = set()
    occurrences = 0
    for row in entries:
        case = ext.cases()[row['index']]
        ext.parent.require(all(row[k] == v for k, v in case.items()), 'certificate case changed')
        core, proof = cert / f"case_{row['index']:02}.cnf", cert / f"case_{row['index']:02}.drat"
        ext.parent.require(ext.parent.file_info(core) == row['core']
                           and ext.parent.file_info(proof) == row['proof'], 'certificate hash')
        phase, _ = phase_audit.semantic_tail(case)
        allowed = set(phase) | {(v,) for v in check_layer.semantic_units()}
        clauses = phase_certificates.read_core(core)
        occurrences += len(clauses)
        wanted.update(c for c in clauses if c not in allowed)
    obligations = len(wanted)
    ext.parent.require(ext.parent.file_info(base)['sha256'] == ext.parent.BASE_SHA, 'base digest')
    with base.open('rb') as stream:
        ext.parent.require(stream.readline() == ext.parent.BASE_HEADER, 'membership header')
        for line in stream:
            tokens = tuple(map(int, line.split()))
            ext.parent.require(tokens[-1] == 0, 'clause terminator')
            wanted.discard(tuple(sorted(tokens[:-1])))
    ext.parent.require(not wanted, 'core clause outside its case formula')
    return {'core_clause_occurrences': occurrences, 'distinct_parent_obligations': obligations}


def verify(work, cert, manifest_path, drat, seconds):
    start = time.monotonic()
    manifest = json.loads(manifest_path.read_text())
    excluded = partition(manifest['sweep'])
    ext.parent.require([r['index'] for r in manifest['cases']] == [r['index'] for r in excluded],
                       'certificate partition')
    preflight()
    work.mkdir(parents=True, exist_ok=True)
    base = work / 'base.cnf'
    if not base.exists():
        subprocess.run([sys.executable, str(ext.parent.PARENT / 'generate.py'),
                        '--red-cycles', '4', '--output', str(base)], check=True)
    ext.parent.require(ext.parent.file_info(base)['sha256'] == ext.parent.BASE_SHA, 'base digest')
    checker = work / 'check_parent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
                    str(ext.parent.PARENT / 'check_formula.cpp'), '-o', str(checker)], check=True)
    subprocess.run([str(checker), '4', str(base)], check=True)
    support = membership(base, cert, manifest['cases'])
    replays = []
    for row in manifest['cases']:
        index = row['index']
        got = replay(drat, cert / f'case_{index:02}.cnf', cert / f'case_{index:02}.drat',
                     work / f'replay_{index:02}.log', seconds)
        ext.parent.require(got['rat_core_lemmas'] == row['rat_core_lemmas'], 'proof statistic changed')
        replays.append(dict(index=index, **got))
    report = {'verified_indices': [r['index'] for r in replays],
              'open_indices': manifest['sweep']['open_indices'], 'membership': support,
              'all_four_extensions_excluded': len(replays) == 4,
              'target_graph_found': False, 'existing_certificates_require_solver': False,
              'replays': replays, 'elapsed_seconds': round(time.monotonic()-start, 6)}
    atomic(work / 'verification.json', report)
    print(json.dumps(report, sort_keys=True), flush=True)
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
        p.add_argument('--replay-seconds', type=int, default=600)
    args = parser.parse_args()
    output = args.output if args.command == 'extract' else args.work
    ext.parent.require(not output.resolve().is_relative_to(ext.ROOT.parent), 'generated work outside Git')
    ext.parent.require(args.replay_seconds > 0, 'invalid replay limit')
    if args.command == 'extract':
        ext.parent.require(1 <= args.workers <= 4, 'worker limit')
        extract(args.sweep.resolve(), output.resolve(), args.drat_trim.resolve(), args.replay_seconds, args.workers)
    else:
        verify(output.resolve(), args.certificates.resolve(), args.manifest.resolve(),
               args.drat_trim.resolve(), args.replay_seconds)
